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

    def preparedata(self
                   ,in_data):

        for dataset in in_data:

            arcpy.AddGlobalIDs_management(dataset)
            arcpy.RegisterAsVersioned_management(dataset
                                                ,"NO_EDITS_TO_BASE")

    def create(self
              ,childsdeconn
              ,parent_data_list
              ,child_data_list):

        self.childsdeconn = childsdeconn
        desc = arcpy.Describe(self.childsdeconn)
        connProps = desc.connectionProperties
        self.fullyqualifiedchildname = '{0}.{1}'.format(connProps.user.upper()
                                                       ,self.name) 

        self.preparedata(child_data_list)

        try:
            arcpy.management.CreateReplica(parent_data_list
                                          ,'ONE_WAY_REPLICA'
                                          ,childsdeconn
                                          ,self.name
                                          ,'SIMPLE'
                                          ,'PARENT_DATA_SENDER'
                                          ,'DO_NOT_ADD'
                                          ,'DO_NOT_REUSE'
                                          ,'DO_NOT_GET_RELATED'
                                          ,''
                                          ,'DO_NOT_USE_ARCHIVING'
                                          ,'REGISTER_EXISTING_DATA')

        except:

            return arcpy.GetMessages(0)
            
        else:

            return 'success'

    def synchronize(self):

        try:

            arcpy.SynchronizeChanges_management(self.gdb.sdeconn
                                               ,self.name
                                               ,self.childsdeconn
                                               ,'FROM_GEODATABASE1_TO_2'
                                               ,'IN_FAVOR_OF_GDB1'
                                               ,'BY_OBJECT')
    
        except:

            return arcpy.GetMessages(0)

        else:

            return 'success'

    def delete(self):

        # I guess this is "delete"
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

