
import SocketServer
import thread
import sys
import pickle
import remotecommand
import copy
import time

import utils
import struct
import traceback
import logging

import struct

logger = logging.getLogger('genteguada')
hdlr = logging.FileHandler('genteguada.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


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
    logger.debug("Iniciando servidor")
    if not (_rServerSingleton == None):
      logger.error("Can't create more then one instance of RServer")
      raise Exception("Can't create more then one instance of RServer")
    _rServerSingleton = self
    self._models = {}
    self._port = port
    self._rootModel = rootModel
    self._start()
  #}}}

  def getModelByID(self, id): #{{{
    logger.debug("Devolviendo el objeto modelo con id "+str(id))
    return self._models[id]
  #}}}

  def registerModel(self, model): #{{{
    if model in self._models.values():
      logger.debug("Intentando registrar un modelo que ya esta registrado "+str(model))
      return
    modelID = utils.nextID()
    model.setID(modelID)
    logger.debug("Registrando un modelo con id "+str(id))
    self._models[modelID] = model
  #}}}

  def getRootModel(self): #{{{
    logger.debug("Devolviendo el rootModel")
    return self._rootModel
  #}}}

  def _start(self): #{{{
    print "iniciando servidor"
    con = SocketServer.ThreadingTCPServer(('', self._port), RServerHandler)
    con.request_queue_size = 500
    thread.start_new(con.serve_forever, ())
    logger.info("Servidor puesto en escucha")
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
    #_objectToSerialize = utils.objectToSerialize(getRServer().getRootModel(), getRServer())
    #serializedRootModel = pickle.dumps(_objectToSerialize)
    #self.request.send(serializedRootModel)
    logger.debug("Enviando el root model")
    self._sendObject(getRServer().getRootModel())
  #}}}

  def setup(self): #{{{
    print self.client_address, 'conectado'
    logger.info("Conectado el cliente "+str(self.client_address))
    self._sendRootModel()
  #}}}

  def handle(self): #{{{
    while 1:
      size = struct.calcsize("i")
      size = self.request.recv(size)
      if len(size):
        size = struct.unpack("i", size)[0]
        commandData = ""
        logger.info("Recibimos del cliente algo con size "+str(size))
        while len(commandData) < size:
          commandData = self.request.recv(size - len(commandData))
        command = pickle.loads(commandData)
        logger.info("Recibimos el comando "+str(command))
        command.setServerHandler(self)
        answer = command.do()
        logger.info("Ejecutamos el comando "+str(command)+ " y obtenemos como respuesta "+str(answer))
        if answer:
          logger.info("Enviamos la respuesta "+str(answer))
          self._sendObject(answer)
      else:
        logger.info("Cerramos la conexion con "+str(self.client_address))
        break
  #}}}

  def _sendObject(self, object):
    toSerialize = utils.objectToSerialize(object, getRServer())
    serialized = pickle.dumps(toSerialize)
    sizeSerialized = len(serialized)
    try:
      size = struct.pack("i",sizeSerialized)
      self.request.send(size)
      self.request.send(serialized)
      return True
    except:
      print sys.exc_info()[1]
      traceback.print_exc()
      return False

  def sendCommand(self, command):
    return self._sendObject(command)

  def finish(self): #{{{
    logger.info("cerramos la conexion con el cliente "+str(self.client_address))
    print self.client_address, 'desconectado'
  #}}}

#}}}

