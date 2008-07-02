import ggmodel
import GG.utils
import inventory_item
import GG.isoview.isoview_item
import dMVC.model

class GGGoldenKey(inventory_item.GGInventoryItem):
  """GGGoldenKey class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, label, position):
    """ Class constructor.
    sprite: image name.
    position: position on screen for the item.
    anchor: anchor for that position.
    """
    inventory_item.GGInventoryItem.__init__(self, spriteName)
    self.label = label
    self.anchor = [20, -40]
    self.__position = position
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.inventory_item.GGInventoryItem.variablesToSerialize(self)
    return parentVars + ['label', 'anchor']
      
  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteName
  
  def getPosition(self):
    return self.__position    
  
  def checkSimilarity(self, item):
    if inventory_item.GGInventoryItem.checkSimilarity(self, item):
      if item.label == self.label:
        return True
    return False   
  
  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    """
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)
  
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    pass
    
  def tick(self, now):
    """ Call for an update on item.
    Not used at the moment.
    """
    pass
  