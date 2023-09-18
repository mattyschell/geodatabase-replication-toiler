import os
import unittest
import tempfile

import arcpy
import punkreplica

class ReplicaTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        # reminder that these are file geodatabases
        # the tests will start with a file geodatabase
        # in the resources directory with some simple data

        self.parentgdb         = os.environ['SDEPARENT']
        self.childgdb          = os.environ['SDECHILD']
        self.featureclass      = os.environ['TARGETFC']
        self.relationshipclass = os.environ['TARGETRELATIONSHIPCLASS']

        self.parentfeatureclass = os.path.join(self.parentgdb
                                              ,self.featureclass)

        self.childfeatureclass = os.path.join(self.childgdb
                                             ,self.featureclass)
        
        self.replica = punkreplica.Replica(self.parentgdb
                                          ,self.childgdb
                                          ,'punktest')

    @classmethod
    def tearDownClass(self):
        self.replica.delete()

    def tearDown(self):
        self.replica.delete()

    def test_acreate(self):

        self.assertEqual(self.replica.create(),'success')     

    def test_bsynchronize(self):

        self.replica.create()

        self.assertEqual(self.replica.synchronize(),'success')
    
        parentcount = arcpy.management.GetCount(self.parentfeatureclass)
        childcount  = arcpy.management.GetCount(self.childfeatureclass)
 
        self.assertEqual(parentcount[0]
                        ,childcount[0])

    def test_ccompare(self):

        self.replica.create()

        self.assertEqual(self.replica.synchronize(),'success')

        self.assertEqual(self.replica.compare(self.featureclass)
                        ,0)
        
    def test_dcomparerelationshipclass(self):

        # test that we can compare counts of attributed relationship classes
        # will be empty but a count of 0 is a count I will allow it
        self.replica.create()

        self.assertEqual(self.replica.synchronize(),'success')

        self.assertEqual(self.replica.compare(self.relationshipclass)
                        ,0)

    def test_esynchfail(self):

        # synch to an illegal path
        self.childgdb  = os.path.join(tempfile.gettempdir()
                                     ,'<>:') 

        # just overrides the child and child path
        self.replica = punkreplica.Replica(self.parentgdb
                                          ,self.childgdb
                                          ,'punktest')
        
        self.assertEqual(self.replica.create(),'success')
        
        retval = self.replica.synchronize()

        # fail: cant copy xxx.gdb to yyyy\<>:
        self.assertTrue(retval.startswith('fail'))

    def test_fdelete(self):
 
        self.replica.delete()

        # test that delete is ok with nonexistent files
        self.replica.delete()


if __name__ == '__main__':
    unittest.main()
