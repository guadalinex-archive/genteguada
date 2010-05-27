# -*- coding: utf-8 -*-

import GG.utils
import isoview
import pygame
import guiobjects

class IsoViewTile(isoview.IsoView):
  """ IsoViewTile class.
  Defines a room tile view
  """

  def __init__(self, model, topLeft, bottomRight, position, img, hud):
    """ Class constructor.
    model: tile model.
    topLeft: top left tile coord.
    bottomRight: lower right tile coord.
    position: tile position.
    img: tile image.
    hud: hud handler.
    """
    isoview.IsoView.__init__(self, model, None)
    self.__topLeft = topLeft
    self.__bottomRight = bottomRight
    self.__position = position
    self.__hud = hud
    self.__img = guiobjects.getSprite(img, GG.utils.p3dToP2d(position, GG.utils.FLOOR_SHIFT), -1)
    
  def getImg(self):
    """ Returns the tile image.
    """
    return self.__img
  
  def setImg(self, imageName):
    """ Sets a new tile image.
    """  
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
    """ Checks if one point is inside the tile limits.
    pos: point.
    """  
    rect = self.__img.rect
    if rect[0] < pos[0] < (rect[0] + rect[2]):
      if rect[1] < pos[1] < (rect[1] + rect[3]):
        if self.__img.image.get_at((pos[0] - rect[0], pos[1] - rect[1]))[3] != 0:
          return 1
    return 0
  
  def contained(self, pos, depth, items):
    """ Checks if a point is contained on a tile.
    pos: point.
    depth: number of items on the tile.
    items: items on the tile.
    """
    if self.__bottomRight[0] > pos[0] > self.__topLeft[0]:
      if self.__bottomRight[1] > pos[1] > self.__topLeft[1]:
        rect = self.__rect.rect  
        if self.__img.image.get_at((pos[0] - rect[0], pos[1] - rect[1]))[3] != 0:
          return 1
    if depth == 0:
      return 0
    itemList = items
    for item in itemList:
      if self.__hud.findIVItem(item).checkClickPosition(pos):
        return 1
    return 0
