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
        self.childsdeconn = os.environ['SDECHILD']

        self.geodatabase = gdb.Gdb()
        self.childfeatureclass = os.path.join(self.childsdeconn
                                             ,'SOMELINES')
        
        self.replica = replica.Replica(self.geodatabase
                                      ,'TEST_REPLICA')

        self.srcshp = os.path.join(pathlib.Path(__file__).parent.resolve()
                                  ,'resources'
                                  ,'somelines.shp')

        self.testfc = fc.Fc(self.geodatabase
                           ,'SOMELINES')

        if self.testfc.exists():
            self.testfc.delete()

        self.geodatabase.importfeatureclass(self.srcshp
                                           ,'SOMELINES')
        self.testfc.version()

        self.editversion = version.Version(self.geodatabase
                                          ,'REPLICATOILER')


    @classmethod
    def tearDownClass(self):
        pass
        retval = self.replica.delete()

        if self.testfc.exists():
            self.testfc.delete()

        try:
            arcpy.Delete_management(self.childfeatureclass)
        except:
            pass

        self.editversion.delete()

    def test_acreate(self):

        in_data = []
        in_data.append(self.testfc.featureclass)

        retval = self.replica.create(self.childsdeconn
                                    ,in_data)

        self.assertEqual(retval,'success')

    def test_bsyncnothing(self):

        retval = self.replica.synchronize()
        
        self.assertEqual(retval,'success')      

        parentcount = arcpy.GetCount_management(self.testfc.featureclass)
        childcount  = arcpy.GetCount_management(self.childfeatureclass)
        
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

        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

        self.editversion.reconcileandpost()
        
        retval = self.replica.synchronize()

        parentcount = arcpy.GetCount_management(self.testfc.featureclass)
        childcount  = arcpy.GetCount_management(self.childfeatureclass)

        #print("parentcount " + parentcount[0])
        #print("childcount " + childcount[0])

        self.assertEqual(parentcount[0]
                        ,childcount[0])

       # self.editversion.delete()

    def test_dsyncfulldelete(self):

        arcpy.DeleteFeatures_management(self.testfc.featureclass)

        retval = self.replica.synchronize()
        
        self.assertEqual(retval,'success')      

        parentcount = arcpy.GetCount_management(self.testfc.featureclass)
        childcount  = arcpy.GetCount_management(self.childfeatureclass)
        
        self.assertEqual(parentcount[0]
                        ,'0')

        self.assertEqual(childcount[0]
                        ,'0')

    def test_zdelete(self):

       self.assertEqual(self.replica.delete()
                       ,'success')
                   


if __name__ == '__main__':
    unittest.main()
