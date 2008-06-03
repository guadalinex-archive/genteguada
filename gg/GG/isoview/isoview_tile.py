import GG.utils
import isoview
import os
import pygame

class IsoViewTile(isoview.IsoView):
  """ IsoViewTile class.
  Defines a room tile view
  """

  def __init__(self, topLeft, bottomRight, spriteName, position):
    """ Class constructor.
    topLeft: top left tile coord.
    bottomRight: lower right tile coord.
    spriteName: name of the sprite used to paint the tile on screen.
    size: tile size.
    blocked: Indicates if the tile is passable or blocked.
    position: tile position.
    """
    isoview.IsoView.__init__(self, None, None, topLeft)
    self.__topLeft = topLeft
    self.__bottomRight = bottomRight
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(spriteName)).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = GG.utils.p3dToP2d(position, GG.utils.FLOOR_SHIFT)
    
  def getImg(self):
    """ Returns the tile image.
    """
    return self.__img
    
  def getTopLeft(self):
    """ Returns the top left coord.
    """
    return self.__topLeft
  
  def getBottomRight(self):
    """ Returns the lower right coord.
    """
    return self.__bottomRight
  
  def contained(self, pos):
    """ Returns if a point is contained on a tile.
    pos: point.
    """
    if self.__bottomRight[0] > pos[0] > self.__topLeft[0]:
      if self.__bottomRight[1] > pos[1] > self.__topLeft[1]:
        return 1
    return 0

  def onBlank(self, pos):
    """ Checks if one point is located on the blank zones of the tile sprite.
    pos: point.
    """
    iniPos = [pos[0] - self.__topLeft[0], pos[1] - self.__topLeft[1]]
    if iniPos[0] < (GG.utils.TILE_SZ[0] / 2):
      if iniPos[1] < (GG.utils.TILE_SZ[1] / 2):
        #top left corner
        if (iniPos[0] + (iniPos[1] * 2)) <= (GG.utils.TILE_SZ[0]/2):
          return 1
      else:
        #bottom left corner
        iniPos[1] -= (GG.utils.TILE_SZ[1] / 2)
        iniPos[1] = (GG.utils.TILE_SZ[1] / 2) - iniPos[1]
        if (iniPos[0] + (iniPos[1] * 2)) <= (GG.utils.TILE_SZ[0]/2):
          return 1
    else:
      if iniPos[1] < (GG.utils.TILE_SZ[1] / 2):
        #top right corner
        iniPos[0] -= (GG.utils.TILE_SZ[0] / 2)
        iniPos[0] = (GG.utils.TILE_SZ[0] / 2) - iniPos[0]
        if (iniPos[0] + (iniPos[1] * 2)) <= (GG.utils.TILE_SZ[0]/2):
          return 1
      else:
        #bottom right corner
        iniPos[0] -= (GG.utils.TILE_SZ[0] / 2)
        iniPos[1] -= (GG.utils.TILE_SZ[1] / 2)
        iniPos[0] = (GG.utils.TILE_SZ[0] / 2) - iniPos[0]
        iniPos[1] = (GG.utils.TILE_SZ[1] / 2) - iniPos[1]
        if (iniPos[0] + (iniPos[1] * 2)) <= (GG.utils.TILE_SZ[0]/2):
          return 1
    return 0    
