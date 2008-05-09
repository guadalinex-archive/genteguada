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
    imgPath = os.path.join(GG.utils.DATA_PATH, model.getSpriteName())
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = self.p3dToP2d(model.getPosition(), model.getOffset())
    self.__parent = parent
    
    self.__animation = None
    self.__position = model.getPosition()
    
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
    """ Creates a new animation and draws a player moving through the screen.
    """
    #print self.__img.rect.topleft, self.p3dToP2d(self.getModel().getPosition(), self.getModel().getOffset())
    self.stopAnimation(newPosition)  
    self.__animation = animation.Animation(GG.utils.MAX_FRAMES, self.__img,
           self.p3dToP2d(self.getModel().getPosition(), self.getModel().getOffset()))

  def updateFrame(self):
    if self.__animation:
      print "update frame", self.__animation.getStep()
      if not self.__animation.move():
        del self.__animation
        self.__animation = None
        
  def stopAnimation(self, newPosition):
    if self.__animation:
      del self.__animation
      self.__animation = None
      self.__img.rect.topleft = self.p3dToP2d(newPosition, self.getModel().getOffset())

  def positionChanged(self, event):
    """ Updates the item position and draws the room after receiving a position change event.
    event: even info.
    """
    print "=================================================="
    self.animatedSetPosition(event.getParams()["position"])
    
    #print "================================ Nuevo movimiento: ", self.__img.rect.topleft
    #self.__img.rect.topleft = self.p3dToP2d(event.getParams()["position"], self.getModel().getOffset())
    