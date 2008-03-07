import math
import os
import sys
import time
import signal
import pygame
from pygame.locals import *

tile_sz = [100,50]
tile2tile = 55.901699437
#tile2tile = math.sqrt(pow(tile_sz[0],2)+pow(tile_sz[1],2))
#55.901699437
char_sz = [50,50]
char_pos = [0,0,0]
screen_sz = [800,600]
screen_or = [screen_sz[0]/2,20]
scene_sz = [7,7]
gamezone_sz = [800,400]
hud_sz = [800,200]
hud_or = [0,gamezone_sz[1]]

animations = 5
anim_delay = 0.2
tile_stone = "tile_stone.png"
player_sprite1 = "black_mage.gif"
obj_book_sprite1 = "book.png"
sin30r = math.sin(math.radians(30))
cos30r = math.cos(math.radians(30))

hud_color_base = [177,174,200]
hud_color_border1 = [104,102,119]
hud_color_border2 = [138,136,160]
hud_color_border3 = [202,199,231]

#***************************************************** 
# CLASE OBSERVADOR
# Observador generico

class Observer:
  
  def __init__(self, name):
    self.name = name
    self.subject_list = []

  def add_subject(self,subject):
    self.subject_list.append(subject)
    subject.register(self)

  def notify(self, caller, momentum):
    pass
  
  def p3dtop2d(self, cord3d):
    x2d = (cord3d[0]-cord3d[2])*cos30r*tile_sz[0]
    y2d = ((cord3d[0]+cord3d[2])*sin30r)-cord3d[1]
    y2d = (y2d*tile_sz[1])
    
    # 0: suelo 
    if self.get_type() == 0:
      x2d = x2d - (tile_sz[0])
    # 1: personaje
    if self.get_type() == 1:
      x2d = x2d - (char_sz[0])
      y2d = y2d - (char_sz[1]/4)
    # 2: objeto -------------------------->> MODIFICAR
    if self.get_type() == 2:
      x2d = x2d - 55
      y2d = y2d + 8
    
    cord2d=[math.floor((x2d/math.sqrt(3))+screen_or[0]),math.floor(y2d+screen_or[1])]
    return cord2d
  
#*****************************************************
# CLASE OBS_HUD (subclase de OBSERVER)
# Observador de HUD

class Obs_Hud(Observer):
  
  def notify(self, caller, momentum):
    self.paint_hud()

  def paint_hud(self):
    pygame.draw.rect(screen,hud_color_border1,(hud_or[0],hud_or[1],hud_sz[0]-1,hud_sz[1]-1))
    pygame.draw.rect(screen,hud_color_border2,(hud_or[0]+2,hud_or[1]+2,hud_sz[0]-5,hud_sz[1]-5))
    pygame.draw.rect(screen,hud_color_border3,(hud_or[0]+10,hud_or[1]+10,hud_sz[0]-21,hud_sz[1]-21))
    pygame.draw.rect(screen,hud_color_base,(hud_or[0]+12,hud_or[1]+12,hud_sz[0]-25,hud_sz[1]-25))
    pygame.display.update()

#*****************************************************
# CLASE OBS_ROOM (subclase de OBSERVER)
# Observador de una habitacion

class Obs_Room(Observer):

  def notify(self, caller, momentum):
    self.paint_floor(self.subject_list[0].get_sprite())

  def paint_floor(self, tile_name):
    tile = os.path.join("data",tile_name)
    tile_surface = pygame.image.load(tile)
    for x in range(scene_sz[0]):
      for z in range(scene_sz[1]):
        screen.blit(tile_surface, self.p3dtop2d([x,0,z]))
    pygame.display.update()

  def get_type(self):
    return 0

#*****************************************************
# CLASE OBS_ITEM (subclase de OBSERVER)
# Observador de un item generico

class Obs_Item(Observer):

  pass

#*****************************************************
# CLASE OBS_PLAYER (subclase de OBS_ITEM)
# Observador de un jugador

class Obs_Player(Obs_Item):

  def notify(self, caller, event):
    pos = self.subject_list[caller].get_position()
    var_pos = [pos[0],pos[1],pos[2]]
    if event == "<move_static>":
      self.paint_pl(player_sprite1,pos)
    if event == "<move_up_1>":
      for x in range(0,animations):
        var_pos[2] = var_pos[2]-anim_delay
        self.paint_pl(player_sprite1,[var_pos[0],var_pos[1],var_pos[2]])
        pygame.display.update()
      self.subject_list[caller].set_position([pos[0],pos[1],pos[2]-1])  
    if event == "<move_down_1>":
      for x in range(0,animations):
        var_pos[2] = var_pos[2]+anim_delay
        self.paint_pl(player_sprite1,[var_pos[0],var_pos[1],var_pos[2]])
        pygame.display.update()
      self.subject_list[caller].set_position([pos[0],pos[1],pos[2]+1])  
    if event == "<move_left_1>":
      self.paint_pl(player_sprite1,[pos[0]-1,pos[1],pos[2]])
      self.subject_list[caller].set_position([pos[0]-1,pos[1],pos[2]])  
    if event == "<move_right_1>":
      self.paint_pl(player_sprite1,[pos[0]+1,pos[1],pos[2]])
      self.subject_list[caller].set_position([pos[0]+1,pos[1],pos[2]])  
      
  def paint_pl(self,sprite,cord3d):
    pl = os.path.join("data",sprite)
    pl_surface = pygame.image.load(pl)
    screen.blit(pl_surface, self.p3dtop2d(cord3d))
    pygame.display.update()

  def get_type(self):
    return 1

#*****************************************************
# CLASE OBS_OBJECT (subclase de OBS_ITEM)
# Observador de un objeto

class Obs_Object(Obs_Item):

  def notify(self, caller, event):
    self.paint_obj(obj_book_sprite1,[3,0,2])

  def paint_obj(self,sprite,cord3d):
    pl = os.path.join("data",sprite)
    pl_surface = pygame.image.load(pl)
    screen.blit(pl_surface, self.p3dtop2d(cord3d))
    pygame.display.update()

  def get_type(self):
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
    
  def notify_observers(self, momentum):
    for observer in self.observers:
      observer.notify(self.id, momentum)
  
  def get_name(self):
    return self.name

  def get_sprite(self):
    return self.sprite
  
  def get_size(self):
    return self.size

#*****************************************************
# CLASE SUB_HUD (subclase de SUBJECT)
# Objeto de tipo HUD

class Sub_Hud(Subject):

  pass

#*****************************************************
# CLASE SUB_ROOM (subclase de SUBJECT)
# Objeto de tipo habitacion
# Incluye informacion del suelo

class Sub_Room(Subject):

  def __init__(self, name, id, sprite):
    self.name = name
    self.id = id
    self.sprite = sprite
    self.observers = []
    self.players = []
    self.objects = []
    
  def insert_floor(self,floor):
    self.floor = floor

  def insert_player(self,player):
    self.players.append(player)
    
  def insert_object(self,object):
    self.objects.append(object)
    
  def notify(self, momentum):
    self.notify_observers(momentum)
#    for objects in self.objects:
#      object.update(momentum)  
    for players in self.players:
      player.notify(momentum)  
  
#*****************************************************
# CLASE SUB_ITEM (subclase de SUBJECT)
# Objeto generico

class Sub_Item(Subject):
  
  def __init__(self, name, id, sprite, size, position):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.id = id
    
  def get_position(self):
    return self.position

  def set_position(self, position):
    self.position = position
  
#*****************************************************
# CLASE SUB_PLAYER (subclase de SUB_ITEM)
# Jugador

class Sub_Player(Sub_Item):
 
  def __init__(self, name, id, sprite, size, position):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.id = id
    self.state_base = "standing_down"
    self.state_frame = 0
    
  def move_one(self,dir):
    # 0: estatico
    # 1: arriba
    # 2: abajo
    # 3: izquierda
    # 4: derecha
    if dir==0:
      self.notify_observers ("<move_static>")
    if dir==1:
      if self.position[2] > 0:
        self.notify_observers ("<move_up_1>")
    if dir==2:
      if self.position[2] < (scene_sz[1]-1):
        self.notify_observers ("<move_down_1>")
    if dir==3:
      if self.position[0] > 0:
        self.notify_observers ("<move_left_1>")
    if dir==4:
      if self.position[0] < (scene_sz[0]-1):
        self.notify_observers ("<move_right_1>")
        
  def get_state_base(self):
    return self.state_base

  def get_state_frame(self):
    return self.state_frame
        
#*****************************************************
# CLASE SUB_OBJECT (subclase de SUB_ITEM)
# Objeto no jugador

class Sub_Object(Sub_Item):
  
  def __init__(self, name, id, sprite, size, position):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.id = id
  
  def metodo_provisional(self): 
    self.name = self.name

""" =====================================================================================
#========================================================================================  
#==================================================================================== """  

def input(events):

  for event in events:
    
    if event.type == QUIT: 
       sys.exit(0)

    if event.type == KEYDOWN:
      
      if event.key == K_UP:
        sub_player1.move_one(1)
        
      if event.key == K_DOWN:
        sub_player1.move_one(2)
        
      if event.key == K_LEFT:
        sub_player1.move_one(3)
        
      if event.key == K_RIGHT:
        sub_player1.move_one(4)
        
      if event.key == K_ESCAPE:
        sys.exit(0)
          
""" =====================================================================================
#========================================================================================  
#==================================================================================== """  
  
pygame.init()
screen = pygame.display.set_mode(screen_sz)
pygame.display.set_caption('GenteGuada 0.01')

clock = pygame.time.Clock()
time_passed = clock.tick(30)
time_passed_seconds = time_passed/1000.0


sub_hud = Sub_Hud("hud", 0, " ", [0,0])
sub_room = Sub_Room("room1", 0, tile_stone)
sub_player1 = Sub_Player("player", 0, player_sprite1, char_sz,(2,0,2))
sub_room.insert_player(sub_player1)
#sub_object = Sub_Object("book", obj_book_sprite1, char_sz,[3,0,2])

obs_hud = Obs_Hud("<observer HUD>")
obs_hud.add_subject(sub_hud)
obs_room = Obs_Room("<observer Room>")
obs_room.add_subject(sub_room)
obs_player = Obs_Player("<observer jugador>")
obs_player.add_subject(sub_player1)
#obs_object = Obs_Object("<observer objeto>",sub_object)

sub_hud.notify_observers ("<pinta HUD>")
sub_room.notify_observers ("<pinta suelo>")
sub_player1.notify_observers ("<move_static>")
#sub_object.notify_observers ("<pinta objeto>")



while True: 
   input(pygame.event.get()) 

  
