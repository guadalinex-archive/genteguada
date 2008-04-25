import os
import pygame

import GG.utils
import isoview
import isoview_tile

class IsoViewRoom(isoview.IsoView):
  """ IsoViewRoom class.
  Defines the room view.
  """

  def __init__(self, model, screen):
    """ Class constructor.
    model: room model.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    bgPath = os.path.join(GG.utils.DATA_PATH, model.getSpriteFull())
    self.__bg = pygame.sprite.Sprite()
    self.__bg.image = pygame.image.load(bgPath)
    self.__bg.rect = self.__bg.image.get_rect()
    self.__bg.rect.topleft = GG.utils.BG_FULL_OR
    self.__isoViewPlayers = []
    self.__isoViewItems = []
    #self.__allPlayers = pygame.sprite.RenderUpdates()
    self.__allPlayers = pygame.sprite.OrderedUpdates()
    self.__tileList = []
    for x in range(GG.utils.SCENE_SZ[0]):
      for z in range(GG.utils.SCENE_SZ[1]):
        varPos = self.p3dToP2d([x, 0, z], [GG.utils.TILE_SZ[0], -5])
        pos = [int(varPos[0]),int(varPos[1])]
        self.__tileList.append([])
        self.__tileList[x].append(isoview_tile.IsoViewTile(\
            [pos[0], pos[1]], \
            [pos[0] + GG.utils.TILE_SZ[0], pos[1] + GG.utils.TILE_SZ[1]], \
            GG.utils.TILE_STONE, GG.utils.TILE_SZ, 0))
        
  def insertIsoViewPlayer(self, player):
    """ Inserts a new player view.
    player: player view.
    """
    player.getModel().subscribeEvent('position', self.startMovementEventFired)
    self.__isoViewPlayers.append(player)
    self.__allPlayers.add(player.getImg())

  def removeIsoViewPlayer(self, player):
    """ Removes an isometric player viewer from the viewers list.
    player: player view to be removed.
    """
    self.__allPlayers.remove(player.getImg())
    self.__isoViewPlayers.remove(player)
     
  def drawFirst(self, parent):
    """ Draws the room and all its components on screen for the first time.
    parent: isoview hud handler.
    """
    """
    for player in self.getModel().getPlayers():
      isoviewplayer = player.defaultView(self.getScreen(), self, parent)
      self.__isoViewPlayers.append(isoviewplayer)
      self.__allPlayers.add(isoviewplayer.getImg())
    """  
    for item in self.getModel().getItems():
      isoviewitem = item.defaultView(self.getScreen(), self, parent)
      self.__isoViewItems.append(isoviewitem)
      self.__allPlayers.add(isoviewitem.getImg())
    self.paintFloorFull()
    self.__allPlayers.draw(self.getScreen())
    pygame.display.update()
  
  def draw(self):
    """ Paints floor, players and items on the room.
    screen: screen handler.
    """
    self.paintPlayers()
    pygame.display.update()
    
  def orderSprites(self):
    """ Order the sprites according to their position.
    """
    #allPlayersTemp = pygame.sprite.OrderedUpdates()
    allPlayersTemp = []
    for image in self.__allPlayers:
      allPlayersTemp.append([image, image.rect.topleft[1]])
      self.__allPlayers.remove(image)
    allPlayersTemp = sorted(allPlayersTemp, key=operator.itemgetter(1), reverse=True)
    while len(allPlayersTemp):
      self.__allPlayers.append(allPlayersTemp.pop()[0])
    
  def paintPlayers(self):
    """ Paints all players on screen.
    """
    #self.orderSprites()
    self.__allPlayers.update()                     
    self.__allPlayers.clear(self.getScreen(), self.__bg.image)
    pygame.display.update(self.__allPlayers.draw(self.getScreen()))
    
  def paintFloorFull(self):
    """ Paints the room's floor using a single sprite.
    screen: screen handler.
    """
    self.getScreen().blit(self.__bg.image, self.__bg.rect)

  def findTile(self,pos):
    """ Gets the 3d tile coords that match a 2d point.
    pos: 2d coords.
    """
    for x in range(GG.utils.SCENE_SZ[0]):
      for z in range(GG.utils.SCENE_SZ[1]):
        if self.__tileList[x][z].contained(pos):
          if not self.__tileList[x][z].onBlank(pos):
            return [x, z]
    return [-1, -1]
   