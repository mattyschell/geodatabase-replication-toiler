import sys
import os
import time
import logging

import punkreplica


if __name__ == "__main__":

    parentgdb   = sys.argv[1]
    childgdb    = sys.argv[2]
    replicaname = sys.argv[3] 
                  
    timestr = time.strftime("%Y%m%d-%H%M%S")
    targetlog = os.path.join(os.environ['TARGETLOGDIR'] 
                            ,'createpunkreplica-{0}-{1}.log'.format(replicaname
                                                                   ,timestr))

    logging.basicConfig(filename=targetlog
                       ,level=logging.INFO)

    babypunkreplica = punkreplica.Replica(parentgdb
                                         ,childgdb
                                         ,replicaname)

    logging.info('Creating baby {0} replica from {1}'.format(babypunkreplica.name
                                                            ,babypunkreplica.parentgdb))

    # Possible
    # PermissionError: [Errno 13] Permission denied: '_gdb.xxxxx.1812.41680.sr.lock'
    retval = babypunkreplica.create()

    if retval != 'success':        
        logging.error('zipping up {0} returned {1}'.format(babypunkreplica.parentgdb
                                                          ,retval))
        exit(1)

    logging.info('Synchronizing baby {0} replica from {1}'.format(babypunkreplica.childgdb
                                                                 ,babypunkreplica.parentgdb))

    retval = babypunkreplica.synchronize()

    if retval != 'success':
        logging.error('synchronizing {0} returned {1}'.format(babypunkreplica.childgdb
                                                             ,retval))
        exit(1)

    else:

        logging.info('Synchronicity success as usual')
        exit(0)

