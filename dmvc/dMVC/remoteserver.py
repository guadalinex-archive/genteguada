import dMVC
import utils
import SocketServer
import thread
import pickle
import struct
import synchronized

class RServer(synchronized.Synchronized):

  def __init__(self, rootModel, port=8000): #{{{
    utils.logger.debug("RServer.__init__")
    synchronized.Synchronized.__init__(self)

    dMVC.setRServer(self)

    self.__models = {}
    self.__port = port
    self.__rootModel = rootModel
    self.__start()
  #}}}


  @synchronized.synchronized(lockName='models')
  def getModelByID(self, id): #{{{
    utils.logger.debug("RServer.getModelByID id: "+str(id))
    return self.__models[id]
  #}}}

  @synchronized.synchronized(lockName='models')
  def registerModel(self, model): #{{{
    utils.logger.debug("RServer.registerModel model: "+str(model))
    if model in self.__models.values():
      utils.logger.error("The molel "+str(model)+" is allready register")
      return
    modelID = utils.nextID()
    model.setID(modelID)
    utils.logger.info("Register the model with id "+str(id))
    self.__models[modelID] = model
  #}}}

  def getRootModel(self): #{{{
    utils.logger.debug("RServer.getRootModel")
    return self.__rootModel
  #}}}

  def __start(self): #{{{
    utils.logger.debug("RServer.__start")
    con = SocketServer.ThreadingTCPServer(('', self.__port), RServerHandler)
    con.request_queue_size = 500
    thread.start_new(con.serve_forever, ())
    utils.logger.info("Server listen...")
    #TODO habra que eliminar este import porque para cerrar el servidor habra que hacerlo de otro manera
    import sys
    while 1:
      data = raw_input('')
      if data.rstrip() == "quit": 
        con.server_close()
        sys.exit(0)
  #}}}


class RServerHandler(SocketServer.BaseRequestHandler):

  def __sendRootModel(self): #{{{
    utils.logger.debug("RServerHandler.sendRootModel client: "+str(self.client_address))
    self.__sendObject(dMVC.getRServer().getRootModel())
  #}}}

  def setup(self): #{{{
    utils.logger.debug("RServerHandler.setup client:  "+str(self.client_address))
    utils.logger.info("Conect client "+str(self.client_address))
    self.__sendRootModel()
  #}}}

  def handle(self): #{{{
    utils.logger.debug("RServerHandler.handle client:  "+str(self.client_address))
    sizeInt = struct.calcsize("i")
    while True:
      size = self.request.recv(sizeInt)
      if len(size):
        size = struct.unpack("i", size)[0]
        commandData = ""
        utils.logger.debug("Receive from the client "+str(self.client_address)+" a command with "+str(size)+" bytes of size")
        while len(commandData) < size:
          commandData = self.request.recv(size - len(commandData))
        command = pickle.loads(commandData)
        utils.logger.debug("Receive from the client "+str(self.client_address)+" the command")
        command.setServerHandler(self)
        answer = command.do()
        utils.logger.info("Run the commnad from the client "+str(self.client_address)+ " and the result is "+str(answer))
        if answer:
          utils.logger.debug("Send the answer "+str(answer)+" to client "+str(self.client_address))
          self.__sendObject(answer)
      else:
        utils.logger.info("Close the connection with "+str(self.client_address))
        break
  #}}}

  def __sendObject(self, object): #{{{
    utils.logger.debug("RServerHandler.sendObject client: "+str(self.client_address)+" object: "+str(object))
    toSerialize = dMVC.objectToSerialize(object, dMVC.getRServer())
    serialized = pickle.dumps(toSerialize)
    sizeSerialized = len(serialized)
    try:
      size = struct.pack("i",sizeSerialized)
      self.request.send(size)
      self.request.send(serialized)
      return True
    except:
      utils.logger.exception("The object can't send")
      return False
  #}}}

  def sendCommand(self, command): #{{{
    utils.logger.debug("RServerHandler.sendCommand client: "+str(self.client_address)+" command: "+str(command))
    return self.__sendObject(command)
  #}}}

  def finish(self): #{{{
    utils.logger.debug("RServerHandler.finish client: "+str(self.client_address))
    utils.logger.info("Close the connection with "+str(self.client_address))
  #}}}
