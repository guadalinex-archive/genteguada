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
    self.__animation = None
    self.__clock = pygame.time.Clock()
    
  def getModel(self):
    """ Returns the list of observed models.
    """
    return self.__model
  
  def getScreen(self):
    """ Returns the screen handler.
    """
    return self.__screen

  def getAnimation(self):
    """ Returns the animation.
    """
    return self.__animation

  def updateFrame(self, ellapsedTime):
    """ Paints a new item frame on screen.
    """
    if self.__animation:
      if self.__animation.isFinished(ellapsedTime):
        self.setAnimation(None)
      else:  
        self.__animation.step(ellapsedTime)
  
  def hasAnimation(self):
    """ Checks if there is an active animation.
    """
    return self.__animation != None
    
  def setAnimation(self, animation):
    """ Creates a new position animation.
    animation: new position animation.
    """
    if self.__animation:
      self.__animation.stop()
    self.__animation = animation
    if animation:
      animation.start()
    
  def unsubscribeAllEvents(self):
    """ Unsubscribe this view's model from all events.
    """
    self.getModel().unsubscribeEventObserver(self)
    
  
