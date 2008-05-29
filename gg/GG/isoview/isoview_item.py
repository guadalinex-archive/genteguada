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
    self.__position = model.getPosition()
    self.__animationDestination = None
    self.__positionAnimation = None
    self.__positionClock = pygame.time.Clock()
    self.__positionTimePassed = 0
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
    pygame.display.update()
    
  def setImgPosition(self, pos):
    self.__img.rect.topleft = pos  
    
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
  
  def activeAnimation(self):
    if self.__positionAnimation != None:
      return True
    return False
  
  def setPositionAnimation(self, animation):
    if self.__positionAnimation:
      self.__positionAnimation.stop()
    self.__positionAnimation = animation
    if animation != None:
      aux = self.__positionClock.tick()
      self.__positionTimePassed = 0
      animation.start()
    
  def animatedSetPosition(self, newPosition):
    """ Starts a new animation for the item.
    newPosition: new item position.
    """
    positionAnim = animation.PositionAnimation(GG.utils.ANIM_WALKING_TIME, self.__img, GG.utils.p3dToP2d(newPosition, self.getModel().offset))
    self.setPositionAnimation(positionAnim)
    
  def updateFrame(self):
    """ Paints a new item frame on screen.
    """
    if self.__positionAnimation:
      self.__positionTimePassed += self.__positionClock.tick(50)
      if not self.__positionAnimation.isFinished(self.__positionTimePassed):
        self.__positionAnimation.step(self.__positionTimePassed)
      else:  
        self.__img.rect.topleft = GG.utils.p3dToP2d(self.getModel().getPosition(), self.getModel().offset)
        self.setPositionAnimation(None)
         
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
    self.setPositionAnimation(None)
    self.setMovieAnimation(None)
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
