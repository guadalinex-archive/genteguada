import ggmodel
import room
import player

class GGSession(ggmodel.GGModel):
    """ GGSession class.
    Includes room and player objects, and some procedures to manage data.
    """
    
    def __init__(self, name, id, player):
      """ Initializes session attributes.
      """
      ggmodel.GGModel.__init__(self, name, id)
      self.__player = player
      
    def getPlayer(self):
      return self.__player
    
      
