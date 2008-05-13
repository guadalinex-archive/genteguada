import time

class ChatMessage:
  """ ChatMessage class.
  Defines a book object behaviour.
  """
     
  def __init__(self, message, sender):
    """ Class constructor.
    message: chat message.
    sender: player who sends the message.
    """
    self.__message = message
    self.__sender = sender
    self.__hour = time.time()
    
  def getMessage(self):
    """ Returns the chat message.
    """
    return self.__message

  def getSender(self):
    """ Returns the sender message label.
    """
    return self.__sender

  def getHour(self):
    """ Returns the hour that the message was sended at.
    """
    return time.strftime("%H:%M",time.localtime(self.__hour))
