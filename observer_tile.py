from observer import *

#******************************************************************************
# CLASE OBS_TILE (subclase de OBSERVER)
# Observador de una baldosa

class ObserverTile(Observer):

  def __init__(self, topLeft, bottomRight, sprite, size):
    self.topLeft = topLeft
    self.bottomRight = bottomRight
    self.id = id
    self.sprite = sprite
    self.size = size
    self.observers = []
  
  def contained(self, pos):
    if self.bottomRight[0] > pos[0] > self.topLeft[0]:
      if self.bottomRight[1] > pos[1] > self.topLeft[1]:
        return 1
    return 0

  def onBlank(self, pos):
    iniPos = [pos[0]-self.topLeft[0], pos[1]-self.topLeft[1]]
    if iniPos[0] < (TILE_SZ[0] / 2):
      if iniPos[1] < (TILE_SZ[1] / 2):
        #top left
        if (iniPos[0] + (iniPos[1] * 2)) <= (TILE_SZ[0]/2):
          return 1
      else:
        #bottom left
        iniPos[1] -= (TILE_SZ[1] / 2)
        iniPos[1] = (TILE_SZ[1] / 2) - iniPos[1]
        if (iniPos[0] + (iniPos[1] * 2)) <= (TILE_SZ[0]/2):
          return 1
    else:
      if iniPos[1] < (TILE_SZ[1] / 2):
        #top right
        iniPos[0] -= (TILE_SZ[0] / 2)
        iniPos[0] = (TILE_SZ[0] / 2) - iniPos[0]
        if (iniPos[0] + (iniPos[1] * 2)) <= (TILE_SZ[0]/2):
          return 1
      else:
        #bottom right
        iniPos[0] -= (TILE_SZ[0] / 2)
        iniPos[1] -= (TILE_SZ[1] / 2)
        iniPos[0] = (TILE_SZ[0] / 2) - iniPos[0]
        iniPos[1] = (TILE_SZ[1] / 2) - iniPos[1]
        if (iniPos[0] + (iniPos[1] * 2)) <= (TILE_SZ[0]/2):
          return 1
    return 0    
