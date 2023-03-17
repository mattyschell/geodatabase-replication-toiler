import sys
import os

import gdb
import fc
import cx_sde
import arcpy

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

    return subaddressfeaturetable

def qa(parentconn
      ,childconn
      ,basetablename):

    sql = 'select count(*) from cscl.{0}_evw'.format(basetablename)

    parentkount = cx_sde.selectavalue(parentconn
                                     ,sql)

    childkount = cx_sde.selectavalue(childconn
                                     ,sql)

    return (parentkount - childkount)
    

if __name__ == "__main__":

    module        = sys.argv[1]
    parentsdeconn = sys.argv[2]
         
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

        subaddressfeaturetable = esrify(childgeodatabase
                                       ,featuretablename
                                       ,featuretableuser)

        qaresult = qa(parentsdeconn
                     ,childsdeconn
                     ,featuretablename)

        if qaresult != 0:
            raise ValueError('Difference of {0} in record counts '.format(qaresult) \
                           + 'comparing {0} in '.format(featuretablename) \
                           + '{0} vs {1}'.format(parentsdeconn,childsdeconn))

    exit(0)
