# -*- coding: utf-8 -*-

import inventory_item

class GGGeneratedInventoryItem(inventory_item.GGInventoryItem):
  """GGGeneratedInventoryItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, label, anchor, parentPosition):
    """ Class constructor.
    spriteName: image name.
    label: item's label.
    anchor: on-screen sprite offset.
    parentPosition: origin position.
    """
    inventory_item.GGInventoryItem.__init__(self, spriteName)
    self.spriteInventory = spriteName
    self.label = label
    self.points = 0
    self.anchor = anchor
    self.__position = parentPosition
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    #parentVars = GG.model.inventory_item.GGInventoryItem.variablesToSerialize(self)
    parentVars = inventory_item.GGInventoryItem.variablesToSerialize(self)
    return parentVars + ['label', 'points', 'anchor']
      
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["removeInventory"]  

  def getName(self):
    """ Returns the item's label.
    """  
    return self.label
  
  def getImageLabel(self):
    """ Returns the item's image filename.
    """  
    return self.spriteInventory

  def setLabel(self, newLabel):
    """ Sets a new label for the item.
    """  
    self.label = newLabel  

  def getPosition(self):
    """ Returns item's position.
    """  
    return self.__position

  def setPoints(self, points):
    """ Sets a new item point value.
    points: new points value.
    """  
    self.points = points
  
  def inventoryOnly(self):
    """ Checks if this is an inventory only item.
    """  
    return True
  
  def tick(self, now):
    """ Call for an update on item.
    Not used at the moment.
    """
    pass
  
  def isStackable(self):
    """ Checks if this item is stackable.
    """  
    return False

