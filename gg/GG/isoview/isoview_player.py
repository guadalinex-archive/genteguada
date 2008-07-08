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
    self.setImg(GG.utils.getSpriteName(model.getState(), model.getHeading(), 0))
    self.getModel().subscribeEvent('heading', self.headingChanged)
    self.getModel().subscribeEvent('state', self.stateChanged)
    self.getModel().subscribeEvent('jump', self.onJump)
    self.getModel().subscribeEvent('avatarConfiguration', self.avatarConfigurationChanged)
    self.getModel().subscribeEvent('destination', self.destinationChanged)
    #self.getModel().subscribeEvent('addInventory', self.inventoryAdded)
    #self.getModel().subscribeEvent('removeFromInventory', self.inventoryRemoved)
    
    #self.getModel().subscribeEvent('position', self.positionChanged)
    self.__heading = self.getModel().getHeading()

  def __del__(self):
    isoview.IsoView.__del__(self)
    if self.__movieAnimation:
      self.__movieAnimation.stop()

  def avatarConfigurationChanged(self, event):
    print "cambio la configuracion del jugador"

  def headingChanged(self, event):
    """ Changes the player's sprite heading.
    """
    self.__heading = event.getParams()["heading"]
    if self.__movieAnimation != None:
      frames = self.createFrameSet()
      self.__movieAnimation.setFrames(frames)
    else:
      str = GG.utils.getSpriteName(event.getParams()["state"], event.getParams()["heading"], 0)
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
    """
    frames = []
    if dataState:
      state = dataState
    else:
      state = self.getModel().getState()
    if state == GG.utils.STATE[1] or state == GG.utils.STATE[3] or state == GG.utils.STATE[5]:
      string = GG.utils.getSpriteName(state, self.__heading, 0)
      frames.append(string)        
    else:
      for i in range(1, GG.utils.ANIM_WALKING_COUNT+1):
        string = GG.utils.getSpriteName(state, self.__heading, i)  
        frames.append(string)        
    return frames
    
  def animatedSetPosition(self, newPosition):
    """ Sets a new position for the player, and creates a new movie animation.
    newPosition: new player's position.
    """
    isoview_item.IsoViewItem.animatedSetPosition(self, newPosition)
    movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, self, self.createFrameSet())
    self.setMovieAnimation(movieAnim)
    
  def updateFrame(self, ellapsedTime):
    """ Paints a new item frame on screen.
    """
    isoview_item.IsoViewItem.updateFrame(self, ellapsedTime)
    if self.__movieAnimation != None:
      self.__movieAnimation.step(ellapsedTime)  
        
  def restoreImageFrame(self):
    self.setImg(GG.utils.getSpriteName(GG.utils.STATE[1], self.__heading, 0))
  
  def restoreImagePosition(self):  
    self.setScreenPosition(GG.utils.p3dToP2d(self.getModel().getPosition(), self.getModel().anchor))
      
  def stateChanged(self, event):
    """ Triggers after receiving a new state change event.
    event: event info.
    """  
    st = event.getParams()["state"]
    pos = event.getParams()["position"]
    #print "************>>>>>>>>>>>>>>> Evento de estado: ", st
    if st == GG.utils.STATE[1]: # standing
      self.getParent().removeMovementDestination()
      self.setAnimation(None)
      self.setMovieAnimation(None)  
      self.setImg(GG.utils.getSpriteName(GG.utils.STATE[1], self.__heading, 0))
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
      self.setImg(GG.utils.getSpriteName(GG.utils.STATE[3], self.__heading, 0))
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
      self.setImg(GG.utils.getSpriteName(GG.utils.STATE[3], self.__heading, 0))
      self.getIVRoom().updateScreenPositionsOn(pos)
    
    #print "============================================"  
      
  def onJump(self, event):
    movieAnim = animation.MovieAnimation(GG.utils.JUMP_ANIMATION_TIME, self, self.createFrameSet("walking"))
    positionUp = animation.ScreenPositionAnimation(GG.utils.JUMP_TIME, self, \
                            self.getScreenPosition(), [self.getScreenPosition()[0],  self.getScreenPosition()[1] - GG.utils.JUMP_DISTANCE], True)
    positionDown = animation.ScreenPositionAnimation(GG.utils.JUMP_TIME, self, \
                            [self.getScreenPosition()[0],  self.getScreenPosition()[1] - GG.utils.JUMP_DISTANCE], self.getScreenPosition(), True)

    secAnim = animation.SecuenceAnimation()
    secAnim.addAnimation(positionUp)
    secAnim.addAnimation(positionDown)
    secAnim.setOnStop(self.stopMovieAnimation, None)
    self.setAnimation(secAnim)
    self.setMovieAnimation(movieAnim)
    
  def stopMovieAnimation(self):
    if self.__movieAnimation:
      self.__movieAnimation.stop()
      self.__movieAnimation = None
      self.setImg(GG.utils.getSpriteName(GG.utils.STATE[1], self.__heading, 0))
      
  def destinationChanged(self, event):
    self.__destination = event.getParams()['destination']  
    self.getParent().setMovementDestination(event.getParams()['destination'])
    
  def positionChanged(self, event):
    pos = event.getParams()['position']
    #print ">>> Recibido 1 -> ", pos  
    if pos == self.__destination:
      self.getParent().removeMovementDestination()
    isoview_item.IsoViewItem.positionChanged(self, event)    
        