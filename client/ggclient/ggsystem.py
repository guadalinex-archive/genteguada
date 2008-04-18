import ggmodel
import room
import player

class GGSystem(ggmodel.GGModel):
    """ GGSystem class.
    Includes room and player objects, and some procedures to manage data.
    """
    
    def __init__(self):
      """ Initializes the model attributes and both room and player lists.
      """
      ggmodel.GGModel.__init__(self, "System model", 0)
      self.__rooms = []
      self.__players = []
      
    def getRoom(self, id):
      """ Returns a specific room.
      """
      for room in self.__rooms:
        if id == room.getId():
          return room
    
    def getPlayer(self, id=None, username=None, password=None):
      """ Searchs and returns a player, either by his id or by his username & password.
      """
      if id <> None:
        for player in self.__players:
          if id == player.getId():
            return player
      else:  
        for player in self.__players:
          if player.checkUser(username, password):
            return player
    
    def createRoom(self, name, id, sprite, spriteFull):
      """ Creates a room and appends it to the room list.
      """
      self.__rooms.append(room.Room(name, id, sprite, spriteFull))
    
    def createPlayer(self, name, id, sprite, size, position, offset, username, password):
      """ Creates a player and appends him to the player list.
      """
      self.__players.append(player.Player(name, id, sprite, size, position, offset, username, password))  
    
    def insertPlayerIntoRoom(self, idPlayer, idRoom):
      """ Inserts an existing player into a room.
      """
      self.getRoom(idRoom).insertPlayer(self.getPlayer(idPlayer))
    
    def tick(self):
      """ Calls for an update on all rooms, including players on them.
      """
      for room in self.__rooms:
        room.tick()
    
    