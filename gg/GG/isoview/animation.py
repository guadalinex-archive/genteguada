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
    img: sprite used for the animation.
    destination: animation destination.
    """
    self.__time = time
    self.__img = img

  def getTime(self):
    return self.__time
  
  def getImg(self):
    return self.__img

  def setImgPosition(self, pos):
    self.__img.rect.topleft = pos

  def setImgSprite(self, imgPath):
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    
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
    
class IdleAnimation(Animation):
  
  def __init__(self, time, img, frame):
    Animation.__init__(self, time, img)
    self.__frame = frame
    
  def start(self):
    Animation.start(self)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.__frame)    
    self.setImgSprite(imgPath)
    
  def step(self, time):
    Animation.step(self, time)
    
  def stop(self):
    Animation.stop(self)
    self.onEnd()
  
  def onStart(self):
    Animation.onStart(self)
  
  def onEnd(self):
    Animation.onEnd(self)
    
  def isFinished(self, time):
    return Animation.isFinished(self, time) 
    
#*****************************************************************************
    
class PositionAnimation(Animation):
  
  def __init__(self, time, img, destination):
    Animation.__init__(self, time, img)
    self.__origin = self.getImg().rect.topleft
    self.__destination = destination
    self.__shift = [self.__destination[0] - self.__origin[0], self.__destination[1] - self.__origin[1]]
    
  def start(self):
    Animation.start(self)
    self.setImgPosition([self.__origin[0], self.__origin[1]])
    self.onStart()
    
  def step(self, time):
    Animation.step(self, time)
    percent = ((time*100)/self.getTime())/100.0
    self.setImgPosition([self.__origin[0] + (self.__shift[0]*percent), self.__origin[1] + (self.__shift[1]*percent)])
      
  def stop(self):
    Animation.stop(self)
    self.setImgPosition([self.__destination[0], self.__destination[1]])
    self.onEnd()
    
  def onStart(self):
    Animation.onStart(self)
  
  def onEnd(self):
    Animation.onEnd(self)
    
  def isFinished(self, time):
    return Animation.isFinished(self, time)
  
#*****************************************************************************
    
class MovieAnimation(Animation):
  
  def __init__(self, time, img, frames):
    Animation.__init__(self, time, img)
    self.__frames = frames
    
  def setFrames(self, frames):
    self.__frames = frames  
    
  def start(self):
    Animation.start(self)
    
  def step(self, time):
    Animation.step(self, time)
    percent = ((time*100)/self.getTime())
    filename = self.__frames[percent % len(self.__frames)]
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(filename)    
    self.setImgSprite(imgPath)
    
  def stop(self):
    Animation.stop(self)
    self.onEnd()
  
  def onStart(self):
    Animation.onStart(self)
  
  def onEnd(self):
    Animation.onEnd(self)
    
  def isFinished(self, time):
    return False
  
#*****************************************************************************
    
class CompositionAnimation(Animation):
  
  def __init__(self, time, img):
    Animation.__init__(self, time, img)
    
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
    
class SecuenceAnimation(CompositionAnimation):
  
  def __init__(self):
    self.__animations = []
    
  def addAnimation(self, animation):
    self.__animations.append(animation)
  
  def removeAnimation(self, animation):
    animation.stop()
    self.__animations.remove(animation)
  
  def start(self):
    CompositionAnimation.start(self)
    if len(self.__animations):
      self.__animations[0].start()
    
  def step(self, time):
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
    CompositionAnimation.stop(self)
    if len(self.__animations):
      self.__animations[0].stop()
    for animation in self.__animations:
      self.__animations.remove(animation)
    
  def onStart(self):
    CompositionAnimation.onStart(self)
  
  def onEnd(self):
    CompositionAnimation.onEnd(self)
    
  def isFinished(self, time):
    if len(self.__animations) > 1:
      return False
    elif len(self.__animations) == 0:
      return True
    else:
      return self.__animations[0].isFinished(time)
        
#*****************************************************************************
    
class ParalelAnimation(CompositionAnimation):
  
  def __init__(self):
    self.__animations = []
    
  def addAnimation(self, animation):
    self.__animations.append(animation)
  
  def removeAnimation(self, animation):
    animation.stop()
    self.__animations.remove(animation)
    
  def start(self):
    CompositionAnimation.start(self)
    for animation in self.__animations:
      animation.start()
    
  def step(self, time):
    CompositionAnimation.step(self, time)
    for animation in self.__animations:
      animation.step(time)
    
  def stop(self):
    CompositionAnimation.stop(self)
    for animation in self.__animations:
      animation.stop()
    for animation in self.__animations:
      self.__animations.remove(animation)
      
  def onStart(self):
    CompositionAnimation.onStart(self)
  
  def onEnd(self):
    CompositionAnimation.onEnd(self)
    
  def isFinished(self, time):
    for animation in self.__animations:    
      if not animation.isFinished(time):
        return False
    return True  
    


