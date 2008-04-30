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
    self.__chat = []
    self.__chat.append("_.-= Wellcome to " + GG.utils.VERSION + " =-._")
      
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
  
  def getChat(self):
    """ Returns the chat log.
    """
    return self.__chat
  
  def setChat(self, chat):
    """ Sets the session's chat with a new log.
    chat: new log.
    """
    if self.__chat <> chat:
      self.__chat = chat
      self.triggerEvent('chat', chat=chat)
      return True
    return False
      
  def addChat(self, chat):
    """ Adds a new string to the chat log.
    chat: new string.
    """
    if not string in self.__chat:
      self.__chat.append(chat)
      self.triggerEvent('addChat', chat=chat)
      return True
    return False
    
  def removeChat(self, chat):
    """ Removes a string from the chat log.
    chat: string to be removed.
    """
    if chat in self.__chat:
      self.__chat.remove(chat)
      self.triggerEvent('removeChat', chat=chat)
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
