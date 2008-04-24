import dMVC.model
import GG.utils
import room
import player
import ggsession
import item
import thread
import time

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
    self.createRoom(GG.utils.BG_FULL)
    if self.createPlayer(GG.utils.NINO_SPRITE, GG.utils.NINO_SZ, [0, 0, 0], [2*GG.utils.CHAR_SZ[0]-35, GG.utils.CHAR_SZ[1]], "pepe", "1234"):
      self.insertPlayerIntoRoom(self.__players[0], self.__rooms[0])
    if self.createPlayer(GG.utils.NINA_SPRITE, GG.utils.NINO_SZ, [2, 0, 2], [2*GG.utils.CHAR_SZ[0]-35, GG.utils.CHAR_SZ[1]], "pepe2", "12345"):
      self.insertPlayerIntoRoom(self.__players[1], self.__rooms[0])
    thread.start_new(self.start,())
      
  def login(self, username, password):
    """ Attempts to login on an user. If succesfull, returns a ggsession model.
    """
    for player in self.__players:
      if player.checkUser(username, password):
        return ggsession.GGSession(player)
    return None
      
  def createRoom(self, spriteFull):
    room_ = room.GGRoom(spriteFull)
    room_.loadItems()
    self.__rooms.append(room_)
      
  def createPlayer(self, sprite, size, position, offset, username, password):
    for pl in self.__players:
      if pl.checkUser(username, password):
        return False
    self.__players.append(player.GGPlayer(sprite, size, position, offset, username, password))
    return True
    
  def insertPlayerIntoRoom(self, player, room):
    room.insertPlayer(player)

  def start(self):
    while True:
      time.sleep(GG.utils.TICK_DELAY)
      self.tick()
    
  def tick(self):
    for room in self.__rooms:
      room.tick()    
