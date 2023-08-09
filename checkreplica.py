import sys
import os
import logging
import time 
import socket

import punkreplica


if __name__ == "__main__":

    pparent      = sys.argv[1] # C:\temp\cscl.gdb
    pchild       = sys.argv[2] # D:\temp\cscl.gdb
    preplicaname = sys.argv[3] # punkpscscl
    playerlist   = sys.argv[4] # cscl.Borough,cscl.xyz

    timestr = time.strftime("%Y%m%d-%H%M%S")
    targetlog = os.path.join(os.environ['TARGETLOGDIR'] 
                            ,'checkreplica-{0}-{1}.log'.format(preplicaname, timestr))

    logging.basicConfig(filename=targetlog
                       ,level=logging.INFO)

    checkreplica = punkreplica.Replica(pparent
                                      ,pchild
                                      ,preplicaname)

    result = 'pass'

    logging.info('   | featurelayer | rowcountdifference |   ')

    for featurelayer in playerlist.split(','):
        
        try:
            
            kount = checkreplica.compare(featurelayer)

            if kount != 0:
                result = 'fail'

        except:

            result = 'fail'
            kount  = 'unknown'

        logging.info('   ')
        logging.info('   | {0} | {1} |   '.format(featurelayer,kount))
        

    logging.info('   ')
    logging.info('   replica QA result: {0}   '.format(result))
    logging.info('   ')
    logging.info('   comparing parent {0} to child {1}    '.format(pparent,pchild))
    logging.info('   ')
    logging.info('   running from {0}   '.format(socket.gethostname()))
    logging.info('   ')
    
    if result == 'pass':
        exit(0)
    else:
        exit(1)
