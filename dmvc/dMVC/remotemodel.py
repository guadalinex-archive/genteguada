import dMVC
import sys
import remotecommand

import utils
import new

import thread

class RemoteModel: 

  def __init__(self, modelID, modelModuleName, modelClassName, variablesDict): 
    self.__modelID         = modelID
    self.__modelModuleName = modelModuleName
    self.__modelClassName  = modelClassName
    self.__variablesDict   = variablesDict
  
  def __str__(self): 
    return '<RemoteModel modelID: ' + str(self.__modelID) + ' (' + self.__modelModuleName + '.' + self.__modelClassName + ')>'

  def __repr__(self): 
    return self.__str__()

  def __setattr__(self, attrName, attrValue):
    if attrName in ('_RemoteModel__modelID', '_RemoteModel__modelModuleName', '_RemoteModel__modelClassName', '_RemoteModel__variablesDict'):
      self.__dict__[attrName] = attrValue
      return
    if attrName in self.__variablesDict:
      raise Exception("Can't assign to transplantable variables")
    self.__dict__[attrName] = attrValue

  def __getattr__(self, attrName): 
    if attrName == "__getinitargs__":       # allows it to be safely pickled
      raise AttributeError()
    varDict = self.__dict__["_RemoteModel__variablesDict"]
    if attrName in varDict:
      return varDict[attrName]
    return RemoteMethod(self.__modelID, attrName, self.__modelClassName)

  def __getstate__(self): 
    # Pickling support, otherwise pickle uses __getattr__:
    newDict = {}
    for key, value in self.__dict__.iteritems():
      if not callable(value):
        newDict[key] = value
    return newDict

  def __setstate__(self, args): 
    # this appears to be necessary otherwise pickle won't work
    self.__dict__ = args

  def getModelID(self):
    return self.__modelID

  def subscribeChildListEvent(self, childListEvent):
    rClient = dMVC.getRClient()
    subscriptionList = []
    for event in childListEvent:
      remoteModel = event[0]
      eventType = event[1]
      method = event[2]
      suscription = [eventType, method, remoteModel]
      suscriptionID = rClient.registerRemoteSuscription(suscription)
      subscriptionList.append([event[1], suscriptionID, remoteModel.getModelID()])
    rClient.sendCommand(remotecommand.REventChildListSuscriber(self.__modelID, subscriptionList))

  def subscribeListEvent(self, eventList):
    rClient = dMVC.getRClient()
    subscriptionList = []
    for event in eventList:
      suscription = [event[0], event[1], self]
      suscriptionID = rClient.registerRemoteSuscription(suscription)
      subscriptionList.append([event[0], suscriptionID])
    rClient.sendCommand(remotecommand.REventListSuscriber(self.__modelID, subscriptionList))

  def subscribeEvent(self, eventType, method):
    """ Indica la accion a realizar ante un evento.
    eventType: tipo de evento.
    method: metodo que se lanzara.
    """
    rClient = dMVC.getRClient()
    suscription = [eventType, method, self]
    suscriptionID = rClient.registerRemoteSuscription(suscription)
    rClient.sendCommand(remotecommand.REventSuscriber(self.__modelID, eventType, suscriptionID))
    
  def triggerEvent(self, eventType, **params):
    """ Activa un evento.
    eventType: tipo de evento.
    params: datos sobre el evento.
    """
    raise Exception('RemoteModel can\'t raise events')
    
  def unsubscribeEventObserver(self, observer, eventType=None):
    rClient = dMVC.getRClient()
    subscriptionIDs =  rClient.unsubscribeEventObserver(observer, eventType, self)
    rClient.sendCommand(remotecommand.REventUnsuscriber(self.__modelID, subscriptionIDs))

  def unsubscribeEventListObserver(self, observers, eventType=None):
    rClient = dMVC.getRClient()
    unsubscribeList = []
    for observer in observers:
      subscriptionIDs =  rClient.unsubscribeEventObserver(observer, eventType, observer.getModel())
      subscriptionData = [observer.getModel().getModelID(), subscriptionIDs]
      unsubscribeList.append(subscriptionData)
    rClient.sendCommand(remotecommand.REventListUnsuscriber(self.__modelID, unsubscribeList))

  def unsubscribeEventMethod(self, method, eventType=None):
    rClient = dMVC.getRClient()
    subscriptionIDs = rClient.unsubscribeEventMethod(method, eventType, self)
    rClient.sendCommand(remotecommand.REventUnsuscriber(self.__modelID, subscriptionIDs))

  def __eq__(self, comparand):
    if not isinstance(comparand, RemoteModel):
      return False
    return self.__modelID == comparand.getModelID()

  def __nonzero__(self):
    return True

  def serverMaterialize(self, rServer):
    return rServer.getModelByID(self.__modelID)

  def __transplantVariables(self):
    for key, value in self.__variablesDict.iteritems():
      utils.logger.debug("Transplanting variable " + str(key) + " in " + str(self) + " with value " + str(value))
      setattr(self, key, value)

  def __transplantMethods(self, donorClass):
    for key in dir(donorClass):
      method = getattr(donorClass, key)
      if callable(method):
        if hasattr(method, "im_func"):
          function = method.im_func
          if 'flag' in function.__dict__:
            if function.__dict__['flag'] == 'localMethod':
              utils.logger.debug("Transplanting method " + str(function.func_name) + " in " + str(self) + " from " + str(donorClass))
              self.__dict__[function.func_name] = new.instancemethod(function, self)

  def __findModelClass(self):
    __import__(self.__modelModuleName)
    mod = sys.modules[self.__modelModuleName]
    klass = getattr(mod, self.__modelClassName)
    return klass

  def clientMaterialize(self, rClient):
    #self.__transplantVariables()
    self.__transplantMethods(self.__findModelClass())
    return self

  def async(self, method, callback, *args):
    asyncMethod = remotecommand.RExecuterCommand(method._modelID, method._methodName, args)
    rClient = dMVC.getRClient()
    #rClient.sendAsyncCommand(asyncMethod, callback)
    thread.start_new(rClient.sendAsyncCommand, (asyncMethod, callback))


class RemoteMethod: 

  def __init__(self, modelID, methodName, className): 
    self._modelID    = modelID
    self._methodName = methodName
    self._className  = className

  def __call__(self, *args): 
    initTime = utils.statClient.initClientCount()
    rClient = dMVC.getRClient()
    executer = remotecommand.RExecuterCommand(self._modelID, self._methodName, args)
    rClient.sendCommand(executer)
    answerer = rClient.waitForExecutionAnswerer(executer)
    result = answerer.do()
    utils.statClient.stopClientCount(initTime, (self._className, self._modelID, self._methodName))
    return result



