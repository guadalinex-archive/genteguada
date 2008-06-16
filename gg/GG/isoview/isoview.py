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
    
  def __del__(self):
    if self.__animation:
      self.__animation.stop()
    
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
    ani = self.__animation
    if ani:
      if ani.isFinished(ellapsedTime):
        self.setAnimation(None)
      else:  
        ani.step(ellapsedTime)
  
  def hasAnimation(self):
    """ Checks if there is an active animation.
    """
    return self.__animation != None
    
  def setAnimation(self, animation=None):
    """ Creates a new position animation.
    animation: new position animation.
    """
    if self.__animation:
      self.__animation.stop()
    self.__animation = animation
    if animation != None:
      animation.start()
    
  def unsubscribeAllEvents(self):
    """ Unsubscribe this view's model from all events.
    """
    self.getModel().unsubscribeEventObserver(self)
    
  def stopAnimation(self):
    if self.__animation:
      self.__animation.stop()
  
