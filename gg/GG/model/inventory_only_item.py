import item
import GG.isoview.isoview_item

class GGInventoryOnlyItem(item.GGItem):
  """ GGInventoryOnlyItem class.
  Defines an inventory-only item behaviour.
  """
  
  def __init__(self, spriteName, label):
    """ Class builder.
    spriteName: inventory item sprite. 
    label: item labe.
    """
    item.GGItem.__init__(self, spriteName, [-1, -1, -1], [0, 0])
    self.spriteInventory = spriteName
    self.label = label
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = item.GGItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']