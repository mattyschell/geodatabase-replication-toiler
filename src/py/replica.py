import arcpy
#from arcpy import env

import gdb


class Replica(object):

    def __init__(self
                ,gdb
                ,name):

        self.gdb = gdb
        self.name = name.upper()

    def exists(self):

        pass


    def forceglobalids(self
                      ,in_data):

        # should do nothing if a globalid managed by ESRI exists
        # the presence of a column named globalid means nothing
        # it must be geodatabase-managed

        for dataset in in_data:

            arcpy.AddGlobalIDs_management(dataset)

    def create(self
              ,childsdeconn
              ,in_data):

        # check if data is versioned?

        self.forceglobalids(in_data)

        try:

            arcpy.management.CreateReplica(in_data
                                          ,'ONE_WAY_REPLICA'
                                          ,childsdeconn
                                          ,self.name
                                          ,'SIMPLE'
                                          ,'PARENT_DATA_SENDER'
                                          ,'DO_NOT_ADD'
                                          ,'DO_NOT_REUSE'
                                          ,'DO_NOT_GET_RELATED')

        except:

            # print('youve got mail')
            # print(arcpy.GetMessages())
            # print('end of mail spool')            
            return arcpy.GetMessages(0)
            
        else:

            return 'success'

    def delete(self):

        try:

            arcpy.UnregisterReplica_management(self.gdb.sdeconn
                                              ,self.name)

        except:

            return arcpy.GetMessages(0)

        else:

            return 'success'



