import os
import unittest
import pathlib
import arcpy

import punkreplica

class ReplicaTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.parentgdb = os.environ['SDEPARENT']
        self.childgdb  = os.environ['SDECHILD']

        self.childfeatureclass = os.path.join(self.childgdb
                                             ,os.environ['TARGETFC'])
        
        self.replica = punkreplica.Replica(self.parentgdb
                                          ,self.childgdb
                                          ,'punk')

        #self.parentfc = fc.Fc(self.geodatabase
        #                     ,'SOMELINES')

        #self.childfc = fc.Fc(self.childgeodatabase
        #                    ,'SOMELINES')


    @classmethod
    def tearDownClass(self):
 
        pass
        #retval = self.replica.delete()


    def test_acreate(self):

        retval = self.replica.create()
        
        self.assertEqual(retval,'success')      

        #parentcount = arcpy.GetCount_management(self.parentfc.featureclass)
        #childcount  = arcpy.GetCount_management(self.childfc.featureclass)
     
        #self.assertEqual(parentcount[0]
        #                ,childcount[0])

if __name__ == '__main__':
    unittest.main()
