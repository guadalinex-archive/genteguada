# -*- coding: utf-8 -*-

import ggmodel
import dMVC.model

class GGInventoryItem(ggmodel.GGModel):
  """GGInventoryItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, label=None):
    """ Class constructor.
    spriteName: image name.
    """
    ggmodel.GGModel.__init__(self)
    self.__player = None
    self.spriteName = spriteName
    self.spriteInventory = None
    if label:
      self.label = label
    else:  
      self.label = "No label"
    self.setImagePath("")

  def objectToPersist(self):
    dict = ggmodel.GGModel.objectToPersist(self)
    dict["spriteName"] = self.spriteName
    dict["spriteInventory"] = self.spriteInventory
    dict["label"] = self.label
    dict["imagePath"] = self.__imagePath
    return dict
  
  def load(self, dict):
    ggmodel.GGModel.load(self, dict)
    self.spriteName = dict["spriteName"]
    self.spriteInventory = dict["spriteInventory"]
    self.label = dict["label"]
    self.__imagePath = dict["imagePath"]
    self.__player = None

  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['spriteInventory']

  def getSpriteName(self):
    return self.spriteName

  def setSpriteName(self, spriteName):
    self.spriteName = spriteName
  
  def getAdminActions(self):
    """ Returns all possible admin actions for this item.
    """  
    return None
  
  def getName(self):
    """ Returns the item's label.
    """  
    return self.label
  
  def setName(self, newLabel):
    """ Sets a new label for the item.
    newLabel: new label.
    """  
    if self.label != newLabel:
      self.label = newLabel
      return True
    return False
  
  def getImagePath(self):
    """ Returns the item image path.
    """  
    return self.__imagePath  
  
  def setImagePath(self, imagePath):
    """ Sets a new item image path.
    imagePath: new image path.
    """  
    self.__imagePath = imagePath 
  
  # self.__player
  
  def getPlayer(self):
    """ Returns this item's owner.
    """  
    return self.__player

  def setPlayer(self, player):
    """ Sets a new player as owner of this item.
    """  
    self.__player = player  

  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    room: item's room.
    parent: isoview hud handler.
    """
    import GG.isoview.isoview_item
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)

  def inventoryOnly(self):
    """ Checks if this is an inventory item or not.
    """  
    return True
  
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player. Do NOT delete.
    clicker: player who clicks.
    """
    pass
    
  def tick(self, now):
    """ Call for an update on item. Do NOT delete.
    Not used at the moment.
    """
    pass

  def isTile(self):
    """ Checks if this item is a tile or not.
    """  
    return False  
