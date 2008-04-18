import ggmodel
import room
import player
import ggsession

class GGLobby(ggmodel.GGModel):
    """ GGLobby class.
    Main lobby model. Manages the user login procedures.
    """
    
    def __init__(self, ggsystem):
      """ Initializes session attributes.
      """
      ggmodel.GGModel.__init__(self, "Lobby", 0)
      self.__ggsystem = ggsystem
      
    def login(self, username, password):
      """ Attempts to login on an user. If succesfull, returns a ggsession model.
      """
      player = self.__ggsystem.getPlayer(None, username, password)
      if player <> None:
        return ggsession.GGSession("Session 1", 0, player)
      else:
        return None
      
