import os
import pygame
from observer_item import *

#******************************************************************************
# CLASE OBS_PLAYER (subclase de OBS_ITEM)
# Observador de un jugador

class ObserverPlayer(ObserverItem):

  def draw(self, screen):
    for ind in range(self.subjectList.__len__()):
      self.drawOne(ind, screen)

  def drawOne(self, caller, screen):
    pos = self.subjectList[caller].getPosition()
    varPos = [pos[0], pos[1], pos[2]]
    event = self.subjectList[caller].getState()
    sprite = self.subjectList[caller].getSprite()
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
      
  def paintPlayer(self, sprite, cord3d, caller, screen):
    pl = os.path.join("data", sprite)
    plSurface = pygame.image.load(pl)
    state = self.subjectList[caller].getStateFrame()
    dir = self.subjectList[caller].getDir()
    screen.blit(plSurface, self.p3dToP2d(cord3d, state, dir))
    pygame.display.update()

  def p3dToP2d(self, cord3d, state, dir):
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
      
    cord2d = [x2d, y2d]
    return cord2d

  def getType(self):
    return 1
