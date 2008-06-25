import room_item
import GG.isoview.isoview_item

class GGBoxHeavy(room_item.GGRoomItem):
  """ GGBoxHeavy class.
  Defines a pickable item behaviour.
  """
 
  def __init__(self, spriteName, position, anchor, label, time, startRoom):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    anchor: image anchor on screen.
    label: item's label
    """
    room_item.GGRoomItem.__init__(self, spriteName, position, anchor)
    self.label = label
    self.points = 2
    self.__startPosition = position
    self.__time = time*1000
    self.__startRoom = startRoom
    self.__startTime = 0
    
  def variablesToSerialize(self):
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label', 'points']

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["lift"]

  def setPlayer(self, player):
    self.__player = player
    
  def getPlayer(self):
    return self.__player  
  
  def clickedBy(self, clicker):
    """ Triggers an event when the item receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)

  def isStackable(self):
    return True
