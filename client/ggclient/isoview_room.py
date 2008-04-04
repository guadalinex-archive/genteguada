import os
import pygame
from isoview import *
from isoview_tile import *

class IsoViewRoom(IsoView):
  """ Clase IsoViewRoom.
  Define a la vista de una habitacion.
  """

  def __init__(self, name):
    """ Constructor de la clase.
    name: nombre de la habitacion.
    """
    self.name = name
    self.modelList = []
    self.spritesList = []
    self.tileList = []
    for x in range(SCENE_SZ[0]):
      for z in range(SCENE_SZ[1]):
        varPos = self.p3dToP2d([x, 0, z])
        pos = [int(varPos[0]),int(varPos[1])]
        self.tileList.append([])
        self.tileList[x].append(IsoViewTile(\
            [pos[0], pos[1]], \
            [pos[0] + TILE_SZ[0], pos[1] + TILE_SZ[1]], \
            TILE_STONE, TILE_SZ, 0))
        
  def insertIsoViewPlayer(self,player):
    """ Inserta un observador de jugadores.
    player: observador de jugadores.
    """
    self.isoViewPlayer = player
    bgPath = os.path.join(DATA_PATH, self.modelList[0].getSpriteFull())
    bg = pygame.sprite.Sprite()
    bg.image = pygame.image.load(bgPath)
    bg.rect = bg.image.get_rect()
    bg.rect.topleft = BG_FULL_OR
    player.setBg(bg)
  
  def insertItem(self,item):
    """ Inserta un observador de items no jugadores.
    item: observador de items no jugadores.
    """
    self.isoViewItem = item

  def drawFirst(self, screen):
    self.paintFloorFull(self.modelList[0].getSpriteFull(), screen)
    self.isoViewPlayer.drawFirst(screen)
  
  def draw(self, screen):
    """ Pinta el suelo, jugadores y objetos de la habitacion.
    screen: controlador de pantalla.
    """
    self.paintFloorFull(self.modelList[0].getSpriteFull(), screen)
    self.isoViewPlayer.draw(screen)
    
  def paintFloorFull(self, spriteFull, screen):
    """ Pinta el suelo de una habitacion con un solo sprite.
    screen: controlador de pantalla.
    """
    self.modelList[0].getSpriteFull()
    bgPath = os.path.join(DATA_PATH, spriteFull)
    bg = pygame.sprite.Sprite()
    bg.image = pygame.image.load(bgPath)
    bg.rect = bg.image.get_rect()
    bg.rect.topleft = BG_FULL_OR
    screen.blit(bg.image, bg.rect)

  def paintFloor(self, tile_name, screen):
    """ Pinta el suelo de la habitacion.
    tile_name: grafico de cada baldosa.
    screen: controlador de pantalla.
    """
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, GAMEZONE_SZ[0], GAMEZONE_SZ[1]))
    tile = os.path.join(DATA_PATH, tile_name)
    tileSurface = pygame.image.load(tile)
    for x in range(SCENE_SZ[0]):
      for z in range(SCENE_SZ[1]):
        screen.blit(tileSurface, self.p3dToP2d([x, 0, z]))

  def findTile(self,pos):
    """ Encuentra la posicion 3d de la baldosa a la que corresponden unas \
    coordenadas 2d.
    pos: coordenadas 2d de pantalla.
    """
    for x in range(SCENE_SZ[0]):
      for z in range(SCENE_SZ[1]):
        if self.tileList[x][z].contained(pos):
          if not self.tileList[x][z].onBlank(pos):
            return [x, z]
    return [-1, -1]

  def getType(self):
    """ Devuelve un valor indicando que esta es una clase tipo IsoViewRoom.
    """
    return 0
  
  def newAction(self, event):
    """ Ejecuta un metodo tras recibir informacion sobre un evento.
    event: informacion sobre el evento.    
    """
    self.isoViewPlayer.newAction(event)

