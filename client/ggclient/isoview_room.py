import os
import pygame

import utils
import isoview
import isoview_tile

class IsoViewRoom(isoview.IsoView):
  """ Clase IsoViewRoom.
  Define a la vista de una habitacion.
  """

  def __init__(self, name, screen):
    """ Constructor de la clase.
    name: nombre de la habitacion.
    """
    isoview.IsoView.__init__(self, name)
    self.screen = screen
    self._spritesList = []
    self._tileList = []
    for x in range(utils.SCENE_SZ[0]):
      for z in range(utils.SCENE_SZ[1]):
        varPos = self._p3dToP2d([x, 0, z])
        pos = [int(varPos[0]),int(varPos[1])]
        self._tileList.append([])
        self._tileList[x].append(isoview_tile.IsoViewTile(\
            [pos[0], pos[1]], \
            [pos[0] + utils.TILE_SZ[0], pos[1] + utils.TILE_SZ[1]], \
            utils.TILE_STONE, utils.TILE_SZ, 0))
        
  def insertIsoViewPlayer(self,player):
    """ Inserta un observador de jugadores.
    player: observador de jugadores.
    """
    self._isoViewPlayer = player
    bgPath = os.path.join(utils.DATA_PATH, self._modelList[0].getSpriteFull())
    bg = pygame.sprite.Sprite()
    bg.image = pygame.image.load(bgPath)
    bg.rect = bg.image.get_rect()
    bg.rect.topleft = utils.BG_FULL_OR
    player.setBg(bg)
  
  def insertItem(self,item):
    """ Inserta un observador de items no jugadores.
    item: observador de items no jugadores.
    """
    self._isoViewItem = item

  def drawFirst(self):
    self.paintFloorFull(self._modelList[0].getSpriteFull())
    self._isoViewPlayer.drawFirst(self.screen)
  
  def draw(self):
    """ Pinta el suelo, jugadores y objetos de la habitacion.
    screen: controlador de pantalla.
    """
    self.paintFloorFull(self._modelList[0].getSpriteFull(), self.screen)
    self.isoViewPlayer.draw(self.screen)
    
  def paintFloorFull(self, spriteFull):
    """ Pinta el suelo de una habitacion con un solo sprite.
    screen: controlador de pantalla.
    """
    self._modelList[0].getSpriteFull()
    bgPath = os.path.join(utils.DATA_PATH, spriteFull)
    bg = pygame.sprite.Sprite()
    bg.image = pygame.image.load(bgPath)
    bg.rect = bg.image.get_rect()
    bg.rect.topleft = utils.BG_FULL_OR
    self.screen.blit(bg.image, bg.rect)

  def paintFloor(self, tile_name):
    """ Pinta el suelo de la habitacion.
    tile_name: grafico de cada baldosa.
    screen: controlador de pantalla.
    """
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, utils.GAMEZONE_SZ[0], utils.GAMEZONE_SZ[1]))
    tile = os.path.join(utils.DATA_PATH, tile_name)
    tileSurface = pygame.image.load(tile)
    for x in range(utils.SCENE_SZ[0]):
      for z in range(utils.SCENE_SZ[1]):
        self.screen.blit(tileSurface, self._p3dToP2d([x, 0, z]))

  def findTile(self,pos):
    """ Encuentra la posicion 3d de la baldosa a la que corresponden unas \
    coordenadas 2d.
    pos: coordenadas 2d de pantalla.
    """
    for x in range(utils.SCENE_SZ[0]):
      for z in range(utils.SCENE_SZ[1]):
        if self._tileList[x][z].contained(pos):
          if not self._tileList[x][z].onBlank(pos):
            return [x, z]
    return [-1, -1]
  
  def newAction(self, event):
    """ Ejecuta un metodo tras recibir informacion sobre un evento.
    event: informacion sobre el evento.    
    """
    self._isoViewPlayer.newAction(event)

  def isoViewRoom(self):
    pass