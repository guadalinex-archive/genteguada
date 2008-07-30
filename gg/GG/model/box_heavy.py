import room_item
import GG.utils

class GGBoxHeavy(room_item.GGRoomItem):
  """ GGBoxHeavy class.
  Defines a pickable item behaviour.
  """
 
  def __init__(self, spriteName, anchor, topAnchor, label):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    anchor: image anchor on screen.
    label: item's label
    """
    room_item.GGRoomItem.__init__(self, spriteName, anchor, topAnchor)
    self.label = label
    self.setPoints(2)
    
  def variablesToSerialize(self):
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']

  def getOptions(self):
    tile = self.getTile()
    depth = tile.getDepth()
    selfDepth = tile.getItemDepth(self)
    if (selfDepth + 1) != depth:
      # Hay elementos por encima de el
      return ["climb"]
    else:
      if selfDepth:  
        return ["lift", "drop", "climb"]
      else: 
        return ["lift", "climb"]
    
  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteName
  
  def setPlayer(self, player):
    self.__player = player
    
  def getPlayer(self):
    return self.__player  
  
  def clickedBy(self, clicker):
    """ Triggers an event when the item receives a click by a player.
    clicker: player who clicks.
    """
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()) \
        or (self.getPosition() == clicker.getPosition()):
      clicker.setSelectedItem(self)
    
  def isStackable(self):
    return True

  def stepOn(self):
    return True
