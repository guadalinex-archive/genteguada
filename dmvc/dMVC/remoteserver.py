import dMVC
import utils
import SocketServer
import thread
import pickle
import struct
import synchronized
import Queue
import remotecommand
import time
import select

class RServer(synchronized.Synchronized):

  def __init__(self,
               rootModel,
               port=8000,
               onConnection=None,
               onDisconnection=None,
               onExecution=[]
               ): #{{{
    utils.logger.debug("RServer.__init__")
    synchronized.Synchronized.__init__(self)

    dMVC.setRServer(self)

    self.__models = {}
    self.__rootModel = rootModel
    self.__port = port
    self._onConnection = onConnection
    self._onDisconnection = onDisconnection
    self._onExecution = onExecution
    self.__start()
  #}}}


  @synchronized.synchronized(lockName='models')
  def getModelByID(self, theId): #{{{
    return self.__models[theId]
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
        #utils.statServer.strServer()
        sys.exit(0)
  #}}}


class RServerHandler(SocketServer.BaseRequestHandler):


  def __sendInitialData(self): #{{{
    utils.logger.debug("RServerHandler.sendRootModel client: "+str(self.client_address))

    initialData = {}
    initialData['rootModel'] = dMVC.getRServer().getRootModel()
    initialData['sessionID'] = self.__sessionID

    self.__sendObject(initialData)
  #}}}

  def setup(self): #{{{
    utils.logger.debug("Conect client "+str(self.client_address))

    self.__sessionID = utils.nextID()

    self.fragmentCommand = {}

    self.__sendInitialData()
    #prueba
    self.__commandsQueue = Queue.Queue()
    self.__asyncCommandQueue = Queue.Queue()
    thread.start_new(self.__sendCommandQueue, ())

    handler = dMVC.getRServer()._onConnection
    if handler:
      handler(self)
  #}}}

  def __sendCommandQueue(self):
    #prueba
    while True:
      time.sleep(0.1)
      try:
        command = self.__commandsQueue.get_nowait()
        self.__sendObject(command)
      except Queue.Empty:
        self.__sendAsyncFragment()

  def __sendAsyncFragment(self):
    #prueba
    try:
      fragmentCommand = self.__asyncCommandQueue.get_nowait()
      self.__sendObject(fragmentCommand)
      print "Enviando ",fragmentCommand," ",fragmentCommand.sequence,"/",fragmentCommand.total
    except Queue.Empty:
      pass
 


    

  def getSessionID(self):
    return self.__sessionID

  def handle(self): #{{{
    utils.logger.debug("RServerHandler.handle client:  "+str(self.client_address))
    sizeInt = struct.calcsize("i")
    while True:
      read, write, error = select.select ([self.request],[self.request],[self.request],0.1)
      if self.request in read:
        size = self.request.recv(sizeInt)
        if len(size):
          size = struct.unpack("i", size)[0]
          data = ""
          while len(data) < size:
            data += self.request.recv(size - len(data))

          commandOrFragment = pickle.loads(data)
          if (isinstance(commandOrFragment, dMVC.remotecommand.RCommand)):
            self.__processCommand(commandOrFragment, size)
          elif (isinstance(commandOrFragment, dMVC.remotecommand.RFragment)):
            self.__processFragment(commandOrFragment, size)
          else:
            raise "Not valid reading from socket: " + str(commandOrFragment)
        else:
          # The conection is lost
          break
      else:
        if not self.request in write:
          self.__sendAsyncFragment()
          
  #}}}


  def __processCommand(self, command, size):
    utils.logger.debug("Receive from the client "+str(self.client_address)+" the command: " + str(command) + " (" + str(size) + "b)")
    command.setServerHandler(self)
    #Estadisticas de lo que recibe el servidor y tarda en procesarlas
    initTime = command.initStat(size)
    #command.stat(size)
    answer = command.do()
    command.stopStat(size, initTime)
    utils.logger.debug("Run the command " + str(command) + " from the client " + \
                         str(self.client_address)+ " and the result is "+str(answer))
    if answer:
      self.__sendObject(answer,command)
      #self.sendCommand(answer)

  def __processFragment(self, fragment, size):
    if not fragment.groupID in self.fragmentCommand.keys():
      self.fragmentCommand[fragment.groupID] = fragment.data
    else:
      self.fragmentCommand[fragment.groupID] += fragment.data
    if fragment.total == fragment.sequence:
      command = pickle.loads(self.fragmentCommand[fragment.groupID])
      del self.fragmentCommand[fragment.groupID]
      command.setServerHandler(self)
      answer = command.do()
      if answer:
        self.__sendAsyncObject(answer, fragment.groupID)

    
  def __sendAsyncObject(self, obj, commandID): #{{{
    toSerialize = dMVC.objectToSerialize(obj, dMVC.getRServer())
    serialized = pickle.dumps(toSerialize)
    #serialized = pickle.dumps(obj)
    sizeSerialized = len(serialized)
    total = sizeSerialized / 10000
    if not sizeSerialized % 10000 == 0:
      total += 1
    lenProcess = 0
    sequence = 0
    asyncCommandID = utils.nextID()
    #asyncQueue = []
    while lenProcess < sizeSerialized:
      sequence += 1
      fragmentCommand = serialized[lenProcess : lenProcess + 10000]
      fragment = remotecommand.RFragment(asyncCommandID, sequence, total, fragmentCommand, commandID)
      #asyncQueue.append(fragment)
      self.__asyncCommandQueue.put(fragment)
      lenProcess += 10000
    #prueba
    #thread.start_new(self.__sendAsyncQueue, (asyncQueue,))
  #}}}

  def __sendAsyncQueue(self, queue):
    #prueba
    import time
    for fragment in queue:
      time.sleep(0.1)
      self.sendCommand(fragment)

  def __sendObject(self, obj, command=None): #{{{
    toSerialize = dMVC.objectToSerialize(obj, dMVC.getRServer())
    serialized = pickle.dumps(toSerialize)
    sizeSerialized = len(serialized)
    try:
      size = struct.pack("i", sizeSerialized)
      utils.logger.debug("Sendind object " + str(obj) + " to client: "+str(self.client_address) + " (" + str(sizeSerialized) + "b)" )
      self.request.send(size)
      self.request.send(serialized)
      #if command:
        #print "Enviado ",sizeSerialized , command
      return True
    except:
      utils.logger.exception("Can''t send an object, probable conexion lost")
      return False
  #}}}

  def sendCommand(self, command): #{{{
    #self.__commandsQueue.put(command)
    #prueba
    return self.__sendObject(command)
  #}}}

  def finish(self): #{{{
    utils.logger.debug("Close the connection with "+str(self.client_address))

    handler = dMVC.getRServer()._onDisconnection
    if handler:
      handler(self)

  #}}}
