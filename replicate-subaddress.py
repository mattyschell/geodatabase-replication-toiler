import sys
import os

import gdb
import fc

# 1. replicate-subaddress.py: TEARDOWN 
# 2. SQLPlus export from oracle
# 3. psql import to postgres
# 4. replicate-subaddress.py: QA 
# 4. replicate-subaddress.py: ESRIFY 
#    4a. register
#    4b. version
#    4c. analyze
#    4d. grants


# TEARDOWN
# QA
# ESRIFY

if __name__ == "__main__":

    module    = sys.argv[1]
    parentsde = sys.argv[2] # only for QA counts

    childsdeconn = os.environ['SDEFILE']
    childgdb = gdb.Gdb()
    featuretable = 'subaddress'

    childfc = fc.Fc(childgdb
                   ,featuretable) 
