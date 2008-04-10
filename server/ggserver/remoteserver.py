
import SocketServer
import thread
import sys
import pickle
import testmodel
import ggcommon.remotecommand
import copy

# global to hold the rserver singleton instance
global _rServerSingleton
_rServerSingleton = None

def objectToSerialize(object): #{{{
  """
  Movel esta funcion a utils, 
  """
  
  if isinstance(object, testmodel.Model):
    return object.objectToSerialize(getRServer())

  elif isinstance(object, ggcommon.remotecommand.RExecutionResult):
    #llamar a esta funcion desde el objeto, igual que en el model
    resultObject = copy.copy(object)
    resultObject._result = objectToSerialize(resultObject._result)
    return resultObject

  elif isinstance(object,list): 
    resultObject = []
    for i in range(len(object)):
      resultObject.append(objectToSerialize(object[i]))
    return resultObject

  elif isinstance(object,tuple):
    resultObject = []
    for i in range(len(object)):
      resultObject.append(objectToSerialize(object[i]))
    return tuple(resultObject)

  elif isinstance(object,dict):
    resultObject = {}
    for key in object.keys():
      resultObject[objectToSerialize(key)] = objectToSerialize(object[key])
    return resultObject

  else:
    return object
#}}}

def getRServer(): #{{{
  if _rServerSingleton == None:
    raise Exception("RServer has to be instanciated before calling getRServer()")
  return _rServerSingleton
#}}}

class RServer: #{{{

  def __init__(self, rootModel, port=8000): #{{{
    global _rServerSingleton
    if not (_rServerSingleton == None):
      raise Exception("Can't create more then one instance of RServer")
    _rServerSingleton = self
    self._models = {}
    self._port = port
    self._rootModel = rootModel
    self._start()
  #}}}

  def getModelByID(self, id): #{{{
    return self._models[id]
  #}}}

  def registerModel(self, model): #{{{
    if model in self._models.values():
      return
    modelID = id(model)
    model.setID(modelID)
    self._models[modelID] = model
  #}}}

  def getRootModel(self): #{{{
    return self._rootModel
  #}}}

  def _start(self): #{{{
    print "iniciando servidor"
    con = SocketServer.ThreadingTCPServer(('', self._port), RServerHandler)
    con.request_queue_size = 500
    thread.start_new(con.serve_forever, ())
    print "servidor iniciado"
    while 1:
      data = raw_input('')
      if data.rstrip() == "quit": 
        con.server_close()
        sys.exit(0)
  #}}}

#}}}

class RServerHandler(SocketServer.BaseRequestHandler): #{{{

  def _sendRootModel(self): #{{{
    _objectToSerialize = objectToSerialize(getRServer().getRootModel())
    serializedRootModel = pickle.dumps(_objectToSerialize)
    self.request.send(serializedRootModel)
  #}}}

  def setup(self): #{{{
    print self.client_address, 'conectado'
    self._sendRootModel()
  #}}}

  def handle(self): #{{{
    while 1:
      commandData = self.request.recv(1024)
      if (len(commandData) != 0):
        command = pickle.loads(commandData)
        answer = command.do()
        answerToSerialize = objectToSerialize(answer)
        serializedAnswer = pickle.dumps(answerToSerialize)
        self.request.send(serializedAnswer)
  #}}}

  def finish(self): #{{{
    print self.client_address, 'desconectado'
  #}}}

#}}}

