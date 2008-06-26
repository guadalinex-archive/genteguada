import ggmodel
import GG.utils
import inventory_item
import GG.isoview.isoview_item
import dMVC.model

class GGGiftInventory(inventory_item.GGInventoryItem):
  """GGGiftInventory class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, label, anchor, parentPosition):
    """ Class constructor.
    spriteName: image name.
    """
    inventory_item.GGInventoryItem.__init__(self, spriteName)
    self.label = label
    self.points = 0
    self.anchor = anchor
    self.__position = parentPosition
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.inventory_item.GGInventoryItem.variablesToSerialize(self)
    #return parentVars + ['label', 'points', 'anchor']
    return parentVars + ['label', 'points']

  def getPosition(self):
    return self.__position

  def setPoints(self, points):
    self.points = points
  
  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    """
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)
    #return GG.isoview.isoview_inventoryitem.IsoViewInventoryItem(self, screen, parent)
  
  def checkSimilarity(self, item):
    if inventory_item.GGInventoryItem.checkSimilarity(self, item):
      if item.label == self.label:
        if item.points == self.points:
          return True
    return False   
  
  def inventoryOnly(self):
    return True
  
  def tick(self, now):
    """ Call for an update on item.
    Not used at the moment.
    """
    pass
  
  def isStackable(self):
    return False

