from utils import *

#******************************************************************************
# CLASE OBSERVADOR
# Observador generico

class Observer:
  
  def __init__(self, name):
    self.name = name
    self.subjectList = []

  def addSubject(self, subject):
    self.subjectList.append(subject)
    subject.register(self)

  def notify(self, caller):
     pass
  
  def p3dToP2d(self, cord3d):
    x2d = (cord3d[0] - cord3d[2]) * COS30R * TILE_SZ[0]
    y2d = ((cord3d[0] + cord3d[2]) * SIN30R) - cord3d[1]
    y2d = (y2d * TILE_SZ[1])
   
    if self.getType() == 0: # tile
      x2d = x2d - (TILE_SZ[0])
    if self.getType() == 1: # player
      x2d = x2d - (CHAR_SZ[0])
      y2d = y2d - (CHAR_SZ[1] / 4)
    if self.getType() == 2: # object
      x2d = x2d - 55
      y2d = y2d + 8
    
    cord2d = [math.floor((x2d/math.sqrt(3)) + SCREEN_OR[0]), \
              math.floor(y2d + SCREEN_OR[1])]
    return cord2d
