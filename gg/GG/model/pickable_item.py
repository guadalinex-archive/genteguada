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
    room_item.GGRoomItem.__init__(self, spriteName, anchor, topAnchor)
    self.spriteInventory = spriteInventory
    self.label = label

  def copyObject(self):
    return GGPickableIte(self.spriteName, self.anchor, self.topAnchor, self.spriteInventory, self.label)
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']

  def getOptions(self):
    """ Returns the item's available options.
    """
    if self.getRoom():
      return ["inventory"]
    else:
      if self.__player.isExchange():
        return ["toExchange"]
      else:
        return ["removeInventory"]

  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    dic = {"Position": self.getPosition(), "Label": [self.label]}
    return dic    
         
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
    return True


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

  def copyObject(self):
    return PaperMoney(self.spriteName, self.anchor, self.topAnchor, self.label, self.points)
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["money"]
    
  def addPointsTo(self, player):
    """ Gives points to a player.
    player: player to give points to.
    """  
    player.addPoints(self.points, self.label)  
    

