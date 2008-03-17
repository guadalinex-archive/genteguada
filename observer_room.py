import os
import pygame
from observer import *
from observer_tile import *

#******************************************************************************

# CLASE OBS_ROOM (subclase de OBSERVER)
# Observador de una habitacion

class ObserverRoom(Observer):

  def __init__(self, name):
    self.name = name
    self.subjectList = []
    self.tileList = []
    for x in range(SCENE_SZ[0]):
      for z in range(SCENE_SZ[1]):
        varPos = self.p3dToP2d([x, 0, z])
        pos = [int(varPos[0]),int(varPos[1])]
        self.tileList.append([])
        self.tileList[x].append(ObserverTile(\
            [pos[0], pos[1]], \
            [pos[0] + TILE_SZ[0], pos[1] + TILE_SZ[1]], \
            TILE_STONE, TILE_SZ))
        
  def insertPlayer(self,player):
    self.observerPlayer = player
      
  def draw(self, screen):
    self.paintFloor(self.subjectList[0].getSprite(), screen)
    self.observerPlayer.draw(screen)
    
  def paintFloor(self, tile_name, screen):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, GAMEZONE_SZ[0], GAMEZONE_SZ[1]))
    tile = os.path.join("data", tile_name)
    tileSurface = pygame.image.load(tile)
    for x in range(SCENE_SZ[0]):
      for z in range(SCENE_SZ[1]):
        screen.blit(tileSurface, self.p3dToP2d([x, 0, z]))

  def findTile(self,pos):
    for x in range(SCENE_SZ[0]):
      for z in range(SCENE_SZ[1]):
        if self.tileList[x][z].contained(pos):
          if not self.tileList[x][z].onBlank(pos):
            print "UBICADO EN --> (", x, ", ",z ,")"
            return [x,z]

  def getType(self):
    return 0
