# -*- coding: utf-8 -*-

import md5
import time
import GG.utils
import room_item
import generated_inventory_item
import ggsystem

class GGGiverNpc(room_item.GGRoomItem):
  """GGGiverNpc class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, spriteInventory, label):
    """ Class constructor.
    spriteName: image name.
    spriteInventory: sprite used to paint this object on player's inventory.
    label: item label.
    """
    room_item.GGRoomItem.__init__(self, spriteName, label)
    self.spriteInventory = spriteInventory
    self.points = 0

  def objectToPersist(self):
    dict = room_item.GGRoomItem.objectToPersist(self)
    dict["spriteInventory"] = self.spriteInventory
    return dict

  def load(self, dict):
    room_item.GGRoomItem.load(self, dict)
    self.spriteInventory = dict["spriteInventory"]
    self.points = 0

  def copyObject(self): 
    """ Copies and returns this object.
    """  
    return GGGiverNpc(self.spriteName, self.spriteInventory, self.getName())
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["copy", "jumpOver"]   

  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    adminDict = room_item.GGRoomItem.getAdminActions(self)
    adminDict["Etiqueta"] = [self.getName()]
    return adminDict    

  def applyChanges(self, fields, player, room):
    keys = fields.keys()
    if "Etiqueta" in keys:
      oldLabel = self.getName()
      newLabel = fields["Etiqueta"]
      if self.setName(newLabel):
        ggsystem.GGSystem.getInstance().labelChange(oldLabel, newLabel)
    return room_item.GGRoomItem.applyChanges(self, fields, player, room)
         
  def clickedBy(self, clicker):
    """ Triggers an event when the item receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)

  def getCopyFor(self, player):
    """ If selected player does not have this item on his inventory, creates a new item and gives it to him.
    player: selected player.
    """  
    if player.hasItemLabeledInInventory(self.getName()):
      message = "Ya has obtenido " + self.getName()
      player.newChatMessage(message, 2)
      return None, [-1, -1]
    else:  
      message = "Obtienes " + self.getName()
      player.newChatMessage(message, 2)
      return generated_inventory_item.GGGeneratedInventoryItem(self.spriteInventory, self.getName(), self.getPosition()), self.getPosition()
  
  def tick(self, now):
    """ Call for an update on item. Do NOT delete.
    now: current timestamp.
    """
    pass
  

class WebGift(GGGiverNpc):
    
  def __init__(self, spriteInventory, label, creator):
    """ Class constructor.
    spriteName: image name.
    spriteInventory: sprite used to paint this object on player's inventory.
    label: item label.
    creator: item's creator.
    """
    GGGiverNpc.__init__(self, GG.utils.GIFT, spriteInventory, label)
    self.__creator = creator
    self.__idGift = self.generateId()

  def objectToPersist(self):
    dict = GGGiverNpc.objectToPersist(self)
    dict["creator"] = self.__creator
    dict["idGift"] = self.__idGift
    return dict

  def load(self, dict):
    GGGiverNpc.load(self, dict)
    self.__creator = dict["creator"]
    self.__idGift = dict["idGift"]

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["gift", "jumpOver"]   

  def copyObject(self):
    """ Copies and returns this item.
    """   
    return WebGift(self.spriteInventory, self.getName(), self.__creator)
  
  def getCopyFor(self, player):
    """ If selected player does not have this item on his inventory, creates a new item and gives it to him.
    player: selected player.
    """ 
    if player.hasItemLabeledInInventory(self.getName()):
      message = "Ya has obtenido " + self.getName()
      player.newChatMessage(message, 2)
      return None, [-1, -1]
    else:  
      message = "Obtienes " + self.getName()
      player.newChatMessage(message, 2)
      return generated_inventory_item.GGGeneratedGift(self.spriteInventory, self.getName(), self.getPosition(), self.__idGift), self.getPosition()
                                                    
  def generateId(self):
    """ Generates an unique id for this item.
    """  
    originalString = self.__creator + str(int(time.time()))
    return md5.new(originalString).hexdigest()

  def getIdGift(self):
    """ Returns the gift id.
    """  
    return self.__idGift  


class RandomPositionGiverNPC(GGGiverNpc):

  def __init__(self, spriteName, spriteInventory, label):
    GGGiverNpc.__init__(self, spriteName, spriteInventory, label)

  def copyObject(self): 
    """ Copies and returns this object.
    """  
    return RandomPositionGiverNPC(self.spriteName, self.spriteInventory, self.getName())

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["copyRemove", "jumpOver"] 

  def getCopyFor(self, player):
    """ If selected player does not have this item on his inventory, creates a new item and gives it to him.
    player: selected player.
    """  
    if player.hasItemLabeledInInventory(self.getName()):
      message = "Ya has obtenido " + self.getName()
      player.newChatMessage(message, 2)
      return None, [-1, -1]
    else:  
      message = "Obtienes " + self.getName()
      player.newChatMessage(message, 2)
      ggsystem.GGSystem.getInstance().changeItemRandomPosition(self, player)
      return generated_inventory_item.GGGeneratedInventoryItem(self.spriteInventory, self.getName(), self.getPosition()), self.getPosition()
    

