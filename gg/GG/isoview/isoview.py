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
    self.__timePassed = 0
    
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

  def updateFrame(self):
    """ Paints a new item frame on screen.
    """
    if self.__animation != None:
      self.__timePassed += self.__clock.tick(50)
      if not self.__animation.isFinished(self.__timePassed):
        self.__animation.step(self.__timePassed)
      else:  
        self.setAnimation(None)
  
  def activeAnimation(self):
    """ Checks if there is an active animation.
    """
    if self.__animation != None:
      return True
    return False
    
  def setAnimation(self, animation):
    """ Creates a new position animation.
    animation: new position animation.
    """
    if self.__animation:
      self.__animation.stop()
    self.__animation = animation
    if animation != None:
      aux = self.__clock.tick()
      self.__timePassed = 0
      animation.start()
    
  def unsubscribeAllEvents(self):
    """ Unsubscribe this view's model from all events.
    """
    self.getModel().unsubscribeEventObserver(self)
    
  