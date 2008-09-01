# -*- coding: utf-8 -*-

import os
import player
import penguin
import box_heavy
import room_item
import web_item
import teleport
import pickable_item
import giver_npc
import random
import GG.utils

FURNITURE_PATH = "furniture"
TILES_GRASS = ["grass01.png", "grass02.png", "grass03.png", "grass04.png"]
TILES_PAVINGSTONE = ["pavingStone01.png", "pavingStone02.png", "pavingStone03.png"]
TILES_PAVINGSTONEWITHGRASS = ["pavingStoneWithGrass01.png", "pavingStoneWithGrass02.png", "pavingStoneWithGrass03.png"]
TILES_SMALLSTONES = ["smallStones01.png", "smallStones02.png", "smallStones03.png"]
TILES_CASTLE1 = ["castle01.png"]
TILES_CASTLE2 = ["castle02.png"]
TILES_ARROWS = ["upArrow.png", "downArrow.png", "leftArrow.png", "rightArrow.png"]
DOOR_GARDEN = os.path.join(FURNITURE_PATH, "garden_door.png")
PENGUIN_SPRITE_RIGHT = os.path.join(FURNITURE_PATH, "andatuz_right.png")
BOX_HEAVY = os.path.join(FURNITURE_PATH, "heavy_box.png")
PAPERMONEY_5 = os.path.join(FURNITURE_PATH, "5Guadapuntos.png")
PAPERMONEY_10 = os.path.join(FURNITURE_PATH, "10Guadapuntos.png")
PAPERMONEY_50 = os.path.join(FURNITURE_PATH, "50Guadapuntos.png")
HEDGE = os.path.join(FURNITURE_PATH, "hedge.png")
FENCE_UP = os.path.join(FURNITURE_PATH, "fence_up.png")
ADVERTISEMENT_LEFT = os.path.join(FURNITURE_PATH, "advertisementLeft.png")
ADVERTISEMENT_MIDDLE = os.path.join(FURNITURE_PATH, "advertisementMiddle.png")
ADVERTISEMENT_RIGHT = os.path.join(FURNITURE_PATH, "advertisementRight.png")
FENCE_LEFT = os.path.join(FURNITURE_PATH, "fence_left.png")
TREE = os.path.join(FURNITURE_PATH, "tree.png")
TILE_ARROW_BACK = os.path.join(GG.utils.TILE, TILES_ARROWS[1]) 
TILE_ARROW_DOWN = os.path.join(GG.utils.TILE, TILES_ARROWS[3]) 
DOOR_WOODEN = os.path.join(FURNITURE_PATH, "wooden_door.png")
DOOR_WOODEN_A = os.path.join(FURNITURE_PATH, "wooden_door_a.png")
DOOR_WOODEN_B = os.path.join(FURNITURE_PATH, "wooden_door_b.png")
WALL_LEFT = os.path.join(FURNITURE_PATH, "wall_left.png")
PENGUIN_SPRITE_BOTTOMRIGHT = os.path.join(FURNITURE_PATH, "andatuz_bottomright.png")
KEY_GOLDEN = os.path.join(FURNITURE_PATH, "golden_key.png")
COLUMN_STONE = os.path.join(FURNITURE_PATH, "stone_column.png")
WALL_UP_GRAFFITI = os.path.join(FURNITURE_PATH, "wall_up_graffiti.png")
WALL_UP = os.path.join(FURNITURE_PATH, "wall_up.png")
DOOR_AMORED =  os.path.join(FURNITURE_PATH, "armored_door_left.png")
YARD_UP = os.path.join(FURNITURE_PATH, "yard_up.png")
YARD_LAMP_UP = os.path.join(FURNITURE_PATH, "yard_lamp_up.png")
YARD_CORNER = os.path.join(FURNITURE_PATH, "yard_corner.png")
YARD_LEFT = os.path.join(FURNITURE_PATH, "yard_left.png")
YARD_LAMP_LEFT = os.path.join(FURNITURE_PATH, "yard_lamp_left.png")
FONT_TOPLEFT = os.path.join(FURNITURE_PATH, "font_topleft.png")
FONT_TOPRIGHT = os.path.join(FURNITURE_PATH, "font_topright.png") 
FONT_BOTTOMLEFT = os.path.join(FURNITURE_PATH, "font_bottomleft.png") 
FONT_BOTTOMRIGHT = os.path.join(FURNITURE_PATH, "font_bottomright.png") 
WAREHOUSE_CORNER = os.path.join(FURNITURE_PATH, "warehouseWallCorner.png")
WAREHOUSE_UP = [os.path.join(FURNITURE_PATH, "warehouseWallUp01.png"), os.path.join(FURNITURE_PATH, "warehouseWallUp02.png")]
WAREHOUSE_LEFT = [os.path.join(FURNITURE_PATH, "warehouseWallLeft01.png"), os.path.join(FURNITURE_PATH, "warehouseWallLeft02.png")]
BEAM_WOODEN = os.path.join(FURNITURE_PATH, "wooden_beam.png")
TILE_MYSTCYRCLE_CASTLE01 = os.path.join(GG.utils.TILE, "mystCircleCastle01.png")
GIFT = os.path.join(FURNITURE_PATH, "gift.png")
SKYLINE_CORNER =  os.path.join(FURNITURE_PATH, "skylineCorner.png")
SKYLINES_UP = [os.path.join(FURNITURE_PATH, "skylineWallUp01.png"), os.path.join(FURNITURE_PATH, "skylineWallUp02.png"), os.path.join(FURNITURE_PATH, "skylineWallUp03.png"), os.path.join(FURNITURE_PATH, "skylineWallUp04.png")]
SKYLINES_LEFT = [os.path.join(FURNITURE_PATH, "skylineWallLeft01.png"), os.path.join(FURNITURE_PATH, "skylineWallLeft02.png")]

class CreateWorld:

  def __init__(self, system):
    print "creando el mundo"
    self.__system = system

  def create(self):
    self.__createPlayers()
    self.__createRooms()
    self.__decorateRoom1()
    self.__decorateRoom2()
    self.__decorateRoom3()
    self.__decorateRoom4()
    self.__decorateRoom5()
    self.__decorateRoom6()

  def __createPlayers(self):
    nino = player.GGPlayer(GG.utils.NINO_PATH, [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], [0, -20], "pepe", "1234", "", True)
    nina = player.GGPlayer(GG.utils.NINA_PATH, [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], [0, -20], "pepa", "12345", "", False)
    self.__system.createPlayer(nino)
    self.__system.createPlayer(nina)
    demoPlayerPath = GG.utils.NINO_PATH
    for i in range(100):
      if demoPlayerPath == GG.utils.NINO_PATH:
        demoPlayerPath = GG.utils.NINA_PATH
      else:
        demoPlayerPath = GG.utils.NINO_PATH
      demoPlayer = player.GGPlayer(demoPlayerPath, [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30], [0, 0], "user"+str(i), "user"+str(i), "", False)
      self.__system.createPlayer(demoPlayer)

  def __createRooms(self):
    self.__room1 = self.__system.createRoom(TILES_GRASS, "habitacion 1", [8, 8], 12)
    self.__room2 = self.__system.createRoom(TILES_PAVINGSTONEWITHGRASS, "habitacion 2", [8, 8], 8)
    self.__room3 = self.__system.createRoom(TILES_PAVINGSTONE, "habitacion 3", [8, 8], 8)
    self.__room4 = self.__system.createRoom(TILES_SMALLSTONES, "habitacion 4", [8, 8], 8)
    self.__room5 = self.__system.createRoom(TILES_CASTLE1, "habitacion 5", [8, 8], 8)
    self.__room6 = self.__system.createRoom(TILES_PAVINGSTONEWITHGRASS, "habitacion 6", [8, 8], 8)

  def __decorateRoom1(self):
    myDoor1 = teleport.GGDoor(DOOR_GARDEN, [25, 2], [0, 0], [6, 6], self.__room2, "puerta lobby")
    self.__room1.addItemFromVoid(myDoor1, [6, 0])
    penguinRightOffset = [30, 0]
    penguinLobbyText = "¡Bienvenido a GenteGuada! Soy Andatuz, y te guiaré a lo largo de este tutorial para conocer GenteGuada. Puedes explorar por este jardín para aprender a moverte. Cuando estés listo, ve a la puerta y ábrela."
    myPenguin = penguin.GGPenguinTalker(PENGUIN_SPRITE_RIGHT, penguinRightOffset, [0, 0], "Andatuz", penguinLobbyText)
    self.__room1.addItemFromVoid(myPenguin, [1, 6])
    myBox = box_heavy.GGBoxHeavy(BOX_HEAVY, [26, -10], [0, -12], "Caja pesada")
    self.__room1.addItemFromVoid(myBox, [6, 6])
    myBox2 = box_heavy.GGBoxHeavy(BOX_HEAVY, [26, -10], [0, -12], "Caja pesada 2")
    self.__room1.addItemFromVoid(myBox2, [7, 6])
    myMoney5 = pickable_item.PaperMoney(PAPERMONEY_5, [14, -25], [0, -10], "Billete de 5", 5)
    self.__room1.addItemFromVoid(myMoney5, [3, 6])
    myMoney10 = pickable_item.PaperMoney(PAPERMONEY_10, [14, -25], [0, -10], "Billete de 10", 10)
    self.__room1.addItemFromVoid(myMoney10, [4, 4])
    myMoney50 = pickable_item.PaperMoney(PAPERMONEY_50, [14, -25], [0, -10], "Billete de 50", 50)
    self.__room1.addItemFromVoid(myMoney50, [4, 2])
    self.__room1.addItemFromVoid(room_item.GGRoomItem(HEDGE, [55, 13], [0, -26]), [0, 0])
    self.__room1.addItemFromVoid(room_item.GGRoomItem(HEDGE, [55, 13], [0, -26]), [6, 3])
    self.__room1.addItemFromVoid(room_item.GGRoomItem(HEDGE, [55, 13], [0, -26]), [2, 4])
    self.__room1.addItemFromVoid(room_item.GGRoomItem(HEDGE, [55, 13], [0, -26]), [6, 7])
    fenceOffset = [25, -15]
    self.__room1.addItemFromVoid(room_item.GGRoomItem(FENCE_UP, fenceOffset, [0, 0]), [1, 0])
    self.__room1.addItemFromVoid(room_item.GGRoomItem(FENCE_UP, fenceOffset, [0, 0]), [2, 0])
    pannel1 = web_item.GGWebPannel(ADVERTISEMENT_LEFT, [60, 140], [0, 0], "http://www.opensourceworldconference.com/", "Panel web")
    pannel2 = web_item.GGWebPannel(ADVERTISEMENT_MIDDLE, [40, 170], [0, 0], "http://www.opensourceworldconference.com/", "Panel web")
    pannel3 = web_item.GGWebPannel(ADVERTISEMENT_RIGHT, [20, 200], [0, 0], "http://www.opensourceworldconference.com/", "Panel web")
    pannel1.addPannels(pannel2, pannel3)
    pannel2.addPannels(pannel1, pannel3)
    pannel3.addPannels(pannel1, pannel2)
    self.__room1.addItemFromVoid(pannel1, [3, 0])
    self.__room1.addItemFromVoid(pannel2, [4, 0])
    self.__room1.addItemFromVoid(pannel3, [5, 0])
    self.__room1.addItemFromVoid(room_item.GGRoomItem(FENCE_UP, fenceOffset, [0, 0]), [7, 0])
    for z in range(1, self.__room1.size[1]-1):
      self.__room1.addItemFromVoid(room_item.GGRoomItem(FENCE_LEFT, fenceOffset, [0, 0]), [0, z])
    self.__room1.addItemFromVoid(room_item.GGRoomItem(TREE, [100, 150], [0, 0]), [0, 7])

  def __decorateRoom2(self):
    wallOffset = [35, -10]
    wallOffset2 = [55, 0]
    wallOffset3 = [20, 0]
    columnOffset = [13, 15]
    myDoor2A = teleport.GGDoor(TILE_ARROW_BACK, GG.utils.FLOOR_SHIFT, [0, 0], [6, 1], self.__room1, "puerta room2b")
    myDoor2B = teleport.GGDoor(DOOR_WOODEN, [28, 23], [0, 0], [6, 6], self.__room3, "puerta room2a")
    myDoor2C = teleport.GGDoor(WALL_LEFT, wallOffset2, [0, 0], [6, 6], self.__room6, "puerta room2c")
    penguinRightOffset = [30, 0]
    penguinTradeText = "Vaya, veo que me traes un regalo. Toma, déjame cambiártelo por esta nueva camiseta."
    myPenguinShirt = penguin.GGPenguinTrade(PENGUIN_SPRITE_BOTTOMRIGHT, penguinRightOffset, [0, 0], "Andatuz Shirt", penguinTradeText, "Regalo")
    self.__room2.addItemFromVoid(myPenguinShirt, [1, 1])
    myGoldenKeyRoom2 = giver_npc.GGGiverNpc(KEY_GOLDEN, [15, -30], [0, 0], KEY_GOLDEN, "Llave Dorada")
    self.__room2.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, columnOffset, [0, 0]), [0, 0])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, columnOffset, [0, 0]), [5, 0])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, columnOffset, [0, 0]), [3, 3])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, columnOffset, [0, 0]), [5, 5])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, columnOffset, [0, 0]), [3, 5])
    for z in range(1, 6):
      self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_LEFT, wallOffset2, [0, 0]), [0, z])    
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_LEFT, wallOffset2, [0, 0]), [0, 7])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_LEFT, wallOffset, [0, 0]), [3, 2])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_LEFT, wallOffset, [0, 0]), [3, 4])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_LEFT, wallOffset, [0, 0]), [3, 6])
    self.__room2.addItemFromVoid(web_item.GGWebItem(WALL_UP_GRAFFITI, wallOffset3, [0, 0], "http://forja.guadalinex.org/repositorio/projects/genteguada/", "Graffitti GenteGuada"), [1, 0, 0])
    for x in range(2, 5):
      self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_UP, wallOffset3, [0, 0]), [x, 0])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_UP, wallOffset3, [0, 0]), [7, 0])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_UP, wallOffset, [0, 0]), [2, 3])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_UP, wallOffset, [0, 0]), [4, 5])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_LEFT, wallOffset, [0, 0]), [5, 1])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_LEFT, wallOffset, [0, 0]), [5, 2])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_LEFT, wallOffset, [0, 0]), [5, 6])
    self.__room2.addItemFromVoid(room_item.GGRoomItem(WALL_LEFT, wallOffset, [0, 0]), [5, 7])
    self.__room2.addItemFromVoid(myDoor2A, [6, 7])
    self.__room2.addItemFromVoid(myDoor2B, [6, 0])
    self.__room2.addItemFromVoid(myDoor2C, [0, 6])
    self.__room2.addItemFromVoid(myGoldenKeyRoom2, [4, 6])

  def __decorateRoom3(self):
    self.__room3.setSpecialTile([2, 0, 1], "tiles/pressed.png")
    self.__room3.setSpecialTile([5, 0, 1], "tiles/pressed.png")
    tiles = [[2, 2], [5, 1]]
    myDoor3A = teleport.GGDoor(TILE_ARROW_BACK, GG.utils.FLOOR_SHIFT, [0, 0], [6, 1], self.__room2, "puerta room3a")
    myDoor3B = teleport.GGDoorWithKey(DOOR_AMORED, [35, 25], [0, 0], [6, 5], self.__room4, "puerta room3b", "Llave Dorada")
    myDoor3C1 = teleport.GGDoorPressedTiles(DOOR_WOODEN_A, [24, 37], [0, 0], [3, 6], self.__room5, "puerta room3c1", tiles)
    myDoor3C2 = teleport.GGDoorPressedTiles(DOOR_WOODEN_B, [24, 55], [0, 0], [3, 6], self.__room5, "puerta room3c2", tiles)
    penguinRightOffset = [30, 0]
    penguinRoom3Text = "Para abrir el portón de madera deberás depositar algo pesado sobre ese resorte. Quizá puedas hallar cajas en el almacén, pero la puerta está cerrada. Me pregunto dónde estará la llave que abre la puerta..."
    myPenguinRoom3 = penguin.GGPenguinTalker(PENGUIN_SPRITE_RIGHT, penguinRightOffset, [0, 0], "Andatuz", penguinRoom3Text)
    wallOffset1 = [25, 50]
    self.__room3.addItemFromVoid(room_item.GGRoomItem(YARD_UP, wallOffset1, [0, 0]), [1, 0])
    self.__room3.addItemFromVoid(room_item.GGRoomItem(YARD_LAMP_UP, wallOffset1, [0, 0]), [2, 0])
    self.__room3.addItemFromVoid(room_item.GGRoomItem(YARD_LAMP_UP, wallOffset1, [0, 0]), [5, 0])
    self.__room3.addItemFromVoid(room_item.GGRoomItem(YARD_UP, wallOffset1, [0, 0]), [6, 0])
    self.__room3.addItemFromVoid(room_item.GGRoomItem(YARD_UP, wallOffset1, [0, 0]), [7, 0])
    wallOffset2 = [45, 50]
    self.__room3.addItemFromVoid(room_item.GGRoomItem(YARD_CORNER, [55, 45], [0, 0]), [0, 0])
    for z in range(1, 5):
      if z % 2 == 0:
        self.__room3.addItemFromVoid(room_item.GGRoomItem(YARD_LEFT, wallOffset2, [30, 0]), [0, z])
      else:
        self.__room3.addItemFromVoid(room_item.GGRoomItem(YARD_LAMP_LEFT, wallOffset2, [0, 0]), [0, z])
    self.__room3.addItemFromVoid(room_item.GGRoomItem(YARD_LEFT, wallOffset2, [0, 0]), [0, 6])
    self.__room3.addItemFromVoid(room_item.GGRoomItem(YARD_LAMP_LEFT, wallOffset2, [0, 0]), [0, 7])
    fountainVertOffset = 10
    self.__room3.addItemFromVoid(room_item.GGRoomItem(FONT_TOPLEFT, [46, -35 + fountainVertOffset], [0, 0]), [3, 3])
    self.__room3.addItemFromVoid(room_item.GGRoomItem(FONT_TOPRIGHT, [55, -35 + fountainVertOffset], [0, 0]), [4, 3])
    self.__room3.addItemFromVoid(room_item.GGRoomItem(FONT_BOTTOMLEFT, [4, -34 + fountainVertOffset], [0, 0]), [3, 4])
    self.__room3.addItemFromVoid(room_item.GGRoomItem(FONT_BOTTOMRIGHT, [50, -30 + fountainVertOffset], [0, 0]), [4, 4])
    self.__room3.addItemFromVoid(myDoor3A, [6, 7])    
    self.__room3.addItemFromVoid(myDoor3B, [0, 5])    
    self.__room3.addItemFromVoid(myDoor3C1, [3, 0])    
    self.__room3.addItemFromVoid(myDoor3C2, [4, 0])    
    self.__room3.addItemFromVoid(myPenguinRoom3, [1, 6])

  def __decorateRoom4(self):
    myDoor4A = teleport.GGDoorWithKey(DOOR_AMORED, [17, 15], [0, 0], [1, 5], self.__room3, "puerta room4a", "Llave Dorada")
    self.__room4.addItemFromVoid(myDoor4A, [7, 5])    
    wallOffset = [35, 33]
    self.__room4.addItemFromVoid(room_item.GGRoomItem(WAREHOUSE_CORNER, wallOffset, [0, 0]), [0, 0])
    for z in range(1, 8):
      image = WAREHOUSE_LEFT[random.randint(0, len(WAREHOUSE_LEFT)-1)]
      self.__room4.addItemFromVoid(room_item.GGRoomItem(image, wallOffset, [0, 0]), [0, z])
    for x in range(1, 8):
      image = WAREHOUSE_UP[random.randint(0, len(WAREHOUSE_UP)-1)]
      self.__room4.addItemFromVoid(room_item.GGRoomItem(image, wallOffset, [0, 0]), [x, 0])
    myBox1 = box_heavy.GGBoxHeavy(BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 1")
    myBox2 = box_heavy.GGBoxHeavy(BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 2")
    myBox3 = box_heavy.GGBoxHeavy(BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 3")
    myBox4 = box_heavy.GGBoxHeavy(BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 4")
    myBox5 = box_heavy.GGBoxHeavy(BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 5")
    myBox6 = box_heavy.GGBoxHeavy(BOX_HEAVY, [26, -12], [0, -10], "Caja pesada 6")
    beamOffset = [57, 142]
    self.__room4.addItemFromVoid(room_item.GGRoomItem(BEAM_WOODEN, beamOffset, [0, 0]), [1, 1])
    self.__room4.addItemFromVoid(room_item.GGRoomItem(BEAM_WOODEN, beamOffset, [0, 0]), [1, 6])
    self.__room4.addItemFromVoid(room_item.GGRoomItem(BEAM_WOODEN, beamOffset, [0, 0]), [6, 1])
    self.__room4.addItemFromVoid(room_item.GGRoomItem(BEAM_WOODEN, beamOffset, [0, 0]), [6, 6])
    self.__room4.addItemFromVoid(myBox1, [1, 4])
    self.__room4.addItemFromVoid(myBox2, [4, 6])
    self.__room4.addItemFromVoid(myBox3, [6, 2])
    self.__room4.addItemFromVoid(myBox4, [4, 1])
    self.__room4.addItemFromVoid(myBox5, [3, 2])
    self.__room4.addItemFromVoid(myBox6, [7, 3])

  def __decorateRoom5(self):
    myDoor5A1 = teleport.GGDoor(TILE_ARROW_BACK, GG.utils.FLOOR_SHIFT, [0, 0], [3, 1], self.__room3, "puerta room5a")
    myDoor5A2 = teleport.GGDoor(TILE_ARROW_BACK, GG.utils.FLOOR_SHIFT, [0, 0], [4, 1], self.__room3, "puerta room5a")
    myDoor5B1 = teleport.GGDoorRoom5b(TILE_MYSTCYRCLE_CASTLE01, GG.utils.FLOOR_SHIFT, [0, 0], [3, 7], self.__room1, "puerta room5b")
    myDoor5B2 = teleport.GGDoorRoom5b(TILE_MYSTCYRCLE_CASTLE01, GG.utils.FLOOR_SHIFT, [0, 0], [4, 7], self.__room1, "puerta room5b")
    penguinRightOffset = [30, 0]
    myPenguinQuiz = penguin.GGPenguinQuiz(PENGUIN_SPRITE_RIGHT, penguinRightOffset, [0, 0], "Andatuz Quiz", GG.utils.QUESTIONS_PATH)
    columnOffset = [13, 15]
    for z in range(0, 8):
      self.__room5.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, columnOffset, [0, 0]), [0, z])
      self.__room5.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, columnOffset, [0, 0]), [1, z])
      self.__room5.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, columnOffset, [0, 0]), [6, z])
      self.__room5.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, columnOffset, [0, 0]), [7, z])
    self.__room5.addItemFromVoid(myDoor5A1, [3, 7])    
    self.__room5.addItemFromVoid(myDoor5A2, [4, 7])    
    self.__room5.addItemFromVoid(myDoor5B1, [3, 0])    
    self.__room5.addItemFromVoid(myDoor5B2, [4, 0])    
    self.__room5.addItemFromVoid(myPenguinQuiz, [2, 3])

  def __decorateRoom6(self):
    myDoor6A = teleport.GGDoor(TILE_ARROW_DOWN, GG.utils.FLOOR_SHIFT, [0, 0], [1, 6], self.__room2, "puerta room6a")
    myGift1 = giver_npc.GGGiverNpc(GIFT, [15, -30], [0, 0], GIFT, "Regalo")
    wallOffset = [35, 40]
    self.__room6.addItemFromVoid(room_item.GGRoomItem(SKYLINE_CORNER, wallOffset, [0, 0]), [0, 0])
    for z in range(1, 8):
      image = SKYLINES_LEFT[random.randint(0, len(SKYLINES_LEFT)-1)]
      self.__room6.addItemFromVoid(room_item.GGRoomItem(image, wallOffset, [0, 0]), [0, z])
    for x in range(1, 8):
      image = SKYLINES_UP[random.randint(0, len(SKYLINES_LEFT)-1)]
      self.__room6.addItemFromVoid(room_item.GGRoomItem(image, wallOffset, [0, 0]), [x, 0])
    self.__room6.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, [13, 15], [0, 0]), [2, 3])
    self.__room6.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, [13, 15], [0, 0]), [5, 2])
    self.__room6.addItemFromVoid(room_item.GGRoomItem(COLUMN_STONE, [13, 15], [0, 0]), [4, 6])
    self.__room6.addItemFromVoid(myDoor6A, [7, 6])
    self.__room6.addItemFromVoid(myGift1, [4, 4])

