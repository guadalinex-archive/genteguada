import dMVC.model
import GG.utils
import GG.model.room
import GG.model.player
import GG.model.ggsession
import GG.model.inventory_item
import GG.model.giver_npc
import GG.model.box_heavy
import GG.model.penguin
import GG.model.teleport
import GG.model.web_item
import GG.model.pickable_item
import thread
import time
import os
import stat
import commands
import random

import GG.avatargenerator.generator
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
    self.__avatarGeneratorHandler = GG.avatargenerator.generator.AvatarGenerator()
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
        player.changeRoom(self.getEntryRoom(), self.getEntryRoom().getNearestEmptyCell([1, 0, 1]))
        #player.changeRoom(self.getEntryRoom(), self.getEntryRoom().getNearestEmptyCell([5, 0, 5]))
        session = GG.model.ggsession.GGSession(player, self)
        self.__sessions.append(session)
        return True, session 
    return False, "No se pudo autenticar el usuario"

  def logout(self, session):
    #session.getPlayer().getRoom().removeItem(session.getPlayer())  
    self.__sessions.remove(session)

  def __loadData(self):
    """ Llamadas provisionales. Se eliminaran cuando se defina como se cargan los datos.
    """
    
    # PLAYERS
    nino = GG.model.player.GGPlayer(GG.utils.NINO_PATH, [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], [0, -20], "pepe", "1234", "", False)
    nina = GG.model.player.GGPlayer(GG.utils.NINA_PATH, [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], [0, 0], "pepe2", "12345", "", False)
    user0 = GG.model.player.GGPlayer(GG.utils.NINA_PATH, [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], [0, 0], "user0", "user0", "", False)
    self.__createPlayer(nino)
    self.__createPlayer(nina)
    
    #nino.addContactTEST(nina)
    nino.addContactTEST(user0)
    #nina.addContactTEST(nino)
    #nina.addContactTEST(user0)
    
    # ROOMS
    room1 = self.__createRoom(GG.utils.TILES_GRASS, "habitacion 1", [8, 8], 12)
    room2 = self.__createRoom(GG.utils.TILES_PAVINGSTONEWITHGRASS, "habitacion 2", [8, 8], 8)
    room3 = self.__createRoom(GG.utils.TILES_PAVINGSTONE, "habitacion 3", [8, 8], 8)
    room4 = self.__createRoom(GG.utils.TILES_SMALLSTONES, "habitacion 4", [8, 8], 8)
    room5 = self.__createRoom(GG.utils.TILES_CASTLE1, "habitacion 5", [8, 8], 8)
    room6 = self.__createRoom(GG.utils.TILES_PAVINGSTONEWITHGRASS, "habitacion 6", [8, 8], 8)
    #room7 = self.__createRoom(GG.utils.TILES_PAVINGSTONE, "habitacion 7", [8, 8])
    room3.setSpecialTile([2, 0, 1], "tiles/pressed.png")
    room3.setSpecialTile([5, 0, 1], "tiles/pressed.png")
    
    penguinRightOffset = [30, 0]

    # ROOM 1
    myDoor1 = GG.model.teleport.GGDoorLobby("furniture/" + GG.utils.DOOR_GARDEN, [25, 2], [0, 0], [6, 0, 6], room2, "puerta lobby")
    myPenguin = GG.model.penguin.GGPenguinLobby(GG.utils.PENGUIN_SPRITE_RIGHT, penguinRightOffset, [0, 0], "Andatuz")
    myBox = GG.model.box_heavy.GGBoxHeavy("furniture/" + GG.utils.BOX_HEAVY, [26, -10], [0, -10], "Caja pesada", 10, room1)
    myBox2 = GG.model.box_heavy.GGBoxHeavy("furniture/" + GG.utils.BOX_HEAVY, [26, -10], [0, -10], "Caja pesada 2", 10, room1)
    myMoney5 = GG.model.pickable_item.PaperMoney("furniture/" + GG.utils.PAPERMONEY_5, [14, -25], [0, -10], "Billete de 5", 5)
    myMoney10 = GG.model.pickable_item.PaperMoney("furniture/" + GG.utils.PAPERMONEY_10, [14, -25], [0, -10], "Billete de 10", 10)
    myMoney50 = GG.model.pickable_item.PaperMoney("furniture/" + GG.utils.PAPERMONEY_50, [14, -25], [0, -10], "Billete de 50", 50)

    fenceOffset = [25, -15]
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.HEDGE, [55, 13], [0, 0]), [0, 0, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.HEDGE, [55, 13], [0, 0]), [6, 0, 3])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.HEDGE, [55, 13], [0, 0]), [2, 0, 4])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.HEDGE, [55, 13], [0, 0]), [6, 0, 7])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.FENCE_UP, fenceOffset, [0, 0]), [1, 0, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.FENCE_UP, fenceOffset, [0, 0]), [2, 0, 0])
    room1.addItemFromVoid(GG.model.web_item.GGWebPannel("furniture/" + GG.utils.ADVERTISEMENT_LEFT, [60, 140], [0, 0], "http://www.opensourceworldconference.com/", "Panel web"), [3, 0, 0])
    room1.addItemFromVoid(GG.model.web_item.GGWebPannel("furniture/" + GG.utils.ADVERTISEMENT_MIDDLE, [40, 170], [0, 0], "http://www.opensourceworldconference.com/", "Panel web"), [4, 0, 0])
    room1.addItemFromVoid(GG.model.web_item.GGWebPannel("furniture/" + GG.utils.ADVERTISEMENT_RIGHT, [20, 200], [0, 0], "http://www.opensourceworldconference.com/", "Panel web"), [5, 0, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.FENCE_UP, fenceOffset, [0, 0]), [7, 0, 0])
    for z in range(1, room2.size[1]-1):
      room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.FENCE_LEFT, fenceOffset, [0, 0]), [0, 0, z])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.TREE, [100, 150], [0, 0]), [0, 0, 7])
    
    room1.addItemFromVoid(myDoor1, [6, 0, 0])    
    room1.addItemFromVoid(myPenguin, [1, 0, 6])    
    #room1.addItemFromVoid(myBox, [5, 0, 5])
    #room1.addItemFromVoid(myBox2, [7, 0, 5])
    room1.addItemFromVoid(myBox, [6, 0, 6])
    room1.addItemFromVoid(myBox2, [7, 0, 6])
    room1.addItemFromVoid(myMoney5, [3, 0, 6])
    room1.addItemFromVoid(myMoney10, [4, 0, 4])
    room1.addItemFromVoid(myMoney50, [4, 0, 2])
    

    # ROOM 2
    wallOffset = [35, -10]
    columnOffset = [13, 15]
    myDoor2A = GG.model.teleport.GGDoorLobby("tiles/" + GG.utils.TILES_ARROWS[1], GG.utils.FLOOR_SHIFT, [0, 0], [6, 0, 1], room1, "puerta room2b")
    myDoor2B = GG.model.teleport.GGDoorLobby("furniture/" + GG.utils.DOOR_WOODEN, [30, 22], [0, 0], [6, 0, 6], room3, "puerta room2a")
    myDoor2C = GG.model.teleport.GGDoorSecretRoom("furniture/" + GG.utils.WALL_LEFT, wallOffset, [0, 0], [6, 0, 6], room6, "puerta room2c")
    myPenguinShirt = GG.model.penguin.GGPenguinRoom5Shirt(GG.utils.PENGUIN_SPRITE_BOTTOMRIGHT, penguinRightOffset, [0, 0], "Andatuz Shirt")
    room2.addItemFromVoid(myPenguinShirt, [1, 0, 1])

    myGoldenKeyRoom2 = GG.model.giver_npc.GGPersistentKey("furniture/" + GG.utils.KEY_GOLDEN, [15, -30], [0, 0], "furniture/" + GG.utils.KEY_GOLDEN, "Llave Dorada")
    
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, columnOffset, [0, 0]), [0, 0, 0])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, columnOffset, [0, 0]), [5, 0, 0])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, columnOffset, [0, 0]), [3, 0, 3])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, columnOffset, [0, 0]), [5, 0, 5])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, columnOffset, [0, 0]), [3, 0, 5])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, columnOffset, [0, 0]), [1, 0, 5])
    
    for z in range(1, 6):
      room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_LEFT, wallOffset, [0, 0]), [0, 0, z])    
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_LEFT, wallOffset, [0, 0]), [0, 0, 7])
    
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_LEFT, wallOffset, [0, 0]), [3, 0, 2])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_LEFT, wallOffset, [0, 0]), [3, 0, 4])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_LEFT, wallOffset, [0, 0]), [3, 0, 6])
    
    #room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_UP_GRAFFITI, wallOffset, [0, 0]), [1, 0, 0])
    room2.addItemFromVoid(GG.model.web_item.GGWebItem("furniture/" + GG.utils.WALL_UP_GRAFFITI, wallOffset, [0, 0], "http://forja.guadalinex.org/repositorio/projects/genteguada/", "Graffitti GenteGuada"), [1, 0, 0])

    for x in range(2, 5):
      room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_UP, wallOffset, [0, 0]), [x, 0, 0])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_UP, wallOffset, [0, 0]), [7, 0, 0])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_UP, wallOffset, [0, 0]), [2, 0, 3])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_UP, wallOffset, [0, 0]), [4, 0, 5])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_LEFT, wallOffset, [0, 0]), [5, 0, 1])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_LEFT, wallOffset, [0, 0]), [5, 0, 2])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_LEFT, wallOffset, [0, 0]), [5, 0, 6])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WALL_LEFT, wallOffset, [0, 0]), [5, 0, 7])
        
    room2.addItemFromVoid(myDoor2A, [6, 0, 7])
    room2.addItemFromVoid(myDoor2B, [6, 0, 0])
    room2.addItemFromVoid(myDoor2C,[0, 0, 6])
    room2.addItemFromVoid(myGoldenKeyRoom2, [4, 0, 6])
    
    # ROOM 3
    myDoor3A = GG.model.teleport.GGDoorLobby("tiles/" + GG.utils.TILES_ARROWS[1], GG.utils.FLOOR_SHIFT, [0, 0], [6, 0, 1], room2, "puerta room3a")
    myDoor3B = GG.model.teleport.GGDoorRoom3B("furniture/" + GG.utils.DOOR_AMORED, [35, 25], [0, 0], [6, 0, 5], room4, "puerta room3b")
    myDoor3C1 = GG.model.teleport.GGDoorRoom3C1("furniture/" + GG.utils.DOOR_WOODEN_A, [24, 37], [0, 0], [3, 0, 6], room5, "puerta room3c")
    myDoor3C2 = GG.model.teleport.GGDoorRoom3C2("furniture/" + GG.utils.DOOR_WOODEN_B, [24, 55], [0, 0], [4, 0, 6], room5, "puerta room3c")
    myPenguinRoom3 = GG.model.penguin.GGPenguinRoom3(GG.utils.PENGUIN_SPRITE_RIGHT, penguinRightOffset, [0, 0], "Andatuz")

    #wallOffset = [35, -10]
    wallOffset1 = [25, 50]
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.YARD_UP, wallOffset1, [0, 0]), [1, 0, 0])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.YARD_LAMP_UP, wallOffset1, [0, 0]), [2, 0, 0])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.YARD_LAMP_UP, wallOffset1, [0, 0]), [5, 0, 0])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.YARD_UP, wallOffset1, [0, 0]), [6, 0, 0])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.YARD_UP, wallOffset1, [0, 0]), [7, 0, 0])
    
    wallOffset2 = [45, 50]
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.YARD_CORNER, [55, 45], [0, 0]), [0, 0, 0])
    for z in range(1, 5):
      if z % 2 == 0:
        room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.YARD_LEFT, wallOffset2, [30, 0]), [0, 0, z])
      else:
        room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.YARD_LAMP_LEFT, wallOffset2, [0, 0]), [0, 0, z])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.YARD_LEFT, wallOffset2, [0, 0]), [0, 0, 6])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.YARD_LAMP_LEFT, wallOffset2, [0, 0]), [0, 0, 7])

    fountainVertOffset = 10
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/font_topleft.png", [46, -35 + fountainVertOffset], [0, 0]), [3, 0, 3])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/font_topright.png", [55, -35 + fountainVertOffset], [0, 0]), [4, 0, 3])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/font_bottomleft.png", [4, -34 + fountainVertOffset], [0, 0]), [3, 0, 4])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/font_bottomright.png", [50, -30 + fountainVertOffset], [0, 0]), [4, 0, 4])
    """
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, [13, 15]), [3, 0, 3])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, [13, 15]), [3, 0, 4])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, [13, 15]), [4, 0, 3])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, [13, 15]), [4, 0, 4])
    """
    room3.addItemFromVoid(myDoor3A, [6, 0, 7])    
    room3.addItemFromVoid(myDoor3B, [0, 0, 5])    
    room3.addItemFromVoid(myDoor3C1, [3, 0, 0])    
    room3.addItemFromVoid(myDoor3C2, [4, 0, 0])    
    room3.addItemFromVoid(myPenguinRoom3, [1, 0, 6])
    
    # ROOM 4
    myDoor4A = GG.model.teleport.GGDoorRoom3B("furniture/" + GG.utils.DOOR_AMORED, [17, 15], [0, 0], [1, 0, 5], room3, "puerta room4a")
    room4.addItemFromVoid(myDoor4A, [7, 0, 5])    
    
    wallOffset = [35, 33]
    room4.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.WAREHOUSE_CORNER, wallOffset, [0, 0]), [0, 0, 0])
    for z in range(1, 8):
      image = "furniture/" + GG.utils.WAREHOUSE_LEFT[random.randint(0,len(GG.utils.WAREHOUSE_LEFT)-1)]
      room4.addItemFromVoid(GG.model.room_item.GGRoomItem(image, wallOffset, [0, 0]), [0, 0, z])
    for x in range(1, 8):
      image = "furniture/" + GG.utils.WAREHOUSE_UP[random.randint(0,len(GG.utils.WAREHOUSE_UP)-1)]
      room4.addItemFromVoid(GG.model.room_item.GGRoomItem(image, wallOffset, [0, 0]), [x, 0, 0])
    
    #pesas: [2, 0, 1] [3, 0, 1][4, 0, 1][5, 0, 1][3, 0, 2][4, 0, 2]
    #cajas: [1, 0, 4] [4, 0, 6][6, 0, 2]
    
    """
    myKilo1 = GG.model.kilo.GGKilo("furniture/" + GG.utils.KILOGRAMME, [32, -17], [0, 0], "furniture/" + GG.utils.KILOGRAMME_INV, "Pesa")
    myKilo2 = GG.model.kilo.GGKilo("furniture/" + GG.utils.KILOGRAMME, [32, -17], [0, 0], "furniture/" + GG.utils.KILOGRAMME_INV, "Pesa")
    myKilo3 = GG.model.kilo.GGKilo("furniture/" + GG.utils.KILOGRAMME, [32, -17], [0, 0], "furniture/" + GG.utils.KILOGRAMME_INV, "Pesa")
    myKilo4 = GG.model.kilo.GGKilo("furniture/" + GG.utils.KILOGRAMME, [32, -17], [0, 0], "furniture/" + GG.utils.KILOGRAMME_INV, "Pesa")
    myKilo5 = GG.model.kilo.GGKilo("furniture/" + GG.utils.KILOGRAMME, [32, -17], [0, 0], "furniture/" + GG.utils.KILOGRAMME_INV, "Pesa")
    myKilo6 = GG.model.kilo.GGKilo("furniture/" + GG.utils.KILOGRAMME, [32, -17], [0, 0], "furniture/" + GG.utils.KILOGRAMME_INV, "Pesa")
    room4.addItemFromVoid(myKilo1, [2, 0, 1])
    room4.addItemFromVoid(myKilo2, [3, 0, 1])
    room4.addItemFromVoid(myKilo3, [4, 0, 1])
    room4.addItemFromVoid(myKilo4, [5, 0, 1])
    room4.addItemFromVoid(myKilo5, [3, 0, 2])
    room4.addItemFromVoid(myKilo6, [4, 0, 2])
    """
    
    myBox1 = GG.model.box_heavy.GGBoxHeavy("furniture/" + GG.utils.BOX_HEAVY, [26, -10], [0, 0], "Caja pesada 1", 10, room4)
    myBox2 = GG.model.box_heavy.GGBoxHeavy("furniture/" + GG.utils.BOX_HEAVY, [26, -10], [0, 0], "Caja pesada 2", 10, room4)
    myBox3 = GG.model.box_heavy.GGBoxHeavy("furniture/" + GG.utils.BOX_HEAVY, [26, -10], [0, 0], "Caja pesada 3", 10, room4)
    myBox4 = GG.model.box_heavy.GGBoxHeavy("furniture/" + GG.utils.BOX_HEAVY, [26, -10], [0, 0], "Caja pesada 4", 10, room4)
    myBox5 = GG.model.box_heavy.GGBoxHeavy("furniture/" + GG.utils.BOX_HEAVY, [26, -10], [0, 0], "Caja pesada 5", 10, room4)
    myBox6 = GG.model.box_heavy.GGBoxHeavy("furniture/" + GG.utils.BOX_HEAVY, [26, -10], [0, 0], "Caja pesada 6", 10, room4)
    beamOffset = [57, 142]
    room4.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.BEAM_WOODEN, beamOffset, [0, 0]), [1, 0, 1])
    room4.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.BEAM_WOODEN, beamOffset, [0, 0]), [1, 0, 6])
    room4.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.BEAM_WOODEN, beamOffset, [0, 0]), [6, 0, 1])
    room4.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.BEAM_WOODEN, beamOffset, [0, 0]), [6, 0, 6])
    room4.addItemFromVoid(myBox1, [1, 0, 4])
    room4.addItemFromVoid(myBox2, [4, 0, 6])
    room4.addItemFromVoid(myBox3, [6, 0, 2])
    room4.addItemFromVoid(myBox4, [4, 0, 1])
    room4.addItemFromVoid(myBox5, [3, 0, 2])
    room4.addItemFromVoid(myBox6, [7, 0, 3])
    
    # ROOM 5
    myDoor5A1 = GG.model.teleport.GGDoorLobby("tiles/" + GG.utils.TILES_ARROWS[1], GG.utils.FLOOR_SHIFT, [0, 0], [3, 0, 1], room3, "puerta room5a")
    myDoor5A2 = GG.model.teleport.GGDoorLobby("tiles/" + GG.utils.TILES_ARROWS[1], GG.utils.FLOOR_SHIFT, [0, 0], [4, 0, 1], room3, "puerta room5a")
    myDoor5B1 = GG.model.teleport.GGDoorRoom5b("tiles/" + GG.utils.TILE_MYSTCYRCLE_CASTLE01, GG.utils.FLOOR_SHIFT, [0, 0], [3, 0, 7], room1, "puerta room5b")
    myDoor5B2 = GG.model.teleport.GGDoorRoom5b("tiles/" + GG.utils.TILE_MYSTCYRCLE_CASTLE01, GG.utils.FLOOR_SHIFT, [0, 0], [4, 0, 7], room1, "puerta room5b")
    myPenguinQuiz = GG.model.penguin.GGPenguinQuiz(GG.utils.PENGUIN_SPRITE_RIGHT, penguinRightOffset, [0, 0], "Andatuz Quiz", ["q1", "q10"])
    columnOffset = [13, 15]
    for z in range(0, 8):
      room5.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, columnOffset, [0, 0]), [0, 0, z])
      room5.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, columnOffset, [0, 0]), [1, 0, z])
      room5.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, columnOffset, [0, 0]), [6, 0, z])
      room5.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, columnOffset, [0, 0]), [7, 0, z])
    
    room5.addItemFromVoid(myDoor5A1, [3, 0, 7])    
    room5.addItemFromVoid(myDoor5A2, [4, 0, 7])    
    room5.addItemFromVoid(myDoor5B1, [3, 0, 0])    
    room5.addItemFromVoid(myDoor5B2, [4, 0, 0])    
    room5.addItemFromVoid(myPenguinQuiz, [2, 0, 3])
    
    # ROOM 6
    myDoor6A = GG.model.teleport.GGDoorLobby("tiles/" + GG.utils.TILES_ARROWS[3], GG.utils.FLOOR_SHIFT, [0, 0], [1, 0, 6], room2, "puerta room6a")
    myGift1 = GG.model.giver_npc.GGGift("furniture/" + GG.utils.GIFT, [15, -30], [0, 0], "furniture/" + GG.utils.GIFT, "Regalo")
    
    wallOffset = [35, 40]
    room6.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.SKYLINE_CORNER, wallOffset, [0, 0]), [0, 0, 0])
    for z in range(1, 8):
      image = "furniture/" + GG.utils.SKYLINES_LEFT[random.randint(0,len(GG.utils.SKYLINES_LEFT)-1)]
      room6.addItemFromVoid(GG.model.room_item.GGRoomItem(image, wallOffset, [0, 0]), [0, 0, z])
    for x in range(1, 8):
      image = "furniture/" + GG.utils.SKYLINES_UP[random.randint(0,len(GG.utils.SKYLINES_LEFT)-1)]
      room6.addItemFromVoid(GG.model.room_item.GGRoomItem(image, wallOffset, [0, 0]), [x, 0, 0])
    room6.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, [13, 15], [0, 0]), [2, 0, 3])
    room6.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, [13, 15], [0, 0]), [5, 0, 2])
    room6.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + GG.utils.COLUMN_STONE, [13, 15], [0, 0]), [4, 0, 6])
    
    room6.addItemFromVoid(myDoor6A, [7, 0, 6])
    room6.addItemFromVoid(myGift1, [4, 0, 4])
        
    #prueba para seleccionar un jugador y poder hablar con el en privado y hacer intercambio de objetos
    #room1.addItemFromVoid(nina,[1,0,2])

    demoPlayerPath = GG.utils.NINO_PATH
    for i in range(100):
      if demoPlayerPath == GG.utils.NINO_PATH:
        demoPlayerPath = GG.utils.NINA_PATH
      else:
        demoPlayerPath = GG.utils.NINO_PATH
      demoPlayer = GG.model.player.GGPlayer(demoPlayerPath, [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], [0, 0], "user"+str(i), "user"+str(i), "", False)
      self.__createPlayer(demoPlayer)
    

  def __createRoom(self, spriteFull, label, size, maxUsers):
    """ Creates a new room.
    spriteFull: sprite used to paint the room floor.
    """
    newRoom = GG.model.room.GGRoom(spriteFull, label, size, maxUsers)
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

  def changeAvatarConfiguration(self, configuration, player, nameMask):
    thread.start_new(self.__changeAvatarConfiguration, (configuration, player, nameMask))

  def __changeAvatarConfiguration(self, configuration, player, nameMask):
    if nameMask:
      f = open(os.path.join(GG.utils.DATA_PATH, nameMask), "rb")
      data = f.read()
      f.close()
      self.__avatarGeneratorHandler.copyImageMask(nameMask, data)
      f = open(os.path.join(GG.utils.DATA_PATH, "avatars/masks", player.username+".png"),"wb")
      f.write(data)
      f.close()
      os.remove(os.path.join(GG.utils.DATA_PATH, nameMask))
    else:
      if os.path.isfile(os.path.join(GG.utils.DATA_PATH, "avatars/masks", player.username+".png")):
        os.remove(os.path.join(GG.utils.DATA_PATH, "avatars/masks", player.username+".png"))
    player.setAvatarConfiguration(configuration, None)
    return 
    #execCommand = self.__avatarGeneratorHandler.executeCommand(configuration, player, nameMask)
    if execCommand:
      images = self.__avatarGeneratorHandler.getImages(player)
      timestamp = self.__copyImages(images, player)
      self.__avatarGeneratorHandler.deleteImages(player)
      player.setAvatarConfiguration(configuration, timestamp)

  def __copyImages(self,images, player):
    #dir = "/home/jmariscal/proyectos/genteguada/src/gg/GG/data/avatars"
    dir = GG.utils.DATA_PATH+"/avatars/"+player.username
    if os.path.isdir(dir):
      for file in os.listdir(dir):
        os.remove(os.path.join(dir,file))
    else:
      os.mkdir(dir)
    timestamp = int(time.time())
    for image in images.keys():
      f = open(os.path.join(dir,image+"_"+str(timestamp)),"wb")
      f.write(images[image])
      f.close()
    return timestamp
