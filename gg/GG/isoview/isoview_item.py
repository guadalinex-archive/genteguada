import os
import pygame
import GG.utils
import isoview
import animation

class IsoViewItem(isoview.IsoView):
  """ IsoViewItem class.
  Defines an item view.
  """
  
  def __init__(self, model, screen, room, parent):
    """ Class constructor.
    screen: screen handler.
    parent: isoview_hud handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__ivroom = room
    self.__parent = parent
    self.__animation = None
    self.__position = model.getPosition()
    self.__animationDestination = None
    self.__clock = pygame.time.Clock()
    #self.__relaxClock = pygame.time.Clock()
    #self.__relaxTimePassed = 0
    self.__timePassed = 0
    self.loadImage()
    #self.getModel().subscribeEvent('chat', parent.pruebaChat)
    self.getModel().subscribeEvent('position', self.positionChanged)
    self.getModel().subscribeEvent('startPosition', self.startPositionChanged)
    #self.getModel().subscribeEvent('room', self.roomChanged)
    
  def loadImage(self):
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.getModel().getImagePath()+self.getModel().spriteName)  
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = GG.utils.p3dToP2d(self.getModel().getPosition(), self.getModel().offset)
        
  def getParent(self):
    """ Returns the isoview hud handler.
    """
    return self.__parent
  
  def getImg(self):
    """ Returns a sprite.
    """
    return self.__img
  
  def setImg(self, img):
    """ Sets a new image for the item.
    img: image name.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.getModel().getImagePath()+img)
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    
  def setSprite(self, sprite):
    self.__img = sprite
    
  def getIVRoom(self):
    """ Returns the isometric view room object.
    """
    return self.__ivroom
  
  def setIVRoom(self, ivroom):
    """ Sets a new isoview room for the item.
    ivroom: new isoview room.
    """
    self.__ivroom = ivroom
  
  def animatedSetPosition(self, newPosition):
    """ Starts a new animation for the item.
    newPosition: new item position.
    """
    if self.__animation:
      self.__animation.stop()
      del self.__animation
      self.__animation = None
    positionAnim = animation.PositionAnimation(GG.utils.ANIM_WALKING_TIME, self.__img, GG.utils.p3dToP2d(newPosition, self.getModel().offset))
    movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, self.__img, self.getModel().getHeading(), \
                  self.getModel().getImagePath(), GG.utils.p3dToP2d(newPosition, self.getModel().offset), GG.utils.ANIM_WALKING_COUNT, "walking")
    self.__animation = animation.ParalelAnimation()
    self.__animation.addAnimation(positionAnim)
    self.__animation.addAnimation(movieAnim)
    aux = self.__clock.tick()
    self.__timePassed = 0
    self.__animation.start()
  
  def updateFrame(self):
    """ Paints a new item frame on screen.
    """
    if self.__animation:
      self.__timePassed += self.__clock.tick(50)
      if not self.__animation.isFinished(self.__timePassed):
        self.__animation.step(self.__timePassed)
      else:  
        self.__animation.stop()
        self.__img.rect.topleft = GG.utils.p3dToP2d(self.getModel().getPosition(), self.getModel().offset)
        aux = self.__clock.tick()
        self.__timePassed = 0
        del self.__animation
        self.__animation = None
        #aux = self.__relaxClock.tick()
        #self.__relaxTimePassed = 0
    """
    else:
      if isinstance(self.getModel(), GG.model.player.GGPlayer):
        self.__relaxTimePassed += self.__relaxClock.tick(50)
        if self.__relaxTimePassed/1000.0 > GG.utils.TIME_BEFORE_RELAX:
          movieAnim = animation.MovieAnimation(GG.utils.ANIM_RELAX_TIME, self.__img, self.getModel().getHeading(), \
                  self.getModel().getImagePath(), GG.utils.p3dToP2d(self.getModel().getPosition(), self.getModel().offset), GG.utils.ANIM_RELAX_COUNT, "relax")
          self.__animation = animation.ParalelAnimation()
          self.__animation.addAnimation(movieAnim)
          aux = self.__clock.tick()
          self.__timePassed = 0
          self.__animation.start()
     """     
        
  def positionChanged(self, event):
    """ Updates the item position and draws the room after receiving a position change event.
    event: even info.
    """
    GG.utils.playSound(GG.utils.SOUND_STEPS01)
    self.animatedSetPosition(event.getParams()["position"])
  
  def startPositionChanged(self, event):
    """ Updates the item position without animation and draws the room after receiving a position change event.
    event: even info.
    """
    del self.__animation
    self.__animation = None
    self.__img.rect.topleft = GG.utils.p3dToP2d(event.getParams()['position'], self.getModel().offset)
  
  def selected(self):
    size = self.__img.rect
    color2 = [0, 0, 0]
    for x in range(0, size[2]):
      for y in range(0, size[3]):
        color = self.__img.image.get_at((x,y))
        if color[3] != 0:
          color2[0] = color[0] + GG.utils.COLOR_SHIFT
          if color2[0] > 255: color2[0] = 255
          color2[1] = color[1] + GG.utils.COLOR_SHIFT
          if color2[1] > 255: color2[1] = 255
          color2[2] = color[2] + GG.utils.COLOR_SHIFT
          if color2[2] > 255: color2[2] = 255
          self.__img.image.set_at((x,y), color2)
    pygame.display.update()
    #self.__img.image.set_colorkey(color_transparente)
    #colorKey = self.__img.image.get_colorkey()
    
  def unselected(self):
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.getModel().getImagePath()+self.getModel().spriteName)
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
