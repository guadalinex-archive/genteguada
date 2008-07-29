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
    
  def variablesToSerialize(self):
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

  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteInventory

  def setPlayer(self, player):
    self.__player = player
    
  def getPlayer(self):
    return self.__player  
  
  def clickedBy(self, clicker):
    """ Triggers an event when the item receives a click by a player.
    clicker: player who clicks.
    """
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    
  def isStackable(self):
    return True

  def stepOn(self):
    return True

#================================================================================

class PaperMoney(GGPickableItem):

  def __init__(self, spriteName, anchor, topAnchor, label, value):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    anchor: image anchor on screen.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
    value: item's value
    """
    GGPickableItem.__init__(self, spriteName, anchor, topAnchor, spriteName, label)
    self.points = value
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["money"]
    
  def addPointsTo(self, player):
    player.addPoints(self.points, self.label)  
    
#================================================================================

