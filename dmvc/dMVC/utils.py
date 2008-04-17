
import threading
import model
import remotecommand
import events
import logging


#Logger #{{{
logger = logging.getLogger('dMVC')
hdlr = logging.FileHandler('dMVC.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
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

#rServerSingleton #{{{
__rServerSingleton = None

def getRServer(): 
  if __rServerSingleton == None:
    raise Exception("RServer has to be instanciated before calling getRServer()")
  return __rServerSingleton

def setRServer(rserver):
  global __rServerSingleton
  __rServerSingleton = rserver
#}}}

#rClientSingleton #{{{
__rClientSingleton = None

def getRClient(): 
  if __rClientSingleton == None:
    raise Exception("RClient has to be instanciated before calling getRClient()")
  return __rClientSingleton

def setRClient(rclient):
  global __rClientSingleton
  __rClientSingleton = rclient
#}}}

def objectToSerialize(object, rServer): #{{{

  if isinstance(object, model.Model):
    return object.objectToSerialize(rServer)

  elif isinstance(object, remotecommand.RCommand):
    return object.objectToSerialize(rServer)

  elif isinstance(object, events.Event):
    return object.objectToSerialize(rServer)

  elif isinstance(object,list): 
    resultObject = []
    for each in object:
      resultObject.append(objectToSerialize(each, rServer))
    return resultObject

  elif isinstance(object,tuple):
    resultObject = []
    for each in object:
      resultObject.append(objectToSerialize(each, rServer))
    return tuple(resultObject)

  elif isinstance(object,dict):
    resultObject = {}
    for key in object.keys():
      resultObject[objectToSerialize(key, rServer)] = objectToSerialize(object[key], rServer)
    return resultObject

  else:
    return object
#}}}

