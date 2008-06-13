import os
import pygame
import GG.utils
import time

class Animation(object):
  """ Animation class.
  Defines animation methods and atributes.
  """
    
  def __init__(self, time, isoview, gentlyProgress=False):
    """ Class constructor.
    time: animation length in time.
    isoview: isoview used on the animation.
    """
    self.__startedTime = None
    self.time = time
    self.isoview = isoview  # public, to speed up the access
    self.__gentlyProgress = gentlyProgress
    self.__endMethods = []
    self.__startMethods = []
    

  def getLinearProgress(self, now):
    percent = (now - self.__startedTime) / self.time
    #if percent >= 1:
    #  return 1
    return percent

  def getGentlyProgress(self, now, lower=0.6, upper=0.85):
    x = self.getLinearProgress(now)

    uperSquared = upper * upper
    lowerPerUpper = lower * upper
    tmp = uperSquared - lowerPerUpper + lower - 1

    if x < lower:
      return ((upper - 1) / (lower *  tmp)) * x * x

    if x > upper:
      a3 = 1 / tmp
      b3 = -2 * a3
      c3 = 1 + a3
      return (a3 * x * x) + (b3 * x) + c3

    m = 2 * (upper - 1) / tmp
    b2 = (0 - m) * lower / 2
    return m * x + b2

  def getProgress(self, now):
    if self.__gentlyProgress:
      result = self.getGentlyProgress(now)
    else:
      result = self.getLinearProgress(now)

    if result <= 0:
      return 0
    if result >= 1:
      return 1

    return result


  def getEllapsedTime(self, now):
    return now - self.__startedTime


  
  def start(self):
    """ Starts the animation.
    """
    self.__startedTime = time.time() * 1000
    self.onStart()

  
  def step(self, now):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    pass

  
  def stop(self):
    """ Stops the animation.
    """  
    self.onStop()
  
    
  def setOnStart(self, method, params):
    self.__startMethods.append([method, params])

    
  def onStart(self):
    """ Method triggered on animation start.
    """
    for method in self.__startMethods:
      if method[1] == None:
        method[0]()
      else:    
        method[0](method[1])
  

  def setOnStop(self, method, params):
    self.__endMethods.append([method, params])

    
  def onStop(self):
    """ Method triggered on animation end.
    """
    for method in self.__endMethods:
      if method[1] == None:
        method[0]()
      else:    
        method[0](method[1])
    
    #if self.__endMethod != None:
    #  self.__endMethod(self.__endParams)
    
  def isFinished(self, now):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    return (now - self.__startedTime) >= self.time
    
#*****************************************************************************
    
class IdleAnimation(Animation):
  """ IdleAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self, time, isoview):
    """ Class constructor.
    time: animation length in time.
    isoview: isoview used on the animation.
    """
    Animation.__init__(self, time, isoview)
    
    
#*****************************************************************************
    
class ScreenPositionAnimation(Animation):
  """ PositionAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self, time, isoview, origin, destination, gentlyProgress=False):
    """ Class constructor.
    time: animation length in time.
    img: image used on the animation.
    destination: animation movement destination.
    """
    Animation.__init__(self, time, isoview, gentlyProgress)
    self.__originX = origin[0]
    self.__originY = origin[1]
    self.__destination = destination
    self.__shiftX = self.__destination[0] - self.__originX
    self.__shiftY = self.__destination[1] - self.__originY

    
  def start(self):
    """ Starts the animation.
    """
    super(self.__class__, self).start()
    self.isoview.setScreenPosition([self.__originX, self.__originY])
    
  def step(self, now):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    #super(self.__class__, self).step(now)
    percent = self.getProgress(now)
    self.isoview.setScreenPosition([self.__originX + int(self.__shiftX*percent),
                                    self.__originY + int(self.__shiftY*percent)])
      
  def stop(self):
    """ Stops the animation.
    """
    self.isoview.setScreenPosition([self.__destination[0], self.__destination[1]])
    #Animation.stop(self)
    super(self.__class__, self).stop()
    
  
#*****************************************************************************
    
class MovieAnimation(Animation):
  """ MovieAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self, time, isoview, frames):
    """ Class constructor.
    time: animation length in time.
    img: image used on the animation.
    frames: frames used on the animation.
    """
    Animation.__init__(self, time, isoview)
    self.setFrames(frames)
    
  def setFrames(self, frames):
    """ Sets a new frame set for the animation.
    frames: new frame set
    """
    self.__frames = frames
    self.loadSprites()  
    
  def loadSprites(self):
    self.__sprites = []
    for frame in self.__frames:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.isoview.getModel().imagePath + frame)
      self.__sprites.append(pygame.image.load(imgPath).convert_alpha())
      
    
  def step(self, now):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    #super(self.__class__, self).step(now)

    sprites = self.__sprites
    len_sprites = len(sprites)

    if len_sprites == 0:
      self.stop()
    else:
      time = self.time
      currentFrame = int((self.getEllapsedTime(now) % time) / time * len_sprites)
      self.isoview.setSprite(sprites[currentFrame])
    
  def isFinished(self, now):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    return False
  
#*****************************************************************************
    
class CompositionAnimation(Animation):
  """ CompositionAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self, time, isoview):
    """ Class constructor.
    time: animation length in time.
    img: image used on the animation.
    """
    Animation.__init__(self, time, isoview)
    
    
#*****************************************************************************
    
class SecuenceAnimation(CompositionAnimation):
  """ SecuenceAnimation class.
  Defines animation methods and atributes.
  """
  
  def __init__(self):
    """ Class constructor.
    """
    CompositionAnimation.__init__(self, 0, None)
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
    super(self.__class__, self).start()
    if len(self.__animations):
      self.__animations[0].start()
    
  def step(self, now):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    #super(self.__class__, self).step(now)
    if self.__animations:
      currentAnimation = self.__animations[0]
      if currentAnimation.isFinished(now):
        currentAnimation.stop()
        self.__animations.remove(currentAnimation)
        if self.__animations:
          self.__animations[0].start()
      else:
        currentAnimation.step(now)
    else:
      self.stop()
    
  def stop(self):
    """ Stops the animation.
    """  
    if len(self.__animations):
      self.__animations[0].stop()
    for animation in self.__animations:
      self.__animations.remove(animation)
    super(self.__class__, self).stop()
    
  def isFinished(self, now):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    len_animations = len(self.__animations)
    if len_animations > 1:
      return False
    elif len_animations == 0:
      return True
    else:
      return self.__animations[0].isFinished(now)

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
    super(self.__class__, self).start()
    for animation in self.__animations:
      animation.start()
    
  def step(self, now):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    #super(self.__class__, self).step(now)
    for animation in self.__animations:
      animation.step(now)
    
  def stop(self):
    """ Stops the animation.
    """  
    for animation in self.__animations:
      animation.stop()
    for animation in self.__animations:
      self.__animations.remove(animation)
    super(self.__class__, self).stop()
      
  def isFinished(self, now):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    for animation in self.__animations:    
      if not animation.isFinished(now):
        return False
    return True
