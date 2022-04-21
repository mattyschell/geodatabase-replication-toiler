import arcpy
#from arcpy import env

import gdb


class Replica(object):

    def __init__(self
                ,gdb
                ,name):

        self.gdb = gdb
        self.name = name.upper()
        self.fullyqualifiedname = '{0}.{1}'.format(self.gdb.username
                                                  ,self.name) 

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

        self.childsdeconn = childsdeconn
        desc = arcpy.Describe(self.childsdeconn)
        connProps = desc.connectionProperties
        self.fullyqualifiedchildname = '{0}.{1}'.format(connProps.user.upper()
                                                       ,self.name) 

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
     
            return arcpy.GetMessages(0)
            
        else:

            return 'success'

    def synchronize(self):

        try:

            arcpy.SynchronizeChanges_management(self.gdb.sdeconn
                                                ,self.name
                                                ,self.childsdeconn
                                                ,'FROM_GEODATABASE1_TO_2')
    
        except:

            return arcpy.GetMessages(0)

        else:

            return 'success'

    def delete(self):

        # one way parent to child, this is "delete"
        # "If providing the replica name, it must be fully qualified, 
        # for example, myuser.myreplica"

        try:
            arcpy.UnregisterReplica_management(self.gdb.sdeconn
                                              ,self.fullyqualifiedname)
        except:
            parentmessages = arcpy.GetMessages(0)
        else:
            parentmessages = 'success'

        try:
            arcpy.UnregisterReplica_management(self.childsdeconn
                                              ,self.fullyqualifiedchildname)
        except:
            childmessages = arcpy.GetMessages(0)
        else:
            childmessages = 'success'

        if  parentmessages == 'success' \
        and childmessages  == 'success':
            return 'success'
        else:
            return '{0}{1}{2}{3}'.format('\n parent: \n '
                                        ,parentmessages
                                        ,'\n  child: \n'
                                        ,childmessages)




