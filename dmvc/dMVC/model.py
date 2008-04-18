import synchronized
import utils
import threading
import remotemodel
import copy
import events



def localMethod(func):
  """
  flag a method to be a ever-local method.  it means the method will be copied to the remotemodel representing the model in the client side.
  """
  func.flag = 'localMethod'
  return func


class Model(synchronized.Synchronized): 

  def __init__(self): #{{{
    #utils.logger.debug("Model.__init__")
    self.__id = None
    synchronized.Synchronized.__init__(self)
    self.__subscriptions = []
  #}}}

  def setID(self, id): #{{{
    #utils.logger.debug("Model.setID id: "+str(id))
    self.__id = id
  #}}}

  def __str__(self): #{{{
    #utils.logger.debug("Model.__str__")
    return '<Model ID: ' + str(self.__id) + ' (' + self.__class__.__module__ + '.' + self.__class__.__name__ + ')>'
  #}}}

  def objectToSerialize(self, server): #{{{
    #utils.logger.debug("Model.objectToSerialize server: "+str(server))
    if self.__id == None:
      #utils.logger.info("Register model into server")
      server.registerModel(self)
    return remotemodel.RemoteModel(self.__id,
                                   self.__class__.__module__,
                                   self.__class__.__name__)
  #}}}


  @synchronized.synchronized(lockName='subscriptions')
  def subscribeEvent(self, eventType, method): #{{{
    utils.logger.debug("Model.subscribeEvent eventType: "+str(eventType)+" method: "+str(method))
    self.__subscriptions.append([eventType, method])
  #}}}
    

  @synchronized.synchronized(lockName='subscriptions')
  def triggerEvent(self, eventType, **params): #{{{
    utils.logger.debug("Model.triggerEvent eventType: "+str(eventType)+ " params: "+str(params))
    subscriptionsCopy = copy.copy(self.__subscriptions)
    for type, method in subscriptionsCopy:
      if type == eventType:
        event = events.Event(self, eventType, params)
        try:
          method(event)
        except:
          utils.logger.exception("Failed exec method "+str(method))
  #}}}
    
  @synchronized.synchronized(lockName='subscriptions')
  def unsubscribeEventObserver(self, observer, eventType=None): #{{{
    utils.logger.debug("Model.unsubscribeEventObserver observer: "+str(observer)+" eventType: "+str(eventType))
    toRemove = []
    for subscription in self.__subscriptions:
      if id(subscription[1].im_self) == id(observer):
        if eventType == None or eventType == subscription[0]: 
          toRemove.append(subscription)
    for subscription in toRemove:
      self.__subscriptions.remove(subscription)
  #}}}

  @synchronized.synchronized(lockName='subscriptions')
  def unsubscribeEventMethod(self, method, eventType=None): #{{{
    utils.logger.debug("Model.unsubscribeEventMethod method: "+str(method)+" eventType: "+str(eventType))
    toRemove = []
    for subscription in self.__subscriptions:
      if subscription[1] == method:
        if eventType == None or eventType == subscription[0]: 
          toRemove.append(subscription)
    for subscription in toRemove:
      self.__subscriptions.remove(subscription)
  #}}}

  def __eq__(self, comparand): #{{{
    #utils.logger.debug("Model.__eq__")
    return id(self) == id(comparand)
  #}}}

