import dMVC.model
import GG.utils
import GG.model.room
import GG.model.player
import GG.model.ggsession
import GG.model.item
import GG.model.pickable_item
import GG.model.temp_pickable_item
import GG.model.giver_npc
import GG.model.teleporter
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
    self.__loadData()
    thread.start_new(self.__start, ())
     
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

  def __loadData(self):
    """ Llamadas provisionales. Se eliminaran cuando se defina como se cargan los datos.
    """
    #key = GG.model.pickable_item.GGPickableItem(GG.utils.KEY_SPRITE, [0, 0, 0], [20, -40], GG.utils.KEY_SPRITE, "llave dorada")
    room1 = self.__createRoom(GG.utils.TILE_STONE, "habitacion 1")
    room2 = self.__createRoom(GG.utils.TILE_WATER, "habitacion 2")
    
    dict = {"object": GG.model.pickable_item.GGPickableItem, "params": [GG.utils.KEY_SPRITE, [0, 0, 0], [20, -40], GG.utils.KEY_SPRITE, "llave dorada"]}
    
    myPenguin = GG.model.giver_npc.GGGiverNPC(GG.utils.PENGUIN_SPRITE, [1, 0, 6], [20, -20], "Pinguino Misterioso", [], dict)
    myMp3 = GG.model.temp_pickable_item.GGTempPickableItem(GG.utils.MP3_SPRITE, [6, 0, 6], [15, -45], GG.utils.MP3_SPRITE, "Reproductor de MP3", 30)
    myBook = GG.model.pickable_item.GGPickableItem(GG.utils.BOOK_SPRITE, [3, 0, 6], [20, -40], GG.utils.BOOK_SPRITE, "Guia de Telefonos")
    myDoor1 = GG.model.teleporter.GGTeleporter(GG.utils.DOOR_DOWN_SPRITE, [3, 0, 1], [3, 0, 7], [3, 0, 0], [20, 62], room2, ["llave dorada"])
    myDoor2 = GG.model.teleporter.GGTeleporter(GG.utils.DOOR_DOWN_SPRITE, [3, 0, 1], [3, 0, 7], [3, 0, 0], [20, 62], room1, [])
    nino = GG.model.player.GGPlayer(GG.utils.NINO_PATH, [1, 0, 1], [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], "pepe", "1234")
    nina = GG.model.player.GGPlayer(GG.utils.NINA_PATH, [2, 0, 2], [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], "pepe2", "12345")
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [0, 0, 0], [55, 43]), [0, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [1, 0, 0], [55, 43]), [1, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [2, 0, 0], [55, 43]), [2, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [4, 0, 0], [55, 43]), [4, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [5, 0, 0], [55, 43]), [5, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [6, 0, 0], [55, 43]), [6, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [7, 0, 0], [55, 43]), [7, 0, 0])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [0, 0, 1], [55, 43]), [0, 0, 1])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [0, 0, 2], [55, 43]), [0, 0, 2])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [0, 0, 4], [55, 43]), [0, 0, 4])
    room1.addItem(GG.model.item.GGItem(GG.utils.CUBE_STONE, [0, 0, 6], [55, 43]), [0, 0, 6])
    room1.addItem(myPenguin, myPenguin.getPosition())    
    room1.addItem(myBook, myBook.getPosition())
    room1.addItem(myMp3, myMp3.getPosition())
    room1.addItem(myDoor1, myDoor1.getPosition())    
    room2.addItem(myDoor2, myDoor2.getPosition())
    self.__createPlayer(nino)
    self.__createPlayer(nina)
        
  def __createRoom(self, spriteFull, label):
    """ Creates a new room.
    spriteFull: sprite used to paint the room floor.
    """
    newRoom = GG.model.room.GGRoom(spriteFull, label)
    self.__rooms.append(newRoom)
    return newRoom
      
  def __createPlayer(self, player):
    """ Creates a new player.
    player: new player.
    """
    if player in self.__players:
      return False
    self.__players.append(player)
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
    
  def __start(self):
    """ Starts the program.
    """
    while True:
      time.sleep(GG.utils.TICK_DELAY)
      self.__tick()
    
  def __tick(self):
    """ Calls for a time tick on all rooms.
    """
    for room in self.__rooms:
      room.tick()    
