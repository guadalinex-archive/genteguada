import dMVC.model
import GG.utils
import room
import player
import ggsession
import item
import book
import penguin
import door
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
    self.loadData()
    thread.start_new(self.start,())
      
  # self.__rooms
  
  def getRooms(self):
    """ Returns the rooms list.
    """
    return self.__rooms
  
  def setRooms(self, rooms):
    """ Sets a new rooms list.
    rooms: new rooms list.
    """
    if self.__rooms <> rooms:
      self.__rooms = rooms
      self.triggerEvent('rooms', rooms=rooms)
      return True
    return False
  
  def addRoom(self, room):
    """ Adds a new room to the rooms list.
    room: new room.
    """
    if not room in self.__rooms:
      self.__rooms.add(room)
      self.triggerEvent('addRoom', room=room)
      return True
    return False
    
  def removeRoom(self, room):
    """ Remove a room from the rooms list.
    room: room to be removed.
    """
    if room in self.__rooms:
      self.__rooms.remove(room)
      self.triggerEvent('removeRoom', room=room)
      return True
    return False
    
  # self.__players
  
  def getPlayers(self):
    """ Returns the players list.
    """
    return self.__players
  
  def setPlayers(self, players):
    """ Sets a new players list.
    players: new players list.
    """
    if self.__players <> players:
      self.__players = players
      self.triggerEvent('players', players=players)
      return True
    return False
    
  def addPlayer(self, player):
    """ Adds a new player to the players list.
    player: new player.
    """
    if not player in self.__players:
      self.__players.add(player)
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
    for player in self.__players:
      if player.checkUser(username, password):
        session = ggsession.GGSession(player)
        #player.setSession(session)
        return session 
    return None

  def loadData(self):
    """ Llamadas provisionales. Se eliminaran cuando se defina como se cargan los datos.
    """
    self.createRoom(GG.utils.BG_FULL, "habitacion 1")
    self.createRoom(GG.utils.BG_FULL2, "habitacion 2")
    myPinguin = GG.model.penguin.GGPenguin(GG.utils.PENGUIN_SPRITE, [50, 55], [0, 0, 6], [55, 8], GG.utils.PENGUIN_SPRITE, 1, "Pinguino Misterioso")
    myBook = GG.model.book.GGBook(GG.utils.BOOK_SPRITE, [50, 35], [3, 0, 6], [60, -13], GG.utils.BOOK_SPRITE, 1, "Guia de Telefonos")
    self.__rooms[0].addItem(myPinguin)    
    self.__rooms[0].addItem(myBook)    
    self.__rooms[0].addItem(GG.model.door.GGDoor(GG.utils.DOOR_DOWN_SPRITE, [60, 141], [3, 0, 0], [58, 95], "down", self.__rooms[1]))    
    self.__rooms[1].addItem(GG.model.door.GGDoor(GG.utils.DOOR_DOWN_SPRITE, [60, 141], [5, 0, 0], [58, 95], "down", self.__rooms[0]))    
    if self.createPlayer(GG.utils.NINO_SPRITE, GG.utils.NINO_SZ, [0, 0, 0], [2*GG.utils.CHAR_SZ[0]-35, GG.utils.CHAR_SZ[1]], "pepe", "1234"):
      self.insertItemIntoRoom(self.__players[0], self.__rooms[0], 1)
        
  def createRoom(self, spriteFull, label):
    """ Creates a new room.
    spriteFull: sprite used to paint the room floor.
    """
    self.__rooms.append(room.GGRoom(spriteFull, label))
      
  def createPlayer(self, sprite, size, position, offset, username, password):
    """ Creates a new player.
    sprite: sprite used to paint the player.
    size: sprite size.
    position: sprite position.
    offset: user sprite offset on screen.
    username: player user name.
    password: player password.
    """
    for pl in self.__players:
      if pl.checkUser(username, password):
        return False
    self.__players.append(player.GGPlayer(sprite, size, position, offset, username, password))
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
          #if player.checkUser(item.getUsername(), item.getPassword()):
          return
        self.__players.append(item)
    
  def removeItem(self, item, isPlayer):
    """ Removes an item.
    item: existing item.
    player: flag used to check it the item is a player or not.
    """
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
