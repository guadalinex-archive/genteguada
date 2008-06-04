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
    self.__movieClock = pygame.time.Clock()
    self.__movieTimePassed = 0
    self.getModel().subscribeEvent('heading', self.headingChanged)
    self.getModel().subscribeEvent('state', self.stateChanged)
    #self.getModel().subscribeEvent('destination', self.destinationChanged)
    #self.getModel().subscribeEvent('addInventory', self.inventoryAdded)
    #self.getModel().subscribeEvent('removeInventory', self.inventoryRemoved)
    self.__heading = self.getModel().getHeading()

  def headingChanged(self, event):
    """ Changes the player's sprite heading.
    """
    self.__heading = event.getParams()["heading"]
    if not self.activeAnimation():
      str = GG.utils.getSpriteName(GG.utils.STATE[1], event.getParams()["heading"], 0)
      self.setImg(str)
    else:
      if self.__movieAnimation:
        frames = self.createFrameSet()
        self.__movieAnimation.setFrames(frames)
    
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

  def activeAnimation(self):
    """ Checks if there is an active animation.
    """
    if self.__movieAnimation != None or isoview_item.IsoViewItem.activeAnimation(self):
      return True
    return False
      
  def setMovieAnimation(self, animation):
    """ Creates a new movie animation.
    animation: new movie animation.
    """
    if self.__movieAnimation:
      self.__movieAnimation.stop()
    self.__movieAnimation = animation
    if animation != None:
      aux = self.__movieClock.tick()
      self.__movieTimePassed = 0
      animation.start()
    
  def setMovieFrames(self, frames):
    """ Sets a new frame set for a movie animation.
    frames: new frame set.
    """
    self.__movieAnimation.setFrames(frames)
        
  def createFrameSet(self):
    """ Creates a new frame set.
    """
    frames = []
    state = self.getModel().getState()
    if state == GG.utils.STATE[1] or state == GG.utils.STATE[3] or state == GG.utils.STATE[5]:
     print "***************************************************"
    for i in range(1, GG.utils.ANIM_WALKING_COUNT+1):
      if i < 10:
        string = state + "_" + self.__heading + "_00" + str(i) + ".png"
      else:  
        string = state + "_" + self.__heading + "_0" + str(i) + ".png"
      frames.append(string)        
    return frames
    
  def animatedSetPosition(self, newPosition):
    """ Sets a new position for the player, and creates a new movie animation.
    newPosition: new player's position.
    """
    isoview_item.IsoViewItem.animatedSetPosition(self, newPosition)
    movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, self, self.createFrameSet())
    self.setMovieAnimation(movieAnim)
    
  def updateFrame(self):
    """ Paints a new item frame on screen.
    """
    isoview_item.IsoViewItem.updateFrame(self)
    if self.__movieAnimation:
      self.__movieTimePassed += self.__movieClock.tick(50)
      self.__movieAnimation.step(self.__movieTimePassed)  
        
  def stateChanged(self, event):
    """ Triggers after receiving a new state change event.
    event: event info.
    """  
    st = event.getParams()["state"]
    if st == GG.utils.STATE[1]: # standing
      if self.activeAnimation():
        #isoview_item.IsoViewItem.setPositionAnimation(self, None)   
        isoview.IsoView.setAnimation(self, None)
        self.setMovieAnimation(None)  
        self.setImg(GG.utils.getSpriteName(GG.utils.STATE[1], self.__heading, 0))
        self.setScreenPosition(GG.utils.p3dToP2d(self.getModel().getPosition(), self.getModel().offset))

    elif st == GG.utils.STATE[2]: # walking
      movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, self, self.createFrameSet())
      self.setMovieAnimation(movieAnim)

    elif st == GG.utils.STATE[3]: # standing_carrying
      if self.activeAnimation():
        #isoview_item.IsoViewItem.setPositionAnimation(self, None)
        isoview.IsoView.setAnimation(self, None)   
        self.setMovieAnimation(None)  
        self.setImg(GG.utils.getSpriteName(GG.utils.STATE[3], self.__heading, 0))
        self.setImgPosition(self.getModel().getPosition())

    elif st == GG.utils.STATE[4]: # walking_carrying
      movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, self, self.createFrameSet())
      self.setMovieAnimation(movieAnim)

    elif st == GG.utils.STATE[5]: # standing_sleeping
      if self.activeAnimation():
        #isoview_item.IsoViewItem.setPositionAnimation(self, None)
        isoview.IsoView.setAnimation(self, None)   
        self.setMovieAnimation(None)  
        self.setImg(GG.utils.getSpriteName(GG.utils.STATE[3], self.__heading, 0))
        self.setImgPosition(self.getModel().getPosition())
    