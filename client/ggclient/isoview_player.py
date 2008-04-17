import os
import math
import pygame
import utils
import isoview

class IsoViewPlayer(isoview.IsoView):
  """ IsoViewPlayer class.
  Defines an object view, either if the object is a player on an item.
  """

  def __init__(self, name, type, screen):
    """ Class constructor.
    name: view name.
    type: type of the object. 0: player, 1: item.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, name)
    self.__type = type
    self.__modelList = []
    self.__modelDataList = []
    self.__spritesList = []
    self.__bg = None
    self.__screen = screen
    self.__allPlayers = pygame.sprite.RenderUpdates()
    
  def getBg(self):
    """ Returns the background image used to clean the screen after moving sprites.
    """
    return self.__bg
  
  def getScreen(self):
    """ Returns the screen handler.
    """
    return self.__screen
    
  def setBg(self, bg):
    """ Sets a background image for player animations.
    bg: background image.
    """
    self.__bg = bg
    self.__bg.rect.topleft = utils.BG_FULL_OR
    
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
    for i in range(0, len(self.__modelDataList)):
      if self.__modelDataList[i]["id"] == event.params["id"]:
        tempModelList = self.getModelList()
        elem = self.p3dToP2d(event.params["pDestin"], tempModelList[i].getOffset())
        self.__spritesList[i].rect.topleft = elem
        self.__modelDataList[i]["pActual"] = event.params["pDestin"]
        self.__modelDataList[i]["pDestin"] = event.params["pDestin"]
        self.__allPlayers.update()                     
        self.__allPlayers.clear(self.__screen, self.__bg.image)
        pygame.display.update(self.__allPlayers.draw(self.__screen))

  def addPlayer(self, model):
    """ Adds a model to the controlled model list.
    model: new model to be added.
    """
    imgPath = os.path.join(utils.DATA_PATH, model.getSprite())
    img = pygame.sprite.Sprite()
    img.image = pygame.image.load(imgPath)
    img.rect = img.image.get_rect()
    img.rect.topleft = self.p3dToP2d(model.getPosition(), model.getOffset())
    self.__allPlayers.add(img)
    self.__spritesList.append(img)
    self.addModel(model)
    #self.__modelList.append(model)
    self.__modelDataList.append({"id":model.getId(), "sprite":model.getSprite(), \
      "pActual":model.getPosition(), "pDestin":model.getDestination(), \
      "dir":model.getState(), "step": 0})

  def drawFirst(self, screen):
    """ Runs some methods to paint on screen all players for the first time.
    screen: screen handler.
    """
    self.__allPlayers.draw(screen)
    pygame.display.update()
    
  def draw(self, screen):
    """ Runs some methods to paint on screen all players.
    screen: screen handler.
    """
    self.__allPlayers.update()                     
    self.__allPlayers.clear(screen, self.__bg.image)
    pygame.display.update(self.__allPlayers.draw(screen))