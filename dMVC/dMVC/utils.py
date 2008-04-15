import threading

try:
  import ggserver.model
except:
  print "client only execution"

import ggcommon.remotecommand
import ggcommon.eventos



#---------------------------------------------------------
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
#---------------------------------------------------------
  




def objectToSerialize(object, rServer): #{{{

  if isinstance(object, ggserver.model.Model):
    return object.objectToSerialize(rServer)

  elif isinstance(object, ggcommon.remotecommand.RCommand):
    return object.objectToSerialize(rServer)

  elif isinstance(object, ggcommon.eventos.Event):
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
