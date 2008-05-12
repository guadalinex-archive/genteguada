import time

class chatMessage:
    
  def __init__(self, message, sender):
    self.__message = message
    self.__sender = sender
    self.__hour = time.time()
    
  def getMessage(self):
    return self.__message

  def getSender(self):
    return self.__sender

  def getHour(self):
    return time.strftime("%H:%M",time.localtime(self.__hour))
