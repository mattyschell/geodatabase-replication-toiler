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

        self.sdeconn = os.environ['SDEFILE']
        self.geodatabase = gdb.Gdb()

        # refactor clue here, toiler gdb always expects one
        # gdb it is in the environment
        self.childsdeconn = os.environ['SDECHILD']
        os.environ['SDEFILE'] = self.childsdeconn
        self.childgeodatabase = gdb.Gdb()

        # switch env back (to parent) just in case
        os.environ['SDEFILE'] = self.geodatabase.sdeconn 
        
        self.childfeatureclass = os.path.join(self.childsdeconn
                                             ,'SOMELINES')
        
        self.replica = replica.Replica(self.geodatabase
                                      ,'TEST_REPLICA')

        self.srcshp = os.path.join(pathlib.Path(__file__).parent.resolve()
                                  ,'resources'
                                  ,'somelines.shp')

        self.parentfc = fc.Fc(self.geodatabase
                           ,'SOMELINES')

        if self.parentfc.exists():
            self.parentfc.delete()

        self.geodatabase.importfeatureclass(self.srcshp
                                           ,'SOMELINES')

        # all fcs must have globalids and be versioned
        # parent datasets should be prepared 
        # children will be prepared in version creation
        arcpy.AddGlobalIDs_management(self.parentfc.featureclass)
        self.parentfc.version()

        self.editversion = version.Version(self.geodatabase
                                          ,'REPLICATOILER')

        self.childfc = fc.Fc(self.childgeodatabase
                                ,'SOMELINES')

        if self.childfc.exists():
            self.childfc.delete()

        self.childgeodatabase.importfeatureclass(self.srcshp
                                                ,'SOMELINES')

        parent_data = []
        parent_data.append(self.parentfc.featureclass)
        child_data = []
        child_data.append(self.childfc.featureclass)

        retval = self.replica.create(self.childgeodatabase.sdeconn
                                    ,parent_data
                                    ,child_data)

        if retval != 'success':
            raise ValueError('failed to set up a replica, cant test')            

    @classmethod
    def tearDownClass(self):
 
        pass
        #retval = self.replica.delete()
        
        #self.parentfc.delete()
        #self.childfc.delete()

        self.editversion.delete()

    def test_asyncnothing(self):

        # confirm we start good, 2 fcs on parent and child
        # with same record count
        # the basic plumbing is working

        retval = self.replica.synchronize()
        
        self.assertEqual(retval,'success')      

        parentcount = arcpy.GetCount_management(self.parentfc.featureclass)
        childcount  = arcpy.GetCount_management(self.childfc.featureclass)
        
        self.assertEqual(parentcount[0]
                        ,childcount[0])

    def test_bsyncupdates(self):

        self.editversion.create()

        sql = """BEGIN
                    sde.version_util.set_current_version('REPLICATOILER');
                    sde.version_user_ddl.edit_version('REPLICATOILER',1);
                    -- update all rows
                    execute immediate 'update '
                                   || '    somelines '
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

    def test_csyncversioneddeletes(self):

        self.editversion.create()

        sql = """BEGIN
                    sde.version_util.set_current_version('REPLICATOILER');
                    sde.version_user_ddl.edit_version('REPLICATOILER',1);
                    -- delete 2965 rows
                    execute immediate 'delete from '
                                || '    somelines '
                                || 'where '
                                || '    objectid < (select '
                                || '                    median(objectid) '
                                || '                from somelines) ';
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

    def test_dsyncfulldelete(self):

        arcpy.DeleteFeatures_management(self.parentfc.featureclass)

        retval = self.replica.synchronize()
        
        self.assertEqual(retval,'success')      

        parentcount = arcpy.GetCount_management(self.parentfc.featureclass)
        childcount  = arcpy.GetCount_management(self.childfc.featureclass)
        
        self.assertEqual(parentcount[0]
                        ,'0')

        self.assertEqual(childcount[0]
                        ,'0')
                  


if __name__ == '__main__':
    unittest.main()
