# -*- coding: iso-8859-15 -*-

import math
import os

# ======================= GENERAL PATHS ===========================

#cache
if os.path.isdir("gg/GG/cache"):
  LOCAL_DATA_PATH = "gg/GG/cache"
else:
  LOCAL_DATA_PATH = "/usr/share/pixmaps/genteguada/cache"

CLEAR_CACHE_WEEKS = 4

#resources
if os.path.isdir("gg/GG/data"):
  DATA_PATH = "gg/GG/data"
else:
  DATA_PATH = "/usr/share/pixmaps/genteguada/data"

HUD_PATH = "interface/hud/"
SOUND_PATH = "sound"
NINO_PATH = "avatars/default_boy/"
NINA_PATH = "avatars/default_girl/"
QUESTIONS_PATH = DATA_PATH+"/questions"

# ======================= CONSTANTS ===========================

# Screen & General values
VERSION = "GenteGuada 0.2.0-1"
BG_FULL_OR = [0, 0]
TILE_SZ = [120, 60]
CHAR_SZ = [50, 50]
CHAR_POS = [0, 0, 0]
SCREEN_SZ = [1024, 768]
SCREEN_OR = [SCREEN_SZ[0]/2 -8, 5]
FLOOR_SHIFT = [55, -30]
TILE_TARGET_SHIFT = [18, 18]
SELECTED_FLOOR_SHIFT = [55, -25]
SCENE_SZ = [8, 8]
GAMEZONE_SZ = [SCREEN_SZ[0], 578]
HUD_SZ = [SCREEN_SZ[0], SCREEN_SZ[1] - GAMEZONE_SZ[1]]
HUD_OR = [0, GAMEZONE_SZ[1]]
COLOR_SHIFT = 80
TEXT_LINE_LENGTH = 40
MAX_DEPTH = 1

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
BALLOON_OPACITY = 210

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
TICK_DELAY = 0.45
ANIM_DELAY = TICK_DELAY/10.0
ANIM_WALKING_COUNT = 10
ANIM_RELAX_COUNT = 40
ANIM_WALKING_TIME = int(TICK_DELAY*ANIM_WALKING_COUNT*100)
ANIM_RELAX_TIME = int(TICK_DELAY*ANIM_RELAX_COUNT*100)
ANIM_INVENTORY_TIME = 1000
ANIM_CHAT_TIME1 = 2000
ANIM_CHAT_TIME2 = 1000
JUMP_TIME = 800
JUMP_ANIMATION_TIME = 100
JUMP_DISTANCE = 70
JUMP_OVER_DISTANCE = JUMP_DISTANCE + 50


POINTS_LOCATION = [800, 30]
EXP_LOCATION = [800, 50]

TEXT_COLOR = {"black": 0, "blue": 1}

# Directions for a player's heading.
HEADING = {0: "none", 1: "up", 2: "down", 3: "left", 4: "right",
           5: "topleft", 6: "bottomright", 7: "bottomleft", 8: "topright"}

# Player states.
STATE = {1: "standing", 2: "walking", 3: "standing_carrying", 4: "walking_carrying", 5: "standing_sleeping"}

# Message types --> 0: general; 1: private; 2: npcs; 3: system)
CHAT_TYPE = {0: "White", 1: "Red", 2: "Green", 3: "Blue"}

# ======================= SPRITES ===========================

LOGIN_SCREEN = "login.png"
BG_BLACK = "bg_black.png"
TILE_STONE = "baldosaIsometricTile.tga"
TILE_WATER = "aguaIsometricTile.tga"
INTERFACE_LOWER = "interface_lower.png"
IMAGE_CHAT_MESSAGE = "chatEntry.png"

# Sprites: items
PENGUIN_SPRITE_RIGHT = "andatuz_right.png"
PENGUIN_SPRITE_DOWN = "andatuz_down.png"
PENGUIN_SPRITE_BOTTOMRIGHT = "andatuz_bottomright.png"
ADVERTISEMENT_LEFT = "advertisementLeft.png"
ADVERTISEMENT_MIDDLE = "advertisementMiddle.png"
ADVERTISEMENT_RIGHT = "advertisementRight.png"
BOOK_SPRITE = "book.png"
BOOK_SPRITE_INV = "book.png"
KEY_SPRITE = "golden_key.png"
BLUE_KEY = "blue_key.png"

KEY_GOLDEN = "golden_key.png"
GIFT = "gift.png"
BOX_HEAVY = "heavy_box.png"
KILOGRAMME = "kilogramme.png"
KILOGRAMME_INV = "kilogramme_inv.png"
BEAM_WOODEN = "wooden_beam.png"
PAPERMONEY_5 = "5Guadapuntos.png"
PAPERMONEY_10 = "10Guadapuntos.png"
PAPERMONEY_50 = "50Guadapuntos.png"

TREE = "tree.png"
COLUMN_STONE = "stone_column.png"
BEAM_WOODEN = "wooden_beam.png"
FENCE_UP = "fence_up.png"
FENCE_LEFT = "fence_left.png"
WALL_UP = "wall_up.png"
WALL_LEFT = "wall_left.png"
WALL_UP_GRAFFITI = "wall_up_graffiti.png"
YARD_LAMP_UP = "yard_lamp_up.png"
YARD_LAMP_LEFT = "yard_lamp_left.png"
YARD_UP = "yard_up.png"
YARD_LEFT = "yard_left.png"
YARD_CORNER = "yard_corner.png"

HEDGE = "hedge.png"
DOOR_GARDEN = "garden_door.png"
DOOR_WOODEN = "wooden_door.png"
DOOR_WOODEN_A = "wooden_door_a.png"
DOOR_WOODEN_B = "wooden_door_b.png"
DOOR_AMORED = "armored_door_left.png"

WAREHOUSE_UP = ["warehouseWallUp01.png", "warehouseWallUp02.png"]
WAREHOUSE_LEFT = ["warehouseWallLeft01.png", "warehouseWallLeft02.png"]
WAREHOUSE_CORNER = "warehouseWallCorner.png"

SKYLINES_UP = ["skylineWallUp01.png", "skylineWallUp02.png", "skylineWallUp03.png", "skylineWallUp04.png"]
SKYLINES_LEFT = ["skylineWallLeft01.png", "skylineWallLeft02.png"]
SKYLINE_CORNER = "skylineCorner.png"

TILE_TARGET = "target.png"
TILE_SELECTED = "selected.png"
TILE_MYSTCYRCLE = "mystCircle.png"
TILE_MYSTCYRCLE_CASTLE01 = "mystCircleCastle01.png"
TILES_GRASS = ["grass01.png", "grass02.png", "grass03.png", "grass04.png"]
TILES_PAVINGSTONE = ["pavingStone01.png", "pavingStone02.png", "pavingStone03.png"]
TILES_PAVINGSTONEWITHGRASS = ["pavingStoneWithGrass01.png", "pavingStoneWithGrass02.png", "pavingStoneWithGrass03.png"]
TILES_SMALLSTONES = ["smallStones01.png", "smallStones02.png", "smallStones03.png"]
TILES_ARROWS = ["upArrow.png", "downArrow.png", "leftArrow.png", "rightArrow.png"]
TILES_CASTLE1 = ["castle01.png"]
TILES_CASTLE2 = ["castle02.png"]

#Backgrounds
PATH_EDITOR_BACKGROUNDS = "interface/backgrounds"

# Sprites: avatar design and buttons
DUMMY = "dummy.png"
GENDER_TAG = "genderTag.png"

# Avatar editor
PATH_EDITOR_IMG = "editor"
PATH_EDITOR_INTERFACE = "interface/editor"
IMG_EXTENSION = ".png"
PATH_PHOTO_MASK = LOCAL_DATA_PATH + "/mask" 
MASK_SIZE = {"S":[112, 105], "M":[124, 116], "L":[134, 127], "XL":[146, 137]}
MASK_COORD = {"S":(91, 114), "M":(86, 111), "L":(80, 105), "XL":(74, 100)}

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
MALE_HEAD = "/boy/head"
MALE_MASK = "/boy/"
MALE_SKIN = "/boy/skin/"
MALE_SHORT_SHIRT = "/boy/short_shirt/"
MALE_LONG_SHIRT = "/boy/long_shirt/"
MALE_LONG_TROUSERS = "/boy/long_trousers/"
MALE_SHORT_TROUSERS = "/boy/short_trousers/"
MALE_SHOES = "/boy/shoes/"
MALE_HAIR_1 = "/boy/hair1"
MALE_HAIR_2 = "/boy/hair2"
MALE_HAIR_3 = "/boy/hair3"

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

# Chat balloon pieces.
CORNER_TOPLEFT = {0: "corner_topleft_white.png", 1: "corner_topleft_red.png", 2: "corner_topleft_green.png", 3: "corner_topleft_blue.png"}
CORNER_TOPRIGHT = {0: "corner_topright_white.png", 1: "corner_topright_red.png", 2: "corner_topright_green.png", 3: "corner_topright_blue.png"}
CORNER_BOTTOMLEFT = {0: "corner_bottomleft_white.png", 1: "corner_bottomleft_red.png", 2: "corner_bottomleft_green.png", 3: "corner_bottomleft_blue.png"}
CORNER_BOTTOMRIGHT = {0: "corner_bottomright_white.png", 1: "corner_bottomright_red.png", 2: "corner_bottomright_green.png", 3: "corner_bottomright_blue.png"}
BORDER_TOP = {0: "border_top_white.png", 1: "border_top_red.png", 2: "border_top_green.png", 3: "border_top_blue.png"}
BORDER_LEFT = {0: "border_left_white.png", 1: "border_left_red.png", 2: "border_left_green.png", 3: "border_left_blue.png"}
BORDER_RIGHT = {0: "border_right_white.png", 1: "border_right_red.png", 2: "border_right_green.png", 3: "border_right_blue.png"}
BORDER_BOTTOM = {0: "border_bottom_white.png", 1: "border_bottom_red.png", 2: "border_bottom_green.png", 3: "border_bottom_blue.png"}
TAIL = {0: "tail_white.png", 1: "tail_red.png", 2: "tail_green.png", 3: "tail_blue.png"}

# ======================= SOUNDS ===========================

SOUND_OCEAN = "ocean.ogg"
SOUND_DROPITEM = "drop_item.ogg"
SOUND_KEYS = "keys.ogg"
SOUND_OPENDOOR = "open_door.ogg"
SOUND_STEPS01 = "steps01.ogg"
SOUND_STEPS02 = "steps02.ogg"



# ===============================================================
# =========================== METHODS ===========================
# ===============================================================

def getJumpDestination(pos, heading, size):
  length = 2
  if heading == HEADING[1]: #up
    dest = [pos[0], pos[1] - length]
  elif heading == HEADING[2]: #down
    dest = [pos[0], pos[1] + length]
  elif heading == HEADING[3]: #left
    dest = [pos[0] - length, pos[1]]
  elif heading == HEADING[4]: #right
    dest = [pos[0] + length, pos[1]]
  elif heading == HEADING[5]: #topleft
    dest = [pos[0] - length, pos[1] - length]
  elif heading == HEADING[6]: #bottomright
    dest = [pos[0] + length, pos[1] + length]
  elif heading == HEADING[7]: #bottomleft
    dest = [pos[0] - length, pos[1] + length]
  elif heading == HEADING[8]: #topright
    dest = [pos[0] + length, pos[1] - length]
  else:
    return None    
  if 0 < dest[0] < size[0]:    
    if 0 < dest[1] < size[1]:
      return dest
  return None    

# ===============================================================

def getSpriteName(state, heading, frame, timestamp):
  timestamp = str(timestamp)
  if timestamp == "":
    tail = ""
  else:
    tail = "_" + timestamp

  maxFrames = 10
  if state == STATE[1] or state == STATE[3]:
    return str(state + "_" + heading + "_0001" + tail)
  elif state == STATE[2] or state == STATE[4]:
    maxFrames = ANIM_WALKING_COUNT
  elif state == STATE[5]:
    maxFrames = ANIM_RELAX_COUNT  
    
  if frame == 0:
    fileName = state + "_" + heading + "_00" + str(maxFrames)
  elif frame < 10:
    fileName = state + "_" + heading + "_000" + str(frame)
  else:  
    fileName = state + "_" + heading + "_00" + str(frame)
  return fileName + tail

# ===============================================================

def getNextDirection(pos1, pos2):
  """ Obtiene la siguiente posicion en el trayecto entre 2 puntos.
  pos1: posicion de inicio.
  pos2: posicion de destino.
  """
  retVar = "down"
  if pos1[0] < pos2[0]:
    if pos1[1] < pos2[1]:
      retVar = "bottomright"
    elif pos1[1] > pos2[1]:
      retVar = "topright"
    else:
      retVar = "right"
  elif pos1[0] > pos2[0]:
    if pos1[1] < pos2[1]:
      retVar = "bottomleft"
    elif pos1[1] > pos2[1]:
      retVar = "topleft"
    else:
      retVar = "left"
  elif pos1[0] == pos2[0]:
    if pos1[1] < pos2[1]:
      retVar = "down" 
    elif pos1[1] > pos2[1]:
      retVar = "up"
  return retVar

# ===============================================================

def checkNeighbour(pos1, pos2):
  """ Checks if 2 points are neighbours or not.
  pos1: point 1.
  pos2: point 2.
  """
  kValue = False
  if pos1 == [pos2[0], pos2[1] - 1]:
    kValue = True
  elif pos1 == [pos2[0], pos2[1] + 1]:
    kValue = True
  elif pos1 == [pos2[0] - 1, pos2[1]]:
    kValue = True
  elif pos1 == [pos2[0] + 1, pos2[1]]:
    kValue = True
  elif pos1 == [pos2[0] - 1, pos2[1] - 1]:
    kValue = True
  elif pos1 == [pos2[0] + 1, pos2[1] + 1]:
    kValue = True
  elif pos1 == [pos2[0] - 1, pos2[1] + 1]:
    kValue = True
  elif pos1 == [pos2[0] + 1, pos2[1] - 1]:
    kValue = True
  return kValue  

# ===============================================================

def getFrontPosition(pos, heading, size):
  """ Returns the tile coords in front of the player.
  pos: player's position.
  heading: direction that the player is heading to.
  size: room's size
  """
  retVar = [-1, -1]
  if heading == "up" and not pos[1] == 0:
    retVar = [pos[0], pos[1] - 1]
  elif heading == "down" and not pos[1] == (size[1] - 1):
    retVar = [pos[0], pos[1] + 1]
  elif heading == "left" and not pos[0] == 0:
    retVar = [pos[0] - 1, pos[1]]
  elif heading == "right" and not pos[0] == (size[0] - 1):
    retVar = [pos[0] + 1, pos[1]]
  elif heading == "topleft" and not pos[0] == 0 and not pos[1] == 0:
    retVar = [pos[0] - 1, pos[1] - 1]
  elif heading == "bottomright" and not pos[0] == (size[0] - 1) and not pos[1] == (size[1] - 1):
    retVar = [pos[0] + 1, pos[1] + 1]
  elif heading == "bottomleft" and not pos[0] == 0 and not pos[1] == (size[1] - 1):
    retVar = [pos[0] - 1, pos[1] + 1]
  elif heading == "topright" and not pos[1] == 0 and not pos[0] == (size[0] - 1):
    retVar = [pos[0] + 1, pos[1] - 1]
  return retVar
    
# ===============================================================

def p2pDistance(point1, point2):
  """ Calculates the distance between 2 points.
  point1: starting point.
  point2: ending point.
  """
  if point1 == point2: 
    return 0
  return '%.3f' % math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[1] - point1[1]), 2))
    
# ===============================================================

def p3dToP2d(cord3d, anchor):
  """ Returns the physical 2d coordinates of a 3d virtual point.
  cord3d: 3d virtual point.
  anchor: point's anchor on screen.
  """
  x2d = SCREEN_OR[0]
  y2d = SCREEN_OR[1]
  x2d = x2d + (cord3d[0]*(TILE_SZ[0]/2)) - (cord3d[1]*(TILE_SZ[1])) 
  y2d = y2d + (cord3d[0]*(TILE_SZ[0]/4)) + (cord3d[1]*(TILE_SZ[1]/2)) 
  x2d = x2d - (anchor[0])
  y2d = y2d - (anchor[1])
    
  cord2d = [x2d, y2d]
  return cord2d
    

