import threading
import socket
import pickle
import sys
import select
import ggcommon.remotecommand

global _rClientSingleton
_rClientSingleton = None

def getRClient(): #{{{
  if _rClientSingleton == None:
    raise Exception("RClient has to be instanciated before calling getRClient()")
  return _rClientSingleton
#}}}

class RClient: #{{{ 

  def __init__(self, serverIP, port=8000): #{{{
    global _rClientSingleton
    if not (_rClientSingleton == None):
      raise Exception("Can't create more then one instance of RClient")
    _rClientSingleton = self
    self._serverIP = serverIP
    self._serverPort = port
    self._rootModel = None
    self._rootModelSemaphore = threading.Semaphore(0)
    self._thread = None
    self._start()
  #}}}

  def hasRootModel(self): #{{{
    return not (self._rootModel == None)
  #}}}

  def setRootModel(self, model): #{{{
    if self._rootModel != None:
      raise Exception('The receiver already has a rootModel')
    self._rootModel = model
    self._rootModelSemaphore.release()
  #}}}

  def getRootModel(self): #{{{
    self._rootModelSemaphore.acquire()
    result = self._rootModel
    self._rootModelSemaphore.release()   
    return result
  #}}}

  def sendCommand(self, command): #{{{
    return self._thread.sendCommand(command)
  #}}}

  def _start(self): #{{{
    self._thread = RClientThread(self)
    self._thread.start()
  #}}}

#}}}

class RClientThread(threading.Thread): #{{{

  def __init__(self, rClient): #{{{
    threading.Thread.__init__(self)
    self.rClient = rClient
    self.socket  = None
    self.resultComand = None
    self._resultCommandSemaphore = threading.Semaphore(0)
  #}}}

  def _receiveRootModel(self): #{{{
    data = self.socket.recv(1024)
    rootModel = pickle.loads(data)
    self.rClient.setRootModel(rootModel)
  #}}}

  def run(self): #{{{
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.rClient._serverIP, self.rClient._serverPort))
    self._receiveRootModel()
    while True:
      read, write, error = select.select ([self.socket],[self.socket],[self.socket],1)
      if read:
        answerData = self.socket.recv(1024)
        answer = pickle.loads(answerData)
        if isinstance(answer,ggcommon.remotecommand.RExecutionResult) or isinstance(answer,ggcommon.remotecommand.RExceptionRaiser):   
          self.resultCommand = answer
          self._resultCommandSemaphore.release()
      
      """
      data = raw_input('')
      if data.rstrip() == "quit": 
        self.socket.close()
        sys.exit(0)
      """
  #}}}

  def sendCommand(self, command): #{{{
    serializedCommand = pickle.dumps(command)
    self.socket.send(serializedCommand)

    self._resultCommandSemaphore.acquire()
    return self.resultCommand.do()

    #answerData = self.socket.recv(1024)
    #answer = pickle.loads(answerData)
    #return answer.do()
  #}}}

#}}}
