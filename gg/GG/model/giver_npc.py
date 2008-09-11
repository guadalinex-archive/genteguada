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
  
  def __init__(self, spriteName, anchor, topAnchor, spriteInventory, label):
    """ Class constructor.
    spriteName: image name.
    anchor: image offset on screen.
    topAnchor: top item's image offset.
    spriteInventory: sprite used to paint this object on player's inventory.
    label: item label.
    """
    room_item.GGRoomItem.__init__(self, spriteName, anchor, topAnchor)
    self.spriteInventory = spriteInventory
    self.label = label
    self.points = 0

  def copyObject(self): 
    return GGGiverNpc(self.spriteName, self.anchor, self.topAnchor, self.spriteInventory, self.label)
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["copy", "jumpOver"]   
      
  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    dic = {"Position": self.getPosition(), "Label": [self.label]}
    return dic    
         
  def getName(self):
    """ Returns the item's label.
    """  
    return self.label
  
  def setLabel(self, newLabel):
    """ Sets a new label for the item.
    """  
    self.label = newLabel  
  
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
    """ If target player does not have this item on his inventory, creates a new item and gives it to him.
    """  
    if player.hasItemLabeledInInventory(self.label):
      player.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage("Ya has obtenido " + self.label, \
                self.label, GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
      return None, [-1, -1]
    else:  
      player.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage("Obtienes " + self.label, \
                self.label, GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
      return generated_inventory_item.GGGeneratedInventoryItem(self.spriteInventory, self.label, self.anchor, self.getPosition()), self.getPosition()
  
  def inventoryOnly(self):
    """ Checks if this is an inventory item or not.
    """  
    return False
  
  def tick(self, now):
    """ Call for an update on item.
    Not used at the moment.
    """
    pass
  
  def isStackable(self):
    """ Checks if this item is stackable or not.
    """  
    return False

# ===============================================================

class WebGift(GGGiverNpc):
    
  def __init__(self, spriteName, anchor, topAnchor, spriteInventory, label, creator):
    """ Class constructor.
    spriteName: image name.
    anchor: image offset on screen.
    topAnchor: top item's image offset.
    spriteInventory: sprite used to paint this object on player's inventory.
    label: item label.
    """
    GGGiverNpc.__init__(self, spriteName, anchor, topAnchor, spriteInventory, label)
    self.__creator = creator
    self.__idGift = self.generateId()
    
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
    return WebGift(self.spriteName, self.anchor, self.topAnchor, self.spriteInventory, self.label, self.__creator)
  
  def getGiftFor(self, player):
    """ If target player does not have this item on his inventory, creates a new item and gives it to him.
    """  
    player.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage("Obtienes " + self.label, \
                self.label, GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
    return generated_inventory_item.GGGeneratedGift(self.spriteInventory, self.label, self.anchor, \
                                                    self.getPosition(), self.__idGift), self.getPosition()
                                                    
  def generateId(self):
    originalString = self.__creator + str(int(time.time()))
    return md5.new(originalString).hexdigest()                                              
