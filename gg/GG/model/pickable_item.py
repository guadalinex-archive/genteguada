# -*- coding: utf-8 -*-

import room_item
import GG.utils
import os
import ggsystem
import dMVC

class GGPickableItem(room_item.GGRoomItem):
  """ GGPickableItem class.
  Defines a pickable item behaviour.
  """
 
  def __init__(self, spriteName, spriteInventory, label):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
    """
    room_item.GGRoomItem.__init__(self, spriteName, label)
    self.spriteInventory = spriteInventory
    self.__disabled = False
    
  def objectToPersist(self):
    dict = room_item.GGRoomItem.objectToPersist(self)
    dict["spriteInventory"] = self.spriteInventory
    return dict

  def load(self, dict):
    room_item.GGRoomItem.load(self, dict)
    self.spriteInventory = dict["spriteInventory"]
    self.__disabled = False

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGPickableItem(self.spriteName, self.spriteInventory, self.getName())
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory']

  def getOptions(self):
    """ Returns the item's available options.
    """
    if self.getRoom() and self.getTile():
      return ["inventory", "jumpOver"]
    else:
      if self.getPlayer().isExchange():
        return ["toExchange"]
      else:
        return ["removeInventory"]
      
  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    if self.getRoom() and self.getTile():
      adminDict = room_item.GGRoomItem.getAdminActions(self)
      adminDict["Etiqueta"] = [self.getName()]
      return adminDict
    else:
      return None

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
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    
  def isStackable(self):
    """ Checks if this item is stackable or not.
    """  
    return True

  @dMVC.synchronized.synchronized(lockName='capture')
  def capture(self):
    if not self.__disabled:
      self.__disabled = True
      return True
    else:
      return False

  @dMVC.synchronized.synchronized(lockName='capture')
  def setEnabled(self):
    self.__disabled = False


class PaperMoney(GGPickableItem):

  def __init__(self, spriteName):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    label: item's label
    value: item's value
    """
    GGPickableItem.__init__(self, spriteName, spriteName, GG.utils.MONEY_LABEL[os.path.split(spriteName)[-1]])
    self.points = GG.utils.MONEY_VALUE[os.path.split(spriteName)[-1]]

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
    return PaperMoney(self.spriteName)

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["money", "jumpOver"]

