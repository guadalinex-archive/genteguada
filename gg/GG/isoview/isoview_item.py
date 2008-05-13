import time
import os
import math
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
    imgPath = os.path.join(GG.utils.DATA_PATH, model.spriteName)
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = self.p3dToP2d(model.getPosition(), model.offset)
    self.__parent = parent
    self.__animation = None
    self.__position = model.getPosition()
    self.__animationDestination = None
    #self.getModel().subscribeEvent('chat', parent.pruebaChat)
    self.getModel().subscribeEvent('position', self.positionChanged)
    #self.getModel().subscribeEvent('room', self.roomChanged)
    
  def getParent(self):
    """ Returns the isoview hud handler.
    """
    return self.__parent
  
  def getSprite(self):
    """ Returns the sprite name of the item.
    """
    return self.__sprite
    
  def getImg(self):
    """ Returns a sprite.
    """
    return self.__img
  
  def setImg(self, img):
    """ Sets a new image for the item.
    img: image name.
    """
    imgPath = os.path.join(GG.utils.DATA_PATH, img)
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    
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
      self.__animation.restart(GG.utils.MAX_FRAMES, self.p3dToP2d(newPosition, self.getModel().offset))
    else:
      self.__animation = animation.Animation(GG.utils.MAX_FRAMES, self.__img,
           self.p3dToP2d(self.getModel().getPosition(), self.getModel().offset))
  
  def updateFrame(self):
    """ Paints a new item frame on screen.
    """
    if self.__animation:
      if not self.__animation.move():
        del self.__animation
        self.__animation = None
        self.__img.rect.topleft = self.p3dToP2d(self.__animationDestination, self.getModel().offset)
  
  def positionChanged(self, event):
    """ Updates the item position and draws the room after receiving a position change event.
    event: even info.
    """
    self.__animationDestination = event.getParams()["position"]
    self.animatedSetPosition(event.getParams()["position"])
  