import dMVC.model
import GG.utils
import GG.model.room
import GG.model.player
import GG.model.ggsession
import GG.model.inventory_item
import GG.model.mp3_lobby
import GG.model.penguin_lobby
import GG.model.penguin_room3
import GG.model.book_lobby
import GG.model.door_lobby
import GG.model.door_room3b
import GG.model.door_room3c1
import GG.model.door_room3c2
import GG.model.web_cube
import GG.model.golden_key_room2
import thread
import time
import os
import stat

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
      if player.checkUser(username, password):# and player.getRoom() == None:
        player.changeRoom(self.getEntryRoom(), player.getPosition())
        session = GG.model.ggsession.GGSession(player, self)
        self.__sessions.append(session)
        return True, session 
    return False, "No se pudo autenticar el usuario"

  def logout(self, session):
    self.__sessions.remove(session)

  def __loadData(self):
    """ Llamadas provisionales. Se eliminaran cuando se defina como se cargan los datos.
    """
    
    # PLAYERS
    nino = GG.model.player.GGPlayer(GG.utils.NINO_PATH, [1, 0, 1], [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], "pepe", "1234")
    nina = GG.model.player.GGPlayer(GG.utils.NINA_PATH, [3, 0, 3], [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], "pepe2", "12345")
    self.__createPlayer(nino)
    self.__createPlayer(nina)
    
    # ROOMS
    room1 = self.__createRoom(GG.utils.TILE_STONE, "habitacion 1", [8, 8])
    room2 = self.__createRoom(GG.utils.TILE_STONE, "habitacion 2", [8, 8])
    room3 = self.__createRoom(GG.utils.TILE_STONE, "habitacion 3", [8, 8])
    room4 = self.__createRoom(GG.utils.TILE_STONE, "habitacion 4", [8, 8])
    room5 = self.__createRoom(GG.utils.TILE_STONE, "habitacion 5", [8, 8])

    # ROOM 1
    myDoor1 = GG.model.door_lobby.GGDoorLobby(GG.utils.DOOR_DOWN_SPRITE, [6, 0, 0], [20, 62], [6, 0, 7], room2)
    myPenguin = GG.model.penguin_lobby.GGPenguinLobby(GG.utils.PENGUIN_SPRITE, [1, 0, 6], [20, -20], "Andatuz")
    myMp3 = GG.model.mp3_lobby.GGMP3Lobby(GG.utils.MP3_SPRITE, [4, 0, 4], [15, -45], GG.utils.MP3_SPRITE, "Reproductor de MP3", 5, room1)
    myBook = GG.model.book_lobby.GGBookLobby(GG.utils.BOOK_SPRITE, [2, 0, 2], [20, -40], GG.utils.BOOK_SPRITE, "Guia de Telefonos")
    
    room1.addItemFromVoid(GG.model.web_cube.GGWebCube(GG.utils.PUZZLECUBEBLUE_SPRITE, [5, 0, 0], [55, 43], "http://forja.guadalinex.org/repositorio/projects/genteguada/"), [5, 0, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem(GG.utils.PUZZLECUBE_SPRITE, [1, 0, 0], [55, 43]), [1, 0, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem(GG.utils.PUZZLECUBE_SPRITE, [2, 0, 0], [55, 43]), [2, 0, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem(GG.utils.PUZZLECUBE_SPRITE, [3, 0, 0], [55, 43]), [3, 0, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem(GG.utils.PUZZLECUBE_SPRITE, [4, 0, 0], [55, 43]), [4, 0, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem(GG.utils.PUZZLECUBE_SPRITE, [7, 0, 0], [55, 43]), [7, 0, 0])
    for z in range(0, room2.size[1]):
      room1.addItemFromVoid(GG.model.room_item.GGRoomItem(GG.utils.PUZZLECUBE_SPRITE, [0, 0, z], [55, 43]), [0, 0, z])
    
    room1.addItemFromVoid(myPenguin, myPenguin.getPosition())    
    room1.addItemFromVoid(myBook, myBook.getPosition())
    room1.addItemFromVoid(myMp3, myMp3.getPosition())
    room1.addItemFromVoid(myDoor1, myDoor1.getPosition())    
    
    # ROOM 2
    myDoor2 = GG.model.door_lobby.GGDoorLobby(GG.utils.DOOR_DOWN_SPRITE, [6, 0, 0], [20, 62], [6, 0, 7], room3)
    myGoldenKeyRoom2 = GG.model.golden_key_room2.GGGoldenKeyRoom2(GG.utils.KEY_SPRITE, [1, 0, 1], [20, -40], GG.utils.KEY_SPRITE, "llave dorada")    
    
    wallOffset = [25, 10]
    for z in range(0, room2.size[1]):
      room2.addItemFromVoid(GG.model.room_item.GGRoomItem("wall_right_TEMP.png", [0, 0, z], wallOffset), [0, 0, z])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("wall_right_TEMP.png", [5, 0, 0], wallOffset), [5, 0, 0])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("wall_right_TEMP.png", [5, 0, 1], wallOffset), [5, 0, 1])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("wall_right_TEMP.png", [5, 0, 2], wallOffset), [5, 0, 2])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("wall_right_TEMP.png", [5, 0, 5], wallOffset), [5, 0, 5])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("wall_right_TEMP.png", [5, 0, 6], wallOffset), [5, 0, 6])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("wall_right_TEMP.png", [5, 0, 7], wallOffset), [5, 0, 7])
        
    room2.addItemFromVoid(myDoor2, myDoor2.getPosition())
    room2.addItemFromVoid(myGoldenKeyRoom2, myGoldenKeyRoom2.getPosition())
    
    # ROOM 3
    myDoor3B = GG.model.door_room3b.GGDoorRoom3B(GG.utils.DOOR_DOWN_SPRITE, [0, 0, 5], [20, 62], [7, 0, 3], room4)
    myDoor3C1 = GG.model.door_room3c1.GGDoorRoom3C1(GG.utils.DOOR_DOWN_SPRITE, [3, 0, 0], [20, 62], [3, 0, 7], room5)
    myDoor3C2 = GG.model.door_room3c2.GGDoorRoom3C2(GG.utils.DOOR_DOWN_SPRITE, [4, 0, 0], [20, 62], [4, 0, 7], room5)
    myPenguinRoom3 = GG.model.penguin_room3.GGPenguinRoom3(GG.utils.PENGUIN_SPRITE, [1, 0, 6], [20, -20], "Andatuz")
    
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("black_tile.tga", [6, 0, 6], [65, -23]), [6, 0, 6])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem(GG.utils.BRICKCUBE_SPRITE, [3, 0, 3], [55, 43]), [3, 0, 3])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem(GG.utils.BRICKCUBE_SPRITE, [3, 0, 4], [55, 43]), [3, 0, 4])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem(GG.utils.BRICKCUBE_SPRITE, [4, 0, 3], [55, 43]), [4, 0, 3])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem(GG.utils.BRICKCUBE_SPRITE, [4, 0, 4], [55, 43]), [4, 0, 4])
    
    room3.addItemFromVoid(myPenguinRoom3, myPenguinRoom3.getPosition())
    room3.addItemFromVoid(myDoor3B, myDoor3B.getPosition())    
    room3.addItemFromVoid(myDoor3C1, myDoor3C1.getPosition())    
    room3.addItemFromVoid(myDoor3C2, myDoor3C2.getPosition())    
    
    # ROOM 4
    
    # ROOM 5
    


    
    #prueba para seleccionar un jugador y poder hablar con el en privado y hacer intercambio de objetos
    #room1.addItem(nina,[4,0,5])

    demoPlayerPath = GG.utils.NINO_PATH
    for i in range(100):
      if demoPlayerPath == GG.utils.NINO_PATH:
        demoPlayerPath = GG.utils.NINA_PATH
      else:
        demoPlayerPath = GG.utils.NINO_PATH
      demoPlayer = GG.model.player.GGPlayer(demoPlayerPath, [1, 0, 1], [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], "user"+str(i), "user"+str(i))
      self.__createPlayer(demoPlayer)
    

  def __createRoom(self, spriteFull, label, size):
    """ Creates a new room.
    spriteFull: sprite used to paint the room floor.
    """
    newRoom = GG.model.room.GGRoom(spriteFull, label, size)
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
    time_time = time.time
    time_sleep = time.sleep
    delay = GG.utils.TICK_DELAY
    try:
        while True:
            time_sleep(delay)
            self.__tick(time_time()*1000)
    except:
        dMVC.utils.logger.exception('Exception in __start')
    
  def __tick(self, now):
    """ Calls for a time tick on all rooms.
    """
    for room in self.__rooms:
      room.tick(now)    

  def getResource(self, img, date):
    """ Returns a resource path.
    img: resource path.
    date: current date.
    """
    sendFile = False
    if not date:
      sendFile = True
    else:
      pathFile = os.path.join(GG.utils.DATA_PATH, img)
      dateFile = os.stat(pathFile)[stat.ST_MTIME]
      if dateFile > date:
        sendFile = True
    if sendFile:
      imgFile = open(os.path.join(GG.utils.DATA_PATH, img), "rb")
      imgData = imgFile.read()
      imgFile.close()
      return imgData
    else:
      return None

  def uploadFile(self, fileName, fileData):
    name = fileName[0] + "_" + str(int(time.time())) + fileName[1]
    try:
      f = open(os.path.join(GG.utils.DATA_PATH, name), "wb")
      f.write(fileData)
      f.close()
    except:
      return None
    return name
    
