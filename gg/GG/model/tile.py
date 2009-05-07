# -*- coding: utf-8 -*-

import ggmodel
import GG.utils
import os

class Tile(ggmodel.GGModel):
  """ Tile class.
  Defines a tile object.
  """

  def __init__(self, position, spriteName, room):
    """ Class constructor.
    position: tile position.
    spriteName: sprite name used on the tile.
    room: tile's room.
    """  
    ggmodel.GGModel.__init__(self)
    self.__items = []
    self.__room = room
    self.position = position
    self.spriteName = spriteName

  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['position', 'spriteName']

  def getOptions(self):
    """ Returns the item's available options.
    """
    return []    
      
  def getName(self):
    """ Returns the tile's name.
    """  
    cad = "Tile [" + str(self.position[0]) + "," + str(self.position[1]) + "]"
    return cad
  
  def getImageLabel(self):
    """ Returns the tile's image file name.
    """  
    return self.spriteName

  def getPosition(self):
    """ Returns the tile position.
    """  
    return self.position  
      
  def getAdminActions(self):
    """ Returns the possible admin actions for this item.
    """  
    dic = {"image": GG.utils.TILES}
    return dic  
    
  def getDepth(self):
    """ Returns the number of items on this tile.
    """  
    return len(self.__items)

  def getItemDepth(self, item):
    """ Returns an item's stack position on a tile.
    item: stacked item.
    """  
    return self.__items.index(item)

  def hasPlayer(self):
    """ Checks if there's a player on the tile.
    """  
    items = self.__room.getItems()
    for item in items:
      if hasattr(item, "username"):
        return True
    return False

  def getRoom(self):
    """ Returns the tile's room.
    """      
    return self.__room

  def stackItem(self, item):
    """ Add an item to the items stack.
    item: new item.
    """  
    self.__items.append(item)
    
  def unstackItem(self):
    """ Removes an item from the items stack.
    """  
    self.__items.pop()
    
  def getTopItem(self):
    """ Returns the top item from the items stack.
    """  
    if len(self.__items) == 0:
      return None
    return self.__items[len(self.__items)-1]  

  def getBottomItem(self):
    """ Returns the bottom item from the items stack.
    """  
    if len(self.__items) == 0:
      return None
    return self.__items[0]  
  
  def getSteppedItem(self, overItem):
    """ Returns the item just below.
    overItem: item on top of the looked for item.
    """  
    prevItem = None
    for currentItem in self.__items:
      if currentItem == overItem:
        return prevItem
      else:
        prevItem = currentItem
    return prevItem
  
  def getItems(self):
    """ Returns the tile's item stack.
    """  
    items = []
    for item in self.__items:
      items.append(item)
    return items
    
  def getItemsAndDestroy(self):
    """ Returns the tile items and removes them from itself.
    """  
    items = self.__items
    self.__items = []
    return items

  def getItemsFrom(self, item):
    """ Returns items from the stack from a given position.
    item: starting position on the items stack.
    """ 
    items = []
    k = 0
    for itFrom in self.__items:
      if itFrom == item:
        items.append(itFrom)
        k = 1
      elif k == 1:  
        items.append(itFrom)
    return items

  def getItemsAndRemoveFrom(self, item):
    """ Returns items from the stack from a given position, removing them from the stack.
    item: starting position on the items stack.
    """ 
    items = []
    k = 0
    for itFrom in self.__items:
      if itFrom == item:
        items.append(itFrom)
        self.__items.remove(itFrom)
        k = 1
      elif k:  
        items.append(itFrom)
        self.__items.remove(itFrom)
    return items

  def stepOn(self):
    """ Checks if an item can be placed over the items stack.
    """  
    xValue = len(self.__items)-1
    while xValue >= 0:
      if self.__items[xValue].stepOn():
        xValue -= 1
      else:
        return False
    return True  

  def inventoryOnly(self):
    """ Check if this is an inventory only item.
    """  
    return False  

  def isTile(self):
    """ Checks if this is a tile object.
    """  
    return True  

  def applyChanges(self, fields, player, room):
    keys = fields.keys()
    if "image" in keys:
      if fields["image"]:
        self.setImage(os.path.join(GG.utils.TILE, fields["image"]))

  def setImage(self, image, noTrigger=None):
    """ Sets a new image for the tile.
    image: new image.
    noTrigger: flag to indicate wether trigger an image change event or not.
    """  
    self.spriteName = image
    if not noTrigger:
      self.__room.tileImageChange(self.position, image)

  def getPlayer(self):
    return None
    
