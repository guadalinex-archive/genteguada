import GG.model.room_item
import GG.isoview.isoview_item

class GGWebPannel(GG.model.room_item.GGRoomItem):
  """ GGWebPannel class.
  """
 
  def __init__(self, sprite, anchor, topAnchor, url, label):
    """ Class builder.
    sprite: sprite used to paint the cube.
    position: penguin position.
    anchor: image anchor on screen.
    url:
    """
    GG.model.room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor)
    self.url = url
    self.label = label
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['url', 'label']
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["url"]
      
  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteName
  
  def checkSimilarity(self, item):
    if GG.model.room_item.GGRoomItem.checkSimilarity(self, item):
      if item.url == self.url:
        return True
    return False   
  
  def clickedBy(self, clicker):
    """ Triggers an event when the npc receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItemWithoutHighlight(self)
    else:
      return False    
