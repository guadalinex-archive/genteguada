import room_item
import GG.isoview.isoview_item

class GGGoldenKeyRoom2(room_item.GGRoomItem):
  """ GGGoldenKeyRoom2 class.
  Defines a pickable item behaviour.
  """
 
  def __init__(self, spriteName, position, offset, spriteInventory, label):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    offset: image offset on screen.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
    """
    room_item.GGRoomItem.__init__(self, spriteName, position, offset)
    self.spriteInventory = spriteInventory
    self.label = label
    
  def variablesToSerialize(self):
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["inventory"]

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
      #clicker.addInventory(self)
      #self.getRoom().removeItem(self)

