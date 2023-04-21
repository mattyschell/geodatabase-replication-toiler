import os
import shutil
import arcpy

# todo: get this outta here
import cx_sde


# loosely follows standard replica wrapper
# punk replicas are ephemeral

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

    def create(self):

        # in a punk geodatabase replica creation is zipping 
        # a file geodatabase. PUNK AF
        # no data list inputs, replicate the full geodatabase or go home

        if not (os.path.exists(self.parentgdb)):

            return 'fail parent {0} doesnt exist'.format(self.parentgdb)
        
        if os.path.exists(self.fullyqualifiedparentname):
            
            os.remove(self.fullyqualifiedparentname)

        shutil.make_archive(self.fullyqualifiedparentname
                            ,'zip'
                            ,self.parentgdb)

        if not (os.path.exists('{0}.{1}'.format(self.fullyqualifiedparentname
                                                ,'zip'))):
            
            return 'fail'

        else:

            return 'success'

    def synchronize(self):

        # create
        # D:\temp\parent\cscl.gdb
        # D:\temp\parent\punkcscl.gdb.zip

        if (self.create() == 'success'):

            if (os.path.exists('{0}.{1}'.format(self.fullyqualifiedchildname
                                               ,'zip'))):

                # not strictly necessary
                os.remove('{0}.{1}'.format(self.fullyqualifiedchildname
                                          ,'zip'))

            # copy to D:\temp\child\punkcscl.gdb.zip 

            shutil.copy('{0}.{1}'.format(self.fullyqualifiedparentname
                                        ,'zip')
                       ,'{0}.{1}'.format(self.fullyqualifiedchildname
                                        ,'zip')
                       )
       
            # unzip to 
            # D:\temp\child\punkcscl.gdb 

            if (os.path.exists(self.fullyqualifiedchildname)):

                # not strictly necessary
                shutil.rmtree(self.fullyqualifiedchildname)                    

            shutil.unpack_archive('{0}.{1}'.format(self.fullyqualifiedchildname
                                                  ,'zip')
                                 ,self.fullyqualifiedchildname
                                 ,'zip')

            # synchronize! :-)
            # copy D:\temp\child\punkcscl.gdb
            # to   D:\temp\child\cscl.gdb

            if (os.path.exists(self.childgdb)):

                shutil.rmtree(self.childgdb)

            #done here
            shutil.copytree(self.fullyqualifiedchildname
                           ,self.childgdb)

            #cleanup punkpscsclcscl.gdb.zip
            if (os.path.exists('{0}.{1}'.format(self.fullyqualifiedchildname
                                               ,'zip'))):

                os.remove('{0}.{1}'.format(self.fullyqualifiedchildname
                                          ,'zip'))

            #cleanup punkpscsclcscl.gdb
            if (os.path.exists(self.fullyqualifiedchildname)):

                # not strictly necessary
                shutil.rmtree(self.fullyqualifiedchildname)   

            return 'success'

        return 'fail'

    def delete(self):

        if (os.path.exists(self.childgdb)):
            shutil.rmtree(self.childgdb)

        if (os.path.exists(self.fullyqualifiedchildname)):
            shutil.rmtree(self.fullyqualifiedchildname) 

        if (os.path.exists('{0}.{1}'.format(self.fullyqualifiedchildname
                                           ,'zip'))):
            os.remove('{0}.{1}'.format(self.fullyqualifiedchildname
                                      ,'zip'))
                                      
        if (os.path.exists('{0}.{1}'.format(self.fullyqualifiedparentname
                                           ,'zip'))):
            os.remove('{0}.{1}'.format(self.fullyqualifiedparentname
                                      ,'zip'))

    def compare(self
               ,featurelayer):

        # this is a hack (on top of a hack), see refactoring issue
        # accept either cscl.centerline or centerline for featurelayer

        # little punk kids never have schemas
        childfeatureclass = os.path.join(self.childgdb
                                         ,featurelayer.split('.')[-1])
                                         
        #print('childfeatureclass {0}'.format(childfeatureclass))

        childkount = int(arcpy.management.GetCount(childfeatureclass)[0])

        # either featurelayer formats are responsible parents  
        # but we can't use arcpy 3 to access CSCL!    

        if "." in featurelayer:  

            sql = 'SELECT count(*) FROM {0}_evw'.format(featurelayer)
            
            #print('sql {0}'.format(sql))

            parentkount = cx_sde.selectavalue(self.parentgdb
                                             ,sql)

        else: 
        
            parentfeatureclass = os.path.join(self.parentgdb
                                             ,featurelayer)
                                             
            # print('parentfeatureclass {0}'.format(parentfeatureclass))
                                             
            parentkount = int(arcpy.management.GetCount(parentfeatureclass)[0]) 

        return (parentkount - childkount)
   
