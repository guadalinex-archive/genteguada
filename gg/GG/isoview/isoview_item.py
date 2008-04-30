import os
import math
import pygame
import GG.utils
import isoview

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
    #self.__sprite = model.getSpriteName()
    #print self.__sprite
    #print "========================"
    #print dir(model)
    #print model.getSpriteName()
    imgPath = os.path.join(GG.utils.DATA_PATH, model.getSpriteName())
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath)
    self.__img.rect = self.__img.image.get_rect()
    position = model.getPosition()
    self.__img.rect.topleft = self.p3dToP2d(position, model.getOffset())
    self.__parent = parent
    self.getModel().subscribeEvent('chat', parent.pruebaChat)
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
    
  def getIVRoom(self):
    """ Returns the isometric view room object.
    """
    return self.__ivroom
  
  def draw(self, screen):
    """ Runs some methods to paint on screen all players.
    screen: screen handler.
    """
    self.__allPlayers.update()                     
    self.__allPlayers.clear(screen, self.__bg.image)
    pygame.display.update(self.__allPlayers.draw(screen))
  
  def positionChanged(self, event):
    """ Updates the item position and draws the room after receiving a position change event.
    event: even info.
    """
    self.__img.rect.topleft = self.p3dToP2d(event.getParams()["position"], self.getModel().getOffset())
    self.__ivroom.draw()

