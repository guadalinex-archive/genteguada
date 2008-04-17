import os
import math
import pygame
import utils
import isoview

class IsoViewPlayer(isoview.IsoView):
  """ IsoViewPlayer class.
  Defines an object view, either if the object is a player on an item.
  """

  def __init__(self, name, type, screen, model):
    """ Class constructor.
    name: view name.
    type: type of the object. 0: player, 1: item.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, name, model)
    self.__type = type
    self.__screen = screen
    self.__sprite = model.getSprite()
    imgPath = os.path.join(utils.DATA_PATH, model.getSprite())
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath)
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = self.p3dToP2d(model.getPosition(), model.getOffset())
    self.__modelData = ({"id":model.getId(), "sprite":model.getSprite(), \
      "pActual":model.getPosition(), "pDestin":model.getDestination(), \
      "dir":model.getState(), "step": 0})
    
  def getScreen(self):
    """ Returns the screen handler.
    """
    return self.__screen
    
  def getModelData(self, info):
    """ Returns specific info from the model data.
    """
    return self.__modelData[info]
    
  def _setScreen(self, screen):
    """ Sets the screen handler.
    screen: screen handler.
    """
    self.__screen = screen

  def newAction(self, event):
    """ Runs an event associated with a new action.
    event: even info.
      > id = self.id
      > sprite = self.sprite
      > pActual = self.position
      > pDestin = self.destination
      > dir = self.state
    """
    elem = self.p3dToP2d(event.params["pDestin"], self.getModel().getOffset())
    self.__img.rect.topleft = elem
    self.__modelData["pActual"] = event.params["pDestin"]
    self.__modelData["pDestin"] = event.params["pDestin"]
    
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