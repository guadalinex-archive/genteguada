import isoview_item
import isoview
import GG.utils
import animation
import pygame

class IsoViewPlayer(isoview_item.IsoViewItem):
  """ IsoViewPlayer class.
  Defines a player view.
  """
  
  def __init__(self, model, screen, room, parent):
    """ Class constructor.
    model: observed object.
    screen: screen handler.
    room: the room where the player is.
    parent: isoview_hud handler.
    """
    isoview_item.IsoViewItem.__init__(self, model, screen, room, parent)
    self.__movieAnimation = None
    self.__destination = None
    self.__timestamp = model.getTimestamp()
    self.setImg(GG.utils.getSpriteName(model.getState(), model.getHeading(), 0, self.__timestamp))
    self.getModel().subscribeEvent('heading', self.headingChanged)
    self.getModel().subscribeEvent('state', self.stateChanged)
    self.getModel().subscribeEvent('jump', self.onJump)
    self.getModel().subscribeEvent('jumpOver', self.onJumpOver)
    self.getModel().subscribeEvent('avatarConfiguration', self.avatarConfigurationChanged)
    self.getModel().subscribeEvent('timestamp', self.timestampChanged)
    self.getModel().subscribeEvent('destination', self.destinationChanged)
    self.__heading = self.getModel().getHeading()

  def __del__(self):
    """ Class destructor.
    """  
    isoview.IsoView.__del__(self)
    if self.__movieAnimation:
      self.__movieAnimation.stop()

  def avatarConfigurationChanged(self, event):
    """ Unfinished method.
    event: event info.
    """  
    print "cambio la configuracion del jugador"

  def timestampChanged(self, event):
    """ Triggers after receiving a timestamp changed method.
    event: event info.
    """  
    timestamp = event.getParams()["timestamp"]
    self.__timestamp = timestamp
    self.getModel().imagePath = event.getParams()["imgPath"]

  def headingChanged(self, event):
    """ Changes the player's sprite heading.
    event: event info.
    """
    self.__heading = event.getParams()["heading"]
    if self.__movieAnimation != None:
      frames = self.createFrameSet()
      self.__movieAnimation.setFrames(frames)
    else:
      str = GG.utils.getSpriteName(event.getParams()["state"], event.getParams()["heading"], 0, self.__timestamp)
      self.setImg(str)
    
  def inventoryAdded(self, event):
    """ Triggers after receiving an inventory added event.
    event: event info.
    """
    self.getParent().addInventoryItem(event.getParams()["item"])
    
  def inventoryRemoved(self, event):
    """ Triggers after receiving an inventory removed event.
    event: event info.
    """
    self.getParent().removeInventoryItem(event.getParams()["item"])

  def hasMovieAnimation(self):
    """ Checks if there is an active animation.
    """
    return self.__movieAnimation != None
      
  def setMovieAnimation(self, animation=None):
    """ Creates a new movie animation.
    animation: new movie animation.
    """
    if self.__movieAnimation:
      self.__movieAnimation.stop()
    self.__movieAnimation = animation
    if animation != None:
      animation.start()
    
  def setMovieFrames(self, frames):
    """ Sets a new frame set for a movie animation.
    frames: new frame set.
    """
    self.__movieAnimation.setFrames(frames)
        
  def createFrameSet(self,dataState = None):
    """ Creates a new frame set.
    state: player's state.
    """
    frames = []
    if dataState:
      state = dataState
    else:
      state = self.getModel().getState()
    if state == GG.utils.STATE[1] or state == GG.utils.STATE[3] or state == GG.utils.STATE[5]:
      string = GG.utils.getSpriteName(state, self.__heading, 0,self.__timestamp)
      frames.append(string)        
    else:
      for i in range(1, GG.utils.ANIM_WALKING_COUNT+1):
        string = GG.utils.getSpriteName(state, self.__heading, i,self.__timestamp)  
        frames.append(string)        
    return frames
    
  def animatedSetPosition(self, newPosition):
    """ Sets a new position for the player and creates a new movie animation.
    newPosition: new player's position.
    """
    isoview_item.IsoViewItem.animatedSetPosition(self, newPosition)
    movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, self, self.createFrameSet())
    self.setMovieAnimation(movieAnim)
    
  def updateFrame(self, ellapsedTime):
    """ Paints a new item frame on screen.
    ellapsedTime: ellapsed time since the game start.
    """
    isoview_item.IsoViewItem.updateFrame(self, ellapsedTime)
    if self.__movieAnimation != None:
      self.__movieAnimation.step(ellapsedTime)  
        
  def restoreImageFrame(self):
    """ Restores the player image according to his state, heading and timestamp.
    """  
    self.setImg(GG.utils.getSpriteName(GG.utils.STATE[1], self.__heading, 0,self.__timestamp))
  
  def restoreImagePosition(self):  
    """ Restores the image position.
    """  
    self.setScreenPosition(GG.utils.p3dToP2d(self.getPosition(), self.getModel().anchor))
      
  def stateChanged(self, event):
    """ Triggers after receiving a new state change event.
    event: event info.
    """  
    st = event.getParams()["state"]
    pos = event.getParams()["position"]
    if st == GG.utils.STATE[1]: # standing
      self.getParent().removeMovementDestination()
      self.setAnimation(None)
      self.setMovieAnimation(None)  
      self.setImg(GG.utils.getSpriteName(GG.utils.STATE[1], self.__heading, 0, self.__timestamp))
      self.getIVRoom().updateScreenPositionsOn(pos)
      
    elif st == GG.utils.STATE[2]: # walking
      self.setAnimation(None)
      self.setMovieAnimation(None)  
      movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, self, self.createFrameSet(st))
      self.setMovieAnimation(movieAnim)

    elif st == GG.utils.STATE[3]: # standing_carrying
      self.getParent().removeMovementDestination()
      self.setAnimation(None)   
      self.setMovieAnimation(None)  
      self.setImg(GG.utils.getSpriteName(GG.utils.STATE[3], self.__heading, 0, self.__timestamp))
      self.getIVRoom().updateScreenPositionsOn(pos)
      
    elif st == GG.utils.STATE[4]: # walking_carrying
      self.setAnimation(None)
      self.setMovieAnimation(None)  
      movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, self, self.createFrameSet(st))
      self.setMovieAnimation(movieAnim)

    elif st == GG.utils.STATE[5]: # standing_sleeping
      self.getParent().removeMovementDestination()
      self.setAnimation(None)   
      self.setMovieAnimation(None)  
      self.setImg(GG.utils.getSpriteName(GG.utils.STATE[3], self.__heading, 0, self.__timestamp))
      self.getIVRoom().updateScreenPositionsOn(pos)
      
  def onJump(self, event):
    """ Triggers after receiving a player jump event.
    event: event info.
    """  
    screenPos = self.getScreenPosition()
    movieAnim = animation.MovieAnimation(GG.utils.JUMP_ANIMATION_TIME, self, self.createFrameSet("walking"))
    positionUp = animation.ScreenPositionAnimation(GG.utils.JUMP_TIME, self, \
                            screenPos, [screenPos[0],  screenPos[1] - GG.utils.JUMP_DISTANCE], True)
    positionDown = animation.ScreenPositionAnimation(GG.utils.JUMP_TIME, self, \
                            [screenPos[0],  screenPos[1] - GG.utils.JUMP_DISTANCE], screenPos, True)

    secAnim = animation.SecuenceAnimation()
    secAnim.addAnimation(positionUp)
    secAnim.addAnimation(positionDown)
    secAnim.setOnStop(self.stopMovieAnimation, None)
    self.setAnimation(secAnim)
    self.setMovieAnimation(movieAnim)

  def onJumpOver(self, event):
    """ Triggers after receiving a player jumpOver event.
    event: event info.
    """  
    movieAnim = animation.MovieAnimation(GG.utils.JUMP_ANIMATION_TIME, self, self.createFrameSet("walking"))
    pos1 = event.getParams()['position']
    pos2 = event.getParams()['oldPosition']
    posOver = [(pos1[0] + pos2[0])/2, pos1[1], (pos1[2] + pos2[2])/2]
    
    startPos = self.getScreenPosition()
    endPos = self.getIVRoom().getFutureScreenPosition(self, pos1)
    cordX = (startPos[0] + endPos[0])/2
    cordY = (startPos[1] + endPos[1])/2 - GG.utils.JUMP_DISTANCE - 50
    halfPos = [cordX, cordY]
    
    positionUp = animation.ScreenPositionAnimation(GG.utils.JUMP_TIME, self, \
                            startPos, halfPos, True)
    positionDown = animation.ScreenPositionAnimation(GG.utils.JUMP_TIME, self, \
                            halfPos, endPos, True)

    self.updateZOrderFor(posOver)
    positionUp.setOnStop(self.updateZOrderFor, pos1)
    secAnim = animation.SecuenceAnimation()
    secAnim.addAnimation(positionUp)
    secAnim.addAnimation(positionDown)
    secAnim.setOnStop(self.stopMovieAnimation, None)
    secAnim.setOnStop(self.getParent().removeMovementDestination, None)
    secAnim.setOnStop(self.updateZOrderFor, pos1)
    #secAnim.setOnStop(self.getIVRoom().updateScreenPositionsOn, pos1)
    self.setAnimation(secAnim)
    self.setMovieAnimation(movieAnim)
    
  def stopMovieAnimation(self):
    """ Stops the movie animation.
    """  
    if self.__movieAnimation:
      self.__movieAnimation.stop()
      self.__movieAnimation = None
      self.setImg(GG.utils.getSpriteName(GG.utils.STATE[1], self.__heading, 0, self.__timestamp))
      
  def destinationChanged(self, event):
    """ Triggers after receiving a destination change event.
    event: event info.
    """  
    self.__destination = event.getParams()['destination']  
    self.getParent().setMovementDestination(event.getParams()['destination'])
    
  def positionChanged(self, event):
    """ Triggers after receiving a position change event.
    event: event info.
    """  
    pos = event.getParams()['position']
    if pos == self.__destination:
      self.getParent().removeMovementDestination()
    isoview_item.IsoViewItem.positionChanged(self, event)    
     
