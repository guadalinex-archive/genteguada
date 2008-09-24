# -*- coding: utf-8 -*-

import room_item
import GG.utils

class GGPickableItem(room_item.GGRoomItem):
  """ GGPickableItem class.
  Defines a pickable item behaviour.
  """
 
  def __init__(self, spriteName, anchor, topAnchor, spriteInventory, label):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    anchor: image anchor on screen.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
    """
    room_item.GGRoomItem.__init__(self, spriteName, anchor, topAnchor, label)
    self.spriteInventory = spriteInventory
    
  def objectToPersist(self):
    dict = room_item.GGRoomItem.objectToPersist(self)
    dict["spriteInventory"] = self.spriteInventory
    return dict

  def load(self, dict):
    room_item.GGRoomItem.load(self, dict)
    self.spriteInventory = dict["spriteInventory"]

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGPickableIte(self.spriteName, self.anchor, self.topAnchor, self.spriteInventory, self.getName())
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory']

  def getOptions(self):
    """ Returns the item's available options.
    """
    if self.getRoom():
      return ["inventory", "jumpOver"]
    else:
      if self.getPlayer().isExchange():
        return ["toExchange"]
      else:
        return ["removeInventory"]
      
  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    if self.getRoom():
      dic = {"Position": self.getPosition(), "Label": [self.getName()]}
      return dic
    return None
         
  def getImageLabel(self):
    """ Returns the item's image filename.
    """  
    return self.spriteInventory

  def clickedBy(self, clicker):
    """ Triggers an event when the item receives a click by a player.
    clicker: player who clicks.
    """
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    
  def isStackable(self):
    """ Checks if this item is stackable or not.
    """  
    return True

  def stepOn(self):
    """ Checks if other items can be placed on top of this one.
    """  
    return False

# ===============================================================

class PaperMoney(GGPickableItem):

  def __init__(self, spriteName, anchor, topAnchor, label, value):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    anchor: image anchor on screen.
    topAnchor: image top anchor on screen.
    label: item's label
    value: item's value
    """
    GGPickableItem.__init__(self, spriteName, anchor, topAnchor, spriteName, label)
    self.points = value

  def objectToPersist(self):
    dict = GGPickableItem.objectToPersist(self)
    dict["points"] = self.points
    return dict

  def load(self, dict):
    GGPickableItem.load(self, dict)
    self.points = dict["points"]
    
  def copyObject(self):
    """ Copies and returns this item.
    """  
    return PaperMoney(self.spriteName, self.anchor, self.topAnchor, self.getName(), self.points)

  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    dic = {"Position": self.getPosition(), "Label": [self.getName()]}
    return dic    
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["money", "jumpOver"]
    
  def addPointsTo(self, player):
    """ Gives points to a player.
    player: player to give points to.
    """  
    player.addPoints(self.points, self.getName())  
    
