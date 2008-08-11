

#rServerSingleton #{{{
__RSERVER_SINGLETON = None

def getRServer(): 
  #global __RSERVER_SINGLETON
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
  #global __RCLIENT_SINGLETON
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
    return list(map(lambda each: objectToSerialize(each, rServer), obj))

  elif isinstance(obj, tuple):
    return tuple(map(lambda each: objectToSerialize(each, rServer), obj))

  elif isinstance(obj, dict):
    resultObject = {}
    for key, value in obj.iteritems():
      resultObject[objectToSerialize(key, rServer)] = objectToSerialize(value, rServer)
    return resultObject

  else:
    return obj
#}}}






def serverMaterialize(obj, rServer): #{{{
  if hasattr(obj, 'serverMaterialize'):
    return obj.serverMaterialize(rServer)

  elif isinstance(obj, list): 
    return list(map(lambda each: serverMaterialize(each, rServer), obj))

  elif isinstance(obj, tuple):
    return tuple(map(lambda each: serverMaterialize(each, rServer), obj))

  elif isinstance(obj, dict):
    resultObj = {}
    for key, value in obj.iteritems():
      resultObj[serverMaterialize(key, rServer)] = serverMaterialize(value, rServer)
    return resultObj

  else:
    return obj
  #}}}


def clientMaterialize(obj, rClient): #{{{
  if hasattr(obj, 'clientMaterialize'):
    return obj.clientMaterialize(rClient)

  elif isinstance(obj, list): 
    return list(map(lambda each: clientMaterialize(each, rClient), obj)) # Serialized lists becomes inmutable in client-side

  elif isinstance(obj, tuple):
    return tuple(map(lambda each: clientMaterialize(each, rClient), obj))

  elif isinstance(obj, dict):
    resultObj = {}
    for key, value in obj.iteritems():
      resultObj[clientMaterialize(key, rClient)] = clientMaterialize(value, rClient)
    return resultObj

  else:
    return obj
  #}}}
