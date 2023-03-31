import os
import shutil

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

            shutil.copytree(self.fullyqualifiedchildname
                           ,self.childgdb)

            return 'success'

        return 'fail'

    #def delete(self):

    #    shutil.rmtree(self.childgdb)
    #    shutil.rmtree(self.fullyqualifiedchildname) 
    #    os.remove('{0}.{1}'.format(self.fullyqualifiedchildname
    #                              ,'zip'))
    #    os.remove('{0}.{1}'.format(self.fullyqualifiedparentname
    #                              ,'zip'))

    #    return 'success'