import pickable_item
import GG.utils
import time
import GG.isoview.isoview_item

class GGPersistentItem(pickable_item.GGPickableItem):
  """ GGPersistentItem class.
  Defines a persistent item behaviour.
  """ 
    
  def __init__(self, spriteName, position, offset, spriteInventory, label, numCopies):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    offset: image offset on screen.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
    numCopies: max copies number.
    """
    pickable_item.GGPickableItem.__init__(self, spriteName, position, offset, spriteInventory, label)
    self.__fullCopies = numCopies
    self.__numCopies = numCopies
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["clone"]
  
  def getClone(self):
    """ Returns a clone of this item if possible.
    """
    if self.__numCopies == 0:
      return None
    if self.__numCopies > 0:
      self.__numCopies -= 1
    #return GGPersistentItem(self.spriteName, self.getPosition(), self.offset, self.spriteInventory, self.label, self.__fullCopies)
    return pickable_item.GGPickableItem(self.spriteName, self.getPosition(), self.offset, self.spriteInventory, self.label)
    
