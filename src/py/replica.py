import arcpy

import gdb

class Replica(object):

    def __init__(self
                ,parentgdb
                ,childgdb
                ,name):

        self.parentgdb = parentgdb
        self.childgdb  = childgdb
        self.name = name.upper()

        self.fullyqualifiedparentname = '{0}.{1}'.format(self.parentgdb.username
                                                        ,self.name) 

        self.fullyqualifiedchildname = '{0}.{1}'.format(self.childgdb.username
                                                        ,self.name) 

    def create(self
              ,data_list):

        try:
            arcpy.management.CreateReplica(data_list
                                          ,'ONE_WAY_REPLICA'
                                          ,self.childgdb.sdeconn
                                          ,self.name
                                          ,'FULL'
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

            arcpy.SynchronizeChanges_management(self.parentgdb.sdeconn
                                               ,self.name
                                               ,self.childgdb.sdeconn
                                               ,'FROM_GEODATABASE1_TO_2'
                                               ,'IN_FAVOR_OF_GDB1'
                                               ,'BY_OBJECT')
    
        except:

            return arcpy.GetMessages(0)

        else:

            return 'success'

    def delete(self):

        # "If providing the replica name, it must be fully qualified, 
        # for example, myuser.myreplica"

        try:
            arcpy.UnregisterReplica_management(self.parentgdb.sdeconn
                                              ,self.fullyqualifiedparentname)
        except:
            parentmessages = arcpy.GetMessages(0)
            print(parentmessages)
        else:
            parentmessages = 'success'

        try:
             arcpy.UnregisterReplica_management(self.childgdb.sdeconn
                                               ,self.fullyqualifiedchildname)
        except:
            childmessages = arcpy.GetMessages(0)
            print(childmessages)
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

