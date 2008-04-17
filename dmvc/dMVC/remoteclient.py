
import utils
import threading
import socket
import time
import pickle
import remotecommand
import struct
import thread

class RClient: 

  def __init__(self, serverIP, port=8000): #{{{
    utils.logger.debug("RClient.__init__")
    try:
      utils.getRClient()
      utils.logger.error("Can't create more then one instance of RClient")
      raise Exception("Can't create more then one instance of RClient")
    except:
      utils.setRClient(self)
      self.__serverIP = serverIP
      self.__serverPort = port
      self.__rootModel = None
      self.__rootModelSemaphore = threading.Semaphore(0)
      self.__commandsList      = []
      self.__commandsListMutex = threading.Semaphore(1)
      self.__remoteSuscriptions = {}  ## TODO: Use weak references
      self.__remoteSuscriptionsMutex = threading.Semaphore(1)
      self.__socket = None
      self.__socketSemaphore = threading.Semaphore(0)
      thread.start_new(self.__start,())
  #}}}

  def __addCommand(self, command): #{{{
    utils.logger.debug("RClient.addCommand command: "+str(command))
    self.__commandsListMutex.acquire()
    self.__commandsList.append(command)
    self.__commandsListMutex.release()
  #}}}

  def setRootModel(self, model): #{{{
    utils.logger.debug("RClient.setRootModel model: "+str(model))
    if self.__rootModel != None:
      utils.logger.error("The receiver already has a rootModel")
      raise Exception('The receiver already has a rootModel')
    self.__rootModel = model
    self.__rootModelSemaphore.release()
  #}}}

  def getRootModel(self): #{{{
    utils.logger.debug("RClient.getRootModel")
    self.__rootModelSemaphore.acquire()
    result = self.__rootModel
    self.__rootModelSemaphore.release()   
    return result
  #}}}

  def sendCommand(self, command): #{{{
    utils.logger.debug("RClient.sendCommand command: "+str(command))
    serializedCommand = pickle.dumps(command)
    sizeCommand = len(serializedCommand)
    size = struct.pack("i",sizeCommand)
    self.__socket.send(size)
    self.__socket.send(serializedCommand)
  #}}}

  def waitForExecutionAnswerer(self, executerCommand): #{{{
    utils.logger.debug("RClient.waitForExecutionAnswerer executerCommand: "+str(executerCommand))
    found = None
    while not found:
      self.__commandsListMutex.acquire()
      for each in self.__commandsList:
        if executerCommand.isYourAnswer(each):
          found = each
          break
      if found:
        self.__commandsList.remove(found)
      self.__commandsListMutex.release()
      if not found:
        time.sleep(0.02)
    return found
  #}}}

  def registerRemoteSuscription(self, suscription): #{{{
    utils.logger.debug("RClient.registerRemoteSuscription suscription: "+str(suscription))
    suscriptionID = utils.nextID()
    self.__remoteSuscriptionsMutex.acquire()
    self.__remoteSuscriptions[suscriptionID] = suscription
    self.__remoteSuscriptionsMutex.release()
    return suscriptionID
  #}}}

  def getRemoteSuscriptionByID(self, suscriptionID): #{{{
    utils.logger.debug("RClient.getRemoteSuscriptionByID suscriptionID: "+str(suscriptionID))
    self.__remoteSuscriptionsMutex.acquire()
    result = self.__remoteSuscriptions[suscriptionID]
    self.__remoteSuscriptionsMutex.release()
    return result
  #}}}

  def __connect(self): #{{{
    utils.logger.debug("RClient.connect")
    self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__socket.connect((self.__serverIP, self.__serverPort))
    utils.logger.info("the client connect to server")
    self.__socketSemaphore.release()
  #}}}

  def __receiveRootModel(self): #{{{
    utils.logger.debug("RClient.receiveRootModel")
    size = struct.calcsize("i")
    size = self.__socket.recv(size)
    if len(size):
      size = struct.unpack("i", size)[0]
      data = ""
      while len(data) < size:
        data = self.__socket.recv(size - len(data))
      rootModel = pickle.loads(data)
      self.setRootModel(rootModel)
  #}}}

  def __start(self): #{{{
    utils.logger.debug("RClient.start")
    self.__connect()
    self.__receiveRootModel()
    sizeInt = struct.calcsize("i")
    while True:
      size = self.__socket.recv(sizeInt)
      if len(size):
        size = struct.unpack("i", size)[0]
        commandData = ""
        utils.logger.debug("Receive from the server a command with "+str(size)+" bytes of size")
        while len(commandData) < size:
          commandData = self.__socket.recv(size - len(commandData))
        command = pickle.loads(commandData)
        utils.logger.debug("Receive from the server the command")
        if isinstance(command, remotecommand.RExecutionAnswerer):
          self.__addCommand(command)
        else:
          command.do()
      else:
        self.__socket.close()
  #}}}

