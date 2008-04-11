
import SocketServer
import thread
import sys
import pickle
import ggcommon.remotecommand
import copy
import time

import ggcommon.utils
import struct
import traceback


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
    modelID = ggcommon.utils.nextID()
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
    #_objectToSerialize = ggcommon.utils.objectToSerialize(getRServer().getRootModel(), getRServer())
    #serializedRootModel = pickle.dumps(_objectToSerialize)
    #self.request.send(serializedRootModel)
    self._sendObject(getRServer().getRootModel())
  #}}}

  def setup(self): #{{{
    print self.client_address, 'conectado'
    self._sendRootModel()
  #}}}

  def handle(self): #{{{
    while 1:
      size = struct.calcsize("i")
      size = self.request.recv(size)
      if len(size):
        size = struct.unpack("i", size)[0]
        commandData = ""
        while len(commandData) < size:
          commandData = self.request.recv(size - len(commandData))
        command = pickle.loads(commandData)
        command.setServerHandler(self)
        answer = command.do()
        if answer:
          self._sendObject(answer)
      else:
        break

      """ 
      commandData = self.request.recv(1024)
      if (len(commandData) == 0):
        time.sleep(0.01)
      else:
        print 'server received ' + str(len(commandData)) + 'bytes'
        command = pickle.loads(commandData)
        command.setServerHandler(self)
        answer = command.do()
        if answer:
          self._sendObject(answer)
        #answerToSerialize = ggcommon.utils.objectToSerialize(answer, getRServer())
        #serializedAnswer = pickle.dumps(answerToSerialize)
        #self.request.send(serializedAnswer)
      """
  #}}}

  """
  def handle(self): #{{{
    while 1:
      commandData = self.request.recv(1024)
      if (len(commandData) == 0):
        time.sleep(0.01)
      else:
        print 'server received ' + str(len(commandData)) + 'bytes'
        command = pickle.loads(commandData)
        command.setServerHandler(self)
        answer = command.do()
        if answer:
          self._sendObject(answer)
        #answerToSerialize = ggcommon.utils.objectToSerialize(answer, getRServer())
        #serializedAnswer = pickle.dumps(answerToSerialize)
        #self.request.send(serializedAnswer)
  #}}}
  """
  def _sendObject(self, object):
    toSerialize = ggcommon.utils.objectToSerialize(object, getRServer())
    serialized = pickle.dumps(toSerialize)
    try:
      self.request.send(serialized)
      return True
    except:
      print sys.exc_info()[1]
      traceback.print_exc()
      return False
    #self.request.flush()

  def sendCommand(self, command):
    return self._sendObject(command)

  def finish(self): #{{{
    print self.client_address, 'desconectado'
  #}}}

#}}}

