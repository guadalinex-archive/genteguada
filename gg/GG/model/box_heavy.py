import room_item
import GG.utils

class GGBoxHeavy(room_item.GGRoomItem):
  """ GGBoxHeavy class.
  Defines a heavy box item behaviour.
  """
 
  def __init__(self, spriteName, anchor, topAnchor, label):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    anchor: image anchor on screen.
    topAnchor: image top anchor on screen.
    label: item's label
    """
    room_item.GGRoomItem.__init__(self, spriteName, anchor, topAnchor)
    self.label = label
    self.setPoints(2)
    
  def variablesToSerialize(self):
    """ Sets some class attributes as public access.
    """  
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']

  def getOptions(self):
    """ Returns the item options.
    """  
    tile = self.getTile()
    depth = tile.getDepth()
    selfDepth = tile.getItemDepth(self)
    selecter = self.getRoom().getSelecter(self)
    if (selfDepth + 1) != depth:
      return ["climb"]
    else:
      if selecter.getPosition() == self.getPosition():  
        if selfDepth:  
          return ["drop", "climb"]
        else: 
          return ["climb"]
      else:
        if selfDepth:  
          return ["lift", "drop", "climb"]
        else: 
          return ["lift", "climb"]
    
  def getName(self):
    """ Returns the item's label.
    """  
    return self.label
  
  def getImageLabel(self):
    """ Returns the item's image filename.
    """  
    return self.spriteName
  
  def clickedBy(self, clicker):
    """ Triggers an event when the item receives a click by a player.
    clicker: player who clicks.
    """
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()) \
        or (self.getPosition() == clicker.getPosition()):
      clicker.setSelectedItem(self)
    
  def isStackable(self):
    """ Checks if this item is stackable or not.
    """  
    return True

  def stepOn(self):
    """ Checks if other items can be placed on top of this one.
    """  
    return True
