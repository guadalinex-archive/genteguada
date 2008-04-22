import os
import math
import pygame
import utils
import isoview

class IsoViewItem(isoview.IsoView):
  
  def __init__(self, model, screen):
    """ Class constructor.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__sprite = model.getSprite()
    imgPath = os.path.join(utils.DATA_PATH, model.getSprite())
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath)
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = self.p3dToP2d(model.getPosition(), model.getOffset())
    self.__modelData = ({"sprite":model.getSprite(), "pActual":model.getPosition()})
    
  def getModelData(self, info):
    """ Returns specific info from the model data.
    """
    return self.__modelData[info]
    
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
    