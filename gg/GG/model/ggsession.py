import dMVC.model
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

