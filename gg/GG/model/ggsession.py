import dMVC.model
import GG.utils
import GG.isoview.isoview_hud
import ggmodel

class GGSession(ggmodel.GGModel):
  """ GGSession class.
  Includes room and player objects, and some procedures to manage data.
  """
    
  def __init__(self, player, system):
    """ Initializes session attributes.
    player: session user.
    """
    ggmodel.GGModel.__init__(self)
    self.__player = player
    self.__system = system
    player.subscribeEvent('chatAdded', self.chatAdded)
    player.getRoom().subscribeEvent('chatAdded', self.chatAdded)
    player.getRoom().subscribeEvent('quizAdded', self.quizAdded)
    player.subscribeEvent('roomChanged', self.roomChanged)
      
  # self.__player
  
  def getPlayer(self):
    """ Returns the active player.
    """
    return self.__player
   
  def roomChanged(self, event):
    """ Triggers after receiving a change room event.
    event: event info.
    """
    oldRoom = event.getParams()['oldRoom']
    if oldRoom:
      oldRoom.unsubscribeEventMethod(self.chatAdded)
    newRoom = self.__player.getRoom()
    if newRoom: 
      newRoom.subscribeEvent('chatAdded', self.chatAdded)
      newRoom.subscribeEvent('quizAdded', self.quizAdded)
    
  @dMVC.model.localMethod
  def defaultView(self, screen, parent):
    """ Esto deberia ser IsoViewSession.
    screen: screen handler.
    """
    return GG.isoview.isoview_hud.IsoViewHud(self, screen, parent)

  def logout(self):
    """ Ends an user session.
    """
    self.__player.abandonRoom()
    
  def chatAdded(self, event):
    """ Triggers after receiving a chat added event.
    event: event info.
    """
    self.triggerEvent('chatAdded', message=event.getParams()['message'])
  
  def quizAdded(self, event):
    """ Triggers after receiving a chat added event.
    event: event info.
    """
    self.triggerEvent('quizAdded', message=event.getParams()['message'])
  

  def logout(self):
    print str(self) + ": logout!"
    self.__system.logout(self)
    self.__player = None
    self.__system = None
