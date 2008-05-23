import pickable_item
import GG.utils
import time
import pygame
import GG.isoview.isoview_item

class GGTempPickableItem(pickable_item.GGPickableItem):
    
  def __init__(self, spriteName, position, offset, spriteInventory, label, time):
    pickable_item.GGPickableItem.__init__(self, spriteName, position, offset, spriteInventory, label)
    self.__time = time*1000
    self.__elapsedTime = 0
    self.__clock = pygame.time.Clock()
  
  def tick(self):
    if self.__elapsedTime:
      print self.__elapsedTime
      self.__elapsedTime += self.__clock.tick()
      #if self.timeLeft():
  
  def startCount(self):
    self.__elapsedTime = self.__clock.tick()
    self.__elapsedTime = 1
      
  def timeLeft(self):
    if self.__time > self.__elapsedTime:
      return True
    else:
      return False
    
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.item.GGItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    
  