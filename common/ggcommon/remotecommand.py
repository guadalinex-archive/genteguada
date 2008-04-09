import sys
import remotemodel

try:
  import ggserver.remoteserver
except:
  print "ejecutando en cliente"

class RCommand: #{{{

  def __init__(self): #{{{
    pass
  #}}}

  def do(self): #{{{
    raise Exception('subclasses must implements do()')
  #}}}

#}}}

class RExecuteResult(RCommand): #{{{

  def __init__(self,result): #{{{
    RCommand.__init__(self)
    self._result = result
  #}}}

  def do(self): #{{{ 
    return self._result
  #}}}

#}}}

class RExceptionRaise(RCommand): #{{{

  def __init__(self,exception): #{{{
    RCommand.__init__(self)
    self._exception = exception
  #}}}

  def do(self): #{{{
    raise self._exception
  #}}}

#}}}

class RExecuteCommand(RCommand): #{{{

  def __init__(self, modelID, methodName, args): #{{{
    RCommand.__init__(self)
    self._modelID    = modelID
    self._methodName = methodName
    self._args       = args
  #}}}

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
      return RExceptionRaise(e)
    else:
      if self._args:
        arguments = []
        for i in range(len(self._args)):
          arguments.append(self.etherRealize(self._args[i],rServer))
        self._args = tuple(arguments)
      try:
        result = method(*self._args)
      except Exception,e:
        return RExceptionRaise(e)
      return RExecuteResult(result)
  #}}}

  def etherRealize(self,arg,rserver): #{{{

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

