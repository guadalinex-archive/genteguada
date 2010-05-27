# -*- coding: utf-8 -*-

import pygame
import GG
import os
import guiobjects

COLOR_SHIFT = 10

class Animation(object):
  """ Animation class.
  Defines animation methods and atributes.
  """
    
  def __init__(self, time, isoview, gentlyProgress=False):
    """ Class constructor.
    time: animation length.
    isoview: isoview used on the animation.
    gentlyProgress: indicates the animation speed variation.
    """
    self.__startedTime = None
    self.time = time
    self.isoview = isoview  # public, to speed up the access
    self.__gentlyProgress = gentlyProgress
    self.__endMethods = []
    self.__halfMethods = []
    self.__startMethods = []
    self.__pastHalf = 0
    
  def getLinearProgress(self, now):
    """ Returns the animation linear progression for any given time.
    now: time.
    """
    return (now - self.__startedTime) / self.time

  def getGentlyProgress(self, now, lower=0.6, upper=0.85):
    """ Returns the animation gently progression for any given time.
    now: time.
    lower: starting animation speed.
    upper: ending animation speed.
    """
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
    """ Returns the progression of the current animation.
    now: actual time.    
    """
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
    """ Ellapsed time on the current animation.
    now: actual time.
    """
    return now - self.__startedTime
  
  def start(self):
    """ Starts the animation.
    """
    self.__startedTime = float(pygame.time.get_ticks())
    self.onStart()
  
  def step(self, now):
    """ Progresses the animation one frame.
    now: elapsed time since the animation start.
    """
    if not self.__pastHalf:
      self.onHalf()
      self.__pastHalf = 1
  
  def stop(self):
    """ Stops the animation.
    """  
    self.onStop()
    
  def setOnStart(self, method, params):
    """ Adds a new method to be executed at animation start.
    method: method to be executed.
    params: method params.
    """  
    self.__startMethods.append([method, params])
    
  def onStart(self):
    """ Runs some methods at animation start.
    """
    for method in self.__startMethods:
      if method[1] == None:
        method[0]()
      else:    
        method[0](method[1])

  def setOnHalf(self, method, params):
    """ Adds a new method to be executed at animation half.
    method: method to be executed.
    params: method params.
    """  
    self.__halfMethods.append([method, params])
  
  def onHalf(self):
    """ Runs some methods at animation half.
    """
    for method in self.__halfMethods:
      if method[1] == None:
        method[0]()
      else:    
        method[0](method[1])

  def setOnStop(self, method, *args):
    """ Adds a new method to be executed at animation end.
    method: method to be executed.
    params: method params.
    """  
    self.__endMethods.append([method, args])
    
  def onStop(self):
    """ Runs some methods at animation end.
    """
    for method in self.__endMethods:
      if len(method[1]) == 1 and str(*method[1]) == "None":
        method[0]()
      else:    
        method[0](*method[1])
    
  def isFinished(self, now):
    """ Checks if the animation is finished.
    now: elapsed time since the animation start.
    """
    return (now - self.__startedTime) >= self.time
    
# ===============================================================
    
class IdleAnimation(Animation):
  """ IdleAnimation class.
  Defines static animation methods and atributes.
  """
  
  def __init__(self, time, isoview):
    """ Class constructor.
    time: animation length in time.
    isoview: isoview used on the animation.
    """
    Animation.__init__(self, time, isoview)

# ===============================================================
    
class ScreenPositionAnimation(Animation):
  """ PositionAnimation class.
  Defines position animation methods and atributes.
  """
  
  def __init__(self, time, isoview, origin, destination, gentlyProgress=False):
    """ Class constructor.
    time: animation length.
    isoview: isoview used on the animation.
    origin: animation starting position.
    destination: animation ending position.
    gentlyProgress: indicates the animation speed variation.
    """
    Animation.__init__(self, time, isoview, gentlyProgress)
    self.__originX = origin[0]
    self.__originY = origin[1]
    self.__destination = destination
    self.__shiftX = self.__destination[0] - self.__originX
    self.__shiftY = self.__destination[1] - self.__originY
    self.isoview.updateZOrder()
    
  def start(self):
    """ Starts the animation.
    """
    Animation.start(self)
    #self.isoview.setScreenPosition([self.__originX, self.__originY])
    
  def step(self, now):
    """ Progresses the animation.
    now: elapsed time since the animation start.
    """
    percent = self.getProgress(now)
    if percent > 0.5:
      Animation.step(self, now)
    self.isoview.setScreenPosition([self.__originX + int(self.__shiftX*percent),
                                    self.__originY + int(self.__shiftY*percent)])
      
  def stop(self):
    """ Stops the animation.
    """
    self.isoview.setScreenPosition([self.__destination[0], self.__destination[1]])
    Animation.stop(self)

# ===============================================================
    
class MovieAnimation(Animation):
  """ MovieAnimation class.
  Defines movie animation methods and atributes.
  """
  
  def __init__(self, time, isoview, frames, path):
    """ Class constructor.
    time: animation length.
    isoview: isoview used on the animation.
    frames: frames used on the animation.
    path: image path.
    """
    Animation.__init__(self, time, isoview)
    self.__frames = None
    self.__sprites = []
    self.setFrames(frames, path)
    
  def setFrames(self, frames, path):
    """ Sets a new frame set for the animation.
    frames: new frame set
    path: image path.
    """
    self.__frames = frames
    self.loadSprites(path)  
    
  def loadSprites(self, path):
    """ Loads a new sprite set using a previously provided frame list.    
    path: image path.
    """
    self.__sprites = []
    if path is None:
      path = self.isoview.getModel().getImagePath()
    for frame in self.__frames:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(path, frame))
      self.__sprites.append(pygame.image.load(imgPath).convert_alpha())
          
  def step(self, now):
    """ Progresses the animation.
    now: elapsed time since the animation start.
    """
    sprites = self.__sprites
    len_sprites = len(sprites)

    if len_sprites == 0:
      self.stop()
    else:
      time = self.time
      currentFrame = int((self.getEllapsedTime(now) % time) / time * len_sprites)
      self.isoview.setSprite(sprites[currentFrame])
    Animation.step(self, now)
    
  def isFinished(self, now):
    """ Checks if the animation is finished.
    time: elapsed time since the animation start.
    """
    return False
  
# ===============================================================
    
class CompositionAnimation(Animation):
  """ CompositionAnimation class.
  Defines composition animation methods and atributes.
  """
  
  def __init__(self, time, isoview):
    """ Class constructor.
    time: animation length.
    isoview: isoview used on the animation.
    """
    Animation.__init__(self, time, isoview)
    
# ===============================================================
    
class SecuenceAnimation(CompositionAnimation):
  """ SecuenceAnimation class.
  Defines sequence animation methods and attributes.
  """
  
  def __init__(self):
    """ Class constructor.
    """
    CompositionAnimation.__init__(self, 0, None)
    self.__animations = []
    
  def addAnimation(self, animation):
    """ Adds a new animation to the sequence.
    animation: new animation. 
    """
    self.__animations.append(animation)
  
  def removeAnimation(self, animation):
    """ Removes an animation from the sequence.
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
    
  def step(self, now):
    """ Progresses the animation.
    now: elapsed time since the animation start.
    """
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
    CompositionAnimation.step(self, now)  
    
  def stop(self):
    """ Stops the animation.
    """  
    if len(self.__animations):
      self.__animations[0].stop()
    for animation in self.__animations:
      animation.start()
      animation.stop()
      self.__animations.remove(animation)
    CompositionAnimation.stop(self)
    
  def isFinished(self, now):
    """ Checks if the animation is finished.
    now: current time.
    """
    len_animations = len(self.__animations)
    if len_animations > 1:
      return False
    elif len_animations == 0:
      return True
    else:
      return self.__animations[0].isFinished(now)

# ===============================================================
    
class ParalelAnimation(CompositionAnimation):
  """ ParalelAnimation class.
  Defines parallel animation methods and attributes.
  """
  
  def __init__(self):
    """ Class constructor.
    """
    CompositionAnimation.__init__(self, 0, None)
    self.__animations = []
    
  def addAnimation(self, animation):
    """ Adds a new animation to the sequence.
    animation: new animation. 
    """
    self.__animations.append(animation)
  
  def removeAnimation(self, animation):
    """ Removes an animation from the sequence.
    animation: animation to be removed. 
    """
    animation.stop()
    self.__animations.remove(animation)
    
  def start(self):
    """ Starts the animation.
    """
    for animation in self.__animations:
      animation.start()
    
  def step(self, now):
    """ Progresses the animation.
    now: elapsed time since the animation start.
    """
    for animation in self.__animations:
      animation.step(now)
    CompositionAnimation.step(self, now)  
    
  def stop(self):
    """ Stops the animation.
    """  
    for animation in self.__animations:
      animation.stop()
    for animation in self.__animations:
      animation.start()
      animation.stop()
      self.__animations.remove(animation)
      
  def isFinished(self, now):
    """ Checks if the animation is finished.
    now: current time.
    """
    for animation in self.__animations:    
      if not animation.isFinished(now):
        return False
    return True
