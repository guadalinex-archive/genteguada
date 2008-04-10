import sys
import remotecommand

try:
  import ggclient.remoteclient
except:
  print "ejecutando en servidor"


class RemoteModel: #{{{

  def __init__(self, id): #{{{
    self._modelID = id
  #}}}

  def __str__(self): #{{{
    return '<RemoteModel modelID: ' + str(self._modelID) +'>'
  #}}}

  def __getattr__(self, attrName): #{{{
    if attrName == "__getinitargs__":       # allows it to be safely pickled
      raise AttributeError()
    return RemoteMethod(self._modelID, attrName)
  #}}}

  # Pickling support, otherwise pickle uses __getattr__:
  def __getstate__(self): #{{{
    return self.__dict__
  #}}}

  def __setstate__(self, args): #{{{
    # this appears to be necessary otherwise pickle won't work
    self.__dict__ = args
  #}}}

#}}}

class RemoteMethod: #{{{

  def __init__(self, modelID, methodName): #{{{
    self._modelID = modelID
    self._methodName = methodName
  #}}}

  def __call__(self, *args): #{{{
    try:
      rClient = ggclient.remoteclient.getRClient()
    except:
      print "ejecutando en servidor"
      sys.exit(0)

    executer = remotecommand.RExecuterCommand(self._modelID, self._methodName, args)
    rClient.sendCommand(executer)

    answerer = rClient.waitForExecutionAnswerer(executer)
    return answerer.do()

  #}}}

#}}}

