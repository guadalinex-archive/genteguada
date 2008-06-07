import os
import pygame
import GG.utils
import time

class Animation(object):
  """ Animation class.
  Defines animation methods and atributes.
  """
    
  def __init__(self, time, isoview):
    """ Class constructor.
    time: animation length in time.
    isoview: isoview used on the animation.
    """
    self.__startedTime = None
    self.__time = time
    self.__isoview = isoview
    self.__endMethods = []
    self.__startMethods = []
    

  def getProgress(self, now):
    percent = (now - self.__startedTime) / self.__time
    if percent >= 1:
      return 1
    return percent


  def getTime(self):
    return self.__time


  def getEllapsedTime(self, now):
    return now - self.__startedTime


  def getIsoview(self):
    """ Returns the sprite used on the animation.
    """
    return self.__isoview

  
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
    return (now - self.__startedTime) >= self.__time
    
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
  
  def __init__(self, time, isoview, origin, destination):
    """ Class constructor.
    time: animation length in time.
    img: image used on the animation.
    destination: animation movement destination.
    """
    Animation.__init__(self, time, isoview)
    self.__origin = origin
    self.__destination = destination
    self.__shift = [self.__destination[0] - self.__origin[0], self.__destination[1] - self.__origin[1]]

  def setScreenPosition(self, pos):
    self.getIsoview().setScreenPosition(pos)
    
  def start(self):
    """ Starts the animation.
    """
    super(self.__class__, self).start()
    self.setScreenPosition([self.__origin[0], self.__origin[1]])
    
  def step(self, now):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    #super(self.__class__, self).step(now)
    percent = self.getProgress(now)
    self.setScreenPosition([self.__origin[0] + int(self.__shift[0]*percent),
                            self.__origin[1] + int(self.__shift[1]*percent)])
      
  def stop(self):
    """ Stops the animation.
    """
    self.setScreenPosition([self.__destination[0], self.__destination[1]])
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
    #print "load sprites"
    self.__sprites = []
    for frame in self.__frames:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.getIsoview().getModel().imagePath + frame)
      self.__sprites.append(pygame.image.load(imgPath).convert_alpha())
      
    
  def step(self, now):
    """ Progresses the animation one frame.
    time: elapsed time since the animation start.
    """
    #super(self.__class__, self).step(now)
    if len(self.__sprites) == 0:
      print "me paro"
      self.stop()
    else:
      time = self.getTime()
      currentFrame = int((self.getEllapsedTime(now) % time) / time * len(self.__sprites))
      self.getIsoview().setSprite(self.__sprites[currentFrame])
    
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
    self.__accumulatedTime = 0
    
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
    if len(self.__animations):
      if self.__animations[0].isFinished(now - self.__accumulatedTime):
        self.__accumulatedTime = now  
        self.__animations[0].stop()
        self.__animations.remove(self.__animations[0])
        if len(self.__animations):
          self.__animations[0].start()
      else:
        self.__animations[0].step(now - self.__accumulatedTime)
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
    if len(self.__animations) > 1:
      return False
    elif len(self.__animations) == 0:
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
