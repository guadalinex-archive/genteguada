import item
import GG.isoview.isoview_item

class GGInventoryOnlyItem(item.GGItem):
  """ GGInventoryOnlyItem class.
  Defines an inventory-only item behaviour.
  """
  
  def __init__(self, spriteName, position, label):
    """ Class builder.
    spriteName: inventory item sprite. 
    label: item labe.
    """
    item.GGItem.__init__(self, spriteName, position, [0, 0])
    self.spriteInventory = spriteName
    self.label = label
    self.__player = None
    
  def setPlayer(self, player):
    self.__player = player
    
  def getPlayer(self):
    return self.__player  
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = item.GGItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']