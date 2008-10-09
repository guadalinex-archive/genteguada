# -*- coding: utf-8 -*-

import room_item
import GG.utils
import ggsystem

class GGBoxHeavy(room_item.GGRoomItem):
  """ GGBoxHeavy class.
  Defines a heavy box item behaviour.
  """
 
  def __init__(self, spriteName, label):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    label: item's label
    """
    room_item.GGRoomItem.__init__(self, spriteName, label)
    self.setPoints(2)
 
  def load(self, dict):
    room_item.GGRoomItem.load(self, dict)
    self.setPoints(2)

  def copyObject(self):
    """ Creates and returns a copy of this item.
    """  
    return GGBoxHeavy(self.spriteName, self.getName())
    
  def getOptions(self):
    """ Returns the item options.
    """  
    tile = self.getTile()
    depth = tile.getDepth()
    selfDepth = tile.getItemDepth(self)
    selecter = self.getRoom().getSelecter(self)
    if selecter.getPosition() == self.getPosition():
      if (selfDepth + 1) >= depth:
      # Same position, box over the player  
        return ["drop"]
      else:    
      # Same position, box under the player  
        return ["climb"]
    else:
      if (selfDepth + 1) == depth:  
      # Different position, box on top of the stack.
        if selfDepth:     
          return ["lift", "climb"]
        else:
          return ["lift", "climb", "jumpOver"]
      else:
      # Different position, box in the middle of the stack.
        return ["climb"]
    
  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    adminDict = room_item.GGRoomItem.getAdminActions(self)
    adminDict["Etiqueta"] = [self.getName()]
    return adminDict    

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
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()) or self.getPosition() == clicker.getPosition():
      clicker.setSelectedItem(self)
    
  def isStackable(self):
    """ Checks if this item is stackable or not.
    """  
    return True

  def stepOn(self):
    """ Checks if other items can be placed on top of this one.
    """  
    return True
