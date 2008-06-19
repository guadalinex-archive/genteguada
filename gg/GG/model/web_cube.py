import GG.model.room_item
import GG.isoview.isoview_item

class GGWebCube(GG.model.room_item.GGRoomItem):
  """ GGWebCube class.
  """
 
  def __init__(self, sprite, position, anchor, url, label):
    """ Class builder.
    sprite: sprite used to paint the cube.
    position: penguin position.
    anchor: image anchor on screen.
    url:
    """
    GG.model.room_item.GGRoomItem.__init__(self, sprite, position, anchor)
    self.url = url
    self.label = label
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['url' + 'label']
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["url"]
  
  def checkSimilarity(self, item):
    if GG.model.room_item.GGRoomItem.checkSimilarity(self, item):
      if item.url == self.url:
        return True
    return False   
  
  def checkCondition(self, condition, player):
    """ Checks a condition for a given player.
    condition: condition to check.
    player: given player.
    """
    return True

  def clickedBy(self, clicker):
    """ Triggers an event when the npc receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    