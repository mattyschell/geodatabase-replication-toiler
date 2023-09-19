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

    mypunkreplica = punkreplica.Replica(parentgdb
                                       ,childgdb
                                       ,replicaname)

    logging.info('Creating punk {0} replica from {1}'.format(mypunkreplica.name
                                                            ,mypunkreplica.parentgdb))

    # Possible
    # PermissionError: [Errno 13] Permission denied: '_gdb.xxxxx.1812.41680.sr.lock'
    retval = mypunkreplica.create()

    if retval != 'success':        
        logging.error('creating {0} returned{1}{2}'.format(mypunkreplica.fullyqualifiedparentname
                                                          ,'\n'
                                                          ,retval))
        exit(1)

    logging.info('Synchronizing {0} replica from {1}'.format(mypunkreplica.childgdb
                                                            ,mypunkreplica.fullyqualifiedparentname))

    retval = mypunkreplica.synchronize()

    if retval != 'success':
        logging.error('synchronizing {0} returned{1}{2}'.format(mypunkreplica.childgdb
                                                               ,'\n'
                                                               ,retval))
        exit(1)

    else:

        logging.info('Synchronicity success as usual')
        exit(0)

