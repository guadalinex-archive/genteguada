# -*- coding: iso-8859-15 -*-
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
import random

import GG.avatargenerator.generator

# ======================= GGSYSTEM ===========================
PENGUIN_SPRITE_RIGHT = "andatuz_right.png"
PENGUIN_SPRITE_DOWN = "andatuz_down.png"
PENGUIN_SPRITE_BOTTOMRIGHT = "andatuz_bottomright.png"
ADVERTISEMENT_LEFT = "advertisementLeft.png"
ADVERTISEMENT_MIDDLE = "advertisementMiddle.png"
ADVERTISEMENT_RIGHT = "advertisementRight.png"
KEY_GOLDEN = "golden_key.png"
GIFT = "gift.png"
BOX_HEAVY = "heavy_box.png"
BEAM_WOODEN = "wooden_beam.png"
PAPERMONEY_5 = "5Guadapuntos.png"
PAPERMONEY_10 = "10Guadapuntos.png"
PAPERMONEY_50 = "50Guadapuntos.png"
TREE = "tree.png"
COLUMN_STONE = "stone_column.png"
BEAM_WOODEN = "wooden_beam.png"
FENCE_UP = "fence_up.png"
FENCE_LEFT = "fence_left.png"
WALL_UP = "wall_up.png"
WALL_LEFT = "wall_left.png"
WALL_UP_GRAFFITI = "wall_up_graffiti.png"
YARD_LAMP_UP = "yard_lamp_up.png"
YARD_LAMP_LEFT = "yard_lamp_left.png"
YARD_UP = "yard_up.png"
YARD_LEFT = "yard_left.png"
YARD_CORNER = "yard_corner.png"
HEDGE = "hedge.png"
DOOR_GARDEN = "garden_door.png"
DOOR_WOODEN = "wooden_door.png"
DOOR_WOODEN_A = "wooden_door_a.png"
DOOR_WOODEN_B = "wooden_door_b.png"
DOOR_AMORED = "armored_door_left.png"

WAREHOUSE_UP = ["warehouseWallUp01.png", "warehouseWallUp02.png"]
WAREHOUSE_LEFT = ["warehouseWallLeft01.png", "warehouseWallLeft02.png"]
WAREHOUSE_CORNER = "warehouseWallCorner.png"

SKYLINES_UP = ["skylineWallUp01.png", "skylineWallUp02.png", "skylineWallUp03.png", "skylineWallUp04.png"]
SKYLINES_LEFT = ["skylineWallLeft01.png", "skylineWallLeft02.png"]
SKYLINE_CORNER = "skylineCorner.png"

TILE_MYSTCYRCLE = "mystCircle.png"
TILE_MYSTCYRCLE_CASTLE01 = "mystCircleCastle01.png"
TILES_GRASS = ["grass01.png", "grass02.png", "grass03.png", "grass04.png"]
TILES_PAVINGSTONE = ["pavingStone01.png", "pavingStone02.png", "pavingStone03.png"]
TILES_PAVINGSTONEWITHGRASS = ["pavingStoneWithGrass01.png", "pavingStoneWithGrass02.png", "pavingStoneWithGrass03.png"]
TILES_SMALLSTONES = ["smallStones01.png", "smallStones02.png", "smallStones03.png"]
TILES_ARROWS = ["upArrow.png", "downArrow.png", "leftArrow.png", "rightArrow.png"]
TILES_CASTLE1 = ["castle01.png"]
TILES_CASTLE2 = ["castle02.png"]
# ======================= GGSYSTEM ===========================

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
      if player.checkUser(username, password) and player.getRoom() == None:
        player.changeRoom(self.getEntryRoom(), self.getEntryRoom().getNearestEmptyCell([1, 1]))
        session = GG.model.ggsession.GGSession(player, self)
        self.__sessions.append(session)
        return True, session 
    return False, "No se pudo autentificar el usuario"

  def logout(self, session):
    """ Logs out a player and ends his session.
    session: player's session.
    """  
    #session.getPlayer().getRoom().removeItem(session.getPlayer())  
    self.__sessions.remove(session)

  def __loadData(self):
    """ Llamadas provisionales. Se eliminaran cuando se defina como se cargan los datos.
    """
    
    # PLAYERS
    nino = GG.model.player.GGPlayer(GG.utils.NINO_PATH, [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], [0, -20], "pepe", "1234", "", True)
    nina = GG.model.player.GGPlayer(GG.utils.NINA_PATH, [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], [0, 0], "pepa", "12345", "", False)
    user0 = GG.model.player.GGPlayer(GG.utils.NINA_PATH, [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], [0, 0], "user0", "user0", "", False)
    self.__createPlayer(nino)
    self.__createPlayer(nina)
    
    nino.addContactTEST(user0)
    
    penguinLobbyText = "¡Bienvenido a GenteGuada! Soy Andatuz, y te guiaré a lo largo de este tutorial para conocer GenteGuada. Puedes explorar por este jardín para aprender a moverte. Cuando estés listo, ve a la puerta y ábrela."
    penguinRoom3Text = "Para abrir el portón de madera deberás depositar algo pesado sobre ese resorte. Quizá puedas hallar cajas en el almacén, pero la puerta está cerrada. Me pregunto dónde estará la llave que abre la puerta..."
    penguinTradeText = "Vaya, veo que me traes un regalo. Toma, déjame cambiártelo por esta nueva camiseta." 
    
    # ROOMS
    room1 = self.createRoom(TILES_GRASS, "habitacion 1", [8, 8], 12)
    room2 = self.createRoom(TILES_PAVINGSTONEWITHGRASS, "habitacion 2", [8, 8], 8)
    room3 = self.createRoom(TILES_PAVINGSTONE, "habitacion 3", [8, 8], 8)
    room4 = self.createRoom(TILES_SMALLSTONES, "habitacion 4", [8, 8], 8)
    room5 = self.createRoom(TILES_CASTLE1, "habitacion 5", [8, 8], 8)
    room6 = self.createRoom(TILES_PAVINGSTONEWITHGRASS, "habitacion 6", [8, 8], 8)
    room3.setSpecialTile([2, 0, 1], "tiles/pressed.png")
    room3.setSpecialTile([5, 0, 1], "tiles/pressed.png")
    
    penguinRightOffset = [30, 0]

    # ROOM 1
    myDoor1 = GG.model.teleport.GGDoor("furniture/" + DOOR_GARDEN, [25, 2], [0, 0], [6, 6], room2, "puerta lobby")
    myPenguin = GG.model.penguin.GGPenguinTalker("furniture/" + PENGUIN_SPRITE_RIGHT, penguinRightOffset, [0, 0], "Andatuz", penguinLobbyText)
    myBox = GG.model.box_heavy.GGBoxHeavy("furniture/" + BOX_HEAVY, [26, -10], [0, -12], "Caja pesada")
    myBox2 = GG.model.box_heavy.GGBoxHeavy("furniture/" + BOX_HEAVY, [26, -10], [0, -12], "Caja pesada 2")
    myMoney5 = GG.model.pickable_item.PaperMoney("furniture/" + PAPERMONEY_5, [14, -25], [0, -10], "Billete de 5", 5)
    myMoney10 = GG.model.pickable_item.PaperMoney("furniture/" + PAPERMONEY_10, [14, -25], [0, -10], "Billete de 10", 10)
    myMoney50 = GG.model.pickable_item.PaperMoney("furniture/" + PAPERMONEY_50, [14, -25], [0, -10], "Billete de 50", 50)

    fenceOffset = [25, -15]
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + HEDGE, [55, 13], [0, -26]), [0, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + HEDGE, [55, 13], [0, -26]), [6, 3])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + HEDGE, [55, 13], [0, -26]), [2, 4])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + HEDGE, [55, 13], [0, -26]), [6, 7])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + FENCE_UP, fenceOffset, [0, 0]), [1, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + FENCE_UP, fenceOffset, [0, 0]), [2, 0])
    pannel1 = GG.model.web_item.GGWebPannel("furniture/" + ADVERTISEMENT_LEFT, [60, 140], [0, 0], "http://www.opensourceworldconference.com/", "Panel web")
    pannel2 = GG.model.web_item.GGWebPannel("furniture/" + ADVERTISEMENT_MIDDLE, [40, 170], [0, 0], "http://www.opensourceworldconference.com/", "Panel web")
    pannel3 = GG.model.web_item.GGWebPannel("furniture/" + ADVERTISEMENT_RIGHT, [20, 200], [0, 0], "http://www.opensourceworldconference.com/", "Panel web")
    pannel1.addPannels(pannel2, pannel3)
    pannel2.addPannels(pannel1, pannel3)
    pannel3.addPannels(pannel1, pannel2)
    room1.addItemFromVoid(pannel1, [3, 0])
    room1.addItemFromVoid(pannel2, [4, 0])
    room1.addItemFromVoid(pannel3, [5, 0])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + FENCE_UP, fenceOffset, [0, 0]), [7, 0])
    for z in range(1, room2.size[1]-1):
      room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + FENCE_LEFT, fenceOffset, [0, 0]), [0, z])
    room1.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + TREE, [100, 150], [0, 0]), [0, 7])
    
    room1.addItemFromVoid(myDoor1, [6, 0])    
    room1.addItemFromVoid(myPenguin, [1, 6])    
    room1.addItemFromVoid(myBox, [6, 6])
    room1.addItemFromVoid(myBox2, [7, 6])
    room1.addItemFromVoid(myMoney5, [3, 6])
    room1.addItemFromVoid(myMoney10, [4, 4])
    room1.addItemFromVoid(myMoney50, [4, 2])
    
    # ROOM 2
    wallOffset = [35, -10]
    wallOffset2 = [55, 0]
    wallOffset3 = [20, 0]
    columnOffset = [13, 15]
    myDoor2A = GG.model.teleport.GGDoor("tiles/" + TILES_ARROWS[1], GG.utils.FLOOR_SHIFT, [0, 0], [6, 1], room1, "puerta room2b")
    myDoor2B = GG.model.teleport.GGDoor("furniture/" + DOOR_WOODEN, [28, 23], [0, 0], [6, 6], room3, "puerta room2a")
    myDoor2C = GG.model.teleport.GGDoor("furniture/" + WALL_LEFT, wallOffset2, [0, 0], [6, 6], room6, "puerta room2c")
    myPenguinShirt = GG.model.penguin.GGPenguinTrade("furniture/" + PENGUIN_SPRITE_BOTTOMRIGHT, penguinRightOffset, [0, 0], "Andatuz Shirt", penguinTradeText, "Regalo")
    room2.addItemFromVoid(myPenguinShirt, [1, 1])

    myGoldenKeyRoom2 = GG.model.giver_npc.GGGiverNpc("furniture/" + KEY_GOLDEN, [15, -30], [0, 0], "furniture/" + KEY_GOLDEN, "Llave Dorada")
    
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, columnOffset, [0, 0]), [0, 0])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, columnOffset, [0, 0]), [5, 0])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, columnOffset, [0, 0]), [3, 3])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, columnOffset, [0, 0]), [5, 5])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, columnOffset, [0, 0]), [3, 5])
    
    for z in range(1, 6):
      room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_LEFT, wallOffset2, [0, 0]), [0, z])    
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_LEFT, wallOffset2, [0, 0]), [0, 7])
    
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_LEFT, wallOffset, [0, 0]), [3, 2])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_LEFT, wallOffset, [0, 0]), [3, 4])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_LEFT, wallOffset, [0, 0]), [3, 6])
    
    room2.addItemFromVoid(GG.model.web_item.GGWebItem("furniture/" + WALL_UP_GRAFFITI, wallOffset3, [0, 0], "http://forja.guadalinex.org/repositorio/projects/genteguada/", "Graffitti GenteGuada"), [1, 0, 0])

    for x in range(2, 5):
      room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_UP, wallOffset3, [0, 0]), [x, 0])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_UP, wallOffset3, [0, 0]), [7, 0])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_UP, wallOffset, [0, 0]), [2, 3])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_UP, wallOffset, [0, 0]), [4, 5])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_LEFT, wallOffset, [0, 0]), [5, 1])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_LEFT, wallOffset, [0, 0]), [5, 2])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_LEFT, wallOffset, [0, 0]), [5, 6])
    room2.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WALL_LEFT, wallOffset, [0, 0]), [5, 7])
        
    room2.addItemFromVoid(myDoor2A, [6, 7])
    room2.addItemFromVoid(myDoor2B, [6, 0])
    room2.addItemFromVoid(myDoor2C, [0, 6])
    room2.addItemFromVoid(myGoldenKeyRoom2, [4, 6])
    
    # ROOM 3
    tiles = [[2, 2], [5, 1]]
    myDoor3A = GG.model.teleport.GGDoor("tiles/" + TILES_ARROWS[1], GG.utils.FLOOR_SHIFT, [0, 0], [6, 1], room2, "puerta room3a")
    myDoor3B = GG.model.teleport.GGDoorWithKey("furniture/" + DOOR_AMORED, [35, 25], [0, 0], [6, 5], room4, "puerta room3b", "Llave Dorada")
    myDoor3C1 = GG.model.teleport.GGDoorPressedTiles("furniture/" + DOOR_WOODEN_A, [24, 37], [0, 0], [3, 6], room5, "puerta room3c1", tiles)
    myDoor3C2 = GG.model.teleport.GGDoorPressedTiles("furniture/" + DOOR_WOODEN_B, [24, 55], [0, 0], [3, 6], room5, "puerta room3c2", tiles)
    myPenguinRoom3 = GG.model.penguin.GGPenguinTalker("furniture/" + PENGUIN_SPRITE_RIGHT, penguinRightOffset, [0, 0], "Andatuz", penguinRoom3Text)

    wallOffset1 = [25, 50]
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + YARD_UP, wallOffset1, [0, 0]), [1, 0])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + YARD_LAMP_UP, wallOffset1, [0, 0]), [2, 0])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + YARD_LAMP_UP, wallOffset1, [0, 0]), [5, 0])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + YARD_UP, wallOffset1, [0, 0]), [6, 0])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + YARD_UP, wallOffset1, [0, 0]), [7, 0])
    
    wallOffset2 = [45, 50]
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + YARD_CORNER, [55, 45], [0, 0]), [0, 0])
    for z in range(1, 5):
      if z % 2 == 0:
        room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + YARD_LEFT, wallOffset2, [30, 0]), [0, z])
      else:
        room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + YARD_LAMP_LEFT, wallOffset2, [0, 0]), [0, z])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + YARD_LEFT, wallOffset2, [0, 0]), [0, 6])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + YARD_LAMP_LEFT, wallOffset2, [0, 0]), [0, 7])

    fountainVertOffset = 10
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/font_topleft.png", [46, -35 + fountainVertOffset], [0, 0]), [3, 3])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/font_topright.png", [55, -35 + fountainVertOffset], [0, 0]), [4, 3])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/font_bottomleft.png", [4, -34 + fountainVertOffset], [0, 0]), [3, 4])
    room3.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/font_bottomright.png", [50, -30 + fountainVertOffset], [0, 0]), [4, 4])
    room3.addItemFromVoid(myDoor3A, [6, 7])    
    room3.addItemFromVoid(myDoor3B, [0, 5])    
    room3.addItemFromVoid(myDoor3C1, [3, 0])    
    room3.addItemFromVoid(myDoor3C2, [4, 0])    
    room3.addItemFromVoid(myPenguinRoom3, [1, 6])
    
    # ROOM 4
    myDoor4A = GG.model.teleport.GGDoorWithKey("furniture/" + DOOR_AMORED, [17, 15], [0, 0], [1, 5], room3, "puerta room4a", "Llave Dorada")
    room4.addItemFromVoid(myDoor4A, [7, 5])    
    
    wallOffset = [35, 33]
    room4.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + WAREHOUSE_CORNER, wallOffset, [0, 0]), [0, 0])
    for z in range(1, 8):
      image = "furniture/" + WAREHOUSE_LEFT[random.randint(0, len(WAREHOUSE_LEFT)-1)]
      room4.addItemFromVoid(GG.model.room_item.GGRoomItem(image, wallOffset, [0, 0]), [0, z])
    for x in range(1, 8):
      image = "furniture/" + WAREHOUSE_UP[random.randint(0, len(WAREHOUSE_UP)-1)]
      room4.addItemFromVoid(GG.model.room_item.GGRoomItem(image, wallOffset, [0, 0]), [x, 0])
    
    myBox1 = GG.model.box_heavy.GGBoxHeavy("furniture/" + BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 1")
    myBox2 = GG.model.box_heavy.GGBoxHeavy("furniture/" + BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 2")
    myBox3 = GG.model.box_heavy.GGBoxHeavy("furniture/" + BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 3")
    myBox4 = GG.model.box_heavy.GGBoxHeavy("furniture/" + BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 4")
    myBox5 = GG.model.box_heavy.GGBoxHeavy("furniture/" + BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 5")
    myBox6 = GG.model.box_heavy.GGBoxHeavy("furniture/" + BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 6")
    beamOffset = [57, 142]
    room4.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + BEAM_WOODEN, beamOffset, [0, 0]), [1, 1])
    room4.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + BEAM_WOODEN, beamOffset, [0, 0]), [1, 6])
    room4.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + BEAM_WOODEN, beamOffset, [0, 0]), [6, 1])
    room4.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + BEAM_WOODEN, beamOffset, [0, 0]), [6, 6])
    room4.addItemFromVoid(myBox1, [1, 4])
    room4.addItemFromVoid(myBox2, [4, 6])
    room4.addItemFromVoid(myBox3, [6, 2])
    room4.addItemFromVoid(myBox4, [4, 1])
    room4.addItemFromVoid(myBox5, [3, 2])
    room4.addItemFromVoid(myBox6, [7, 3])
    
    # ROOM 5
    myDoor5A1 = GG.model.teleport.GGDoor("tiles/" + TILES_ARROWS[1], GG.utils.FLOOR_SHIFT, [0, 0], [3, 1], room3, "puerta room5a")
    myDoor5A2 = GG.model.teleport.GGDoor("tiles/" + TILES_ARROWS[1], GG.utils.FLOOR_SHIFT, [0, 0], [4, 1], room3, "puerta room5a")
    myDoor5B1 = GG.model.teleport.GGDoorRoom5b("tiles/" + TILE_MYSTCYRCLE_CASTLE01, GG.utils.FLOOR_SHIFT, [0, 0], [3, 7], room1, "puerta room5b")
    myDoor5B2 = GG.model.teleport.GGDoorRoom5b("tiles/" + TILE_MYSTCYRCLE_CASTLE01, GG.utils.FLOOR_SHIFT, [0, 0], [4, 7], room1, "puerta room5b")
    myPenguinQuiz = GG.model.penguin.GGPenguinQuiz("furniture/" + PENGUIN_SPRITE_RIGHT, penguinRightOffset, [0, 0], "Andatuz Quiz", GG.utils.QUESTIONS_PATH)
    columnOffset = [13, 15]
    for z in range(0, 8):
      room5.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, columnOffset, [0, 0]), [0, z])
      room5.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, columnOffset, [0, 0]), [1, z])
      room5.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, columnOffset, [0, 0]), [6, z])
      room5.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, columnOffset, [0, 0]), [7, z])
    
    room5.addItemFromVoid(myDoor5A1, [3, 7])    
    room5.addItemFromVoid(myDoor5A2, [4, 7])    
    room5.addItemFromVoid(myDoor5B1, [3, 0])    
    room5.addItemFromVoid(myDoor5B2, [4, 0])    
    room5.addItemFromVoid(myPenguinQuiz, [2, 3])
    
    # ROOM 6
    myDoor6A = GG.model.teleport.GGDoor("tiles/" + TILES_ARROWS[3], GG.utils.FLOOR_SHIFT, [0, 0], [1, 6], room2, "puerta room6a")
    myGift1 = GG.model.giver_npc.GGGiverNpc("furniture/" + GIFT, [15, -30], [0, 0], "furniture/" + GIFT, "Regalo")
    
    wallOffset = [35, 40]
    room6.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + SKYLINE_CORNER, wallOffset, [0, 0]), [0, 0])
    for z in range(1, 8):
      image = "furniture/" + SKYLINES_LEFT[random.randint(0, len(SKYLINES_LEFT)-1)]
      room6.addItemFromVoid(GG.model.room_item.GGRoomItem(image, wallOffset, [0, 0]), [0, z])
    for x in range(1, 8):
      image = "furniture/" + SKYLINES_UP[random.randint(0, len(SKYLINES_LEFT)-1)]
      room6.addItemFromVoid(GG.model.room_item.GGRoomItem(image, wallOffset, [0, 0]), [x, 0])
    room6.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, [13, 15], [0, 0]), [2, 3])
    room6.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, [13, 15], [0, 0]), [5, 2])
    room6.addItemFromVoid(GG.model.room_item.GGRoomItem("furniture/" + COLUMN_STONE, [13, 15], [0, 0]), [4, 6])
    
    room6.addItemFromVoid(myDoor6A, [7, 6])
    room6.addItemFromVoid(myGift1, [4, 4])
        
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
    
  def createRoom(self, spriteFull, label, size, maxUsers):
    """ Creates a new room.
    spriteFull: sprite used to paint the room floor.
    label: room label.
    size: room size.
    maxUsers: max users per room.
    """
    if self.getRoom(label):
      return None  
    newRoom = GG.model.room.GGRoom(spriteFull, label, size, maxUsers)
    self.__rooms.append(newRoom)
    return newRoom

  def deleteRoom(self, label):
    """ Deletes a room.
    label: room label.
    """  
    for room in self.__rooms:
      if room.label == label:
        chosenRoom = room
      else:
        itemsList = room.getItems()
        for item in itemsList:
          if isinstance(item, GG.model.teleport.GGTeleport):
            if item.getDestinationRoom().label == label: 
              item.setDestinationRoom(None)
    self.__rooms.remove(chosenRoom)
    del chosenRoom
    chosenRoom = None
    return True
      
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
    isPlayer: flag used to check it the item is a player or not.
    """
    if room.addItem(item):
      if isPlayer:
        if item in self.__players:
          return
        self.__players.append(item)
    
  def removeItem(self, item, isPlayer):
    """ Removes an item.
    item: existing item.
    isPlayer: flag used to check it the item is a player or not.
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
    now: timestamp.
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
    """ Uploads a new file to the system.
    """  
    name = fileName[0] + "_" + str(int(time.time())) + fileName[1]
    try:
      upFile = open(os.path.join(GG.utils.DATA_PATH, name), "wb")
      upFile.write(fileData)
      upFile.close()
    except:
      return None
    return name

  def changeAvatarConfiguration(self, configuration, player, nameMask):
    """ Changes the avatar configuration.
    configuration: new config.
    player: player to change the configuration for.
    nameMask: mask filename.
    """  
    thread.start_new(self.__changeAvatarConfiguration, (configuration, player, nameMask))

  def __changeAvatarConfiguration(self, configuration, player, nameMask):
    """ Changes the avatar configuration.
    configuration: new config.
    player: player to change the configuration for.
    nameMask: mask filename.
    """  
    if nameMask:
      maskFile = open(os.path.join(GG.utils.DATA_PATH, nameMask), "rb")
      data = maskFile.read()
      maskFile.close()
      self.__avatarGeneratorHandler.copyImageMask(nameMask, data)
      maskFile = open(os.path.join(GG.utils.DATA_PATH, "avatars/masks", player.username+".png"),"wb")
      maskFile.write(data)
      maskFile.close()
      os.remove(os.path.join(GG.utils.DATA_PATH, nameMask))
    else:
      if os.path.isfile(os.path.join(GG.utils.DATA_PATH, "avatars/masks", player.username+".png")):
        os.remove(os.path.join(GG.utils.DATA_PATH, "avatars/masks", player.username+".png"))
    execCommand = self.__avatarGeneratorHandler.executeCommand(configuration, player, nameMask)
    if execCommand:
      images = self.__avatarGeneratorHandler.getImages(player)
      timestamp = self.__copyImages(images, player)
      self.__avatarGeneratorHandler.deleteImages(player)
      player.setAvatarConfiguration(configuration, timestamp)

  def __copyImages(self, images, player):
    """ Copies images for a given player.
    images: images to copy.
    player: given player.
    """  
    #dir = "/home/jmariscal/proyectos/genteguada/src/gg/GG/data/avatars"
    dirImage = GG.utils.DATA_PATH + "/avatars/"+player.username
    if os.path.isdir(dirImage):
      for fileName in os.listdir(dirImage):
        os.remove(os.path.join(dir, fileName))
    else:
      os.mkdir(dirImage)
    timestamp = int(time.time())
    for image in images.keys():
      f = open(os.path.join(dir, image + "_" + str(timestamp)), "wb")
      f.write(images[image])
      f.close()
    return timestamp

  def getRoom(self, label):
    """ Returns a selected room.
    label: room's label.
    """  
    for room in self.__rooms:
      if room.label == label:
        return room
    return None

  def existsRoom(self, name):
    """ Checks if a room exists.
    name: room label.
    """  
    for room in self.__rooms:
      if room.label == name:
        return room  
    return None

  def getRoomLabels(self):
    """ Returns a list containing all room labels.
    """  
    listLabels = []
    for room in self.__rooms:
      listLabels.append(room.label)
    return listLabels  

  def getAvatarImages(self, avatar):
    dirPlayerImages = os.path.join(GG.utils.DATA_PATH, avatar.imagePath)
    files = {}
    files["path"] = avatar.imagePath
    files["avatar"] = avatar
    for playerImage in os.listdir(dirPlayerImages):
      if os.path.isfile(os.path.join(dirPlayerImages, playerImage)):
        filePlayerImage = open(os.path.join(dirPlayerImages, playerImage), "rb")
        files[playerImage] = filePlayerImage.read()
        filePlayerImage.close()
    return files
    
  def getPlayersList(self):
    """ Returns the active players list.
    """  
    pList = []  
    for session in self.__sessions:
      pList.append(session.getPlayer().username)
    return pList

  def getSpecificPlayer(self, name):
    """ Returns a specific player.
    name: player name.
    """  
    for player in self.__players:
      if player.getName() == name:
        return player
    return None  

  def newBroadcastMessage(self, line, player):
    for room in self.__rooms:
      room.newChatMessage(line, player, 3)    
