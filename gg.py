import math
import os
import sys
import time
import signal
import pygame
from pygame.locals import *

TILE_SZ = [100, 50]
TILE2TILE = 55.901699437
#tile2tile = math.sqrt(pow(TILE_SZ[0],2)+pow(TILE_SZ[1],2))
#55.901699437
CHAR_SZ = [50, 50]
CHAR_POS = [0, 0, 0]
SCREEN_SZ = [800, 600]
SCREEN_OR = [SCREEN_SZ[0]/2, 20]
SCENE_SZ = [7, 7]
GAMEZONE_SZ = [800, 400]
HUD_SZ = [800, 200]
HUD_OR = [0, GAMEZONE_SZ[1]]

ANIMATIONS = 5
MAX_FRAMES = 5
ANIM_DELAY = 0.2
SPEED = 55.901699437

TILE_STONE = "tile_stone.png"
PLAYER_SPRITE1 = "black_mage.gif"
PLAYER_SPRITE2 = "black_mage_red.gif"
OBJ_BOOK_SPRITE1 = "book.png"
SIN30R = math.sin(math.radians(30))
COS30R = math.cos(math.radians(30))

HUD_COLOR_BASE = [177, 174, 200]
HUD_COLOR_BORDER1 = [104, 102, 119]
HUD_COLOR_BORDER2 = [138, 136, 160]
HUD_COLOR_BORDER3 = [202, 199, 231]

#***************************************************** 
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
   
    # 0: suelo 
    if self.getType() == 0:
      x2d = x2d - (TILE_SZ[0])
    # 1: personaje
    if self.getType() == 1:
      x2d = x2d - (CHAR_SZ[0])
      y2d = y2d - (CHAR_SZ[1] / 4)
    # 2: objeto -------------------------->> MODIFICAR
    if self.getType() == 2:
      x2d = x2d - 55
      y2d = y2d + 8
    
    cord2d = [math.floor((x2d/math.sqrt(3)) + SCREEN_OR[0]), math.floor(y2d + SCREEN_OR[1])]
    return cord2d
  
#*****************************************************
# CLASE OBS_HUD (subclase de OBSERVER)
# Observador de HUD

class ObserverHud(Observer):
  
  def paint(self):
    self.paintHud()

  def paintHud(self):
    pygame.draw.rect(screen, HUD_COLOR_BORDER1, (HUD_OR[0], HUD_OR[1], HUD_SZ[0] - 1, HUD_SZ[1] - 1))
    pygame.draw.rect(screen, HUD_COLOR_BORDER2, (HUD_OR[0] + 2,HUD_OR[1] + 2, HUD_SZ[0] - 5, HUD_SZ[1] - 5))
    pygame.draw.rect(screen, HUD_COLOR_BORDER3, (HUD_OR[0] + 10, HUD_OR[1] + 10, HUD_SZ[0] - 21, HUD_SZ[1] - 21))
    pygame.draw.rect(screen, HUD_COLOR_BASE, (HUD_OR[0] + 12, HUD_OR[1] + 12, HUD_SZ[0] - 25, HUD_SZ[1] - 25))
    pygame.display.update()

#*****************************************************
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
        self.tileList[x].append(ObserverTile([pos[0] - SCREEN_OR[0], pos[1]-SCREEN_OR[1]], [pos[0] + SCREEN_OR[0], pos[1] + SCREEN_OR[1]], TILE_STONE, TILE_SZ))
        
  def insertPlayer(self,player):
    self.observerPlayer = player
      
  def draw(self):
    self.paintFloor(self.subjectList[0].getSprite())
    self.observerPlayer.draw()
    
  def paintFloor(self, tile_name):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, GAMEZONE_SZ[0], GAMEZONE_SZ[1]))
    tile = os.path.join("data", tile_name)
    tileSurface = pygame.image.load(tile)
    for x in range(SCENE_SZ[0]):
      for z in range(SCENE_SZ[1]):
        screen.blit(tileSurface, self.p3dToP2d([x, 0, z]))

  def findTile(self,pos):
    #x, y = pygame.mouse.get_pos()
    for x in range(SCENE_SZ[0]):
      for z in range(SCENE_SZ[1]):
        #self.tileList[x].[z].
        pass
    # devuelve la posicion [x,z] en la que ha pinchado el usuario

  def getType(self):
    return 0

#*****************************************************
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
        return true
    return false

  def onBlank(self, pos):
    iniPos = [pos[0]-self.topLeft[0], pos[1]-self.topLeft[1]]
    if iniPos[0] < (TILE_SZ[0] / 2):
      if iniPos[1] < (TILE_SZ[1] / 2):
        if iniPos[0] <= (iniPos[0] * 2): #cuadrante 1
          return true
      else:
        iniPos[1] -= (TILE_SZ[1] / 2)
        iniPos[1] = (TILE_SZ[1] / 2) - iniPos[1]
        if iniPos[0] <= (iniPos[0] * 2): #cuadrante 2
          return true
    else:
      if iniPos[1] < (TILE_SZ[1] / 2):
        iniPos[0] -= (TILE_SZ[0] / 2)
        iniPos[0] = (TILE_SZ[0] / 2) - iniPos[0]
        if iniPos[0] <= (iniPos[0] * 2): #cuadrante 3
          return true
        else:
          iniPos[0] -= (TILE_SZ[0] / 2)
          iniPos[1] -= (TILE_SZ[1] / 2)
          iniPos[0] = (TILE_SZ[0] / 2) - iniPos[0]
          iniPos[1] = (TILE_SZ[1] / 2) - iniPos[1]
          if iniPos[0] <= (iniPos[0] * 2): #cuadrante 4
            return true
    return false    
    
#*****************************************************
# CLASE OBS_ITEM (subclase de OBSERVER)
# Observador de un item generico

class ObserverItem(Observer):

  pass

#*****************************************************
# CLASE OBS_PLAYER (subclase de OBS_ITEM)
# Observador de un jugador

class ObserverPlayer(ObserverItem):

  def draw(self):
    for ind in range(self.subjectList.__len__()):
      self.drawOne(ind)

  def drawOne(self, caller):
    pos = self.subjectList[caller].getPosition()
    varPos = [pos[0], pos[1], pos[2]]
    event = self.subjectList[caller].getState()
    sprite = self.subjectList[caller].getSprite()
    if event == "standing_down":
      self.paintPlayer(sprite, pos, caller)
    if event == "walking_up":
      self.paintPlayer(sprite, pos, caller)
    if event == "walking_down":
      self.paintPlayer(sprite, pos, caller)
    if event == "walking_left":
      self.paintPlayer(sprite, pos, caller)
    if event == "walking_right":
      self.paintPlayer(sprite, pos, caller)
      
  def paintPlayer(self, sprite, cord3d, caller):
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

#*****************************************************
# CLASE OBS_OBJECT (subclase de OBS_ITEM)
# Observador de un objeto

class ObserverObject(ObserverItem):

  def notify(self, caller, event):
    self.paintObject(OBJ_BOOK_SPRITE1, [3, 0, 2])

  def paintObject(self, sprite, cord3d):
    pl = os.path.join("data", sprite)
    plSurface = pygame.image.load(pl)
    screen.blit(plSurface, self.p3dToP2d(cord3d))
    pygame.display.update()

  def getType(self):
    return 2

""" =====================================================================================
#========================================================================================  
#==================================================================================== """  

#*****************************************************
# CLASE SUBJECT
# Objeto generico

class Subject:
  
  def __init__(self, name, id, sprite, size):
    self.name = name
    self.sprite = sprite
    self.size = size
    self.id = id
    self.observers = []
    
  def register(self, observer):
    self.observers.append(observer)
    
  def unregister(self, observer):
    self.observers.remove(observer)
    
  def getName(self):
    return self.name

  def getSprite(self):
    return self.sprite
  
  def getSize(self):
    return self.size

#*****************************************************
# CLASE SUB_HUD (subclase de SUBJECT)
# Objeto de tipo HUD

class SubjectHud(Subject):

  pass

#*****************************************************
# CLASE SUB_ROOM (subclase de SUBJECT)
# Objeto de tipo habitacion
# Incluye informacion del suelo

class SubjectRoom(Subject):

  def __init__(self, name, id, sprite):
    self.name = name
    self.id = id
    self.sprite = sprite
    self.observers = []
    self.players = []
    self.objects = []
    
  def insertFloor(self, floor):
    self.floor = floor

  def insertPlayer(self, player):
    self.players.append(player)
    
  def insertObject(self, object):
    self.objects.append(object)
    
  def notify(self):
    self.notify_observers(id)
    for player in self.players:
      player.notify()  
  
  def tick(self):
    for player in self.players:
      player.tick()  
    
#*****************************************************
# CLASE SUB_ITEM (subclase de SUBJECT)
# Objeto generico

class SubjectItem(Subject):
  
  def __init__(self, name, id, sprite, size, position):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.id = id
    
  def getPosition(self):
    return self.position

  def setPosition(self, position):
    self.position = position
  
#*****************************************************
# CLASE SUB_PLAYER (subclase de SUB_ITEM)
# Jugador

class SubjectPlayer(SubjectItem):
 
  def __init__(self, name, id, sprite, size, position):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.id = id
    self.state = "standing_down"
    self.stateFrame = 0
    
  def moveOne(self, dir):
    if self.stateFrame <> 0:
      pass
    else:
      if dir <> 0:
        self.stateFrame = 0
      if dir == 1 and self.position[2] > 0:
        self.state = "walking_up"  
      if dir == 2 and self.position[2] < (SCENE_SZ[1] - 1):
        self.state = "walking_down"  
      if dir == 3 and self.position[0] > 0:
        self.state = "walking_left"  
      if dir == 4 and self.position[0] < (SCENE_SZ[0] - 1):
        self.state = "walking_right"
  
  def getState(self):
    return self.state

  def getStateFrame(self):
    return self.stateFrame

  def getDir(self):
    if self.state == "standing_up" or self.state == "standing_down" or self.state == "standing_left" or self.state == "standing_right":
      return 0
    if self.state == "walking_up":
      return 1
    if self.state == "walking_down":
      return 2
    if self.state == "walking_left":
       return 3
    if self.state == "walking_right":
      return 4

  def tick(self):
    if self.state == "walking_up" or self.state == "walking_down" or self.state == "walking_left" or self.state == "walking_right":
      if self.stateFrame == (MAX_FRAMES - 1):
        pos = self.getPosition()
        if self.state == "walking_up":
          self.setPosition([pos[0], pos[1], pos[2] - 1])
        if self.state == "walking_down":
          self.setPosition([pos[0], pos[1], pos[2] + 1])
        if self.state == "walking_left":
          self.setPosition([pos[0] - 1, pos[1], pos[2]])  
        if self.state == "walking_right":
          self.setPosition([pos[0] + 1, pos[1], pos[2]])  
        self.state = "standing_down"
        self.stateFrame = 0
      else:
        self.stateFrame += 1
        
  def notify(self):
    self.notify_observers(self.state)
        
#*****************************************************
# CLASE SUB_OBJECT (subclase de SUB_ITEM)
# Objeto no jugador

class SubjectObject(SubjectItem):
  
  def __init__(self, name, id, sprite, size, position):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.id = id

""" =====================================================================================
#========================================================================================  
#==================================================================================== """  

def input(events):

  for event in events:
    if event.type == QUIT: 
      sys.exit(0)
    if event.type == KEYDOWN:
      if event.key == K_UP:
        subPlayer1.moveOne(1)
      if event.key == K_DOWN:
        subPlayer1.moveOne(2)
      if event.key == K_LEFT:
        subPlayer1.moveOne(3)
      if event.key == K_RIGHT:
        subPlayer1.moveOne(4)
      if event.key == MOUSEBUTTONDOWN:
        #subPlayer1.
        pass
      if event.key == K_ESCAPE:
        sys.exit(0)
          
""" =====================================================================================
#========================================================================================  
#==================================================================================== """  
  
pygame.init()
screen = pygame.display.set_mode(SCREEN_SZ)
pygame.display.set_caption('GenteGuada 0.01')

subHud = SubjectHud("hud", 0, " ", [0,0])
subRoom = SubjectRoom("room1", 0, TILE_STONE)
subPlayer1 = SubjectPlayer("player", 0, PLAYER_SPRITE1, CHAR_SZ, (2, 0, 2))
subPlayer2 = SubjectPlayer("player", 0, PLAYER_SPRITE2, CHAR_SZ, (4, 0, 4))
subRoom.insertPlayer(subPlayer1)
subRoom.insertPlayer(subPlayer2)
#sub_object = SubjectObject("book", obj_book_sprite1, CHAR_SZ,[3,0,2])

obsHud = ObserverHud("<observer HUD>")
obsHud.addSubject(subHud)
obsRoom = ObserverRoom("<observer Room>")
obsRoom.addSubject(subRoom)
observerPlayer = ObserverPlayer("<observer jugador>")
observerPlayer.addSubject(subPlayer1)
observerPlayer.addSubject(subPlayer2)
obsRoom.insertPlayer(observerPlayer)
#obs_object = ObserverObject("<observer objeto>",sub_object)

#subHud.notify_observers ("<pinta HUD>")
#subRoom.notify_observers ("<pinta suelo>")
#subPlayer1.notify_observers ("standing_down")
#subPlayer2.notify_observers ("standing_down")

timePassed = 0
clock = pygame.time.Clock()

while True:
  clock = pygame.time.Clock()
  timePassed = timePassed + clock.tick(30)
  timePassedSeconds = timePassed / 1000.0
  if timePassedSeconds >= 0.02:
    timePassed = 0
    subRoom.tick()
    obsRoom.draw()
    obsHud.paintHud()
  input(pygame.event.get()) 
    
  