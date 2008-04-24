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
    name: room label.
    """
    isoview.IsoView.__init__(self, model, screen)
    bgPath = os.path.join(GG.utils.DATA_PATH, model.getSpriteFull())
    self.__bg = pygame.sprite.Sprite()
    self.__bg.image = pygame.image.load(bgPath)
    self.__bg.rect = self.__bg.image.get_rect()
    self.__bg.rect.topleft = GG.utils.BG_FULL_OR
    self.__isoViewPlayers = []
    self.__isoViewItems = []
    self.__allPlayers = pygame.sprite.RenderUpdates()
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
    self.__allPlayers.remove(player.getImg())
    self.__isoViewPlayers.remove(player)
     
  def drawFirst(self, parent):
    """ Draws the room and all its components on screen for the first time.
    """
    for player in self.getModel().getPlayers():
      isoviewplayer = player.defaultView(self.getScreen(), self, parent)
      self.__isoViewPlayers.append(isoviewplayer)
      self.__allPlayers.add(isoviewplayer.getImg())
    for item in self.getModel().getItems():
      isoviewitem = item.defaultView(self.getScreen(), parent)
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
    
  def paintPlayers(self):
    """ Paints all players on screen.
    """
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
  
  def newAction(self, event):
    """ Runs a method after receiving an event.
    event: event info.    
    """
    for player in self.__isoViewPlayers:
      if player.getModel() == event.getParams()["player"]:
        player.newAction(event)
    self.draw()
    
  def startMovementEventFired(self, event):
    """ Starts some methods after receiving a movement event.
    event: movement event data.
    """
    self.newAction(event)
  