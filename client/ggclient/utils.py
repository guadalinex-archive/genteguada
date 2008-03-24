import math
import os

if os.path.isdir("data"):
  DATA_PATH = "data"
else:
  DATA_PATH = "/usr/share/pixmaps/genteguada-client"

TILE_SZ = [100, 50]
#TILE2TILE = 55.901699437
#tile2tile = math.sqrt(pow(TILE_SZ[0],2)+pow(TILE_SZ[1],2))
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

def getNextDirection(pos1, pos2):
  """ Obtiene la siguiente posicion en el trayecto entre 2 puntos.
  pos1: posicion de inicio.
  pos2: posicion de destino.
  """
  if pos1[0] < pos2[0]:
    if pos1[2] < pos2[2]:
      return "walking_bottomright"
    elif pos1[2] > pos2[2]:
      return "walking_topright"
    else:
      return "walking_right"
  elif pos1[0] > pos2[0]:
    if pos1[2] < pos2[2]:
      return "walking_bottomleft"
    elif pos1[2] > pos2[2]:
      return "walking_topleft"
    else:
      return "walking_left"
  elif pos1[0] == pos2[0]:
    if pos1[2] < pos2[2]:
      return "walking_down" 
    elif pos1[2] > pos2[2]:
      return "walking_up"
  return "standing_down"
