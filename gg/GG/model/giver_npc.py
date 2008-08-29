# -*- coding: utf-8 -*-

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
    return ["copy"]   
      
  def getName(self):
    """ Returns the item's label.
    """  
    return self.label
  
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
      return None, [-1, -1, -1]
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

