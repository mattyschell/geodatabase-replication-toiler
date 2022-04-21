import os
import unittest
import pathlib
import arcpy

import gdb
import fc
import replica

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

    @classmethod
    def tearDownClass(self):

        retval = self.replica.delete()

        if self.testfc.exists():
            self.testfc.delete()

        try:
            arcpy.Delete_management(self.childfeatureclass )
        except:
            pass

        #pass 

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


    #def test_csyncsomeupdates(self):

    def test_dsyncsomedeletes(self):

        arcpy.DeleteFeatures_management(self.testfc.featureclass)

        retval = self.replica.synchronize()
        
        self.assertEqual(retval,'success')      

        parentcount = arcpy.GetCount_management(self.testfc.featureclass)
        childcount  = arcpy.GetCount_management(self.childfeatureclass)
        
        self.assertEqual(parentcount[0]
                        ,'0')

        self.assertEqual(childcount[0]
                        ,'0')


if __name__ == '__main__':
    unittest.main()
