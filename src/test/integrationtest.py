import os
import unittest
import pathlib

import gdb
import fc
import replica

class ReplicaTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.sdeconn = os.environ['SDEFILE']
        self.childsdeconn = os.environ['SDECHILD']
        self.geodatabase = gdb.Gdb()

        print('creating test replica')
        
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

    def test_acreate(self):

        in_data = []
        in_data.append(self.testfc.featureclass)

        retval = self.replica.create(self.childsdeconn
                                    ,in_data)

        self.assertEqual(retval,'success')

if __name__ == '__main__':
    unittest.main()
