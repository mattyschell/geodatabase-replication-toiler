import os
import shutil
from io import StringIO
import re
import arcpy

# todo: get this outta here
import cx_sde


# loosely follows the api of replica.py
# punk replicas are ephemeral however

class Replica(object):

    def __init__(self
                ,parentgdb # D:\temp\parent\project.gdb
                ,childgdb  # D:\temp\child\project.gdb 
                ,name):    # departmentreplica-dev-

        self.parentgdb = parentgdb
        self.childgdb  = childgdb
        self.name      = name
        
        #PunknameParentname.gdb
        punkgdb = '{0}{1}'.format(self.name,os.path.basename(self.parentgdb))

        # D:\temp\parent\PunknameParentname.gdb
        self.fullyqualifiedparentname = os.path.join(os.path.dirname(self.parentgdb)
                                                    ,punkgdb)
        self.fullyqualifiedchildname = os.path.join(os.path.dirname(self.childgdb)
                                                   ,punkgdb)
        
    def copytree(self
                ,sourcedir
                ,targetdir):
        
        try:
            shutil.copytree(sourcedir
                           ,targetdir)
        except Exception as e:
            error_message = StringIO()
            error_message.write(str(e))
            error_message.seek(0)
            return 'fail: copying {0} to {1} returns {2}'.format(sourcedir
                                                                ,targetdir
                                                                ,error_message.read())
        
        for root, dirs, files in os.walk(targetdir):
            for dir in dirs:
                shutil.copystat(os.path.join(root, dir), os.path.join(targetdir, dir))
            for file in files:
                shutil.copystat(os.path.join(root, file), os.path.join(targetdir, file))
                
        return 'success' 

    def create(self):

        # in a punk geodatabase replica creation is copying and renaming  
        # a file geodatabase. PUNK AF
        # no data list inputs, replicate the full geodatabase or go home

        # create
        # X:\path\parent\project.gdb
        # X:\path\parent\departmentreplica-dev-project.gdb

        # always catch errors and return clues
        # we want to triage emails not RDP to poke around in logs
        retval = 'success'
        
        if not (os.path.exists(self.parentgdb)):

            return 'fail: parent {0} doesnt exist'.format(self.parentgdb)
        
        if os.path.exists(self.fullyqualifiedparentname):
            
            try:
                shutil.rmtree(self.fullyqualifiedparentname)
            except Exception as e:
                error_message = StringIO()
                error_message.write(str(e))
                error_message.seek(0)
                return 'fail: removing {0} returns {1}'.format(self.fullyqualifiedparentname
                                                              ,error_message.read()) 

        retval = self.copytree(self.parentgdb
                              ,self.fullyqualifiedparentname)
            
        if not (os.path.exists(self.fullyqualifiedparentname)):
                
            return 'fail: after copying {0} doesnt exist'.format(self.parentzip)

        return retval

    def synchronize(self):

        # caller must create() and handle failures
        # sychronize transfers a gdb to the child
        # we tend to synchronize across flakey networks
        # at weird hours so everything is wrapped in try except

        if (os.path.exists(self.fullyqualifiedchildname)):

            try:
                shutil.rmtree(self.fullyqualifiedchildname)    
            except:
                return 'fail: cant remove defunct {0}'.format(self.fullyqualifiedchildname)                
   
        try:
            # childpath\departmentreplica-dev-project.gdb
            retval = self.copytree(self.fullyqualifiedparentname
                                  ,self.fullyqualifiedchildname)
        except:
            return 'fail: cant copy {0} to {1}'.format(self.parentzip
                                                      ,self.childzip)

        # synchronize! :-)
        # copy childpath\departmentreplica-dev-project.gdb
        # to   childpath\project.gdb
        retval = self.copytree(self.fullyqualifiedchildname
                              ,self.childgdb)
        
        if retval != 'success':
            return retval

        #cleanup punkpscsclcscl.gdb
        if (os.path.exists(self.fullyqualifiedchildname)):

            # not strictly necessary
            shutil.rmtree(self.fullyqualifiedchildname)   

        return 'success'

    def delete(self):

        if os.path.exists(self.childgdb):
            shutil.rmtree(self.childgdb)

        if os.path.exists(self.fullyqualifiedchildname):
            shutil.rmtree(self.fullyqualifiedchildname) 

        if os.path.exists(self.fullyqualifiedparentname):
            shutil.rmtree(self.fullyqualifiedparentname) 

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
   
