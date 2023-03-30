import arcpy
import os
import glob
import shutil
# import zipfile
# import gdb

class Replica(object):

    def __init__(self
                ,parentgdb # D:\temp\parent\cscl.gdb
                ,childgdb  # D:\temp\child\cscl.gdb
                ,name):    # PUNK

        self.parentgdb = parentgdb
        self.childgdb  = childgdb
        self.name      = name

        
        #punkcscl.gdb
        punkgdb = '{0}{1}'.format(self.name,os.path.basename(self.parentgdb))

        # D:\temp\parent\punkcscl.gdb
        self.fullyqualifiedparentname = os.path.join(os.path.dirname(self.parentgdb)
                                                    ,punkgdb)

        self.fullyqualifiedchildname = os.path.join(os.path.dirname(self.childgdb)
                                                   ,punkgdb)

    def create(self):

        # in a punk geodatabase replica creation is zipping 
        # a file geodatabase. PUNK AF
        # no data list input, full geodatabase or go home

        try:
            if not (os.path.exists(self.parentgdb)):
                return 'fail parent {0} doesnt exist'.format(self.parentgdb)
            
            if os.path.exists(self.fullyqualifiedparentname):
                
                os.remove(self.fullyqualifiedparentname)

            shutil.make_archive(self.fullyqualifiedparentname
                                ,'zip'
                                ,self.parentgdb)

        except:

            return 'fail'
            
        else:

            return 'success'

    def synchronize(self):

        try:

            pass
    
        except:

            return 'fail'

        else:

            return 'success'

    def delete(self):

        # "If providing the replica name, it must be fully qualified, 
        # for example, myuser.myreplica"

        try:
            pass
            #arcpy.UnregisterReplica_management(self.parentgdb.sdeconn
            #                                  ,self.fullyqualifiedparentname)
        except:
            parentmessages = 'fail'
        else:
            parentmessages = 'success'

        try:
            pass
            #arcpy.UnregisterReplica_management(self.childgdb.sdeconn
            #                             ,self.fullyqualifiedchildname)
        except:
            childmessages = 'fail'
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

