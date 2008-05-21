import GG.utils

class Animation:
  """ Animation class.
  Defines animation methods and atributes.
  """
    
  def __init__(self, time, img, destination):
    """ Class constructor.
    time: animation length in time.
    img: sprite used for the animation.
    destination: animation destination.
    """
    self.__time = time
    self.__img = img
    self.__origin = img.rect.topleft
    self.__destination = destination
    
  def getTime(self):
    return self.__time
  
  def getImg(self):
    return self.__img
  
  def getOrigin(self):
    return self.__origin
  
  def getDestination(self):
    return self.__destination

  def setImgPosition(self, pos):
    self.__img.rect.topleft = pos

  # Vanilla methods
  
  def start(self):
    pass
  
  def step(self, time):
    pass
  
  def stop(self):
    pass
  
  def onStart(self):
    pass
  
  def onEnd(self):
    pass
    
  def isFinished(self, time):
    return (self.__time < time)
    
#*****************************************************************************
    
class PositionAnimation(Animation):
  
  def __init__(self, time, img, destination):
    Animation.__init__(self, time, img, destination)
    self.__shift = [self.getDestination()[0] - self.getOrigin()[0], self.getDestination()[1] - self.getOrigin()[1]]
    
  def start(self):
    Animation.start(self)
    self.setImgPosition([self.getOrigin()[0], self.getOrigin()[1]])
    self.onStart()
    
  def step(self, time):
    """ Moves the sprite to the next frame position.
    time: time passed since the animation start.
    """
    Animation.step(self, time)
    percent = ((time*100)/GG.utils.ANIM_TIME)/100.0
    self.setImgPosition([self.getOrigin()[0] + (self.__shift[0]*percent), self.getOrigin()[1] + (self.__shift[1]*percent)])
      
  def stop(self):
    Animation.stop(self)
    self.setImgPosition([self.getDestination()[0], self.getDestination()[1]])
    self.onEnd()
    
  def onStart(self):
    Animation.onStart(self)
  
  def onEnd(self):
    Animation.onEnd(self)
    
  def isFinished(self, time):
    return Animation.isFinished(self, time)
    
#*****************************************************************************
    
class MovieAnimation(Animation):
  
  def __init__(self, time, img, destination):
    Animation.__init__(self, time, img, destination)
    
  def start(self):
    Animation.start(self)
    
  def step(self, time):
    Animation.step
    
  def stop(self):
    Animation.stop(self)
  
  def onStart(self):
    Animation.onStart(self)
  
  def onEnd(self):
    Animation.onEnd(self)
    
  def isFinished(self, time):
    return Animation.isFinished(self, time)

#*****************************************************************************
    
class CompositionAnimation(Animation):
  
  def __init__(self, time, img, destination):
    Animation.__init__(self, time, img, destination)
    
  def start(self):
    Animation.start(self)
    
  def step(self, time):
    Animation.step
    
  def stop(self):
    Animation.stop(self)
  
  def onStart(self):
    Animation.onStart(self)
  
  def onEnd(self):
    Animation.onEnd(self)
    
  def isFinished(self, time):
    return Animation.isFinished(self, time)
    
#*****************************************************************************
    
class SequenceAnimation(CompositionAnimation):
  
  def __init__(self, time, img, destination):
    CompositionAnimation.__init__(self, time, img, destination)
    
  def start(self):
    CompositionAnimation.start(self)
    
  def step(self, time):
    CompositionAnimation.step
    
  def stop(self):
    CompositionAnimation.stop(self)
  
  def onStart(self):
    CompositionAnimation.onStart(self)
  
  def onEnd(self):
    CompositionAnimation.onEnd(self)
    
  def isFinished(self, time):
    return CompositionAnimation.isFinished(self, time)
    
#*****************************************************************************
    
class ParalelAnimation(CompositionAnimation):
  
  def __init__(self, time, img, destination):
    CompositionAnimation.__init__(self, time, img, destination)
    
  def start(self):
    CompositionAnimation.start(self)
    
  def step(self, time):
    CompositionAnimation.step
    
  def stop(self):
    CompositionAnimation.stop(self)
  
  def onStart(self):
    CompositionAnimation.onStart(self)
  
  def onEnd(self):
    CompositionAnimation.onEnd(self)
    
  def isFinished(self, time):
    return CompositionAnimation.isFinished(self, time)
    


