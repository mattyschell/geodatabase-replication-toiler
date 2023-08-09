import os
import shutil
import arcpy

# todo: get this outta here
import cx_sde


# loosely follows the api of replica.py
# punk replicas are ephemeral however

class Replica(object):

    def __init__(self
                ,parentgdb # D:\temp\parent\cscl.gdb
                ,childgdb  # D:\temp\child\cscl.gdb
                ,name):    # punk

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

        self.childzip  = '{0}.{1}'.format(self.fullyqualifiedchildname
                                         ,'zip')
        self.parentzip = '{0}.{1}'.format(self.fullyqualifiedparentname
                                         ,'zip')

    def create(self):

        # in a punk geodatabase replica creation is zipping 
        # a file geodatabase. PUNK AF
        # no data list inputs, replicate the full geodatabase or go home

        # create
        # D:\temp\parent\cscl.gdb
        # D:\temp\parent\punkcscl.gdb.zip

        if not (os.path.exists(self.parentgdb)):

            return 'fail parent {0} doesnt exist'.format(self.parentgdb)
        
        if os.path.exists(self.fullyqualifiedparentname):
            
            os.remove(self.fullyqualifiedparentname)

        shutil.make_archive(self.fullyqualifiedparentname
                           ,'zip'
                           ,self.parentgdb)

        if not (os.path.exists(self.parentzip)):
            
            return 'fail'

        else:

            return 'success'

    def synchronize(self):

        # caller must create() and handle failures
        # sychronize transfers a zipped gdb to the child

        # we tend to synchronize across flakey networks
        # at weird hours so everything is wrapped in try except

        if (os.path.exists(self.childzip)):

            # not strictly necessary
            try:
                os.remove(self.childzip)
            except:
                return 'fail: cant remove defunct zipped child {0}'.format(self.childzip)

        # copy to D:\temp\child\punkcscl.gdb.zip 

        try:
            shutil.copy(self.parentzip
                       ,self.childzip)
        except:
            return 'fail: cant copy {0} to {1}'.format(self.parentzip
                                                      ,self.childzip)
    
        # unzip to 
        # D:\temp\child\punkcscl.gdb 

        if (os.path.exists(self.fullyqualifiedchildname)):

            # not strictly necessary
            try:
                shutil.rmtree(self.fullyqualifiedchildname)    
            except:
                return 'fail: cant remove defunct {0}'.format(self.fullyqualifiedchildname)                

        try:
            shutil.unpack_archive(self.childzip
                                 ,self.fullyqualifiedchildname
                                ,'zip')
        except:
            return 'fail: cant unpack {0} to {1}'.format(self.childzip
                                                        ,self.fullyqualifiedchildname)

        # synchronize! :-)
        # copy D:\temp\child\punkcscl.gdb
        # to   D:\temp\child\cscl.gdb

        if (os.path.exists(self.childgdb)):

            try:
                shutil.rmtree(self.childgdb)
            except:
                return 'fail: cant remove defunct {0}'.format(self.childgdb)

        #done here
        try:
            shutil.copytree(self.fullyqualifiedchildname
                           ,self.childgdb)
        except:
            return 'fail: cant copy {0} to {1}'.format(self.fullyqualifiedchildname
                                                      ,self.childgdb)

        #cleanup punkpscsclcscl.gdb.zip
        if (os.path.exists(self.childzip)):

            os.remove(self.childzip)

        #cleanup punkpscsclcscl.gdb
        if (os.path.exists(self.fullyqualifiedchildname)):

            # not strictly necessary
            shutil.rmtree(self.fullyqualifiedchildname)   

        return 'success'

    def delete(self):

        if (os.path.exists(self.childgdb)):
            shutil.rmtree(self.childgdb)

        if (os.path.exists(self.fullyqualifiedchildname)):
            shutil.rmtree(self.fullyqualifiedchildname) 

        if (os.path.exists(self.childzip)):
            os.remove(self.childzip)
                                      
        if (os.path.exists(self.parentzip)):
            os.remove(self.parentzip)

    def compare(self
               ,featurelayer):

        # this is a hack (on top of a hack), see refactoring issue
        # accept either cscl.centerline or centerline for featurelayer

        # little punk kids never have schemas

        childfeatureclass = os.path.join(self.childgdb
                                        ,featurelayer.split('.')[-1])

        childkount = int(arcpy.management.GetCount(childfeatureclass)[0])

        # either featurelayer formats are responsible parents  
        # but we can't use arcpy 3 to access CSCL!
        # (unless we are getting a count from a table)
        
        if "." in featurelayer:  

            sql = 'SELECT count(*) FROM {0}_evw'.format(featurelayer)

            try:
                parentkount = cx_sde.selectavalue(self.parentgdb
                                                 ,sql)
            except:

                # relationship classes will bounce to here
                parentfeatureclass = os.path.join(self.parentgdb
                                                 ,featurelayer)
                parentkount = int(arcpy.management.GetCount(parentfeatureclass)[0]) 

        else: 
        
            # likely a relationship class
            # this section is almost unreachable
            # would need to be counting in the data owner schema, not
            # from a read only schema. Since we are dropping the schema
            parentfeatureclass = os.path.join(self.parentgdb
                                             ,featurelayer)
            
            parentkount = int(arcpy.management.GetCount(parentfeatureclass)[0]) 

        return int(parentkount - childkount)
   
