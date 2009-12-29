# -*- coding: utf-8 -*-

import inventory_item
import dMVC.model

class GGGeneratedInventoryItem(inventory_item.GGInventoryItem):
  """GGGeneratedInventoryItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, label, parentPosition):
    """ Class constructor.
    spriteName: image name.
    label: item's label.
    parentPosition: origin position.
    """
    inventory_item.GGInventoryItem.__init__(self, spriteName, label)
    self.spriteInventory = spriteName
    self.points = 0
    self.__position = parentPosition

  def objectToPersist(self):
    dict = inventory_item.GGInventoryItem.objectToPersist(self)
    dict["spriteInventory"] = self.spriteInventory
    dict["position"] = self.__position
    return dict

  def load(self, dict):
    inventory_item.GGInventoryItem.load(self, dict)
    self.spriteInventory = dict["spriteInventory"]
    self.points = 0
    self.__position = dict["position"]

  def getItemBuildPackage(self):
    """ Returns item info used to create the isometric view object.
    """      
    infoPackage = {}
    infoPackage["position"] = self.getPosition() 
    infoPackage["imagepath"] = self.getImagePath()
    infoPackage["spriteName"] = self.spriteInventory
    return infoPackage
  
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = inventory_item.GGInventoryItem.variablesToSerialize(self)
    return parentVars + ['points']
      
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["removeInventory"]  

  def getImageLabel(self):
    """ Returns the item's image filename.
    """  
    return self.spriteInventory

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

# ===============================================================

class GGGeneratedGift(GGGeneratedInventoryItem):
  """GGGeneratedGift class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, label, parentPosition, idGift):
    """ Class constructor.
    spriteName: image name.
    label: item's label.
    parentPosition: origin position.
    spriteName: image name.
    idGift: gift identifier.
    """
    GGGeneratedInventoryItem.__init__(self, spriteName, label, parentPosition)
    self.__idGift = idGift

  def objectToPersist(self):
    dict = GGGeneratedInventoryItem.objectToPersist(self)
    dict["idGift"] = self.__idGift
    return dict

  def load(self, dict):
    GGGeneratedInventoryItem.load(self, dict)
    self.__idGift = dict["idGift"]

  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    room: item's room.
    parent: isoview hud handler.
    """
    import GG.isoview.isoview_item
    return GG.isoview.isoview_item.IsoViewResizedItem(self, screen, room, parent, None, self.spriteInventory)
      
  def getOptions(self):
    """ Returns the item's available options.
    """
    if self.getPlayer().isExchange():
      return ["toExchange"]
    else:
      return ["url"]  
      
  def getUrl(self):
    """ Returns the internet address.
    """  
    return "http://www.guadalinex.org/genteguada/inventario"  
 
  def getIdGift(self):
    """ Returns the gift id value.
    """  
    return self.__idGift
