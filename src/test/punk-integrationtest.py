import os
import unittest

import arcpy
import punkreplica

class ReplicaTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.parentgdb    = os.environ['SDEPARENT']
        self.childgdb     = os.environ['SDECHILD']
        self.featureclass = os.environ['TARGETFC']

        self.parentfeatureclass = os.path.join(self.parentgdb
                                              ,self.featureclass)

        self.childfeatureclass = os.path.join(self.childgdb
                                             ,self.featureclass)
        
        self.replica = punkreplica.Replica(self.parentgdb
                                          ,self.childgdb
                                          ,'punk')

    @classmethod
    def tearDownClass(self):
 
        self.replica.delete()

    def test_acreate(self):

        self.assertEqual(self.replica.create(),'success')      

    def test_bsynchronize(self):

        self.assertEqual(self.replica.synchronize(),'success')
        
        parentcount = arcpy.management.GetCount(self.parentfeatureclass)
        childcount  = arcpy.management.GetCount(self.childfeatureclass)
     
        self.assertEqual(parentcount[0]
                        ,childcount[0])

    def test_ccompare(self):

        self.assertEqual(self.replica.synchronize(),'success')

        self.assertEqual(self.replica.compare(self.featureclass)
                        ,0)

    def test_ddelete(self):
 
        self.replica.delete()

        # test that delete is ok with nonexistent files
        self.replica.delete()


if __name__ == '__main__':
    unittest.main()
