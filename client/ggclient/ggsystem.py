import dMVC.model
import utils
import room
import player
import ggsession

class GGSystem(dMVC.model.Model):
    """ GGSystem class.
    Includes room and player objects, and some procedures to manage data.
    """
    
    def __init__(self):
      """ Initializes the model attributes and both room and player lists.
      """
      dMVC.model.Model.__init__(self)
      self.__rooms = []
      self.__players = []
      # llamadas solo para realizar pruebas
      self.createRoom(utils.BG_FULL)
      self.createPlayer(utils.NINO_SPRITE, utils.NINO_SZ, [0, 0, 0], [2*utils.CHAR_SZ[0]-35, utils.CHAR_SZ[1]], "pepe", "1234")
      self.createPlayer(utils.NINA_SPRITE, utils.NINO_SZ, [2, 0, 2], [2*utils.CHAR_SZ[0]-35, utils.CHAR_SZ[1]], "pepe2", "12345")
      self.insertPlayerIntoRoom(self.__players[0], self.__rooms[0])
      self.insertPlayerIntoRoom(self.__players[1], self.__rooms[0])
      
    def login(self, username, password):
      """ Attempts to login on an user. If succesfull, returns a ggsession model.
      """
      for player in self.__players:
        if player.checkUser(username, password):
          return ggsession.GGSession(player)
      return None
      
    def createRoom(self, spriteFull):
      self.__rooms.append(room.GGRoom(spriteFull))
    
    def createPlayer(self, sprite, size, position, offset, username, password):
      self.__players.append(player.GGPlayer(sprite, size, position, offset, username, password))  
    
    def insertPlayerIntoRoom(self, player, room):
      room.insertPlayer(player)
    
    def tick(self):
      for room in self.__rooms:
        room.tick()    
      
    """  
    def getRoom(self, id):
      for room in self.__rooms:
        if id == room.getId():
          return room
    
    def getPlayer(self, id=None, username=None, password=None):
      if id <> None:
        for player in self.__players:
          if id == player.getId():
            return player
      else:  
        for player in self.__players:
          if player.checkUser(username, password):
            return player
      return None
    
    
    
    

    """
    