import os
import pygame
from isoview_item import *

class IsoViewPlayer(IsoViewItem):
  """ Clase IsoViewPlayer.
  Define a la vista de un item de tipo jugador.
  """

  def draw(self, screen):
    """ Realiza llamadas para pintar en pantalla todos los jugadores observados.
    screen: controlador de pantalla.
    """
    for ind in range(self.modelList.__len__()):
      self.drawOne(ind, screen)

  def drawOne(self, caller, screen):
    """ Pinta un jugador moviendose en una direccion en pantalla.
    caller: jugador a pintar
    screen: controlador de pantalla
    NOTA -> Este metodo se emplea solo para mover al jugador con el teclado.
    NOTA -> Si se elimina el control de teclado, se puede prescindir del metodo.
    """
    pos = self.modelList[caller].getPosition()
    varPos = [pos[0], pos[1], pos[2]]
    event = self.modelList[caller].getState()
    sprite = self.modelList[caller].getSprite()
    if event == "standing_down":
      self.paintPlayer(sprite, pos, caller, screen)
    if event == "walking_up":
      self.paintPlayer(sprite, pos, caller, screen)
    if event == "walking_down":
      self.paintPlayer(sprite, pos, caller, screen)
    if event == "walking_left":
      self.paintPlayer(sprite, pos, caller, screen)
    if event == "walking_right":
      self.paintPlayer(sprite, pos, caller, screen)
    if event == "walking_topleft":
      self.paintPlayer(sprite, pos, caller, screen)
    if event == "walking_bottomright":
      self.paintPlayer(sprite, pos, caller, screen)
    if event == "walking_bottomleft":
      self.paintPlayer(sprite, pos, caller, screen)
    if event == "walking_topright":
      self.paintPlayer(sprite, pos, caller, screen)
      
  def paintPlayer(self, sprite, cord3d, caller, screen):
    """ Pinta un jugador en pantalla.
    sprite: grafico del jugador.
    cord3d: coordenadas 3d del jugador.
    caller: jugador a pintar.
    screen: controlador de pantalla.
    """
    pl = os.path.join(DATA_PATH, sprite)
    plSurface = pygame.image.load(pl)
    state = self.modelList[caller].getStateFrame()
    dir = self.modelList[caller].getDir()
    screen.blit(plSurface, self.p3dToP2d(cord3d, state, dir))
    pygame.display.update()

  def p3dToP2d(self, cord3d, state, dir):
    """ Convierte un punto con coordenadas 3d virtuales en 2d con cord fisicas.
    cord3d: punto 3d a convertir.
    state: estado de la animacion en la que se encuentra el personaje.
    dir: direccion de movimiento del jugador.
    """
    x2d = (cord3d[0] - cord3d[2]) * COS30R * TILE_SZ[0]
    y2d = ((cord3d[0] + cord3d[2]) * SIN30R) - cord3d[1]
    y2d = (y2d * TILE_SZ[1])
    
    x2d = x2d - (CHAR_SZ[0])
    y2d = y2d - (CHAR_SZ[1] / 4)
    
    x2d = math.floor((x2d / math.sqrt(3)) + SCREEN_OR[0])
    y2d = math.floor(y2d + SCREEN_OR[1])
   
    if dir == 1: #arriba
      x2d = x2d + (((TILE_SZ[0] / 2)*state) / 5)
      y2d = y2d - (((TILE_SZ[1] / 2)*state) / 5)
    if dir == 2: #abajo
      x2d = x2d - (((TILE_SZ[0] / 2)*state) / 5)
      y2d = y2d + (((TILE_SZ[1] / 2)*state) / 5)
    if dir == 3: #izquierda
      x2d = x2d - (((TILE_SZ[0] / 2)*state) / 5)  
      y2d = y2d - (((TILE_SZ[1] / 2)*state) / 5)
    if dir == 4: #derecha
      x2d = x2d + (((TILE_SZ[0] / 2)*state) / 5)
      y2d = y2d + (((TILE_SZ[1] / 2)*state) / 5)
    if dir == 5: #arriba-izquierda
      y2d = y2d - (((TILE_SZ[1])*state) / 5)
    if dir == 6: #abajo-derecha
      y2d = y2d + (((TILE_SZ[1])*state) / 5)
    if dir == 7: #abajo-izquierda
      x2d = x2d - (((TILE_SZ[0])*state) / 5)  
    if dir == 8: #arriba-derecha
      x2d = x2d + (((TILE_SZ[0])*state) / 5)
      
    cord2d = [x2d, y2d]
    return cord2d

  def getType(self):
    """ Devuelve un valor indicando que esta es una clase tipo IsoViewPlayer.
    """
    return 1
