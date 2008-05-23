import item
import GG.isoview.isoview_item

class GGInventoryOnlyItem(item.GGItem):
  
  def __init__(self, spriteName, label):
    item.GGItem.__init__(self, spriteName, [-1, -1, -1], [0, 0])
    self.spriteInventory = spriteName
    self.label = label
    
  def variablesToSerialize(self):
    parentVars = item.GGItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']