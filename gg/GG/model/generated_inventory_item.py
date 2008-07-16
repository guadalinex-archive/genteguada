import ggmodel
import GG.utils
import inventory_item
import GG.isoview.isoview_item
import dMVC.model

class GGGeneratedInventoryItem(inventory_item.GGInventoryItem):
  """GGGeneratedInventoryItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, label, anchor, parentPosition):
    """ Class constructor.
    spriteName: image name.
    """
    inventory_item.GGInventoryItem.__init__(self, spriteName)
    self.spriteInventory = spriteName
    self.label = label
    self.points = 0
    self.anchor = anchor
    self.__position = parentPosition
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.inventory_item.GGInventoryItem.variablesToSerialize(self)
    return parentVars + ['label', 'points', 'spriteInventory']
      
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["removeInventory"]  

  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteInventory

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

