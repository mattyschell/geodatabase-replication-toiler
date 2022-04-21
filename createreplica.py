import sys
import os

import replica
import gdb


if __name__ == "__main__":

    parentsdeconn = sys.argv[1]
    childsdeconn  = sys.argv[2]
    replicaname   = sys.argv[3].upper()
    in_data       = sys.argv[4] 

    os.environ['SDEFILE'] = parentsdeconn
    parentgdb = gdb.Gdb()

    # slow and steady so we can read it later

    in_datalist = in_data.split(",") 

    featureclasslist = []
    for featureclass in in_datalist:
        featureclasslist.append(os.path.join(parentsdeconn
                                            ,featureclass))
                  
    babyreplica = replica.Replica(parentgdb
                                 ,replicaname)

    retval = babyreplica.create(childsdeconn
                               ,featureclasslist)

    if retval == 'success':
        exit(0)
    else:
        print(retval)
        exit(1)

