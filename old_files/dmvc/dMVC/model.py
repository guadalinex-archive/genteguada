import synchronized
import utils
import remotemodel
import copy
import events
import dMVC


def localMethod(func):
  """
  flag a method to be a ever-local method.  it means the method will be copied to the remotemodel representing the model in the client side.
  """
  func.flag = 'localMethod'
  return func


class Model(synchronized.Synchronized): 

  def __init__(self): #{{{
    self.__id = None
    synchronized.Synchronized.__init__(self)
    self.__subscriptions  = []
  #}}}

  def variablesToSerialize(self):
    return []

  def setID(self, newId): #{{{
    if self.__id:
      raise Exception("The receiver already has an ID")
    self.__id = newId
  #}}}

  def __str__(self): #{{{
    return '<Model ID: ' + str(self.__id) + ' (' + self.__class__.__module__ + '.' + self.__class__.__name__ + ')>'
  #}}}

  def objectToSerialize(self, server): #{{{
    if self.__id == None:
      server.registerModel(self)

    variablesDict = {}
    for variable in self.variablesToSerialize():
      variablesDict[variable] = dMVC.objectToSerialize(getattr(self, variable), server)

    return remotemodel.RemoteModel(self.__id,
                                   self.__class__.__module__,
                                   self.__class__.__name__,
                                   variablesDict)
  #}}}


  @synchronized.synchronized(lockName='subscriptions')
  def subscribeEvent(self, eventType, method, suscriptionID = None, sessionID = None): #{{{
    utils.logger.debug("Subscribed event="+str(eventType)+", method: "+str(method) + ', model=' + str(self))
    self.__subscriptions.append([eventType, method, suscriptionID, sessionID])
  #}}}
    

  @synchronized.synchronized(lockName='subscriptions')
  def triggerEvent(self, eventType, **params): #{{{
    utils.logger.debug("Model " + str(self) + " triggered eventType: "+str(eventType)+ " params: "+str(params))
    subscriptionsCopy = copy.copy(self.__subscriptions)
    for typ, method, subscriptionID, sessionID in subscriptionsCopy:
      if typ == eventType:
        event = events.Event(self, eventType, params) 
        try:
          method(event)
        except:
          utils.logger.exception('Exception while event triggering')
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

  @synchronized.synchronized(lockName='subscriptions')
  def unsubscribeEventById(self, subscriptionIDs, sessionID): #{{{
    utils.logger.debug("Model.unsubscribeEventByIDs subscriptionIDs: "+str(subscriptionIDs))
    toRemove = []
    for subscription in self.__subscriptions:
      if subscription[2] in  subscriptionIDs and subscription[3] == sessionID:
        toRemove.append(subscription)
    for subscription in toRemove:
      self.__subscriptions.remove(subscription)
  #}}}

  def async(self, method, callback, *args):
    try:
      returnValue = method(args)
      callback(returnValue)
    except:
      Exception("Error executing async method")
      

  def __eq__(self, comparand): #{{{
    return self is comparand
  #}}}
