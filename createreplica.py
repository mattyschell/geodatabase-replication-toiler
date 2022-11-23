import sys
import os

import replica
import gdb

# have not run this recently leaving  here as ref


if __name__ == "__main__":

    parentsdeconn = sys.argv[1]
    childsdeconn  = sys.argv[2]
    replicaname   = sys.argv[3].upper()
    in_data       = sys.argv[4] 

    os.environ['SDEFILE'] = parentsdeconn
    parentgdb = gdb.Gdb()
    os.environ['SDEFILE'] = childsdeconn
    childgdb = gdb.Gdb()

    # slow and steady so we can read it later

    in_datalist = in_data.split(",") 

    featureclasslist = []
    for featureclass in in_datalist:
        featureclasslist.append(os.path.join(parentsdeconn
                                            ,featureclass))
                  
    babyreplica = replica.Replica(parentgdb
                                 ,childgdb
                                 ,replicaname)

    retval = babyreplica.create(featureclasslist)

    if retval == 'success':
        exit(0)
    else:
        print(retval)
        exit(1)

