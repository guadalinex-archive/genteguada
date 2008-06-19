import ggmodel
import time
import dMVC.model
import GG.isoview.isoview_chatmessage

class ChatMessage(ggmodel.GGModel):
  """ ChatMessage class.
  Defines a book object behaviour.
  """
     
  def __init__(self, message, sender, color, position, type):
    """ Class constructor.
    message: chat message.
    sender: player who sends the message.
    color: text color.
    position: on-screen chat message starting position.
    """
    ggmodel.GGModel.__init__(self)
    self.__message = message
    self.__sender = sender
    self.__hour = time.time()
    self.__color = color
    self.__position = position
    self.type = type
    self.imagePath = ""
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['imagePath', 'type']
    
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
    return time.strftime("%H:%M", time.localtime(self.__hour))

  def getColor(self):
    """ Returns the message color.
    """
    return self.__color

  def getPosition(self):
    """ On-screen chat message starting position.
    """
    return self.__position

  def getType(self):
    return self.type

  @dMVC.model.localMethod 
  def chatView(self, screen, isohud):
    """ Creates an isometric view object for the chat message.
    screen: screen handler.
    """
    return GG.isoview.isoview_chatmessage.IsoViewChatMessage(self, screen, isohud)
    