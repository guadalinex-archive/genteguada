import pickable_item
import GG.utils
import time
import pygame
import GG.isoview.isoview_item

class GGPersistentItem(pickable_item.GGPickableItem):
    
  def __init__(self, spriteName, position, offset, spriteInventory, label, numCopies):
    pickable_item.GGPickableItem.__init__(self, spriteName, position, offset, spriteInventory, label)
    self.__fullCopies = numCopies
    self.__numCopies = numCopies
    
  def getOptions(self):
    return ["clone"]
  
  def getClone(self):
    if self.__numCopies == 0:
      return None
    if self.__numCopies > 0:
      self.__numCopies -= 1
    #return GGPersistentItem(self.spriteName, self.getPosition(), self.offset, self.spriteInventory, self.label, self.__fullCopies)
    return pickable_item.GGPickableItem(self.spriteName, self.getPosition(), self.offset, self.spriteInventory, self.label)
    