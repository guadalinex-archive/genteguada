import sys
import remotemodel
import utils
import traceback

try:
  import ggclient.remoteclient
except:
  print "ejecutando en el server"

try:
  import ggserver.remoteserver
except:
  print "ejecutando en el cliente"



class RCommand: #{{{

  def __init__(self): #{{{
    self._serverHandler = None
  #}}}

  def do(self): #{{{
    raise Exception('subclasses must implements do()')

  def objectToSerialize(self, server):
    return self
  #}}}


  def setServerHandler(self, serverHandler):
    self._serverHandler = serverHandler

#}}}

class RExecuterCommand(RCommand): #{{{

  def __init__(self, modelID, methodName, args): #{{{
    RCommand.__init__(self)
    self._executionID = utils.nextID() 
    self._modelID    = modelID
    self._methodName = methodName
    self._args       = args

    print 'created an RExecuterCommand with ID ' + str( self._executionID )
  #}}}


  def isYourAnswer(self, command):
    if not isinstance(command, RExecutionAnswerer):
      return False

    return command._executionID == self._executionID


  def do(self): #{{{
    try:
      rServer = ggserver.remoteserver.getRServer()
    except:
      print "ejecutando en cliente"
      sys.exit(0)
    model = rServer.getModelByID(self._modelID)
    try:
      method = getattr(model, self._methodName)
    except AttributeError,e:
      return RExceptionRaiser(self._executionID, e)
    else:
      if self._args:
        arguments = []
        for i in range(len(self._args)):
          arguments.append(self.etherRealize(self._args[i],rServer))
        self._args = tuple(arguments)
      try:
        print ' executing method ' + self._methodName + ' in ' + str(model)
        result = method(*self._args)
        print '   method ' + self._methodName + ' in ' + str(model) + ' answered ' + str(result)
      except Exception,e:
        traceback.print_exc()   # TODO: Ver como meter esto en el LOG
        return RExceptionRaiser(self._executionID, e)
      return RExecutionResult(self._executionID, result)
  #}}}

  def etherRealize(self, arg, rserver): #{{{

    if isinstance(arg, remotemodel.RemoteModel):
      return rserver.getModelByID(arg._modelID)

    elif isinstance(arg,list): 
      resultArg = []
      for i in range(len(arg)):
        resultArg.append(self.etherRealize(arg[i],rserver))
      return resultArg

    elif isinstance(arg,tuple):
      resultArg = []
      for i in range(len(arg)):
        resultArg.append(self.etherRealize(arg[i],rserver))
      return tuple(resultArg)

    elif isinstance(arg,dict):
      resultArg = {}
      for key in arg.keys():
        resultArg[self.etherRealize(key,rserver)] = self.etherRealize(arg[key],rserver)
      return resultArg

    else:
      return arg
  #}}}

#}}}

class RExecutionAnswerer(RCommand): #{{{

  def __init__(self, executionID): #{{{
    RCommand.__init__(self)
    self._executionID = executionID

    print 'created an RExecutionAnswerer with ID ' + str( self._executionID )

  #}}}

#}}}  

class RExecutionResult(RExecutionAnswerer): #{{{

  def __init__(self, executionID, result): #{{{
    RExecutionAnswerer.__init__(self, executionID)
    self._result = result
  #}}}

  def do(self): #{{{ 
    return self._result
  #}}}


  def objectToSerialize(self, server):
    self._result = utils.objectToSerialize(self._result, server)
    return self

#}}}

class RExceptionRaiser(RExecutionAnswerer): #{{{

  def __init__(self, executionID, exception): #{{{
    RExecutionAnswerer.__init__(self, executionID)
    self._exception = exception
  #}}}

  def do(self): #{{{
    raise self._exception
  #}}}

#}}}




class REventSuscriber(RCommand):
  def __init__(self, modelID, eventType, suscriptionID):
    RCommand.__init__(self)
    self._modelID       = modelID
    self._eventType     = eventType
    self._suscriptionID = suscriptionID
  
  def do(self):
    model = ggserver.remoteserver.getRServer().getModelByID(self._modelID)
    model.subscribeEvent(self._eventType, self.eventFired)

  def eventFired(self, event):
    command = REventTriggerer(self._suscriptionID, event)
    self._serverHandler.sendCommand(command)


class REventTriggerer(RCommand):
  def __init__(self, suscriptionID, event):
    RCommand.__init__(self)
    self._suscriptionID = suscriptionID
    self._event         = event

  def objectToSerialize(self, server):
    self._event = utils.objectToSerialize(self._event, server)
    return self

  def do(self):
    rClient = ggclient.remoteclient.getRClient()
    suscription = rClient.getRemoteSuscriptionByID(self._suscriptionID)
    suscription[1](self._event)
