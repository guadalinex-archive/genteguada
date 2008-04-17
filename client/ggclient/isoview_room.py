import os
import pygame

import utils
import isoview
import isoview_tile

class IsoViewRoom(isoview.IsoView):
  """ IsoViewRoom class.
  Defines the room view.
  """

  def __init__(self, name, screen, model):
    """ Class constructor.
    name: room label.
    """
    isoview.IsoView.__init__(self, name, model)
    bgPath = os.path.join(utils.DATA_PATH, model.getSpriteFull())
    self.__bg = pygame.sprite.Sprite()
    self.__bg.image = pygame.image.load(bgPath)
    self.__bg.rect = self.__bg.image.get_rect()
    self.__bg.rect.topleft = utils.BG_FULL_OR
    self.__screen = screen
    self.__spritesList = []
    self.__tileList = []
    self.__isoViewPlayer = []
    self.__allPlayers = pygame.sprite.RenderUpdates()
    for x in range(utils.SCENE_SZ[0]):
      for z in range(utils.SCENE_SZ[1]):
        varPos = self.p3dToP2d([x, 0, z], [utils.TILE_SZ[0], -5])
        pos = [int(varPos[0]),int(varPos[1])]
        self.__tileList.append([])
        self.__tileList[x].append(isoview_tile.IsoViewTile(\
            [pos[0], pos[1]], \
            [pos[0] + utils.TILE_SZ[0], pos[1] + utils.TILE_SZ[1]], \
            utils.TILE_STONE, utils.TILE_SZ, 0))
        
  def insertIsoViewPlayer(self,player):
    """ Inserts a new player view.
    player: player view.
    """
    self.__isoViewPlayer.append(player)
    self.__allPlayers.add(player.getImg())

  def drawFirst(self):
    """ Draws the room and all its components on screen for the first time.
    """
    self.paintFloorFull()
    self.__allPlayers.draw(self.__screen)
    pygame.display.update()
  
  def draw(self):
    """ Paints floor, players and items on the room.
    screen: screen handler.
    """
    self.paintFloorFull()
    self.paintPlayers()
    pygame.display.update()
    
  def paintPlayers(self):
    """ Paints all players on screen.
    """
    self.__allPlayers.update()                     
    self.__allPlayers.clear(self.__screen, self.__bg.image)
    pygame.display.update(self.__allPlayers.draw(self.__screen))
    
  def paintFloorFull(self):
    """ Paints the room's floor using a single sprite.
    screen: screen handler.
    """
    self.__screen.blit(self.__bg.image, self.__bg.rect)

  def findTile(self,pos):
    """ Gets the 3d tile coords that match a 2d point.
    pos: 2d coords.
    """
    for x in range(utils.SCENE_SZ[0]):
      for z in range(utils.SCENE_SZ[1]):
        if self.__tileList[x][z].contained(pos):
          if not self.__tileList[x][z].onBlank(pos):
            return [x, z]
    return [-1, -1]
  
  def newAction(self, event):
    """ Runs a method after receiving an event.
    event: event info.    
    """
    for player in self.__isoViewPlayer:
      if player.getModelData("id") == event.params["id"]:
        player.newAction(event)
    self.draw()    