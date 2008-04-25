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

  if isinstance(obj, model.Model):
    return obj.objectToSerialize(rServer)

  elif isinstance(obj, remotecommand.RCommand):
    return obj.objectToSerialize(rServer)

  elif isinstance(obj, events.Event):
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






def serverMaterialize(arg, rServer): #{{{

  if isinstance(arg, remotemodel.RemoteModel):
    return arg.serverMaterialize(rServer)

  elif isinstance(arg, list): 
    resultArg = []
    for i in range(len(arg)):
      resultArg.append(serverMaterialize(arg[i], rServer))
    return resultArg

  elif isinstance(arg, tuple):
    resultArg = []
    for i in range(len(arg)):
      resultArg.append(serverMaterialize(arg[i], rServer))
    return tuple(resultArg)

  elif isinstance(arg, dict):
    resultArg = {}
    for key in arg.keys():
      resultArg[serverMaterialize(key, rServer)] = serverMaterialize(arg[key], rServer)
    return resultArg

  else:
    return arg
  #}}}


def clientMaterialize(arg, rClient): #{{{

  if isinstance(arg, remotemodel.RemoteModel):
    return arg.clientMaterialize(rClient)

  elif isinstance(arg, events.Event):
    return arg.clientMaterialize(rClient)

  elif isinstance(arg, list): 
    resultArg = []
    for i in range(len(arg)):
      resultArg.append(clientMaterialize(arg[i], rClient))
    return resultArg

  elif isinstance(arg, tuple):
    resultArg = []
    for i in range(len(arg)):
      resultArg.append(clientMaterialize(arg[i], rClient))
    return tuple(resultArg)

  elif isinstance(arg, dict):
    resultArg = {}
    for key in arg.keys():
      resultArg[clientMaterialize(key, rClient)] = clientMaterialize(arg[key], rClient)
    return resultArg

  else:
    return arg
  #}}}
