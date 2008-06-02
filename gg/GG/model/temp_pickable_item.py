import pickable_item
import GG.utils
import time
import pygame
import GG.isoview.isoview_item

class GGTempPickableItem(pickable_item.GGPickableItem):
  """ TempPickableItem class.
  Defines a temporary pickable item behaviour.
  """
    
  def __init__(self, spriteName, position, offset, spriteInventory, label, time, startRoom):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    offset: image offset on screen.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
    time: item's life time.
    startRoom: item's starting room.
    """
    pickable_item.GGPickableItem.__init__(self, spriteName, position, offset, spriteInventory, label)
    self.__time = time*1000
    self.__elapsedTime = 0
    self.__clock = pygame.time.Clock()
    self.__startRoom = startRoom
  
  def getStartRoom(self):
    """ Returns the item's starting room.
    """
    return self.__startRoom

  def setStartRoom(self, room):
    """ Sets a new item's starting room.
    room: new starting room.
    """
    self.__startRoom = room
  
  def tick(self):
    """ Call for an update on item.
    """
    if self.__elapsedTime:
      self.__elapsedTime += self.__clock.tick()
      #if self.timeLeft():
  
  def startCount(self):
    """ Starts the item time count.
    """
    self.__elapsedTime = self.__clock.tick()
    self.__elapsedTime = 1
      
  def timeLeft(self):
    """ Returns the item's time left.
    """
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
    
  