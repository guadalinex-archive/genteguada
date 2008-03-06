import math
import os
import sys
import time
import signal
import pygame
from pygame.locals import *
#from pygame.display import *

#*****************************************************
# 
#*****************************************************

tile_sz = [100,50]
char_sz = [50,50]
char_pos = [0,0,0]
screen_sz = [800,600]
screen_or = [screen_sz[0]/2,20]
scene_sz = [7,7]
gamezone_sz = [800,400]
hud_sz = [800,200]
hud_or = [0,gamezone_sz[1]]

animations = 5
anim_delay = 1/animations
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
#*****************************************************

class Observer:
  
  # listener = observer
  # name: nombre del observador
  
  """
  def __init__(self, name, subject):
    self.name = name
    self.count = 1
    self.subject_list = []
    self.subject_list.append(subject)
    subject.register(self)
  """

  def __init__(self, name):
    self.name = name
    self.count = 0
    self.subject_list = []

  def add_subject(self,subject):
    self.subject_list.append(subject)
    self.count += 1
    subject.register(self)

  def notify(self, caller, event):
    #print self.name, "received event", event
    self.name = self.name
  
  def p3dtop2d(self, cord3d):
    # cord3d: punto 3d en el mundo
    x2d = (cord3d[0]-cord3d[2])*cos30r*tile_sz[0]
    y2d = ((cord3d[0]+cord3d[2])*sin30r)-cord3d[1]
    y2d = (y2d*tile_sz[1])
    
    # Ajusta la posicion del sprite dependiendo de su tipo y su tamanyo
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
#*****************************************************

class Obs_Hud(Observer):
  
  def notify(self, caller, event):
    #print self.name, "received event", event
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
#*****************************************************

class Obs_Room(Observer):

  def metodo_provisional(self):
    self.name = self.name 

#*****************************************************
# CLASE OBS_FLOOR (subclase de OBSERVER)
# Observador del suelo de una habitacion
#*****************************************************

class Obs_Floor(Observer):

  def notify(self, caller, event):
    #print self.name, "received event", event
    self.paint_floor(tile_stone)

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
#*****************************************************

class Obs_Item(Observer):

  def metodo_provisional(self):
    self.name = self.name 

#*****************************************************
# CLASE OBS_PLAYER (subclase de OBS_ITEM)
# Observador de un jugador
#*****************************************************

class Obs_Player(Obs_Item):

  def notify(self, caller, event):
    #print self.name, "received event", event
    pos = self.subject_list[caller].get_position()
    var_pos = [pos[0],pos[1],pos[2]]
    if event == "<move_static>":
      self.paint_pl(player_sprite1,pos)
    if event == "<move_up_1>":
      for i in range(0,animations):
        var_pos[2] = var_pos[2]-anim_delay
        self.paint_pl(player_sprite1,[var_pos[0],var_pos[1],var_pos[2]-1])
        pygame.display.update()
        #self.paint_pl(player_sprite1,[pos[0],pos[1],pos[2]-1])
      self.subject_list[0].set_position([pos[0],pos[1],pos[2]-1])  
    if event == "<move_down_1>":
      self.paint_pl(player_sprite1,[pos[0],pos[1],pos[2]+1])
      self.subject_list[0].set_position([pos[0],pos[1],pos[2]+1])  
    if event == "<move_left_1>":
      self.paint_pl(player_sprite1,[pos[0]-1,pos[1],pos[2]])
      self.subject_list[0].set_position([pos[0]-1,pos[1],pos[2]])  
    if event == "<move_right_1>":
      self.paint_pl(player_sprite1,[pos[0]+1,pos[1],pos[2]])
      self.subject_list[0].set_position([pos[0]+1,pos[1],pos[2]])  
      
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
#*****************************************************

class Obs_Object(Obs_Item):

  def notify(self, caller, event):
    #print self.name, "received event", event
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
#========================================================================================  
#==================================================================================== """  

#*****************************************************
# CLASE SUBJECT
# Objeto generico
#*****************************************************

class Subject:
  
  # views: vistas asociadas al objeto
  # name: nombre del objeto
  # sprite: nombre del sprite asociado al objeto
  
  def __init__(self, name, id, sprite, size):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.id = id

  def register(self, observer):
    self.observers.append(observer)

  def unregister(self, observer):
    self.observers.remove(observer)

  def notify_observers(self, event):
    for observer in self.observers:
      observer.notify(self.id, event)
  
  def get_name(self):
    return self.name

  def get_sprite(self):
    return self.sprite
  
  def get_size(self):
    return self.size

#*****************************************************
# CLASE SUB_HUD (subclase de SUBJECT)
# Objeto de tipo HUD
#*****************************************************

class Sub_Hud(Subject):

  def metodo_provisional(self):
    self.name = self.name 

#*****************************************************
# CLASE SUB_ROOM (subclase de SUBJECT)
# Objeto de tipo habitacion
#*****************************************************

class Sub_Room(Subject):

  def metodo_provisional(self):
    self.name = self.name 
  
#*****************************************************
# CLASE SUB_FLOOR (subclase de SUBJECT)
# Objeto de suelo de habitacion
#*****************************************************

class Sub_Floor(Subject):

  def metodo_provisional(self):
    self.name = self.name 

#*****************************************************
# CLASE SUB_ITEM (subclase de SUBJECT)
# Objeto generico
#*****************************************************

class Sub_Item(Subject):
  
  # views: vistas asociadas al objeto
  # name: nombre del objeto
  # sprite: nombre del sprite asociado al objeto
  # position: posicion del item
  
  def __init__(self, name, id, sprite, size, position):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.id = id
  
  def get_position(self):
    #print self.position
    return self.position

  def set_position(self, position):
    #print self.position
    self.position = position
  
#*****************************************************
# CLASE SUB_PLAYER (subclase de SUB_ITEM)
# Jugador
#*****************************************************

class Sub_Player(Sub_Item):
  
  def metodo_provisional(self):
    self.name = self.name
  
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
    

#*****************************************************
# CLASE SUB_OBJECT (subclase de SUB_ITEM)
# Objeto no jugador
#*****************************************************

class Sub_Object(Sub_Item):
  
  # views: vistas asociadas al objeto
  # name: nombre del objeto
  # sprite: nombre del sprite asociado al objeto
  # position: posicion del item
  # move: indica si es posible mover el objeto
  # pick: indica si es posible recoger el objeto
  
  def __init__(self, name, id, sprite, size, position, move, pick):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.move = move
    self.pick = pick
    self.id = id
  
  def metodo_provisional(self):
    self.name = self.name

""" =====================================================================================
#========================================================================================  
#========================================================================================  
#==================================================================================== """  

def input(events):

  for event in events:
    
    if event.type == QUIT: 
       sys.exit(0)

    if event.type == KEYDOWN:
      
      if event.key == K_UP:
        sub_player1.move_one(1)
        #if char_pos[2] > 0:
        #  pj1.move_pl(0)

      if event.key == K_DOWN:
        sub_player1.move_one(2)
        #if char_pos[2] < (scene_sz[1]-1):
        #  pj1.move_pl(1)

      if event.key == K_LEFT:
        sub_player1.move_one(3)
        #if char_pos[0] > 0:
        #  pj1.move_pl(2)

      if event.key == K_RIGHT:
        sub_player1.move_one(4)
        #if char_pos[0] < (scene_sz[0]-1):
        #  pj1.move_pl(3)

"""
    if event.type == MOUSEBUTTONDOWN:
      x, y = pygame.mouse.get_pos()
      p3d = p2dtop3d([x,y])
      print (x,y)
      print p3d
      #f p3d[0] > char_pos[0]:
      #  move_char(3)

    #print event
  #pygame.display.flip()
"""  
  
""" =====================================================================================
#========================================================================================  
#========================================================================================  
#==================================================================================== """  
  
pygame.init()
screen = pygame.display.set_mode(screen_sz)

#subject = Subject("paquito", "black_mage.gif", [0,0])
sub_hud = Sub_Hud("hud", 0, " ", [0,0])
sub_floor = Sub_Floor("floor", 0, tile_stone, tile_sz)
sub_player1 = Sub_Player("player", 0, player_sprite1, char_sz,(2,0,2))
sub_player2 = Sub_Player("player", 1, player_sprite1, char_sz,(4,0,4))
#sub_object = Sub_Object("book", obj_book_sprite1, char_sz,[3,0,2],0,1)

#observerA = Observer("<observer A>", subject)
obs_hud = Obs_Hud("<observer HUD>")
obs_hud.add_subject(sub_hud)
obs_floor = Obs_Floor("<observer suelo>")
obs_floor.add_subject(sub_floor)
obs_player = Obs_Player("<observer jugador>")
obs_player.add_subject(sub_player1)
obs_player.add_subject(sub_player2)
#obs_object = Obs_Object("<observer objeto>",sub_object)

#subject.notify_observers ("<event 1>")
sub_hud.notify_observers ("<pinta HUD>")
sub_floor.notify_observers ("<pinta suelo>")
sub_player1.notify_observers ("<move_static>")
sub_player2.notify_observers ("<move_static>")
#sub_object.notify_observers ("<pinta objeto>")

pygame.display.set_caption('GenteGuada 0.01')

#time.sleep (2)
  
while True: 
   input(pygame.event.get()) 

   
