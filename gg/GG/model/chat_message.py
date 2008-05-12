

class chatMessage:
    
  def __init__(self, message, sender):
    self.__message = message
    self.__sender = sender
    
  def getMessage(self):
    return self.__message

  def getSender(self):
    return self.__sender