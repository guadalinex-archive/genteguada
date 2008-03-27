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
        
  def insertPlayer(self,player):
    """ Inserta un observador de jugadores.
    player: observador de jugadores.
    """
    self.isoViewPlayer = player
      
  def insertItem(self,item):
    """ Inserta un observador de items no jugadores.
    item: observador de items no jugadores.
    """
    self.isoViewItem = item

  def draw(self, screen):
    """ Pinta el suelo, jugadores y objetos de la habitacion.
    screen: controlador de pantalla.
    """
    self.paintFloor(self.modelList[0].getSprite(), screen)
    self.isoViewPlayer.draw(screen)
    #self.isoViewItem.draw(screen)
    
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
