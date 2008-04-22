import dMVC.model
import isoview_hud

class GGSession(dMVC.model.Model):
    """ GGSession class.
    Includes room and player objects, and some procedures to manage data.
    """
    
    def __init__(self, player):
      """ Initializes session attributes.
      """
      dMVC.model.Model.__init__(self)
      self.__player = player
      
    def getPlayer(self):
      """ Returns the active player.
      """
      return self.__player
    
    def defaultView(self, screen):
      """ Esto debería ser IsoViewSession.
      """
      return isoview_hud.IsoViewHud(self, screen)
    