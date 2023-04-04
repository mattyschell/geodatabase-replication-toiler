import os
import unittest

import arcpy
import punkreplica

class ReplicaTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.parentgdb = os.environ['SDEPARENT']
        self.childgdb  = os.environ['SDECHILD']

        self.parentfeatureclass = os.path.join(self.parentgdb
                                              ,os.environ['TARGETFC'])

        self.childfeatureclass = os.path.join(self.childgdb
                                             ,os.environ['TARGETFC'])
        
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
        
        parentcount = arcpy.GetCount_management(self.parentfeatureclass)
        childcount  = arcpy.GetCount_management(self.childfeatureclass)
     
        self.assertEqual(parentcount[0]
                        ,childcount[0])

    def test_cdelete(self):
 
        self.replica.delete()

        # test that delete is ok with nonexistent files
        self.replica.delete()


if __name__ == '__main__':
    unittest.main()
