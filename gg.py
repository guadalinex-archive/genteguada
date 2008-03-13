import math
import os
import sys
import time
import signal
import pygame
from pygame.locals import *

tile_sz = [100, 50]
tile2tile = 55.901699437
#tile2tile = math.sqrt(pow(tile_sz[0],2)+pow(tile_sz[1],2))
#55.901699437
char_sz = [50, 50]
char_pos = [0, 0, 0]
screen_sz = [800, 600]
screen_or = [screen_sz[0]/2, 20]
scene_sz = [7, 7]
gamezone_sz = [800, 400]
hud_sz = [800, 200]
hud_or = [0, gamezone_sz[1]]

animations = 5
max_frames = 5
anim_delay = 0.2
speed = 55.901699437

tile_stone = "tile_stone.png"
player_sprite1 = "black_mage.gif"
player_sprite2 = "black_mage_red.gif"
obj_book_sprite1 = "book.png"
sin30r = math.sin(math.radians(30))
cos30r = math.cos(math.radians(30))

hud_color_base = [177, 174, 200]
hud_color_border1 = [104, 102, 119]
hud_color_border2 = [138, 136, 160]
hud_color_border3 = [202, 199, 231]

#***************************************************** 
# CLASE OBSERVADOR
# Observador generico

class Observer:
  
    def __init__(self, name):
        self.name = name
        self.subject_list = []

    def add_subject(self, subject):
        self.subject_list.append(subject)
        subject.register(self)

    def notify(self, caller):
        pass
  
    def p3dtop2d(self, cord3d):
        x2d = (cord3d[0] - cord3d[2]) * cos30r * tile_sz[0]
        y2d = ((cord3d[0] + cord3d[2]) * sin30r) - cord3d[1]
        y2d = (y2d * tile_sz[1])
    
        # 0: suelo 
        if self.get_type() == 0:
            x2d = x2d - (tile_sz[0])
        # 1: personaje
        if self.get_type() == 1:
            x2d = x2d - (char_sz[0])
            y2d = y2d - (char_sz[1] / 4)
        # 2: objeto -------------------------->> MODIFICAR
        if self.get_type() == 2:
            x2d = x2d - 55
            y2d = y2d + 8
    
        cord2d = [math.floor((x2d/math.sqrt(3)) + screen_or[0]), math.floor(y2d + screen_or[1])]
        return cord2d
  
#*****************************************************
# CLASE OBS_HUD (subclase de OBSERVER)
# Observador de HUD

class Obs_Hud(Observer):
  
    def paint(self):
        self.paint_hud()

    def paint_hud(self):
        pygame.draw.rect(screen, hud_color_border1, (hud_or[0], hud_or[1], hud_sz[0] - 1, hud_sz[1] - 1))
        pygame.draw.rect(screen, hud_color_border2, (hud_or[0] + 2,hud_or[1] + 2, hud_sz[0] - 5, hud_sz[1] - 5))
        pygame.draw.rect(screen, hud_color_border3, (hud_or[0] + 10, hud_or[1] + 10, hud_sz[0] - 21, hud_sz[1] - 21))
        pygame.draw.rect(screen, hud_color_base, (hud_or[0] + 12, hud_or[1] + 12, hud_sz[0] - 25, hud_sz[1] - 25))
        pygame.display.update()

#*****************************************************
# CLASE OBS_ROOM (subclase de OBSERVER)
# Observador de una habitacion

class Obs_Room(Observer):

    def __init__(self, name):
        self.name = name
        self.subject_list = []
        self.tile_list = []
        for x in range(scene_sz[0]):
          for z in range(scene_sz[1]):
              var_pos = self.p3dtop2d([x, 0, z])
              pos = [int(var_pos[0]),int(var_pos[1])]
              self.tile_list.append([])
              self.tile_list[x].append(Obs_tile([pos[0] - screen_or[0], pos[1]-screen_or[1]], [pos[0] + screen_or[0], pos[1] + screen_or[1]], tile_stone, tile_sz))
        
    def insert_player(self,player):
        self.obs_player = player
      
    def draw(self):
        self.paint_floor(self.subject_list[0].get_sprite())
        self.obs_player.draw()
    
    def paint_floor(self, tile_name):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, gamezone_sz[0], gamezone_sz[1]))
        tile = os.path.join("data", tile_name)
        tile_surface = pygame.image.load(tile)
        for x in range(scene_sz[0]):
            for z in range(scene_sz[1]):
                screen.blit(tile_surface, self.p3dtop2d([x, 0, z]))

    def find_tile(self,pos):
        #x, y = pygame.mouse.get_pos()
        for x in range(scene_sz[0]):
            for z in range(scene_sz[1]):
                #self.tile_list[x].[z].
                pass
    
        # devuelve la posicion [x,z] en la que ha pinchado el usuario
        pass

    def get_type(self):
        return 0

#*****************************************************
# CLASE OBS_TILE (subclase de OBSERVER)
# Observador de una baldosa

class Obs_tile(Observer):

    def __init__(self, top_left, bot_right, sprite, size):
        self.top_left = top_left
        self.bot_right = bot_right
        self.id = id
        self.sprite = sprite
        self.size = size
        self.observers = []
  
    def contained(self, pos):
        if self.bot_right[0] > pos[0] > self.top_left[0]:
            if self.bot_right[1] > pos[1] > self.top_left[1]:
                return true
        return false

    def on_blank(self, pos):
        ini_pos = [pos[0]-self.top_left[0], pos[1]-self.top_left[1]]
        if ini_pos[0] < (tile_sz[0] / 2):
            if ini_pos[1] < (tile_sz[1] / 2):
                if ini_pos[0] <= (ini_pos[0] * 2): #cuadrante 1
                    return true
            else:
                ini_pos[1] -= (tile_sz[1] / 2)
                ini_pos[1] = (tile_size[1] / 2) - ini_pos[1]
                if ini_pos[0] <= (ini_pos[0] * 2): #cuadrante 2
                    return true
        else:
            if ini_pos[1] < (tile_sz[1] / 2):
                ini_pos[0] -= (tile_sz[0] / 2)
                ini_pos[0] = (tile_size[0] / 2) - ini_pos[0]
                if ini_pos[0] <= (ini_pos[0] * 2): #cuadrante 3
                    return true
            else:
                ini_pos[0] -= (tile_sz[0] / 2)
                ini_pos[1] -= (tile_sz[1] / 2)
                ini_pos[0] = (tile_size[0] / 2) - ini_pos[0]
                ini_pos[1] = (tile_size[1] / 2) - ini_pos[1]
                if ini_pos[0] <= (ini_pos[0] * 2): #cuadrante 4
                    return true
        return false    
    
#*****************************************************
# CLASE OBS_ITEM (subclase de OBSERVER)
# Observador de un item generico

class Obs_Item(Observer):
    pass

#*****************************************************
# CLASE OBS_PLAYER (subclase de OBS_ITEM)
# Observador de un jugador

class Obs_Player(Obs_Item):

    def draw(self):
        for ind in range(self.subject_list.__len__()):
            self.draw_one(ind)

    def draw_one(self, caller):
        pos = self.subject_list[caller].get_position()
        var_pos = [pos[0], pos[1], pos[2]]
        event = self.subject_list[caller].get_state()
        sprite = self.subject_list[caller].get_sprite()
        if event == "standing_down":
            self.paint_pl(sprite, pos, caller)
        if event == "walking_up":
            self.paint_pl(sprite, pos, caller)
        if event == "walking_down":
            self.paint_pl(sprite, pos, caller)
        if event == "walking_left":
            self.paint_pl(sprite, pos, caller)
        if event == "walking_right":
            self.paint_pl(sprite, pos, caller)
      
    def paint_pl(self, sprite, cord3d, caller):
        pl = os.path.join("data", sprite)
        pl_surface = pygame.image.load(pl)
        state = self.subject_list[caller].get_state_frame()
        dir = self.subject_list[caller].get_dir()
        screen.blit(pl_surface, self.p3dtop2d(cord3d, state, dir))
        pygame.display.update()

    def p3dtop2d(self, cord3d, state, dir):
        x2d = (cord3d[0] - cord3d[2]) * cos30r * tile_sz[0]
        y2d = ((cord3d[0] + cord3d[2])*sin30r) - cord3d[1]
        y2d = (y2d * tile_sz[1])
    
        x2d = x2d - (char_sz[0])
        y2d = y2d - (char_sz[1] / 4)
    
        x2d = math.floor((x2d / math.sqrt(3)) + screen_or[0])
        y2d = math.floor(y2d + screen_or[1])
   
        if dir == 1: #arriba
            x2d = x2d + (((tile_sz[0] / 2)*state) / 5)
            y2d = y2d - (((tile_sz[1] / 2)*state) / 5)
        if dir == 2: #abajo
            x2d = x2d - (((tile_sz[0] / 2)*state) / 5)
            y2d = y2d + (((tile_sz[1] / 2)*state) / 5)
        if dir == 3: #izquierda
            x2d = x2d - (((tile_sz[0] / 2)*state) / 5)  
            y2d = y2d - (((tile_sz[1] / 2)*state) / 5)
        if dir == 4: #derecha
            x2d = x2d + (((tile_sz[0] / 2)*state) / 5)
            y2d = y2d + (((tile_sz[1] / 2)*state) / 5)
      
        cord2d = [x2d, y2d]
        return cord2d

    def get_type(self):
        return 1

#*****************************************************
# CLASE OBS_OBJECT (subclase de OBS_ITEM)
# Observador de un objeto

class Obs_Object(Obs_Item):

    def notify(self, caller, event):
        self.paint_obj(obj_book_sprite1, [3, 0, 2])

    def paint_obj(self, sprite, cord3d):
        pl = os.path.join("data", sprite)
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
    
    def insert_floor(self, floor):
        self.floor = floor

    def insert_player(self, player):
        self.players.append(player)
    
    def insert_object(self, object):
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
        self.state = "standing_down"
        self.state_frame = 0
    
    def move_one(self, dir):
        if self.state_frame <> 0:
            pass
        else:
            if dir <> 0:
                self.state_frame = 0
            if dir == 1 and self.position[2] > 0:
                self.state = "walking_up"  
            if dir == 2 and self.position[2] < (scene_sz[1] - 1):
                self.state = "walking_down"  
            if dir == 3 and self.position[0] > 0:
                self.state = "walking_left"  
            if dir == 4 and self.position[0] < (scene_sz[0] - 1):
                self.state = "walking_right"
  
    def get_state(self):
        return self.state

    def get_state_frame(self):
        return self.state_frame

    def get_dir(self):
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
            if self.state_frame == (max_frames - 1):
                pos = self.get_position()
                if self.state == "walking_up":
                    self.set_position([pos[0], pos[1], pos[2] - 1])
                if self.state == "walking_down":
                    self.set_position([pos[0], pos[1], pos[2] + 1])
                if self.state == "walking_left":
                    self.set_position([pos[0] - 1, pos[1], pos[2]])  
                if self.state == "walking_right":
                    self.set_position([pos[0] + 1, pos[1], pos[2]])  
                self.state = "standing_down"
                self.state_frame = 0
            else:
                self.state_frame += 1
        
    def notify(self):
        self.notify_observers(self.state)
        
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
            if event.key == MOUSEBUTTONDOWN:
                #sub_player1.
                pass
            if event.key == K_ESCAPE:
                sys.exit(0)
          
""" =====================================================================================
#========================================================================================  
#==================================================================================== """  
  
pygame.init()
screen = pygame.display.set_mode(screen_sz)
pygame.display.set_caption('GenteGuada 0.01')

sub_hud = Sub_Hud("hud", 0, " ", [0,0])
sub_room = Sub_Room("room1", 0, tile_stone)
sub_player1 = Sub_Player("player", 0, player_sprite1, char_sz, (2, 0, 2))
sub_player2 = Sub_Player("player", 0, player_sprite2, char_sz, (4, 0, 4))
sub_room.insert_player(sub_player1)
sub_room.insert_player(sub_player2)
#sub_object = Sub_Object("book", obj_book_sprite1, char_sz,[3,0,2])

obs_hud = Obs_Hud("<observer HUD>")
obs_hud.add_subject(sub_hud)
obs_room = Obs_Room("<observer Room>")
obs_room.add_subject(sub_room)
obs_player = Obs_Player("<observer jugador>")
obs_player.add_subject(sub_player1)
obs_player.add_subject(sub_player2)
obs_room.insert_player(obs_player)
#obs_object = Obs_Object("<observer objeto>",sub_object)

#sub_hud.notify_observers ("<pinta HUD>")
#sub_room.notify_observers ("<pinta suelo>")
#sub_player1.notify_observers ("standing_down")
#sub_player2.notify_observers ("standing_down")

time_passed = 0
clock = pygame.time.Clock()

while True:
  clock = pygame.time.Clock()
  time_passed = time_passed + clock.tick(30)
  time_passed_seconds = time_passed / 1000.0
  if time_passed_seconds >= 0.02:
    time_passed = 0
    sub_room.tick()
    obs_room.draw()
    obs_hud.paint_hud()
  input(pygame.event.get()) 
    
  