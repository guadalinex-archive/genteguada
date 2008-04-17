import os
import pygame

import utils
import isoview
import isoview_tile

class IsoViewRoom(isoview.IsoView):
  """ IsoViewRoom class.
  Defines the room view.
  """

  def __init__(self, name, screen):
    """ Class constructor.
    name: room label.
    """
    isoview.IsoView.__init__(self, name)
    self.__screen = screen
    self.__spritesList = []
    self.__tileList = []
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
    self.__isoViewPlayer = player
    bgPath = os.path.join(utils.DATA_PATH, self.getModelList()[0].getSpriteFull())
    bg = pygame.sprite.Sprite()
    bg.image = pygame.image.load(bgPath)
    bg.rect = bg.image.get_rect()
    bg.rect.topleft = utils.BG_FULL_OR
    player.setBg(bg)
  
  def drawFirst(self):
    """ Draws the room and all its components on screen for the first time.
    """
    self.paintFloorFull(self.getModelList()[0].getSpriteFull())
    self.__isoViewPlayer.drawFirst(self.__screen)
  
  def draw(self):
    """ Paints floor, players and items on the room.
    screen: screen handler.
    """
    self.paintFloorFull(self.getModelList()[0].getSpriteFull(), self.__screen)
    self.isoViewPlayer.draw(self.__screen)
    
  def paintFloorFull(self, spriteFull):
    """ Paints the room's floor using a single sprite.
    screen: screen handler.
    """
    self.getModelList()[0].getSpriteFull()
    bgPath = os.path.join(utils.DATA_PATH, spriteFull)
    bg = pygame.sprite.Sprite()
    bg.image = pygame.image.load(bgPath)
    bg.rect = bg.image.get_rect()
    bg.rect.topleft = utils.BG_FULL_OR
    self.__screen.blit(bg.image, bg.rect)

  def paintFloor(self, tileName):
    """ Paints the roo floor.
    tileName: tile sprite.
    screen: screen handler.
    """
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, utils.GAMEZONE_SZ[0], utils.GAMEZONE_SZ[1]))
    tile = os.path.join(utils.DATA_PATH, tileName)
    tileSurface = pygame.image.load(tile)
    for x in range(utils.SCENE_SZ[0]):
      for z in range(utils.SCENE_SZ[1]):
        self.__screen.blit(tileSurface, self.__p3dToP2d([x, 0, z]))

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
    self.__isoViewPlayer.newAction(event)