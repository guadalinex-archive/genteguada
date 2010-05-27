# -*- coding: utf-8 -*- 

import dMVC.synchronized
import GG

class IsoView(dMVC.synchronized.Synchronized):
  """ IsoView Superclass.
  Defines attributes and methods for a generic view.
  """
  
  def __init__(self, model, screen):
    """ Class constructor.
    model: view model.
    screen: screen handler.
    """  
    self.__model = model
    self.__screen = screen
    self.__animation = None
    dMVC.synchronized.Synchronized.__init__(self)
    
  def __del__(self):
    """ Class destructor.
    """  
    if self.__animation:
      self.__animation.stop()
    
  def getModel(self):
    """ Returns the view model.
    """
    return self.__model
  
  def getScreen(self):
    """ Returns the screen handler.
    """
    return self.__screen

  def getAnimation(self):
    """ Returns the current animation.
    """
    return self.__animation

  def updateFrame(self, elapsedTime):
    """ Paints a new item frame on screen.
    elapsedTime: time since the animation beginning.
    """
    #ani = self.__animation
    if self.__animation:
      if self.__animation.isFinished(elapsedTime):
        self.setAnimation(None)
      else:  
        self.__animation.step(elapsedTime)
  
  def hasAnimation(self):
    """ Checks if there is an active animation.
    """
    return self.__animation != None
  
  @dMVC.synchronized.synchronized(lockName='animation')
  def setAnimation(self, anim=None):
    """ Creates a new position animation.
    anim: new position animation.
    """
    if self.__animation:
      self.__animation.stop()
    self.__animation = anim
    if anim != None:
      anim.start()
    
  def unsubscribeAllEvents(self):
    """ Unsubscribe this view's model from all events.
    """
    self.getModel().unsubscribeEventObserver(self)
    
  def stopAnimation(self):
    """ Stops the isometric view current animation.
    """  
    if self.__animation:
      self.__animation.stop()
