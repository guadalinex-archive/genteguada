import dMVC.model
import GG.utils
import GG.isoview.isoview_hud
import ggmodel

class GGSession(ggmodel.GGModel):
  """ GGSession class.
  Includes room and player objects, and some procedures to manage data.
  """
    
  def __init__(self, player):
    """ Initializes session attributes.
    player: session user.
    """
    ggmodel.GGModel.__init__(self)
    self.__player = player
    #self.__room = 
    self.__messagesChat = []
    self.__messagesChat.append("_.-= Wellcome to " + GG.utils.VERSION + " =-._")
      
  # self.__player
  
  def getPlayer(self):
    """ Returns the active player.
    """
    return self.__player

  def setPlayer(self, player):
    """ Sets a new active player.
    """
    if self.__player <> player:
      self.__player = player
      self.triggerEvent('player', player=player)
      return True
    return False

  # self.__chat
  
  def getMessagesChat(self):
    """ Returns the chat log.
    """
    return self.__messagesChat
  
  def setMessagesChat(self, messagesChat):
    """ Sets the session's chat with a new log.
    chat: new log.
    """
    if self.__messagesChat <> messagesChat:
      self.__messagesChat = chat
      self.triggerEvent('messagesChat', messagesChat=messagesChat)
      return True
    return False
      
  def addMessageChat(self, messageChat):
    """ Adds a new string to the chat log.
    chat: new string.
    """
    if not messageChat in self.__messagesChat:
      self.__messagesChat.append(messageChat)
      self.triggerEvent('addMessageChat', messageChat=messageChat)
      return True
    return False
    
  def removeMessageChat(self, messageChat):
    """ Removes a string from the chat log.
    chat: string to be removed.
    """
    if messageChat in self.__messageChat:
      self.__messagesChat.remove(messageChat)
      self.triggerEvent('removeMessageChat', messageChat=messageChat)
      return True
    return False
    
  @dMVC.model.localMethod
  def defaultView(self, screen):
    """ Esto deberia ser IsoViewSession.
    screen: screen handler.
    """
    return GG.isoview.isoview_hud.IsoViewHud(self, screen)

  def logout(self):
    """
    """
    #lanzar evento removePlayer a la habitacion. Metodo por definir.
    pass

