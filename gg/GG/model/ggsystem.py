import dMVC.model
import GG.utils
import GG.model.room
import GG.model.player
import GG.model.ggsession
import GG.model.item
import GG.model.book
import GG.model.penguin
import GG.model.door
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
    self.__sessions = [] # Variable privada solo para uso interno.
    self.loadData()
    thread.start_new(self.start, ())
     
  def getEntryRoom(self):
    """ Returns the room used as lobby for all new players.
    """
    return self.__rooms[0]
      
  # self.__players
  
  def getPlayers(self):
    """ Returns the players list.
    """
    return self.__players
  
  def setPlayers(self, players):
    """ Sets a new players list.
    players: new players list.
    """
    if not self.__players == players:
      self.__players = players
      self.triggerEvent('players', players=players)
      return True
    return False
    
  def addPlayer(self, player):
    """ Adds a new player to the players list.
    player: new player.
    """
    if not player in self.__players:
      self.__players.append(player)
      self.triggerEvent('addPlayer', player=player)
      return True
    return False
    
  def removePlayer(self, player):
    """ Remove a player from the players list.
    player: player to be removed.
    """
    if player in self.__players:
      self.__players.remove(player)
      self.triggerEvent('removePlayer', player=player)
      return True
    return False

  def login(self, username, password):
    """ Attempts to login on an user. If succesfull, returns a ggsession model.
    username: user name.
    password: user password.
    """
    for sess in self.__sessions:
      if sess.getPlayer().checkUser(username, password):
        return False, "El usuario tiene una sesion abierta"    
    for player in self.__players:
      if player.checkUser(username, password) and player.getRoom() == None:
        player.changeRoom(self.getEntryRoom(), player.getPosition())
        session = GG.model.ggsession.GGSession(player)
        self.__sessions.append(session)
        return True, session 
    return False, "No se pudo autenticar el usuario"

  def loadData(self):
    """ Llamadas provisionales. Se eliminaran cuando se defina como se cargan los datos.
    """
    room1 = self.createRoom(GG.utils.TILE_STONE, "habitacion 1")
    room2 = self.createRoom(GG.utils.TILE_WATER, "habitacion 2")
    myPenguin = GG.model.penguin.GGPenguin(GG.utils.PENGUIN_SPRITE, [50, 55], [1, 0, 6], [20, -20], GG.utils.PENGUIN_SPRITE, 1, "Pinguino Misterioso")
    myBook = GG.model.book.GGBook(GG.utils.BOOK_SPRITE, [50, 35], [3, 0, 6], [20, -40], GG.utils.BOOK_SPRITE, 1, "Guia de Telefonos")
    myDoor1 = GG.model.door.GGDoor(GG.utils.DOOR_DOWN_SPRITE, [53, 135], [3, 0, 1], [3, 0, 7], [3, 0, 0], [20, 62], "down", room2)
    myDoor2 = GG.model.door.GGDoor(GG.utils.DOOR_DOWN_SPRITE, [53, 135], [3, 0, 1], [3, 0, 7], [3, 0, 0], [20, 62], "down", room1)
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [0, 0, 0], [55, 43]), [0, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [1, 0, 0], [55, 43]), [1, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [2, 0, 0], [55, 43]), [2, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [4, 0, 0], [55, 43]), [4, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [5, 0, 0], [55, 43]), [5, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [6, 0, 0], [55, 43]), [6, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [7, 0, 0], [55, 43]), [7, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [0, 0, 1], [55, 43]), [0, 0, 1])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [0, 0, 2], [55, 43]), [0, 0, 2])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [0, 0, 4], [55, 43]), [0, 0, 4])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [120, 133], [0, 0, 6], [55, 43]), [0, 0, 6])
    room1.addItem(myPenguin, myPenguin.getPosition())    
    room1.addItem(myBook, myBook.getPosition())    
    room1.addItem(myDoor1, myDoor1.getPosition())    
    room2.addItem(myDoor2, myDoor2.getPosition())
    self.createPlayer(GG.utils.NINO_SPRITE, GG.utils.NINO_SPRITES, GG.utils.NINA_SZ, [1, 0, 1], [2*GG.utils.CHAR_SZ[0]-75, GG.utils.CHAR_SZ[1]-20], "pepe", "1234")
    self.createPlayer(GG.utils.NINA_SPRITE, GG.utils.NINA_SPRITES, GG.utils.NINO_SZ, [2, 0, 2], [2*GG.utils.CHAR_SZ[0]-75, GG.utils.CHAR_SZ[1]-20], "pepe2", "12345")
        
  def createRoom(self, spriteFull, label):
    """ Creates a new room.
    spriteFull: sprite used to paint the room floor.
    """
    newRoom = GG.model.room.GGRoom(spriteFull, label)
    self.__rooms.append(newRoom)
    return newRoom
      
  def createPlayer(self, sprite, spriteList, size, position, offset, username, password):
    """ Creates a new player.
    sprite: sprite used to paint the player.
    size: sprite size.
    position: sprite position.
    offset: user sprite offset on screen.
    username: player user name.
    password: player password.
    """
    for player in self.__players:
      if player.checkUser(username, password):
        return False
    self.__players.append(GG.model.player.GGPlayer(sprite, spriteList, size, position, offset, username, password))
    return True
    
  def insertItemIntoRoom(self, item, room, isPlayer):
    """ Inserts a new item into a room.
    item: new item.
    room: existing room.
    player: flag used to check it the item is a player or not.
    """
    if room.addItem(item):
      if isPlayer:
        if item in self.__players:
          return
        self.__players.append(item)
    
  def removeItem(self, item, isPlayer):
    """ Removes an item.
    item: existing item.
    player: flag used to check it the item is a player or not.
    """
    if item.getRoom():
      item.getRoom().removeItem(item)    
    if isPlayer and item in self.__players:
      self.__players.remove(item)
    
  def start(self):
    """ Starts the program.
    """
    while True:
      time.sleep(GG.utils.TICK_DELAY)
      self.tick()
    
  def tick(self):
    """ Calls for a time tick on all rooms.
    """
    for room in self.__rooms:
      room.tick()    
