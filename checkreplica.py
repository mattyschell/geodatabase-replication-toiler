import sys
import os
import logging
import time 

import punkreplica


if __name__ == "__main__":

    pparent      = sys.argv[1] # C:\temp\cscl.gdb
    pchild       = sys.argv[2] # D:\temp\cscl.gdb
    preplicaname = sys.argv[3] # punk
    playerlist   = sys.argv[4] # nybb

    timestr = time.strftime("%Y%m%d-%H%M%S")
    targetlog = os.path.join(os.environ['TARGETLOGDIR'] 
                            ,'checkreplica-{0}-{1}.log'.format(preplicaname, timestr))

    logging.basicConfig(filename=targetlog
                       ,level=logging.INFO)

    checkreplica = punkreplica.Replica(pparent
                                      ,pchild
                                      ,preplicaname)

    result = 'pass'

    logging.info('| featurelayer | rowcountdifference |')
    logging.info('| --- | --- |')

    for featurelayer in playerlist.split(','):
        
        try:
            
            kount = checkreplica.compare(featurelayer)

            if kount > 0:
                result = 'fail'

        except:

            result = 'fail'
            kount  = 'unknown'

        logging.info('| {0} | {1} | '.format(featurelayer,kount))


    if result == 'pass':
        exit(0)
    else:
        exit(1)
