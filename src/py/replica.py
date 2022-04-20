import arcpy

import gdb


class Replica(object):

    def __init__(self
                ,gdb
                ,name):

        self.gdb = gdb
        self.name = name.upper()

    def exists(self):

        pass

    def create(self
              ,childsdeconn
              ,in_data):

        # check if data is versioned?

        arcpy.management.CreateReplica(in_data
                                      ,'ONE_WAY_REPLICA'
                                      ,childsdeconn
                                      ,self.name
                                      ,'SIMPLE'
                                      ,'PARENT_DATA_SENDER'
                                      ,'DO_NOT_ADD'
                                      ,'DO_NOT_REUSE'
                                      ,'DO_NOT_GET_RELATED')


    def delete(self):

        arcpy.UnregisterReplica_management(self.gdb.sdeconn
                                          ,self.name)



