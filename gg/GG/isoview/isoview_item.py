import os
import math
import pygame
import GG.utils
import isoview

class IsoViewItem(isoview.IsoView):
  """ IsoViewItem class.
  Defines an item view.
  """
  
  def __init__(self, model, screen, parent):
    """ Class constructor.
    screen: screen handler.
    parent: isoview_hud handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__sprite = model.getSprite()
    imgPath = os.path.join(GG.utils.DATA_PATH, self.__sprite)
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath)
    self.__img.rect = self.__img.image.get_rect()
    position = model.getPosition()
    self.__img.rect.topleft = self.p3dToP2d(position, model.getOffset())
    self.__parent = parent
    self.getModel().subscribeEvent('chat', parent.pruebaChat)

  def getSprite(self):
    """ Returns the sprite name of the item.
    """
    return self.__sprite
    
  def getImg(self):
    """ Returns a sprite.
    """
    return self.__img
    
  def draw(self, screen):
    """ Runs some methods to paint on screen all players.
    screen: screen handler.
    """
    self.__allPlayers.update()                     
    self.__allPlayers.clear(screen, self.__bg.image)
    pygame.display.update(self.__allPlayers.draw(screen))
    
    
