
import SocketServer
import thread
import sys
import pickle
import testmodel
import ggcommon.remotecommand
import copy

import ggcommon.utils


# global to hold the rserver singleton instance
global _rServerSingleton
_rServerSingleton = None


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
    _objectToSerialize = ggcommon.utils.objectToSerialize(getRServer().getRootModel(), getRServer())
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
        answerToSerialize = ggcommon.utils.objectToSerialize(answer, getRServer())
        serializedAnswer = pickle.dumps(answerToSerialize)
        self.request.send(serializedAnswer)
  #}}}

  def finish(self): #{{{
    print self.client_address, 'desconectado'
  #}}}

#}}}

