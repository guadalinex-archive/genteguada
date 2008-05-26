import math
import os
import pygame
import ocempgui.widgets

if os.path.isdir("gg/GG/data"):
  DATA_PATH = "gg/GG/data"
  SOUND_PATH = "gg/GG/data/sound"
  NINO_PATH = "gg/GG/data/nino"
  NINA_PATH = "gg/GG/data/nina"
  STYLES_PATH = "gg/GG/styles"
else:
  DATA_PATH = "/usr/share/pixmaps/genteguada"
  SOUND_PATH = "/usr/share/pixmaps/genteguada/sound"
  NINO_PATH = "/usr/share/pixmaps/genteguada/nino"
  NINA_PATH = "/usr/share/pixmaps/genteguada/nina"
  STYLES_PATH = "/usr/share/pixmaps/genteguada/styles"

VERSION = "GenteGuada 0.0.3.1"
BG_FULL_OR = [0, 0]
TILE_SZ = [120, 60]
CHAR_SZ = [50, 50]
CHAR_POS = [0, 0, 0]
SCREEN_SZ = [1024, 768]
SCREEN_OR = [SCREEN_SZ[0]/2 -8, 5]
FLOOR_SHIFT = [55, -30]
SCENE_SZ = [8, 8]
GAMEZONE_SZ = [1024, 578]
HUD_SZ = [1024, SCREEN_SZ[1] - GAMEZONE_SZ[1]]
HUD_OR = [0, GAMEZONE_SZ[1]]

COLOR_SHIFT = 80

# Login
LOGIN_USERNAME_OR = [SCREEN_SZ[0]/2 + 10, SCREEN_SZ[1]/2 - 20]
LOGIN_USERNAME_SZ = [100, 20]
LOGIN_PASSWORD_OR = [SCREEN_SZ[0]/2 + 10, SCREEN_SZ[1]/2 + 20]
LOGIN_PASSWORD_SZ = [100, 20]
LOGIN_OKBUTTON_OR = [SCREEN_SZ[0]/2 - 60, SCREEN_SZ[1]/2 + 80]
LOGIN_CANCELBUTTON_OR = [SCREEN_SZ[0]/2 + 60, SCREEN_SZ[1]/2 + 80]

# Chat & iventory
CHAT_SZ = [753, 118]
CHAT_OR = [14, GAMEZONE_SZ[1]+14]
TEXT_BOX_SZ = [CHAT_SZ[0], 32]
TEXT_BOX_OR = [CHAT_OR[0], GAMEZONE_SZ[1]+CHAT_SZ[1]+27]
INV_OR = [CHAT_SZ[0]+ 53, GAMEZONE_SZ[1]+28]
INV_ITEM_SZ = [60, 60]
INV_ITEM_COUNT = [3, 2]
INV_SZ = [INV_ITEM_SZ[0]*INV_ITEM_COUNT[0] + 10, INV_ITEM_SZ[1]*INV_ITEM_COUNT[1] + 15]
IMAGE_CHAT_MESSAGE = "chatEntry.png"

#Avatar editor
TAG_POSITION = [288, 0]
TAG_OFFSET = 76

# Upper pannel
UPPERPANNEL_COUNT = 8
UPPERPANNEL_ITEM_SPACING = 8
UPPERPANNEL_ITEM_SZ = [65, 65]
UPPERPANNEL_SZ = [(UPPERPANNEL_ITEM_SZ[0] + UPPERPANNEL_ITEM_SPACING)*UPPERPANNEL_COUNT, UPPERPANNEL_ITEM_SZ[1] + UPPERPANNEL_ITEM_SPACING]
UPPERPANNEL_OR = [(SCREEN_SZ[0]/2) - (UPPERPANNEL_SZ[0]/2), 0]
ACTION_BUTTON_SZ = [80, 80]

# Animation values
TIME_BEFORE_RELAX = 5
TICK_DELAY = 0.5
ANIM_DELAY = TICK_DELAY/10.0
ANIM_WALKING_COUNT = 10
ANIM_RELAX_COUNT = 40
ANIM_WALKING_TIME = int(TICK_DELAY*ANIM_WALKING_COUNT*100)
ANIM_RELAX_TIME = int(TICK_DELAY*ANIM_RELAX_COUNT*100)

HEADING = {0: "none", 1: "up", 2: "down", 3: "left", 4: "right",
           5: "topleft", 6: "bottomright", 7: "bottomleft", 8: "topright"}

STATE = {1: "standing", 2: "walking", 3: "relax"}

# ======================= SPRITES ===========================

LOGIN_SCREEN = "login.png"
BG_BLACK = "black.png"
TILE_STONE = "baldosaIsometricTile.tga"
TILE_WATER = "aguaIsometricTile.tga"
INTERFACE_LOWER = "interface_lower.png"

# Sprites: items
OAK_SPRITE = "oak.png"
PENGUIN_SPRITE = "andatuz_01.png"
BOOK_SPRITE = "book.png"
BOOK_SPRITE_INV = "book.png"
KEY_SPRITE = "key.png"
DOOR_DOWN_SPRITE = "door_down.png"
MP3_SPRITE = "mp3.png"
TRASH_SPRITE = "trash.png"
PUZZLECUBE_SPRITE = "puzzle_cube.png"
BRICKCUBE_SPRITE = "brick_cube.png"

# Sprites: avatar design and buttons
DUMMY = "dummy.png"
GENDER_TAG = "genderTag.png"

# Avatar editor
BACKGROUNDLEFT = "backgroundleft.png"
BACKGROUNDRIGHT = "backgroundright.png"
BACKGROUNDMIDDLE = "backgroundmiddle.png"
MALE_DUMMY = "maleDummy.png"
FEMALE_DUMMY = "femaleDummy.png"
GENDER_TAG = "genderTag.png"
SKIN_TAG = "skinTag.png"
HEAD_TAG = "headSizeTag.png"
BODY_TAG = "bodySizeTag.png"
MASK_TAG = "maskTag.png"
HAIR_TAG = "hairTag.png"
SHIRT_TAG = "shirtTag.png"
SHORT_TAG = "shortsTag.png"
SKIRT_TAG = "skirtTag.png"
SHOES_TAG = "shoesTag.png"
MALE_BTN = "maleButton.png"
MALE_MASK = "mask.png"
MALE_SKIN = "skin.png"
MALE_SHIRT = "shirt.png"
MALE_SLEEVE = "sleeve.png"
MALE_TYPETROUSERS = "typetrousers.png"
MALE_TROUSERS = "trousers.png"
MALE_SHOES = "shoes.png"
FEMALE_BTN = "femaleButton.png"
TAGS = [GENDER_TAG, SKIN_TAG, HEAD_TAG, BODY_TAG, MASK_TAG, HAIR_TAG, SHIRT_TAG, SHORT_TAG, SKIRT_TAG, SHOES_TAG]

# ======================= SOUNDS ===========================

SOUND_OCEAN = "ocean.ogg"
SOUND_DROPITEM = "drop_item.ogg"
SOUND_KEYS = "keys.ogg"
SOUND_OPENDOOR = "open_door.ogg"
SOUND_STEPS01 = "steps01.ogg"
SOUND_STEPS02 = "steps02.ogg"

# ======================= COLORS ===========================

HUD_COLOR_BASE = [177, 174, 200]
HUD_COLOR_BORDER1 = [104, 102, 119]
HUD_COLOR_BORDER2 = [138, 136, 160]
HUD_COLOR_BORDER3 = [202, 199, 231]
CHAT_COLOR_BG = [61, 61, 91]
CHAT_COLOR_FONT = [216, 216, 216]
INV_COLOR_BG = [0, 0, 0]
TEXT_BOX_COLOR_BG = [255, 255, 255]
GUADALINEX_BLUE = [34, 133, 234]

#styles
#TODO investigar un poco el tema de las fuentes y de los colores que no lo tengo muy claro
STYLES = {
          "textFieldChat" : { "font" : { "name" : "Helvetica", "size" : 30, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 255) 
                                          }
                            },   
          "chatEntryBlack" : { "font" : { "name" : "Helvetica", "size" : 20, "alias" : True },
                               "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                           }
                            },
          "chatEntryRed" : { "font" : { "name" : "Helvetica", "size" : 20, "alias" : True },
                             "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (255, 0, 0),
                                           ocempgui.widgets.Constants.STATE_ENTERED      : (255, 0, 0),
                                           ocempgui.widgets.Constants.STATE_ACTIVE       : (255, 0, 0),
                                           ocempgui.widgets.Constants.STATE_INSENSITIVE  : (255, 0, 0) 
                                         }
                            },
          "chatEntryGreen" : { "font" : { "name" : "Helvetica", "size" : 20, "alias" : True },
                               "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 255, 0),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (0, 255, 0),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 255, 0),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 255, 0) 
                                          }
                            },
          "chatEntryBlue" : { "font" : { "name" : "Helvetica", "size" : 20, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 255) 
                                          }
                            },
         }

def getNextDirection(pos1, pos2):
  """ Obtiene la siguiente posicion en el trayecto entre 2 puntos.
  pos1: posicion de inicio.
  pos2: posicion de destino.
  """
  retVar = "down"
  if pos1[0] < pos2[0]:
    if pos1[2] < pos2[2]:
      retVar = "bottomright"
    elif pos1[2] > pos2[2]:
      retVar = "topright"
    else:
      retVar = "right"
  elif pos1[0] > pos2[0]:
    if pos1[2] < pos2[2]:
      retVar = "bottomleft"
    elif pos1[2] > pos2[2]:
      retVar = "topleft"
    else:
      retVar = "left"
  elif pos1[0] == pos2[0]:
    if pos1[2] < pos2[2]:
      retVar = "down" 
    elif pos1[2] > pos2[2]:
      retVar = "up"
  return retVar

def checkNeighbour(pos1, pos2):
  """ Checks if 2 points are neighbours or not.
  pos1: point 1.
  pos2: point 2.
  """
  if [pos1[0], pos1[1], pos1[2]] == [pos2[0], pos2[1], pos2[2] - 1]:
    return True
  elif [pos1[0], pos1[1], pos1[2]] == [pos2[0], pos2[1], pos2[2] + 1]:
    return True
  elif [pos1[0], pos1[1], pos1[2]] == [pos2[0] - 1, pos2[1], pos2[2]]:
    return True
  elif [pos1[0], pos1[1], pos1[2]] == [pos2[0] + 1, pos2[1], pos2[2]]:
    return True
  elif [pos1[0], pos1[1], pos1[2]] == [pos2[0] - 1, pos2[1], pos2[2] - 1]:
    return True
  elif [pos1[0], pos1[1], pos1[2]] == [pos2[0] + 1, pos2[1], pos2[2] + 1]:
    return True
  elif [pos1[0], pos1[1], pos1[2]] == [pos2[0] - 1, pos2[1], pos2[2] + 1]:
    return True
  elif [pos1[0], pos1[1], pos1[2]] == [pos2[0] + 1, pos2[1], pos2[2] - 1]:
    return True
  return False  

def getFrontPosition(pos, heading):
  """ Returns the tile coords in front of the player.
  pos: player's position.
  heading: direction that the player is heading to.
  """
  retVar = [-1, -1, -1]
  if heading == "up" and not pos[2] == 0:
    retVar = [pos[0], pos[1], pos[2] - 1]
  elif heading == "down" and not pos[2] == (SCENE_SZ[1] - 1):
    retVar = [pos[0], pos[1], pos[2] + 1]
  elif heading == "left" and not pos[0] == 0:
    retVar = [pos[0] - 1, pos[1], pos[2]]
  elif heading == "right" and not pos[0] == (SCENE_SZ[0] - 1):
    retVar = [pos[0] + 1, pos[1], pos[2]]
  elif heading == "topleft" and not pos[0] == 0 and not pos[2] == 0:
    retVar = [pos[0] - 1, pos[1], pos[2] - 1]
  elif heading == "bottomright" and not pos[0] == (SCENE_SZ[0] - 1) and not pos[2] == (SCENE_SZ[1] - 1):
    retVar = [pos[0] + 1, pos[1], pos[2] + 1]
  elif heading == "bottomleft" and not pos[0] == 0 and not pos[2] == (SCENE_SZ[1] - 1):
    retVar = [pos[0] - 1, pos[1], pos[2] + 1]
  elif heading == "topright" and not pos[2] == 0 and not pos[0] == (SCENE_SZ[0] - 1):
    retVar = [pos[0] + 1, pos[1], pos[2] - 1]
  return retVar
    
def p2pDistance(point1, point2):
  """ Calculates the distance between 2 points.
  point1: starting point.
  point2: ending point.
  """
  if point1 == point2: 
    return 0
  return '%.3f' % math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[2] - point1[2]), 2))
    
def p3dToP2d(cord3d, offset):
  """ Returns the physical 2d coordinates of a 3d virtual point.
  cord3d: 3d virtual point.
  offset: point's offset on screen.
  """
  x2d = SCREEN_OR[0]
  y2d = SCREEN_OR[1]
  x2d = x2d + (cord3d[0]*(TILE_SZ[0]/2)) - (cord3d[2]*(TILE_SZ[1])) 
  y2d = y2d + (cord3d[0]*(TILE_SZ[0]/4)) + (cord3d[2]*(TILE_SZ[1]/2)) 
  x2d = x2d - (offset[0])
  y2d = y2d - (offset[1])
    
  cord2d = [x2d, y2d]
  return cord2d
    
def playSound(sound):
  sndPath = os.path.join(SOUND_PATH, sound)
  if not os.path.isfile(sndPath):
    return False
  pygame.mixer.music.load(sndPath)
  pygame.mixer.music.play()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
