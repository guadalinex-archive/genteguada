import math
import os
import pygame
import ocempgui.widgets

#cache
if os.path.isdir("gg/GG/cache"):
  LOCAL_DATA_PATH = "gg/GG/cache"
else:
  LOCAL_DATA_PATH = "/usr/share/pixmaps/genteguada"
CLEAR_CACHE_WEEKS = 4

#resources
if os.path.isdir("gg/GG/data"):
  DATA_PATH = "gg/GG/data"
  SOUND_PATH = "gg/GG/data/sound"
  NINO_PATH = "nino/"
  NINA_PATH = "nina/"
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
#TICK_DELAY = 0.5
TICK_DELAY = 0.45
ANIM_DELAY = TICK_DELAY/10.0
ANIM_WALKING_COUNT = 10
ANIM_RELAX_COUNT = 40
ANIM_WALKING_TIME = int(TICK_DELAY*ANIM_WALKING_COUNT*100)
ANIM_RELAX_TIME = int(TICK_DELAY*ANIM_RELAX_COUNT*100)
ANIM_INVENTORY_TIME = 10000

HEADING = {0: "none", 1: "up", 2: "down", 3: "left", 4: "right",
           5: "topleft", 6: "bottomright", 7: "bottomleft", 8: "topright"}

STATE = {1: "standing", 2: "walking", 3: "standing_carrying", 4: "walking_carrying", 5: "standing_sleeping"}

# ======================= SPRITES ===========================

LOGIN_SCREEN = "login.png"
BG_BLACK = "bg_black.png"
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
BACKGROUND_LEFT = "background_left.png"
BACKGROUND_RIGHT = "background_right.png"
BACKGROUND_MIDDLE = "background_middle.png"
MALE_DUMMY = "male_dummy.png"
FEMALE_DUMMY = "female_dummy.png"
GENDER_TAG = "gender_tag.png"
SKIN_TAG = "skin_tag.png"
HEAD_TAG = "head_size_tag.png"
BODY_TAG = "body_size_tag.png"
MASK_TAG = "mask_tag.png"
HAIR_TAG = "hair_tag.png"
SHIRT_TAG = "shirt_tag.png"
SHORT_TAG = "shorts_tag.png"
SKIRT_TAG = "skirt_tag.png"
SHOES_TAG = "shoes_tag.png"
MALE_BTN = "male_button.png"
MALE_MASK = "male_mask.png"
MALE_SKIN = "male_skin.png"
MALE_SHIRT = "male_shirt.png"
MALE_SLEEVE = "male_sleeve.png"
MALE_TYPE_TROUSERS = "male_type_trousers.png"
MALE_TROUSERS = "male_trousers.png"
MALE_SHOES = "male_shoes.png"
MALE_HAIR_1 = "male_hair_1.png"
MALE_HAIR_2 = "male_hair_2.png"
MALE_HAIR_3 = "male_hair_3.png"
FEMALE_BTN = "female_button.png"
FEMALE_MASK = "female_mask.png"
FEMALE_SKIN = "female_skin.png"
FEMALE_SKIRT = "female_skirt.png"
FEMALE_SLEEVE = "female_sleeve.png"
FEMALE_SHOES = "female_shoes.png"
FEMALE_HAIR_1 = "female_hair_1.png"
FEMALE_HAIR_2 = "female_hair_2.png"
FEMALE_HAIR_3 = "female_hair_3.png"
COLOR_YELLOW = "yellow.png"
COLOR_ORANGE = "orange.png"
COLOR_RED = "red.png"
COLOR_PINK = "pink.png"
COLOR_BLUE = "blue.png"
COLOR_PURPLE = "purple.png"
COLOR_GREEN = "green.png"
COLOR_WHITE = "white.png"
COLOR_BLACK = "black.png"
COLOR_BLONDE = "blonde.png"
COLOR_BROWN = "brown.png"
SKIN_1 = "skin_1.png"
SKIN_2 = "skin_2.png"
SKIN_3 = "skin_3.png"
SKIN_4 = "skin_4.png"
SKIN_5 = "skin_5.png"
SKIN_6 = "skin_6.png"
SKIN_7 = "skin_7.png"
SKIN_8 = "skin_8.png"
SKIN_9 = "skin_9.png"
COLORS = {1:"COLOR_YELLOW", 2:"COLOR_ORANGE", 3:"COLOR_RED", 4:"COLOR_PINK", 5:"COLOR_BLUE", 6:"COLOR_PURPLE", 7:"COLOR_GREEN", 8:"COLOR_WHITE", 9:"COLOR_BLACK"}
HAIR_COLORS = {1:"COLOR_BLONDE", 2:"COLOR_BROWN", 3:"COLOR_BLACK"}
SKIN_COLORS = {1:"SKIN_1", 2:"SKIN_2", 3:"SKIN_3", 4:"SKIN_4", 5:"SKIN_5", 6:"SKIN_6", 7:"SKIN_7", 8:"SKIN_8", 9:"SKIN_9"}

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

BALLOON_FON_SZ = 16

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

def getSpriteName(state, heading, frame):
  #STATE = {1: "standing", 2: "walking", 3: "standing_carrying", 4: "walking_carrying", 5: "standing_sleeping"}
  maxFrames = 10
  if state == STATE[1] or state == STATE[3]:
    return str(state + "_" + heading + ".png")
  elif state == STATE[2] or state == STATE[4]:
    maxFrames = ANIM_WALKING_COUNT
  elif state == STATE[5]:
    maxFrames = ANIM_RELAX_COUNT  
    
  if frame == 0:
    fileName = state + "_" + heading + "_0" + str(maxFrames) + ".png"
  elif frame < 10:
    rgb= [0, 0, 0]
    fileName = state + "_" + heading + "_00" + str(frame) + ".png"
  else:  
    fileName = state + "_" + heading + "_0" + str(frame) + ".png"
  return fileName

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

def getRGBColor(color):
  rgb = [0,0,0]
  if color == "COLOR_YELLOW":
    rgb = [255, 255, 0]
  elif color == "COLOR_ORANGE":
    rgb = [255, 153, 0]
  elif color == "COLOR_RED":
    rgb = [255, 51, 0]
  elif color == "COLOR_PINK":
    rgb = [255, 0, 241]
  elif color == "COLOR_BLUE":
    rgb = [0, 0, 255]
  elif color == "COLOR_PURPLE":
    rgb = [153, 0, 204]
  elif color == "COLOR_GREEN":
    rgb = [0, 255, 102]
  elif color == "COLOR_WHITE":
    rgb = [255, 255, 255]
  elif color == "COLOR_BLACK":
    rgb = [0, 0, 0]
  elif color == "COLOR_BLONDE":
    rgb = [217, 224, 98]
  elif color == "COLOR_BROWN":
    rgb = [100, 79, 54]
  elif color == "SKIN_1":
    rgb = [254, 231, 215]
  elif color == "SKIN_2":
    rgb = [240, 205, 183]
  elif color == "SKIN_3":
    rgb = [255, 219, 183]
  elif color == "SKIN_4":
    rgb = [186, 147, 116]
  elif color == "SKIN_5":
    rgb = [192, 142, 107]
  elif color == "SKIN_6":
    rgb = [177, 115, 92]
  elif color == "SKIN_7":
    rgb = [139, 94, 61]
  elif color == "SKIN_8":
    rgb = [106, 66, 40]
  elif color == "SKIN_9":
    rgb = [67, 36, 18]
  return rgb
    
    
def createBalloon(self, string):
  """ Creates a balloon for a given string:
  string: string to be included on the balloon.
  """
  
  pygame.transform.resize(img, [(len(string)+2)*BALOON_FONT_SZ+40, BALOON_FONT_SZ+40])
  pass    
    
    
    
    
    
