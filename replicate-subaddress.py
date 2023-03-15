import sys
import os

import gdb
import fc
import  arcpy

# 1. replicate-subaddress.py: TEARDOWN 
# 2. SQLPlus export from oracle
# 3. psql import to postgres
# 4. replicate-subaddress.py: ESRIFY 
#    4a. register
#    4b. version
#    4c. Index sub_address_id 
#    4c. analyze
#    4d. grants
# 4. replicate-subaddress.py: QA 


# TEARDOWN
# QA
# ESRIFY

def teardown(subaddressfeaturetable):

    subaddressfeaturetable.delete()
    return 0

def esrify(childgeodatabase
          ,featuretablename
          ,featuretableuser):

    childgeodatabase.registerfeatureclass(featuretablename)

    subaddressfeaturetable = fc.Fc(childgeodatabase
                                  ,featuretablename) 

    subaddressfeaturetable.version()

    subaddressfeaturetable.index('sub_address_id')
                           
    subaddressfeaturetable.analyze()

    arcpy.management.ChangePrivileges(subaddressfeaturetable.featureclass
                                     ,featuretableuser
                                     ,'GRANT'
                                     ,'AS_IS')

    return 0
    

if __name__ == "__main__":

    module    = sys.argv[1]

    childsdeconn     = os.environ['SDEFILE']
    childgeodatabase = gdb.Gdb(database='postgres')
    featuretablename = 'subaddress'
    featuretableuser = 'psgis'

    # questionable pattern: todo refactor
    if module.lower() == 'teardown':
        
        childfeatureclass = fc.Fc(childgeodatabase
                                 ,featuretablename) 

        retval = teardown(childfeatureclass)

    else:

        retval = esrify(childgeodatabase
                       ,featuretablename
                       ,featuretableuser)


    exit(0)
