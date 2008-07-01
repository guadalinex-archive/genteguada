import GG.utils
import isoview
import os
import pygame

class IsoViewTile(isoview.IsoView):
  """ IsoViewTile class.
  Defines a room tile view
  """

  def __init__(self, model, topLeft, bottomRight, position, img, hud):
    """ Class constructor.
    topLeft: top left tile coord.
    bottomRight: lower right tile coord.
    position: tile position.
    """
    isoview.IsoView.__init__(self, model, None)
    self.__topLeft = topLeft
    self.__bottomRight = bottomRight
    self.__position = position
    self.__hud = hud
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(img)).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = GG.utils.p3dToP2d(position, GG.utils.FLOOR_SHIFT)
    self.__img.zOrder = -1
    
  def getImg(self):
    """ Returns the tile image.
    """
    return self.__img
  
  def setImg(self, imageName):
    self.__img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(imageName)).convert_alpha()
    
  def getTopLeft(self):
    """ Returns the top left coord.
    """
    return self.__topLeft
  
  def getBottomRight(self):
    """ Returns the lower right coord.
    """
    return self.__bottomRight
  
  def checkClickPosition(self, pos):
    rect = self.__img.rect
    if rect[0] < pos[0] < (rect[0] + rect[2]):
      if rect[1] < pos[1] < (rect[1] + rect[3]):
        if self.__img.image.get_at((pos[0] - rect[0], pos[1] - rect[1]))[3] != 0:
          return 1
    return 0
  
  def contained(self, pos, depth, items):
    """ Checks if a point is contained on a tile.
    pos: point.
    """
    if self.__bottomRight[0] > pos[0] > self.__topLeft[0]:
      if self.__bottomRight[1] > pos[1] > self.__topLeft[1]:
        rect = self.__rect.rect  
        if self.__img.image.get_at((pos[0] - rect[0], pos[1] - rect[1]))[3] != 0:
          return 1
        #if not self.onBlank(pos):
        #  return 1
        
    #if self.getModel().getDepth() == 0:
    if depth == 0:
      return 0
    #itemList = self.getModel().getItems()
    itemList = items
    for item in itemList:
      if self.__hud.findIVItem(item).checkClickPosition(pos):
        return 1
    return 0
    
  """  
  def onBlank(self, pos):
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
  """