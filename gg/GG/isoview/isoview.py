import animation
import pygame
import GG.utils

class IsoView:
  """ IsoView Superclass.
  It defines attributes and methods for a generic view.
  """
  
  def __init__(self, model, screen):
    """ Class constructor.
    name: view name.
    """  
    self.__model = model
    self.__screen = screen
    self.__positionAnimation = None
    self.__positionClock = pygame.time.Clock()
    self.__positionTimePassed = 0
  
  def getModel(self):
    """ Returns the list of observed models.
    """
    return self.__model
  
  def getScreen(self):
    """ Returns the screen handler.
    """
    return self.__screen

  def getPositionAnimation(self):
    """ Returns the position animation.
    """
    return self.__positionAnimation
  
  def animationToInventory(self):
    """ Creates a new position animation, from the item's position to the inventory.
    """ 
    positionAnim = animation.PositionAnimation(GG.utils.ANIM_INVENTORY_TIME, self, GG.utils.INV_OR)
    self.setPositionAnimation(positionAnim)
    
  def updateFrame(self):
    """ Paints a new item frame on screen.
    """
    if self.__positionAnimation != None:
      self.__positionTimePassed += self.__positionClock.tick(50)
      if not self.__positionAnimation.isFinished(self.__positionTimePassed):
        self.__positionAnimation.step(self.__positionTimePassed)
      else:  
        self.setPositionAnimation(None)
  
  def activeAnimation(self):
    """ Checks if there is an active animation.
    """
    if self.__positionAnimation != None:
      return True
    return False
    
  def setPositionAnimation(self, animation):
    """ Creates a new position animation.
    animation: new position animation.
    """
    if self.__positionAnimation:
      self.__positionAnimation.stop()
    self.__positionAnimation = animation
    if animation != None:
      aux = self.__positionClock.tick()
      self.__positionTimePassed = 0
      animation.start()
    
  def animatedSetPosition(self, newPosition):
    """ Starts a new animation for the item.
    newPosition: new item position.
    """
    positionAnim = animation.PositionAnimation(GG.utils.ANIM_WALKING_TIME, self, GG.utils.p3dToP2d(newPosition, self.getModel().offset))
    self.setPositionAnimation(positionAnim)
    
  def unsubscribeAllEvents(self):
    """ Unsubscribe this view's model from all events.
    """
    self.getModel().unsubscribeEventObserver(self)
