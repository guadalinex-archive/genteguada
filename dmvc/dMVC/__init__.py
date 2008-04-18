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






def serverMaterialize(arg, rServer): #{{{

  if isinstance(arg, remotemodel.RemoteModel):
    return arg.serverMaterialize(rServer)

  elif isinstance(arg,list): 
    resultArg = []
    for i in range(len(arg)):
      resultArg.append(serverMaterialize(arg[i],rServer))
    return resultArg

  elif isinstance(arg,tuple):
    resultArg = []
    for i in range(len(arg)):
      resultArg.append(serverMaterialize(arg[i],rServer))
    return tuple(resultArg)

  elif isinstance(arg,dict):
    resultArg = {}
    for key in arg.keys():
      resultArg[serverMaterialize(key,rServer)] = serverMaterialize(arg[key],rServer)
    return resultArg

  else:
    return arg
  #}}}


def clientMaterialize(arg, rClient): #{{{

  if isinstance(arg, remotemodel.RemoteModel):
    return arg.clientMaterialize(rClient)

  elif isinstance(arg,list): 
    resultArg = []
    for i in range(len(arg)):
      resultArg.append(clientMaterialize(arg[i],rClient))
    return resultArg

  elif isinstance(arg,tuple):
    resultArg = []
    for i in range(len(arg)):
      resultArg.append(clientMaterialize(arg[i],rClient))
    return tuple(resultArg)

  elif isinstance(arg,dict):
    resultArg = {}
    for key in arg.keys():
      resultArg[clientMaterialize(key,rClient)] = clientMaterialize(arg[key],rClient)
    return resultArg

  else:
    return arg
  #}}}
