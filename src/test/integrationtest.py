import os
import unittest
import pathlib
import arcpy

import gdb
import fc
import version
import replica
import cx_sde

class ReplicaTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        print('we are starting slow setup steps')

        self.setupdone = os.environ['SDEINIT'] 

        self.sdeconn = os.environ['SDEFILE']
        self.geodatabase = gdb.Gdb()

        # sadly toiler gdb always expects one
        # gdb it is in the environment
        self.childsdeconn = os.environ['SDECHILD']
        os.environ['SDEFILE'] = self.childsdeconn
        self.childgeodatabase = gdb.Gdb()

        # switch env back (to parent) just in case
        os.environ['SDEFILE'] = self.geodatabase.sdeconn 

        self.editversion = version.Version(self.geodatabase
                                          ,'REPLICATOILER')
        
        self.childfeatureclass = os.path.join(self.childsdeconn
                                             ,'SOMELINES')
        
        self.replica = replica.Replica(self.geodatabase
                                      ,self.childgeodatabase
                                      ,'TEST_REPLICA')

        self.srcshp = os.path.join(pathlib.Path(__file__).parent.resolve()
                                  ,'resources'
                                  ,'somelines.shp')

        self.parentfc = fc.Fc(self.geodatabase
                             ,'SOMELINES')

        self.childfc = fc.Fc(self.childgeodatabase
                            ,'SOMELINES')

        # this is dumb but it is a workaround for ESRIs versioned view bug
        # we call this test 2x with py27 view creation in the intermission
        if self.setupdone == 'N':

            if self.parentfc.exists():
                self.parentfc.delete()

            self.geodatabase.importfeatureclass(self.srcshp
                                               ,'SOMELINES')

            # all parent fcs must have globalids and be versioned
            arcpy.AddGlobalIDs_management(self.parentfc.featureclass)
            self.parentfc.version()

            if self.childfc.exists():
                self.childfc.delete()

            # must use magic sticky copy (same as copy-paste in catalog)
            # import feature class will not replicate I dont know why

            # import from parent, these globalids must match
            arcpy.management.Copy(self.parentfc.featureclass
                                 ,self.childfc.featureclass)

            replicated_fcs = []
            replicated_fcs.append(self.parentfc.featureclass)

            retval = self.replica.create(replicated_fcs)

            if retval != 'success':
                print('failed to set up a replica, cant test') 
                print(retval)
                exit(1)


    @classmethod
    def tearDownClass(self):
 
        if self.setupdone == 'Y':

            pass

            retval = self.replica.delete()

            self.parentfc.delete()
            self.childfc.delete()

            self.editversion.delete()

            if retval != 'success':
                print(retval)
                raise ValueError('Replica deletion failed in teardown')


    def test_asyncnothing(self):

        # confirm we start good, 2 fcs on parent and child
        # with same record count
        # tests that replica setup is working

        if self.setupdone == 'Y':

            retval = self.replica.synchronize()
        
            self.assertEqual(retval,'success')      

            parentcount = arcpy.GetCount_management(self.parentfc.featureclass)
            childcount  = arcpy.GetCount_management(self.childfc.featureclass)
        
            self.assertEqual(parentcount[0]
                            ,childcount[0])

        else:
            pass

    def test_bsyncupdates(self):

        if self.setupdone == 'Y':

            self.editversion.create()

            sql = """BEGIN
                        sde.version_util.set_current_version('REPLICATOILER');
                        sde.version_user_ddl.edit_version('REPLICATOILER',1);
                        -- update all rows
                        execute immediate 'update '
                                       || '    somelines_evw '
                                       || 'set created_by = ''THETOIL'' ';
                        commit;
                        sde.version_user_ddl.edit_version('REPLICATOILER',2);
                        sde.version_util.set_current_version('SDE.DEFAULT');
                     END;"""

            sdereturn = cx_sde.execute_immediate(self.sdeconn
                                                ,sql)

            self.editversion.reconcileandpost()

            retval = self.replica.synchronize()

            arcpy.management.SelectLayerByAttribute(self.parentfc.featureclass
                                                   ,'NEW_SELECTION'
                                                   ,"created_by = 'THETOIL'")
            parentcount = arcpy.GetCount_management(self.parentfc.featureclass)


            arcpy.management.SelectLayerByAttribute(self.childfc.featureclass
                                                   ,'NEW_SELECTION'
                                                   ,"created_by = 'THETOIL'")
            childcount = arcpy.GetCount_management(self.childfc.featureclass)

            self.assertEqual(parentcount[0]
                            ,childcount[0])

        else:

            pass

    def test_csyncversioneddeletes(self):

        if self.setupdone == 'Y':

            self.editversion.create()

            sql = """BEGIN
                        sde.version_util.set_current_version('REPLICATOILER');
                        sde.version_user_ddl.edit_version('REPLICATOILER',1);
                        -- delete 2965 rows
                        execute immediate 'delete from '
                                    || '    somelines_evw '
                                    || 'where '
                                    || '    objectid < (select '
                                    || '                    median(objectid) '
                                    || '                from somelines_evw) ';
                        commit;
                        sde.version_user_ddl.edit_version('REPLICATOILER',2);
                        sde.version_util.set_current_version('SDE.DEFAULT');
                     END;"""

            sdereturn = cx_sde.execute_immediate(self.sdeconn
                                                ,sql)

            self.editversion.reconcileandpost()

            retval = self.replica.synchronize()

            parentcount = arcpy.GetCount_management(self.parentfc.featureclass)
            childcount  = arcpy.GetCount_management(self.childfc.featureclass)

            self.assertEqual(parentcount[0]
                            ,childcount[0])

        else:

            pass

    def test_dsyncfulldelete(self):

        if self.setupdone == 'Y':

            arcpy.DeleteFeatures_management(self.parentfc.featureclass)

            retval = self.replica.synchronize()

            self.assertEqual(retval,'success')      

            parentcount = arcpy.GetCount_management(self.parentfc.featureclass)
            childcount  = arcpy.GetCount_management(self.childfc.featureclass)

            self.assertEqual(parentcount[0]
                            ,'0')

            self.assertEqual(childcount[0]
                            ,'0')

        else:

            pass                  


if __name__ == '__main__':
    unittest.main()
