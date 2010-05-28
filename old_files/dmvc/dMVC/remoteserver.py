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
import signal
import gzip
import weakref

class RServer(synchronized.Synchronized):

  def __init__(self, rootModel, version = None ,port=8000, onConnection=None, onDisconnection=None, onExecution=[]): 
    utils.logger.debug("RServer.__init__")
    synchronized.Synchronized.__init__(self)
    dMVC.setRServer(self)
    self.__models = {}
    #self.__models = weakref.WeakValueDictionary()
    self.__rootModel = rootModel
    self.__version = version
    self.__port = port
    self.__con = None
    self.__activeServer = False
    self._onConnection = onConnection
    self._onDisconnection = onDisconnection
    self._onExecution = onExecution
    signal.signal(signal.SIGINT, self.__finish)
    self.__listHandlers = []
    self.__start()

  @synchronized.synchronized(lockName='handler')
  def registerHandler(self, handler):
    if not handler in self.__listHandlers:
      self.__listHandlers.append(handler)

  @synchronized.synchronized(lockName='handler')
  def unregisterHandler(self, handler):
    if handler in self.__listHandlers:
      self.__listHandlers.remove(handler)

  def __finish(self, signal, frame):
    for handler in self.__listHandlers:
      player = handler.ggSession.getPlayer()
      player.kick()
    while not len(self.__listHandlers) == 0:
      pass
    self.__activeServer = False

  @synchronized.synchronized(lockName='models')
  def getModelByID(self, theId): 
    return self.__models[theId]

  @synchronized.synchronized(lockName='models')
  def registerModel(self, model): 
    if model in self.__models.values():
      utils.logger.error("The model "+str(model)+" is allready register")
      return
    modelID = utils.nextID()
    model.setID(modelID)
    self.__models[modelID] = model
    utils.logger.debug("Registered the model " + str(model) + " with id "+str(modelID))

  def getRootModel(self): 
    return self.__rootModel

  def getSocket(self):
    return self.__con

  def __start(self): 
    utils.logger.debug("RServer.__start")
    self.__con = SocketServer.ThreadingTCPServer(('', self.__port), RServerHandler)
    self.__con.request_queue_size = 500
    thread.start_new(self.__con.serve_forever, ())
    utils.logger.debug("Server listen...")
    self.__activeServer = True
    while self.__activeServer:
      time.sleep(2)
    time.sleep(2)
    self.__con.server_close()

  def getVersion(self):
    return self.__version


class RServerHandler(SocketServer.BaseRequestHandler, synchronized.Synchronized):

  def __sendInitialData(self): 
    utils.logger.debug("RServerHandler.sendRootModel client: "+str(self.client_address))
    synchronized.Synchronized.__init__(self)
    initialData = {}
    initialData['rootModel'] = dMVC.getRServer().getRootModel()
    initialData['sessionID'] = self.__sessionID
    initialData['version'] = dMVC.getRServer().getVersion()
    self.sendCommand(initialData)

  def setup(self): 
    utils.logger.debug("Conect client "+str(self.client_address))
    self.__sessionID = utils.nextID()
    self.fragmentCommand = {}
    self.__commandsQueue = Queue.Queue()
    self.__asyncCommandQueue = Queue.Queue()
    thread.start_new(self.__sendCommandQueue, ())
    self.__sendInitialData()
    dMVC.getRServer().registerHandler(self)
    handler = dMVC.getRServer()._onConnection
    if handler:
      handler(self)

  def __sendCommandQueue(self):
    while True:
      time.sleep(0.025)
      try:
        command = self.__commandsQueue.get_nowait()
        commands = []
        commands.append(command)
        time.sleep(0.015) # Wait for more commands, to send them all in a shot
        try:
          while True:
            commands.append(self.__commandsQueue.get_nowait())
        except Queue.Empty:
          pass
        if len(commands) == 1:
          self.__sendObject(command)
        else:
          utils.logger.debug("Sending " + str(len(commands)) + " commands in a shot")
          self.__sendObject(remotecommand.RCompositeCommand(commands))
      except Queue.Empty:
        self.__sendAsyncFragment()

  def __sendAsyncFragment(self):
    try:
      fragmentCommand = self.__asyncCommandQueue.get_nowait()
      self.__sendObject(fragmentCommand)
      print "Enviando ",fragmentCommand," ",fragmentCommand.sequence,"/",fragmentCommand.total
    except Queue.Empty:
      pass

  def getSessionID(self):
    return self.__sessionID

  def handle(self): 
    utils.logger.debug("RServerHandler.handle client:  "+str(self.client_address))
    sizeInt = struct.calcsize("i")
    while True:
      time.sleep(0.01)
      try:
        read, write, error = select.select ([self.request],[self.request],[self.request],0)
        if self.request in read:
          size = self.request.recv(sizeInt)
          if len(size):
            size = struct.unpack("i", size)[0]
            data = ""
            while len(data) < size:
              data += self.request.recv(size - len(data))
            data = gzip.zlib.decompress(data)
            commandOrFragment = pickle.loads(data)
            print commandOrFragment
            if (isinstance(commandOrFragment, dMVC.remotecommand.RCommand)):
              self.__processCommand(commandOrFragment, size)
            elif (isinstance(commandOrFragment, dMVC.remotecommand.RFragment)):
              self.__processFragment(commandOrFragment, size)
            else:
              raise "Not valid reading from socket: " + str(commandOrFragment)
          else:
            # The conection is lost
            self.finish()
            break
        else:
          if not self.request in write:
            self.__sendAsyncFragment()
      except:
        self.finish()
        break

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
      self.sendCommand(answer)

  def __processFragment(self, fragment, size):
    if not fragment.groupID in self.fragmentCommand.keys():
      self.fragmentCommand[fragment.groupID] = fragment.data
    else:
      self.fragmentCommand[fragment.groupID] += fragment.data
    if fragment.total == fragment.sequence:
      command = pickle.loads(self.fragmentCommand[fragment.groupID])
      del self.fragmentCommand[fragment.groupID]
      command.setServerHandler(self)
      print "voy a ejecutar el comando asincrono"
      answer = command.do()
      if answer:
        print "tengo respuesta"
        self.__sendAsyncObject(answer, fragment.groupID)

  def __sendAsyncObject(self, obj, commandID): 
    toSerialize = dMVC.objectToSerialize(obj, dMVC.getRServer())
    serialized = pickle.dumps(toSerialize)
    sizeSerialized = len(serialized)
    total = sizeSerialized / 10000
    if not sizeSerialized % 10000 == 0:
      total += 1
    lenProcess = 0
    sequence = 0
    asyncCommandID = utils.nextID()
    while lenProcess < sizeSerialized:
      sequence += 1
      fragmentCommand = serialized[lenProcess : lenProcess + 10000]
      fragment = remotecommand.RFragment(asyncCommandID, sequence, total, fragmentCommand, commandID)
      self.__asyncCommandQueue.put(fragment)
      lenProcess += 10000
    print "Ya tenemos todos los fragmentos puestos en la cola"

  @synchronized.synchronized(lockName='sendObject')
  def __sendObject(self, obj, command=None): 
    toSerialize = dMVC.objectToSerialize(obj, dMVC.getRServer())
    serialized = pickle.dumps(toSerialize)
    sizeSerialized = len(serialized)
    serializedCompress = gzip.zlib.compress(serialized)
    sizeSerializedCompress = len(serializedCompress)
    compress = '%.2f'% (100 - ((float(sizeSerializedCompress) / float(sizeSerialized)) * 100))
    try:
      size = struct.pack("i", sizeSerializedCompress)
      utils.logger.debug("Sendind object " + str(obj) + " to client: "+str(self.client_address) + " (" + str(sizeSerializedCompress) + "b), compress: "+compress )
      self.request.send(size)
      self.request.send(serializedCompress)
      #if command:
      #  print "Enviado ",sizeSerialized , command
      return True
    except:
      #utils.logger.exception("Can''t send an object, probable conexion lost")
      self.finish()
      return False

  def sendCommand(self, command): 
    self.__commandsQueue.put(command)
    return True

  def finish(self): 
    SocketServer.BaseRequestHandler.finish(self)
    utils.logger.debug("Close the connection with "+str(self.client_address))
    dMVC.getRServer().unregisterHandler(self)
    handler = dMVC.getRServer()._onDisconnection
    if handler:
      handler(self)

