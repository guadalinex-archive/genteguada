
import threading
import logging
import logging.handlers
import sys
import statistic


#Logger #{{{
logger = logging.getLogger('dMVC')
# log to file
hdlr = logging.FileHandler("dMVC.log")
# log to rotate file
#hdlr = logging.handlers.RotatingFileHandler("dMVC.log", "a", 200000, 5)
# log to console
#hdlr = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.CRITICAL)
#}}}


#nextID #{{{
__ID_MUTEX = threading.Semaphore(1)
__ID = 0

def nextID():
  global __ID
  global __ID_MUTEX
  __ID_MUTEX.acquire() 
  __ID += 1
  result = __ID
  __ID_MUTEX.release() 
  return result
#}}}


statServer = statistic.Statistics("server")
statClient = statistic.Statistics("client")
statEventTriggered = statistic.Statistics("event")

