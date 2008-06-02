import os
import pygame
import GG.utils

class Animation:
  """ Animation class.
  Defines animation methods and atributes.
  """
    
  def __init__(self, time, img):
    """ Class constructor.
    time: animation length in time.
    img: image used on the animation.
    """
    self.__time = time
    self.__img = img

  def getTime(self):
    """ Returns the animation length in time.
    """
    return self.__time
  
  def getImg(self):
    """ Returns the sprite used on the animation.
    """
    return self.__img

  def setImgPosition(self, pos):
    """ Sets a new position for the image.
    pos: image position.
    """
    self.__img.rect.topleft = pos

  def setImgSprite(self, imgPath):
    """ Sets a new sprite for the image.
    imgPath: image path.
    """
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    
  # Vanilla methods
  
  def start(self):
    """ Starts the animation.
    """
    self.onStart()
  
  def step(self, time):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    pass
  
  def stop(self):
    """ Stops the animation.
    """  
    self.onEnd()
  
  def onStart(self):
    """ Method triggered on animation start.
    """
    pass
  
  def onEnd(self):
    """ Method triggered on animation end.
    """
    pass
    
  def isFinished(self, time):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    return (self.__time < time)
    
#*****************************************************************************
    
class IdleAnimation(Animation):
  """ IdleAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self, time, img, frame):
    """ Class constructor.
    time: animation length in time.
    img: image used on the animation.
    frame: frame used for the animation.
    """
    Animation.__init__(self, time, img)
    self.__frame = frame
    
  def start(self):
    """ Starts the animation.
    """
    Animation.start(self)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.__frame)    
    self.setImgSprite(imgPath)
    
  def step(self, time):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    Animation.step(self, time)
    
  def stop(self):
    """ Stops the current animation.
    """
    Animation.stop(self)
    self.onEnd()
  
  def onStart(self):
    """ Method triggered on animation start.
    """
    Animation.onStart(self)
  
  def onEnd(self):
    """ Method triggered on animation end.
    """
    Animation.onEnd(self)
    
  def isFinished(self, time):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    return Animation.isFinished(self, time) 
    
#*****************************************************************************
    
class PositionAnimation(Animation):
  """ PositionAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self, time, img, destination):
    """ Class constructor.
    time: animation length in time.
    img: image used on the animation.
    destination: animation movement destination.
    """
    Animation.__init__(self, time, img)
    self.__origin = self.getImg().rect.topleft
    self.__destination = destination
    self.__shift = [self.__destination[0] - self.__origin[0], self.__destination[1] - self.__origin[1]]
    
  def start(self):
    """ Starts the animation.
    """
    Animation.start(self)
    self.setImgPosition([self.__origin[0], self.__origin[1]])
    self.onStart()
    
  def step(self, time):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    Animation.step(self, time)
    percent = ((time*100)/self.getTime())/100.0
    self.setImgPosition([self.__origin[0] + (self.__shift[0]*percent), self.__origin[1] + (self.__shift[1]*percent)])
      
  def stop(self):
    """ Stops the animation.
    """  
    Animation.stop(self)
    self.setImgPosition([self.__destination[0], self.__destination[1]])
    self.onEnd()
    
  def onStart(self):
    """ Method triggered on animation start.
    """
    Animation.onStart(self)
  
  def onEnd(self):
    """ Method triggered on animation end.
    """
    Animation.onEnd(self)
    
  def isFinished(self, time):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    return Animation.isFinished(self, time)
  
#*****************************************************************************
    
class MovieAnimation(Animation):
  """ MovieAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self, time, img, frames):
    """ Class constructor.
    time: animation length in time.
    img: image used on the animation.
    frames: frames used on the animation.
    """
    Animation.__init__(self, time, img)
    self.__frames = frames
    
  def setFrames(self, frames):
    """ Sets a new frame set for the animation.
    frames: new frame set
    """
    self.__frames = frames  
    
  def start(self):
    """ Starts the animation.
    """
    Animation.start(self)
    
  def step(self, time):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    Animation.step(self, time)
    percent = ((time*100)/self.getTime())
    filename = self.__frames[percent % len(self.__frames)]
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(filename)    
    self.setImgSprite(imgPath)
    
  def stop(self):
    """ Stops the animation.
    """  
    Animation.stop(self)
    self.onEnd()
  
  def onStart(self):
    """ Method triggered on animation start.
    """
    Animation.onStart(self)
  
  def onEnd(self):
    """ Method triggered on animation end.
    """
    Animation.onEnd(self)
    
  def isFinished(self, time):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    return False
  
#*****************************************************************************
    
class CompositionAnimation(Animation):
  """ CompositionAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self, time, img):
    """ Class constructor.
    time: animation length in time.
    img: image used on the animation.
    """
    Animation.__init__(self, time, img)
    
  def start(self):
    """ Starts the animation.
    """
    Animation.start(self)
    
  def step(self, time):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    Animation.step
    
  def stop(self):
    """ Stops the animation.
    """  
    Animation.stop(self)
  
  def onStart(self):
    """ Method triggered on animation start.
    """
    Animation.onStart(self)
  
  def onEnd(self):
    """ Method triggered on animation end.
    """
    Animation.onEnd(self)
    
  def isFinished(self, time):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    return Animation.isFinished(self, time)
    
#*****************************************************************************
    
class SecuenceAnimation(CompositionAnimation):
  """ SecuenceAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self):
    """ Class constructor.
    """
    self.__animations = []
    
  def addAnimation(self, animation):
    """ Adds a new animation to the secuence.
    animation: new animation. 
    """
    self.__animations.append(animation)
  
  def removeAnimation(self, animation):
    """ Removes an animation from the secuence.
    animation: animation to be removed. 
    """
    animation.stop()
    self.__animations.remove(animation)
  
  def start(self):
    """ Starts the animation.
    """
    CompositionAnimation.start(self)
    if len(self.__animations):
      self.__animations[0].start()
    
  def step(self, time):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    CompositionAnimation.step(self, time)
    if len(self.__animations):
      if self.__animations[0].isFinished(time):
        self.__animations[0].stop()
        self.__animations.remove(self.__animations[0])
        if len(self.__animations):
          self.__animations[0].start()
          self.__animations[0].step(time)
      else:
        self.__animations[0].step(time)
    
  def stop(self):
    """ Stops the animation.
    """  
    CompositionAnimation.stop(self)
    if len(self.__animations):
      self.__animations[0].stop()
    for animation in self.__animations:
      self.__animations.remove(animation)
    
  def onStart(self):
    """ Method triggered on animation start.
    """
    CompositionAnimation.onStart(self)
  
  def onEnd(self):
    """ Method triggered on animation end.
    """
    CompositionAnimation.onEnd(self)
    
  def isFinished(self, time):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    if len(self.__animations) > 1:
      return False
    elif len(self.__animations) == 0:
      return True
    else:
      return self.__animations[0].isFinished(time)
        
#*****************************************************************************
    
class ParalelAnimation(CompositionAnimation):
  """ ParalelAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self):
    """ Class constructor.
    """
    self.__animations = []
    
  def addAnimation(self, animation):
    """ Adds a new animation to the secuence.
    animation: new animation. 
    """
    self.__animations.append(animation)
  
  def removeAnimation(self, animation):
    """ Removes an animation from the secuence.
    animation: animation to be removed. 
    """
    animation.stop()
    self.__animations.remove(animation)
    
  def start(self):
    """ Starts the animation.
    """
    CompositionAnimation.start(self)
    for animation in self.__animations:
      animation.start()
    
  def step(self, time):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    CompositionAnimation.step(self, time)
    for animation in self.__animations:
      animation.step(time)
    
  def stop(self):
    """ Stops the animation.
    """  
    CompositionAnimation.stop(self)
    for animation in self.__animations:
      animation.stop()
    for animation in self.__animations:
      self.__animations.remove(animation)
      
  def onStart(self):
    """ Method triggered on animation start.
    """
    CompositionAnimation.onStart(self)
  
  def onEnd(self):
    """ Method triggered on animation end.
    """
    CompositionAnimation.onEnd(self)
    
  def isFinished(self, time):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    for animation in self.__animations:    
      if not animation.isFinished(time):
        return False
    return True  
    


