# -*- coding: utf-8 -*-

import md5
import time
import GG.utils
import room_item
import generated_inventory_item

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
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["copy", "jumpOver"]   
      
  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    dic = {"Position": self.getPosition(), "Label": [self.getName()]}
    return dic    
         
  def getImageLabel(self):
    """ Returns the item's image filename.
    """  
    return self.spriteInventory

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
  
  def inventoryOnly(self):
    """ Checks if this is an inventory item or not.
    """  
    return False
  
  def tick(self, now):
    """ Call for an update on item. Do NOT delete.
    now: current timestamp.
    """
    pass
  
  def isStackable(self):
    """ Checks if this item is stackable or not.
    """  
    return False


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
    #print self.__idGift

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
      
  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    dic = {"Position": self.getPosition()}
    return dic    

  def copyObject(self):
    """ Copies and returns this item.
    """   
    return WebGift(self.spriteName, self.spriteInventory, self.getName(), self.__creator)
  
  def getCopyFor(self, player):
    """ If selected player does not have this item on his inventory, creates a new item and gives it to him.
    player: selected player.
    """ 
    player.newChatMessage("Obtienes " + self.getName(), 2)
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
