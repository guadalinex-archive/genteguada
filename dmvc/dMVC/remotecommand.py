import dMVC
import sys
import utils


class RCommand: 

  def __init__(self): 
    self._serverHandler = None

  def do(self): 
    raise Exception('subclasses must implements do()')

  def objectToSerialize(self, server):
    return self

  def initStat(self, size):
    return utils.statServer.initCount((self.getCommandType(), str(self.getClass()), str(self.getMethod())), size )

  def stopStat(self, size, initTime):
    utils.statServer.stopCount((self.getCommandType(), str(self.getClass()), str(self.getMethod())), size, initTime )
 
  def getCommandType(self):
    return ""

  def getClass(self):
    rServer = dMVC.getRServer()
    model = rServer.getModelByID(self._modelID)
    return model.__class__.__name__

  def getMethod(self):
    return "" 

  def setServerHandler(self, serverHandler):
    self._serverHandler = serverHandler

  def getSessionID(self):
    return self._serverHandler.getSessionID()

  def __str__(self):
    return str(self.__class__.__name__) + ":" 


class RExecuterCommand(RCommand): 

  def __init__(self, modelID, methodName, args): 
    RCommand.__init__(self)
    self._executionID = utils.nextID() 
    self._modelID    = modelID
    self._methodName = methodName
    self._args       = args

  def getMethod(self):
    return self._methodName

  def getCommandType(self):
    return "RPC"

  def isYourAnswer(self, command):
    if not isinstance(command, RExecutionAnswerer):
      return False
    return command._executionID == self._executionID

  def do(self): 
    rServer = dMVC.getRServer()
    model = rServer.getModelByID(self._modelID)
    result = None
    error = None
    try:
      try:
        method = getattr(model, self._methodName)
      except AttributeError, ex:
        error = ex
        utils.logger.exception('Exception in remote method invocation')
        return RExceptionRaiser(self._executionID, ex)

      else:
        if self._args:
          arguments = []
          for i in range(len(self._args)):
            arguments.append(dMVC.serverMaterialize(self._args[i], rServer))
          self._args = tuple(arguments)
        try:
          result = method(*self._args)
        except:
          utils.logger.exception('Exception in remote method invocation')
          error = sys.exc_info()[1]
          return RExceptionRaiser(self._executionID, error)
        return RExecutionResult(self._executionID, result)
    finally:
      for klass, methodName, handler in rServer._onExecution:
        if (model.__class__ is klass) and (self._methodName == methodName):
          handler(self._serverHandler,
                  result,
                  error)

  def __str__(self):
    return RCommand.__str__(self) + 'executionID=' + str(self._executionID) + \
        ', modelID=' + str(self._modelID) + ', ' + str(self._methodName)# + str(self._args)
    #return RCommand.__str__(self) + 'executionID=' + str(self._executionID)


class RExecutionAnswerer(RCommand): 

  def __init__(self, executionID): 
    RCommand.__init__(self)
    self._executionID = executionID

  def __str__(self):
    return RCommand.__str__(self) + 'executionID=' + str(self._executionID)
#}}}  


class RExecutionResult(RExecutionAnswerer): 

  def __init__(self, executionID, result): 
    RExecutionAnswerer.__init__(self, executionID)
    self._result = result

  def do(self):  
    rClient = dMVC.getRClient()
    return dMVC.clientMaterialize(self._result, rClient)

  def objectToSerialize(self, server):
    self._result = dMVC.objectToSerialize(self._result, server)
    return self

  def __str__(self):
    return RExecutionAnswerer.__str__(self)# + ', result=' + str(self._result)
#}}}


class RExceptionRaiser(RExecutionAnswerer): 

  def __init__(self, executionID, exception): 
    RExecutionAnswerer.__init__(self, executionID)
    self._exception = exception

  def do(self): 
    raise self._exception

  def __str__(self):
    return RExecutionAnswerer.__str__(self) + ', exception=' + str(self._exception)


class REventUnsuscriber(RCommand):

  def __init__(self, modelID, suscriptionIDs):
    RCommand.__init__(self)
    self._modelID        = modelID
    self._suscriptionIDs = suscriptionIDs

  def getCommandType(self):
    return "EventUnSubscribe"

  def getMethod(self):
    return self._suscriptionIDs

  def do(self):
    model = dMVC.getRServer().getModelByID(self._modelID)
    model.unsubscribeEventById(self._suscriptionIDs, self.getSessionID())

  def __str__(self):
    return RCommand.__str__(self) + 'modelID=' + str(self._modelID) + \
         ', suscriptionIDs=' + str(self._suscriptionIDs)


class REventListUnsuscriber(RCommand):

  def __init__(self, modelID, suscriptionList):
    RCommand.__init__(self)
    self._modelID        = modelID
    self._suscriptionList = suscriptionList

  def getCommandType(self):
    return "EventListUnSubscribe"

  def do(self):
    for suscription in self._suscriptionList:
      model = dMVC.getRServer().getModelByID(suscription[0])
      model.unsubscribeEventById(suscription[1], self.getSessionID())

  def __str__(self):
    return RCommand.__str__(self) + 'modelID=' + str(self._modelID) + \
         ', suscriptionList=' + str(self._suscriptionList)



class REventSuscriber(RCommand):

  def __init__(self, modelID, eventType, suscriptionID):
    RCommand.__init__(self)
    self._modelID       = modelID
    self._eventType     = eventType
    self._suscriptionID = suscriptionID

  def getCommandType(self):
    return "EventSubscribe"

  def getMethod(self):
    return self._eventType

  def do(self):
    model = dMVC.getRServer().getModelByID(self._modelID)
    model.subscribeEvent(self._eventType, self.eventFired, self._suscriptionID, self.getSessionID())

  def eventFired(self, event):
    command = REventTriggerer(self._suscriptionID, event)
    if not self._serverHandler.sendCommand(command):
      utils.logger.debug("Can't send event to client, unsuscribing (" + str(self) + ")")
      self.unsubscribeEventObserver()

  def unsubscribeEventObserver(self):
    model = dMVC.getRServer().getModelByID(self._modelID)
    model.unsubscribeEventObserver(self)

  def __str__(self):
    return RCommand.__str__(self) + 'modelID=' + str(self._modelID) + \
        ', eventType=' + str(self._eventType) + ', suscriptionID=' + str(self._suscriptionID)

class REventListSuscriber(RCommand):

  def __init__(self, modelID, suscriptionList):
    RCommand.__init__(self)
    self._modelID       = modelID
    self._suscriptionList = suscriptionList

  def getCommandType(self):
    return "EventListSubscribe"

  def do(self):
    for suscription in self._suscriptionList:
      eventSubscriber = REventSuscriber(self._modelID, suscription[0], suscription[1])
      eventSubscriber.setServerHandler(self._serverHandler)
      eventSubscriber.do()

  def __str__(self):
    return RCommand.__str__(self) + 'modelID=' + str(self._modelID) + ', suscriptionList=' + str(self._suscriptionList)


class REventChildListSuscriber(RCommand):

  def __init__(self, modelID, suscriptionList):
    RCommand.__init__(self)
    self._modelID = modelID
    self._suscriptionList = suscriptionList

  def getCommandType(self):
    return "EventChildListSubscribe"

  def do(self):
    for suscription in self._suscriptionList:
      eventSubscriber = REventSuscriber(suscription[2], suscription[0], suscription[1])
      eventSubscriber.setServerHandler(self._serverHandler)
      eventSubscriber.do()

  def __str__(self):
    return RCommand.__str__(self) + 'modelID=' + str(self._modelID) + ', suscriptionList=' + str(self._suscriptionList)


class REventTriggerer(RCommand):

  def __init__(self, suscriptionID, event):
    RCommand.__init__(self)
    self._suscriptionID = suscriptionID
    self._event         = event

  def objectToSerialize(self, server):
    self._event = dMVC.objectToSerialize(self._event, server)
    return self

  def do(self):
    rClient = dMVC.getRClient()
    self._event = dMVC.clientMaterialize(self._event, rClient)
    utils.statEventTriggered.addEvent(self)
    suscription = rClient.getRemoteSuscriptionByID(self._suscriptionID)
    if suscription:
      suscription[1](self._event)

  def __str__(self):
    return RCommand.__str__(self) + 'suscriptionID=' + str(self._suscriptionID) + ', event=' + str(self._event)


class RFragment:

  def __init__(self, groupID, sequence, total, data, commandID = None):
    self.groupID  = groupID
    self.sequence = sequence
    self.total    = total
    self.data     = data
    self.commandID = commandID


class RCompositeCommand(RCommand):

  def __init__(self, commandList):
    RCommand.__init__(self)
    self.commandList  = commandList

  def objectToSerialize(self, server):
    self.commandList = dMVC.objectToSerialize(self.commandList, server)
    return self

