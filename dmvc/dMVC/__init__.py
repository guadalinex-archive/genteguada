import model
import remotemodel
import remotecommand
import events



#rServerSingleton #{{{
__rServerSingleton = None

def getRServer(): 
  global __rServerSingleton
  if __rServerSingleton == None:
    raise Exception("RServer has to be instanciated before calling getRServer()")
  return __rServerSingleton

def setRServer(rserver):
  global __rServerSingleton
  if __rServerSingleton != None:
    raise Exception("Can't create more then one instance of RServer")
  __rServerSingleton = rserver
#}}}


#rClientSingleton #{{{
__rClientSingleton = None

def getRClient():
  global __rClientSingleton
  if __rClientSingleton == None:
    raise Exception("RClient has to be instanciated before calling getRClient()")
  return __rClientSingleton

def setRClient(rclient):
  global __rClientSingleton
  if __rClientSingleton != None:
    raise Exception("Can't create more then one instance of RClient")
  __rClientSingleton = rclient
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
