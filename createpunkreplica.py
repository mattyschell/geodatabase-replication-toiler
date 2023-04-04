import sys
import os

import punkreplica
#import gdb


if __name__ == "__main__":

    parentgdb   = sys.argv[1]
    childgdb    = sys.argv[2]
    replicaname = sys.argv[3] 
                  
    babypunkreplica = punkreplica.Replica(parentgdb
                                         ,childgdb
                                         ,replicaname)

    # Possible
    # PermissionError: [Errno 13] Permission denied: '_gdb.T2UA64237XN.1812.41680.sr.lock'
    retval = babypunkreplica.create()

    if retval != 'success':
        print('zipping up {0} returned {1}'.format(babypunkreplica.parentgdb
                                                  ,retval))
        exit(1)

    retval = babypunkreplica.synchronize()

    if retval != 'success':
        print('synchronizing {0} returned {1}'.format(babypunkreplica.childgdb
                                                     ,retval))
        exit(1)

    else:

        exit(0)

