import math
import os
import sys
import time
import pygame
from pygame.locals import *

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
  
  def __init__(self, name, subject):
    self.name = name
    subject.register(self)

  def notify(self, event):
    print self.name, "received event", event
  
  def p3dtop2d(self, cord3d):
    
    # cord3d: punto 3d en el mundo
    
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
    
    cord2d=[math.floor((x2d/math.sqrt(3))+screen_or[0]),math.floor(y2d+screen_or[1])]
    
    return cord2d

#*****************************************************
# CLASE OBS_HUD (subclase de OBSERVER)
# Observador de HUD
#*****************************************************

class Obs_Hud(Observer):
  
  def notify(self, event):
    print self.name, "received event", event
    #self.paint_hud()

  def paint_hud(self):
    screen = pygame.display.get_surface()
    pygame.draw.rect(screen,hud_color_border1,(hud_or[0],hud_or[1],hud_sz[0]-1,hud_sz[1]-1))
    pygame.draw.rect(screen,hud_color_border2,(hud_or[0]+2,hud_or[1]+2,hud_sz[0]-5,hud_sz[1]-5))
    pygame.draw.rect(screen,hud_color_border3,(hud_or[0]+10,hud_or[1]+10,hud_sz[0]-21,hud_sz[1]-21))
    pygame.draw.rect(screen,hud_color_base,(hud_or[0]+12,hud_or[1]+12,hud_sz[0]-25,hud_sz[1]-25))

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

  def notify(self, event):
    print self.name, "received event", event
    self.paint_floor(tile_stone)

  def paint_floor(self, tile_name):
    screen = pygame.display.get_surface()
    tile = os.path.join("data",tile_name)
    tile_surface = pygame.image.load(tile)
    for x in range(scene_sz[0]):
      for z in range(scene_sz[1]):
        screen.blit(tile_surface, p3dtop2d([x,0,z],tile_sz,0))
        screen.blit(tile_surface, self.p3dtop2d([x,0,z]))

  def get_type(self):
    return 0
  
#****************************************************************************************
#****************************************************************************************
#****************************************************************************************

#*****************************************************
# CLASE SUBJECT
# Objeto generico
#*****************************************************

class Subject:
  
  # views: vistas asociadas al objeto
  # name: nombre del objeto
  # sprite: nombre del sprite asociado al objeto
  
  def __init__(self, name, sprite, size):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size

  def register(self, observer):
    self.observers.append(observer)

  def unregister(self, observer):
    self.observers.remove(observer)

  def notify_observers(self, event):
    for observer in self.observers:
      observer.notify(event)
  
  def get_name(self):
    return self.name

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

  def get_tile(self):
    return self.sprite

  def metodo_provisional(self):
    self.name = self.name 
  
#*****************************************************

subject = Subject("paquito", "black_mage.gif", [50,50])
sub_hud = Sub_Hud("hud", "black_mage.gif", [50,50])
sub_floor = Sub_Floor("floor", tile_stone, tile_sz)

observerA = Observer("<observer A>", subject)
obs_hud = Obs_Hud("<observer HUD>", sub_hud)
obs_floor = Obs_Floor("<suelo>", sub_floor)

subject.notify_observers ("<event 1>")
sub_hud.notify_observers ("<event HUD>")
sub_floor.notify_observers ("<pintasuelo>")

pygame.init()
window = pygame.display.set_mode((screen_sz[0], screen_sz[1]))
pygame.display.set_caption('GenteGuada 0.01')

#obs_floor.paint_floor(tile_stone)
time.sleep (2)

#*****************************************************
