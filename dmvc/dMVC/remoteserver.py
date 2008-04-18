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
    return self.__models[id]
  #}}}

  @synchronized.synchronized(lockName='models')
  def registerModel(self, model): #{{{
    if model in self.__models.values():
      utils.logger.error("The model "+str(model)+" is allready register")
      return
    modelID = utils.nextID()
    model.setID(modelID)
    self.__models[modelID] = model
    utils.logger.debug("Registered the model " + str(model) + " with id "+str(modelID))
  #}}}

  def getRootModel(self): #{{{
    return self.__rootModel
  #}}}

  def __start(self): #{{{
    utils.logger.debug("RServer.__start")
    con = SocketServer.ThreadingTCPServer(('', self.__port), RServerHandler)
    con.request_queue_size = 500
    thread.start_new(con.serve_forever, ())
    utils.logger.debug("Server listen...")
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
    utils.logger.debug("Conect client "+str(self.client_address))
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
        while len(commandData) < size:
          commandData = self.request.recv(size - len(commandData))
        command = pickle.loads(commandData)
        utils.logger.debug("Receive from the client "+str(self.client_address)+" the command: " + str(command) + " (" + str(size) + "b)")
        command.setServerHandler(self)
        answer = command.do()
        utils.logger.debug("Run the command " + str(command) + " from the client "+str(self.client_address)+ " and the result is "+str(answer))
        if answer:
          self.__sendObject(answer)
      else:
        break
  #}}}

  def __sendObject(self, object): #{{{
    utils.logger.debug("Sendind object " + str(object) + " to client: "+str(self.client_address))
    toSerialize = dMVC.objectToSerialize(object, dMVC.getRServer())
    serialized = pickle.dumps(toSerialize)
    sizeSerialized = len(serialized)
    try:
      size = struct.pack("i", sizeSerialized)
      self.request.send(size)
      self.request.send(serialized)
      return True
    except:
      utils.logger.exception("Can''t send an object, probable conexion lost")
      return False
  #}}}

  def sendCommand(self, command): #{{{
    return self.__sendObject(command)
  #}}}

  def finish(self): #{{{
    utils.logger.debug("Close the connection with "+str(self.client_address))
  #}}}
