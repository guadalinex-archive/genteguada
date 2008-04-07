import sys
import remotemodel

try:
  import ggserver.remoteserver
except:
  print "ejecutando en cliente"

class RCommand: #{{{

  def __init__(self):
    pass

  def do(self):
    raise Exception('subclasses must implements do()')

#}}}

class RExecuteResult(RCommand): #{{{

  def __init__(self,result):
    RCommand.__init__(self)
    self._result = result

  def do(self):
    return self._result
#}}}

class RExecuteCommand(RCommand): #{{{

  def __init__(self, modelID, methodName, args):
    RCommand.__init__(self)
    self._modelID    = modelID
    self._methodName = methodName
    self._args       = args

  def do(self):
    try:
      rServer = ggserver.remoteserver.getRServer()
    except:
      print "ejecutando en cliente"
      sys.exit(0)
    model = rServer.getModelByID(self._modelID)
    method = getattr(model, self._methodName, self._args)
    if callable(method):
        result = method(*self._args)
        return RExecuteResult(result)
    raise remotemodel.InvalidRemoteMethod(self)
#}}}

