import dMVC
import sys
import remotecommand

import utils
import new


class RemoteModel: #{{{

  def __init__(self, modelID, modelModuleName, modelClassName, variablesDict): #{{{
    self.__modelID         = modelID
    self.__modelModuleName = modelModuleName
    self.__modelClassName  = modelClassName
    self.__variablesDict   = variablesDict
  #}}}

  
  def __str__(self): #{{{
    return '<RemoteModel modelID: ' + str(self.__modelID) + ' (' + self.__modelModuleName + '.' + self.__modelClassName + ')>'
  #}}}

  def __repr__(self): #{{{
    return self.__str__()
  #}}}

  def __getattr__(self, attrName): #{{{
    if attrName == "__getinitargs__":       # allows it to be safely pickled
      raise AttributeError()
    return RemoteMethod(self.__modelID, attrName, self.__modelClassName)
  #}}}

  # Pickling support, otherwise pickle uses __getattr__:
  def __getstate__(self): #{{{
    newDict = {}
    for key in self.__dict__.keys():
      value = self.__dict__[key]
      if not callable(value):
        newDict[key] = value
    return newDict
  #}}}

  def __setstate__(self, args): #{{{
    # this appears to be necessary otherwise pickle won't work
    self.__dict__ = args
  #}}}


  def getModelID(self):
    return self.__modelID


  def subscribeEvent(self, eventType, method):
    """ Indica la accion a realizar ante un evento.
    eventType: tipo de evento.
    method: metodo que se lanzara.
    """
    rClient = dMVC.getRClient()
    suscription = [eventType, method]
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
    subscriptionIDs =  rClient.unsubscribeEventObserver(observer, eventType)
    rClient.sendCommand(remotecommand.REventUnsuscriber(self.__modelID, subscriptionIDs))

  def unsubscribeEventMethod(self, method, eventType=None):
    rClient = dMVC.getRClient()
    rClient.unsubscribeEventMethod(method,eventType)

  def __eq__(self, comparand):
    if not isinstance(comparand, RemoteModel):
      return False

    return self.__modelID == comparand.getModelID()


  def serverMaterialize(self, rServer):
    return rServer.getModelByID(self.__modelID)


  def __transplantVariables(self):
    for key in self.__variablesDict.keys():
      value = self.__variablesDict[key]
      utils.logger.debug("Transplanting variable " + str(key) + " in " + str(self) + " with value " + str(value))
      setattr(self, key, value)

  def __transplantMethods(self, donorClass):
    for key in dir(donorClass):
      method = getattr(donorClass, key)
      if callable(method):
        function = method.im_func
        if 'flag' in function.__dict__.keys():
          if function.__dict__['flag'] == 'localMethod':
            utils.logger.debug("Transplanting method " + str(function.func_name) + " in " + str(self) + " from " + str(donorClass))
            self.__dict__[function.func_name] = new.instancemethod(function, self)

  def __findModelClass(self):
    __import__(self.__modelModuleName)
    mod = sys.modules[self.__modelModuleName]
    klass = getattr(mod, self.__modelClassName)
    return klass


  def clientMaterialize(self, rClient):
    self.__transplantVariables()
    self.__transplantMethods(self.__findModelClass())
    return self

#}}}





class RemoteMethod: #{{{

  def __init__(self, modelID, methodName, className): #{{{
    self._modelID = modelID
    self._methodName = methodName
    self._className = className
  #}}}

  def __call__(self, *args): #{{{
    initTime = utils.statClient.initClientCount()

    rClient = dMVC.getRClient()
    executer = remotecommand.RExecuterCommand(self._modelID, self._methodName, args)
    rClient.sendCommand(executer)
    answerer = rClient.waitForExecutionAnswerer(executer)
    result = answerer.do()

    utils.statClient.stopClientCount(initTime, (self._className, self._modelID, self._methodName))
    return result

  #}}}

#}}}

