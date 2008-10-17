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

class CreateWorld:
  """ CreateWorld class.
  Creates and initializes all GenteGuada items, players and rooms. 
  """  

  def __init__(self, system):
    """ Class constructor.
    system: system object.
    """  
    self.__system = system

  def create(self):
    """ Creates all GenteGuada components.
    """  
    self.__createExampleWorld()

  def __createExampleWorld(self):
    self.__beachRoom = self.__system.createRoom(GG.utils.TILES_BEACH, "Playa", [8, 8], 12, True, True)
    self.__desertRoom = self.__system.createRoom(GG.utils.TILES_DESERT, "Desierto", [8, 8], 12, True, True)
    self.__gravelRoom = self.__system.createRoom(GG.utils.TILES_GRAVEL, "Gravilla", [8, 8], 12, True, True)
    self.__alberoRoom = self.__system.createRoom(GG.utils.TILES_ALBERO, "Albero", [8, 8], 12, True, True)
    self.__grassRoom = self.__system.createRoom(GG.utils.TILES_GRASS, "Hierba", [8, 8], 12, True, True)
    self.__snowRoom = self.__system.createRoom(GG.utils.TILES_SNOW, "Nieve", [8, 8], 12, True, True)
    self.__terrazoRoom = self.__system.createRoom(GG.utils.TILES_TERRAZO, "Terrazo", [8, 8], 12, True, True)
    self.__mudRoom = self.__system.createRoom(GG.utils.TILES_MUD, "Barro", [8, 8], 12, True, True)
    self.__mozarabeRoom = self.__system.createRoom(GG.utils.TILES_MOZARABE, "Mozarabe", [8, 8], 12, True, True)
    self.__footballRoom = self.__system.createRoom(GG.utils.TILES_FOOTBALL, "Futbol", [8, 8], 12, True, True)
    self.__chessRoom = self.__system.createRoom(GG.utils.TILES_CHESS, "Ajedrez", [8, 8], 12, True, True)
    self.__roadRoom = self.__system.createRoom(GG.utils.TILES_GRASS, "Carretera", [8, 8], 12, True, True)
    self.__decorateBeach()
    self.__decorateDesert()
    self.__decorateGravel()
    self.__decorateGrass()
    self.__decorateTerrazo()
    self.__decorateFootball()
    self.__decorateMud()
    self.__decorateChess()
    self.__decorateRoad()

  def __decorateBeach(self):
    self.__beachRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.CORNER_WIRE), [0, 0])
    for i in range(8):
      if not i == 0:
        self.__beachRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.WIRE_LEFT), [0, i])
        self.__beachRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.WIRE_UP), [i, 0])
    self.__beachRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.ORANGETREE), [7, 7])
    self.__beachRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.OLIVETREE), [7, 2])
    self.__beachRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.RACK), [5, 2])
    self.__beachRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.PINE_1), [1, 7])
    self.__beachRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.PINE_2), [1, 3])
    self.__beachRoom.addItemFromVoid(box_heavy.GGBoxHeavy(GG.utils.WEIGHS, "Pesa"), [7, 1])
    self.__beachRoom.addItemFromVoid(box_heavy.GGBoxHeavy(GG.utils.BOX, "Caja"), [3, 1])
    self.__beachRoom.addItemFromVoid(pickable_item.GGPickableItem(GG.utils.GIFT, GG.utils.GIFT, "regalo"), [5,3])

  def __decorateDesert(self):
    self.__desertRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.CACTUS_1), [4, 4])
    self.__desertRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.CACTUS_2), [1, 7])
    self.__desertRoom.addItemFromVoid(box_heavy.GGBoxHeavy(GG.utils.HAY, "Bala de heno"), [7, 1])
    self.__desertRoom.addItemFromVoid(box_heavy.GGBoxHeavy(GG.utils.TABLE, "Mesa"), [7, 7])
    self.__desertRoom.addItemFromVoid(pickable_item.PaperMoney(GG.utils.TICKET_5), [4,3])

  def __decorateGravel(self):
    self.__gravelRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.CORNER_BUSH), [0, 0])
    for i in range(8):
      if not i == 0:
        self.__gravelRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.BUSH_LEFT), [0, i])
        self.__gravelRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.BUSH_UP), [i, 0])
    self.__gravelRoom.addItemFromVoid(giver_npc.GGGiverNpc(GG.utils.KEY_RED, GG.utils.KEY_RED, "Llave"),[2,2])

  def __decorateGrass(self):
    self.__grassRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.FIR), [4, 4])
    self.__grassRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.BUSH), [4, 4])

  def __decorateTerrazo(self):
    self.__terrazoRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.CORNER_BRICK), [0, 0])
    for i in range(8):
      if not i == 0:
        self.__terrazoRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.BRICK_LEFT), [0, i])
        self.__terrazoRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.BRICK_UP), [i, 0])
    self.__terrazoRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.COLUMN), [4, 4])

  def __decorateFootball(self):
    self.__footballRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.CORNER_WOOD), [0, 0])
    for i in range(8):
      if not i == 0:
        self.__footballRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.WOOD_LEFT), [0, i])
        self.__footballRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.WOOD_UP), [i, 0])

  def __decorateMud(self):
    self.__mudRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.CORNER_STONE), [0, 0])
    for i in range(8):
      if not i == 0:
        self.__mudRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.STONE_LEFT), [0, i])
        self.__mudRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.STONE_UP), [i, 0])
    self.__mudRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.SHELF_1), [4, 4])
    self.__mudRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.SHELF_2), [2, 2])

  def __decorateChess(self):
    self.__chessRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.LAMP), [4, 4])
    self.__chessRoom.addItemFromVoid(room_item.GGRoomItem(GG.utils.FONT), [1, 7])

  def __decorateRoad(self):
    for i in range(8):
      self.__roadRoom.setSpecialTile([4,i], os.path.join(GG.utils.TILE,"disc_vert.png"))
    for i in range(8):
      self.__roadRoom.setSpecialTile([5,i], os.path.join(GG.utils.TILE,"asfalto.png"))
    for i in range(8):
      self.__roadRoom.setSpecialTile([3,i], os.path.join(GG.utils.TILE,"asfalto.png"))

