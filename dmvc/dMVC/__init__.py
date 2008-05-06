import model
import remotemodel
import remotecommand
import events



#rServerSingleton #{{{
__RSERVER_SINGLETON = None

def getRServer(): 
  global __RSERVER_SINGLETON
  if __RSERVER_SINGLETON == None:
    raise Exception("RServer has to be instanciated before calling getRServer()")
  return __RSERVER_SINGLETON

def setRServer(rserver):
  global __RSERVER_SINGLETON
  if __RSERVER_SINGLETON != None:
    raise Exception("Can't create more then one instance of RServer")
  __RSERVER_SINGLETON = rserver
#}}}


#rClientSingleton #{{{
__RCLIENT_SINGLETON = None

def getRClient():
  global __RCLIENT_SINGLETON
  if __RCLIENT_SINGLETON == None:
    raise Exception("RClient has to be instanciated before calling getRClient()")
  return __RCLIENT_SINGLETON

def setRClient(rclient):
  global __RCLIENT_SINGLETON
  if __RCLIENT_SINGLETON != None:
    raise Exception("Can't create more then one instance of RClient")
  __RCLIENT_SINGLETON = rclient
#}}}



def objectToSerialize(obj, rServer): #{{{
  if hasattr(obj, 'objectToSerialize'):
    return obj.objectToSerialize(rServer)

  elif isinstance(obj, list): 
    resultObject = []
    for each in obj:
      resultObject.append(objectToSerialize(each, rServer))
    return resultObject

  elif isinstance(obj, tuple):
    resultObject = []
    for each in obj:
      resultObject.append(objectToSerialize(each, rServer))
    return tuple(resultObject)

  elif isinstance(obj, dict):
    resultObject = {}
    for key in obj.keys():
      resultObject[objectToSerialize(key, rServer)] = objectToSerialize(obj[key], rServer)
    return resultObject

  else:
    return obj
#}}}






def serverMaterialize(obj, rServer): #{{{
  if hasattr(obj, 'serverMaterialize'):
    return obj.serverMaterialize(rServer)

  elif isinstance(obj, list): 
    resultObj = []
    for i in range(len(obj)):
      resultObj.append(serverMaterialize(obj[i], rServer))
    return resultObj

  elif isinstance(obj, tuple):
    resultObj = []
    for i in range(len(obj)):
      resultObj.append(serverMaterialize(obj[i], rServer))
    return tuple(resultObj)

  elif isinstance(obj, dict):
    resultObj = {}
    for key in obj.keys():
      resultObj[serverMaterialize(key, rServer)] = serverMaterialize(obj[key], rServer)
    return resultObj

  else:
    return obj
  #}}}


def clientMaterialize(obj, rClient): #{{{
  if hasattr(obj, 'clientMaterialize'):
    return obj.clientMaterialize(rClient)

  elif isinstance(obj, list): 
    resultObj = []
    for i in range(len(obj)):
      resultObj.append(clientMaterialize(obj[i], rClient))
    return resultObj

  elif isinstance(obj, tuple):
    resultObj = []
    for i in range(len(obj)):
      resultObj.append(clientMaterialize(obj[i], rClient))
    return tuple(resultObj)

  elif isinstance(obj, dict):
    resultObj = {}
    for key in obj.keys():
      resultObj[clientMaterialize(key, rClient)] = clientMaterialize(obj[key], rClient)
    return resultObj

  else:
    return obj
  #}}}
