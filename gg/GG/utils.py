import math
import os
import pygame
import ocempgui.widgets
import stat

#cache
if os.path.isdir("gg/GG/cache"):
  LOCAL_DATA_PATH = "gg/GG/cache"
else:
  LOCAL_DATA_PATH = "/usr/share/pixmaps/genteguada/cache"
CLEAR_CACHE_WEEKS = 4

#resources
if os.path.isdir("gg/GG/data"):
  DATA_PATH = "gg/GG/data"
  SOUND_PATH = "gg/GG/data/sound"
  NINO_PATH = "avatars/default_boy/"
  NINA_PATH = "avatars/default_girl/"
else:
  DATA_PATH = "/usr/share/pixmaps/genteguada/data"
  SOUND_PATH = "/usr/share/pixmaps/genteguada/data/sound"
  NINO_PATH = "/usr/share/pixmaps/genteguada/data/avatars/default_boy/"
  NINA_PATH = "/usr/share/pixmaps/genteguada/data/avatars/default_girl/"

VERSION = "GenteGuada 0.0.3.1"
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
GAMEZONE_SZ = [1024, 578]
HUD_SZ = [1024, SCREEN_SZ[1] - GAMEZONE_SZ[1]]
HUD_OR = [0, GAMEZONE_SZ[1]]

COLOR_SHIFT = 80
TEXT_LINE_LENGTH = 40

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
ANIM_INVENTORY_TIME = 1000
ANIM_CHAT_TIME1 = 2000
ANIM_CHAT_TIME2 = 1000

JUMP_TIME = 800
JUMP_ANIMATION_TIME = 100
JUMP_DISTANCE = 70

MAX_DEPTH = 1

POINTS_LOCATION = [800, 30]
EXP_LOCATION = [800, 50]

TEXT_COLOR = {"black": 0, "blue": 1}

HEADING = {0: "none", 1: "up", 2: "down", 3: "left", 4: "right",
           5: "topleft", 6: "bottomright", 7: "bottomleft", 8: "topright"}

STATE = {1: "standing", 2: "walking", 3: "standing_carrying", 4: "walking_carrying", 5: "standing_sleeping"}

CHAT_TYPE = {0: "White", 1: "Red", 2: "Green", 3: "Blue"}
#0: general; 1: privado; 2: npcs; 3: sistema)

CORNER_TOPLEFT = {0: "corner_topleft_white.png", 1: "corner_topleft_red.png", 2: "corner_topleft_green.png", 3: "corner_topleft_blue.png"}
CORNER_TOPRIGHT = {0: "corner_topright_white.png", 1: "corner_topright_red.png", 2: "corner_topright_green.png", 3: "corner_topright_blue.png"}
CORNER_BOTTOMLEFT = {0: "corner_bottomleft_white.png", 1: "corner_bottomleft_red.png", 2: "corner_bottomleft_green.png", 3: "corner_bottomleft_blue.png"}
CORNER_BOTTOMRIGHT = {0: "corner_bottomright_white.png", 1: "corner_bottomright_red.png", 2: "corner_bottomright_green.png", 3: "corner_bottomright_blue.png"}

BORDER_TOP = {0: "border_top_white.png", 1: "border_top_red.png", 2: "border_top_green.png", 3: "border_top_blue.png"}
BORDER_LEFT = {0: "border_left_white.png", 1: "border_left_red.png", 2: "border_left_green.png", 3: "border_left_blue.png"}
BORDER_RIGHT = {0: "border_right_white.png", 1: "border_right_red.png", 2: "border_right_green.png", 3: "border_right_blue.png"}
BORDER_BOTTOM = {0: "border_bottom_white.png", 1: "border_bottom_red.png", 2: "border_bottom_green.png", 3: "border_bottom_blue.png"}

TAIL = {0: "tail_white.png", 1: "tail_red.png", 2: "tail_green.png", 3: "tail_blue.png"}

# ======================= SPRITES ===========================

LOGIN_SCREEN = "login.png"
BG_BLACK = "bg_black.png"
TILE_STONE = "baldosaIsometricTile.tga"
TILE_WATER = "aguaIsometricTile.tga"
INTERFACE_LOWER = "interface/hud/interface_lower.png"
PATH_HUD = DATA_PATH + "/interface/hud"

# Sprites: items
OAK_SPRITE = "oak.png"
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
DOOR_DOWN_SPRITE = "door_down.png"
MP3_SPRITE = "mp3.png"
TRASH_SPRITE = "trash.png"
PUZZLECUBE_SPRITE = "puzzle_cube.png"
PUZZLECUBEBLUE_SPRITE = "puzzle_cube_blue.png"
BRICKCUBE_SPRITE = "brick_cube.png"

BLUE_KEY = "blue_key.png"
KEY_GOLDEN = "golden_key.png"
GIFT = "gift.png"
BOX_HEAVY = "heavy_box.png"
KILOGRAMME = "kilogramme.png"
KILOGRAMME_INV = "kilogramme_inv.png"
BEAM_WOODEN = "wooden_beam.png"

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
PATH_EDITOR_BACKGROUNDS = DATA_PATH + "/interface/backgrounds"

# Sprites: avatar design and buttons
DUMMY = "dummy.png"
GENDER_TAG = "genderTag.png"

# Avatar editor
PATH_EDITOR_IMG = DATA_PATH + "/editor"
PATH_EDITOR_INTERFACE = DATA_PATH + "/interface/editor"
IMG_EXTENSION = ".png"
PATH_PHOTO_MASK = LOCAL_DATA_PATH + "/mask" 
MASK_SIZE = {"S": [112,105],"M": [124,116],"L": [134,127],"XL": [146,137]}
MASK_COORD = {"S": (91,114),"M": (86,111), "L": (80,105),"XL": (74,100)}

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
          "inventoryArea" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                              "bordercolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 255),
                                                ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 255),
                                                ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 255),
                                                ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 255) 
                                              },
                            },
           "chatArea" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                          "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_ENTERED : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_ACTIVE : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_INSENSITIVE : (255, 0, 255) },
                          "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_ENTERED : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_ACTIVE : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_INSENSITIVE : (255, 0, 255) },
                          "lightcolor" : { ocempgui.widgets.Constants.STATE_NORMAL : (0, 0, 0),
                                          ocempgui.widgets.Constants.STATE_ENTERED : (0, 0, 0),
                                          ocempgui.widgets.Constants.STATE_ACTIVE : (0, 0, 0),
                                          ocempgui.widgets.Constants.STATE_INSENSITIVE : (0, 0, 0) },
                          "darkcolor" : { ocempgui.widgets.Constants.STATE_NORMAL : (0, 0, 0),
                                         ocempgui.widgets.Constants.STATE_ENTERED : (0, 0, 0),
                                         ocempgui.widgets.Constants.STATE_ACTIVE : (0, 0, 0),
                                         ocempgui.widgets.Constants.STATE_INSENSITIVE : (0, 0, 0) },
                          "bordercolor" : { ocempgui.widgets.Constants.STATE_NORMAL : (0, 0, 0),
                                           ocempgui.widgets.Constants.STATE_ENTERED : (0, 0, 0),
                                           ocempgui.widgets.Constants.STATE_ACTIVE : (0, 0, 0),
                                           ocempgui.widgets.Constants.STATE_INSENSITIVE : (0, 0, 0) },
                          "shadowcolor": ((0, 0, 0), (0, 0, 0)),
                          "image" : { ocempgui.widgets.Constants.STATE_NORMAL : None,
                                     ocempgui.widgets.Constants.STATE_ENTERED : None,
                                     ocempgui.widgets.Constants.STATE_ACTIVE : None,
                                     ocempgui.widgets.Constants.STATE_INSENSITIVE : None },
                           "font" : { "name" : None,
                                    "size" : 0,
                                    "alias" : False,
                                    "style" : 0 },
                           "shadow" : 0
            },
          "textFieldChat" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 255) 
                                          },
                              "bordercolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (97, 171, 193),
                                                ocempgui.widgets.Constants.STATE_ENTERED      : (97, 171, 193),
                                                ocempgui.widgets.Constants.STATE_ACTIVE       : (97, 171, 193),
                                                ocempgui.widgets.Constants.STATE_INSENSITIVE  : (97, 171, 193) 
                                              },
                            },
          "textFieldLogin" : { "font" : { "name" : "Bitstream", "size" : 25, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 255),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 255) 
                                          },
                              "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (200, 200, 200),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (200, 200, 200),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (200, 200, 200),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (200, 200, 200) 
                                          },
                              "bordercolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 255),
                                                ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 255),
                                                ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 255),
                                                ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 255) 
                                              },
                            },   
          "chatEntryWhite" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                          }
                            },
          "chatEntryRed" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                             "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (120, 30, 30),
                                           ocempgui.widgets.Constants.STATE_ENTERED      : (120, 30, 30),
                                           ocempgui.widgets.Constants.STATE_ACTIVE       : (120, 30, 30),
                                           ocempgui.widgets.Constants.STATE_INSENSITIVE  : (120, 30, 30) 
                                         }
                            },
          "chatEntryGreen" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                               "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (30, 120, 30),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (30, 120, 30),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (30, 120, 30),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (30, 120, 30) 
                                          }
                            },
          "chatEntryBlue" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (30, 30, 120),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (30, 30, 120),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (30, 30, 120),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (30, 30, 120) 
                                          }
                            },
          "chatBalloonWhite" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True }, 
                                "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (255, 255, 255),
                                           ocempgui.widgets.Constants.STATE_ENTERED      : (255, 255, 255),
                                           ocempgui.widgets.Constants.STATE_ACTIVE       : (255, 255, 255),
                                           ocempgui.widgets.Constants.STATE_INSENSITIVE  : (255, 255, 255) 
                                         }
                            },
          "chatBalloonBlue" : {"font" : { "name" : "Bitstream", "size" : 18, "alias" : True }, 
                               "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (200, 200, 255),
                                           ocempgui.widgets.Constants.STATE_ENTERED      : (200, 200, 255),
                                           ocempgui.widgets.Constants.STATE_ACTIVE       : (200, 200, 255),
                                           ocempgui.widgets.Constants.STATE_INSENSITIVE  : (200, 200, 255) 
                                         }
                            },
          "chatBalloonGreen" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                                 "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (200, 255, 200),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (200, 255, 200),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (200, 255, 200),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (200, 255, 200) 
                                          }
                            },
          "chatBalloonRed" : {  "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                                "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (255, 200, 200),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (255, 200, 200),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (255, 200, 200),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (255, 200, 200) 
                                          }
                            },
          "points" : {  "font" : { "name" : "Bitstream", "size" : 14, "alias" : True },
                                "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 74, 153) 
                                            },
                                "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (255, 246, 155),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (255, 246, 155),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (255, 246, 155),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (255, 246, 155) 
                                          }
                            },
          "userName" : {  "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                                "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 74, 153) 
                                            },
                                "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (255, 246, 155),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (255, 246, 155),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (255, 246, 155),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (255, 246, 155) 
                                          }
                            },   
          "hudLabel" : {  "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                                "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 74, 153) 
                                            },
                                "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (107, 177, 197),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (107, 177, 197),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (107, 177, 197),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (107, 177, 197) 
                                          }
                            },                          
            "itemLabel" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                            "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (255, 255, 255),
                                          ocempgui.widgets.Constants.STATE_ENTERED      : (255, 255, 255),
                                          ocempgui.widgets.Constants.STATE_ACTIVE       : (255, 255, 255),
                                          ocempgui.widgets.Constants.STATE_INSENSITIVE  : (255, 255, 255) 
                                        },
                            "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (48, 122, 173),
                                          ocempgui.widgets.Constants.STATE_ENTERED      : (48, 122, 173),
                                          ocempgui.widgets.Constants.STATE_ACTIVE       : (48, 122, 173),
                                          ocempgui.widgets.Constants.STATE_INSENSITIVE  : (48, 122, 173) 
                                        }
                            },
          "exchangeLabel" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                            "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (255, 255, 255),
                                          ocempgui.widgets.Constants.STATE_ENTERED      : (255, 255, 255),
                                          ocempgui.widgets.Constants.STATE_ACTIVE       : (255, 255, 255),
                                          ocempgui.widgets.Constants.STATE_INSENSITIVE  : (255, 255, 255) 
                                        },
                            "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (99, 172, 193),
                                          ocempgui.widgets.Constants.STATE_ENTERED      : (99, 172, 193),
                                          ocempgui.widgets.Constants.STATE_ACTIVE       : (99, 172, 193),
                                          ocempgui.widgets.Constants.STATE_INSENSITIVE  : (99, 172, 193) 
                                        }
                            },
          "buttonBar" :     { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True }, 
                             "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (97, 171, 193),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (97, 171, 193),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (97, 171, 193),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (97, 171, 193) 
                                          }
                            },
          "buttonTopBar" :     { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True }, 
                                "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL    : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                          }
                            },
          "nameFrame" : {  "font" : { "name" : "Bitstream", "size" : 40, "alias" : True },
                                "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (255, 255, 255),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (255, 255, 255),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (255, 255, 255),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (255, 255, 255) 
                                            },
                              "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (186, 216, 232),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (186, 216, 232),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (186, 216, 232),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (186, 216, 232) 
                                          }
                            },
          "quizLabel" : { "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                            "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                          ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                          ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                          ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                        },
                            "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (254, 245, 155),
                                          ocempgui.widgets.Constants.STATE_ENTERED      : (254, 245, 155),
                                          ocempgui.widgets.Constants.STATE_ACTIVE       : (254, 245, 155),
                                          ocempgui.widgets.Constants.STATE_INSENSITIVE  : (254, 245, 155) 
                                        }
                            }

         }
# ===============================================================
# ========================== FUNCTIONS ==========================
# ===============================================================

def getSpriteName(state, heading, frame, timestamp):
  #STATE = {1: "standing", 2: "walking", 3: "standing_carrying", 4: "walking_carrying", 5: "standing_sleeping"}
  timestamp = str(timestamp)
  if timestamp == "":
    tail = ""
  else:
    tail = "_"+timestamp

  maxFrames = 10
  if state == STATE[1] or state == STATE[3]:
    return str(state + "_" + heading + "_0001"+tail)
  elif state == STATE[2] or state == STATE[4]:
    maxFrames = ANIM_WALKING_COUNT
  elif state == STATE[5]:
    maxFrames = ANIM_RELAX_COUNT  
    
  if frame == 0:
    fileName = state + "_" + heading + "_00" + str(maxFrames)
  elif frame < 10:
    rgb= [0, 0, 0]
    fileName = state + "_" + heading + "_000" + str(frame)
  else:  
    fileName = state + "_" + heading + "_00" + str(frame)
  return fileName+tail

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
    
def p3dToP2d(cord3d, anchor):
  """ Returns the physical 2d coordinates of a 3d virtual point.
  cord3d: 3d virtual point.
  anchor: point's anchor on screen.
  """
  x2d = SCREEN_OR[0]
  y2d = SCREEN_OR[1]
  x2d = x2d + (cord3d[0]*(TILE_SZ[0]/2)) - (cord3d[2]*(TILE_SZ[1])) 
  y2d = y2d + (cord3d[0]*(TILE_SZ[0]/4)) + (cord3d[2]*(TILE_SZ[1]/2)) 
  x2d = x2d - (anchor[0])
  y2d = y2d - (anchor[1])
    
  y2d = y2d - (cord3d[1]*TILE_SZ[1]) 
    
  cord2d = [x2d, y2d]
  return cord2d
    
def playSound(sound):
  sndPath = os.path.join(SOUND_PATH, sound)
  if not os.path.isfile(sndPath):
    return False
  if not pygame.mixer.get_busy():
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
    
def distPoints(aPoint, anotherPoint):
  deltaX = anotherPoint[0] - aPoint[0]
  deltaY = anotherPoint[1] - aPoint[1]

  dotProduct = deltaX*deltaX + deltaY*deltaY

  return math.sqrt(dotProduct)

# ===============================================================
# =========================== CLASSES ===========================
# ===============================================================

class GroupSprite(pygame.sprite.Group):
  """ GroupSprite class.
  Redefines an OrderedUpdates sprite group class.
  """
  
  def __init__(self, *sprites):
    """ Constructor method.
    *sprites: sprites list.
    """
    pygame.sprite.Group.__init__(self, *sprites)
  
  def sprites(self):
    """ Order the group sprites according to their position.
    """
    keys = self.spritedict.keys()
    keys.sort(lambda x, y : (x.zOrder - y.zOrder))
    return keys
  
  def add(self, *sprites):
    for sprite in sprites:
      if hasattr(sprite, "zOrder"):
        if sprite.zOrder != None:
          pygame.sprite.Group.add(self, sprite)
        else:  
          raise "ERROR: zOrder = None"  
      else:    
        raise "ERROR: sprite sin zOrder"

class OcempLabel(ocempgui.widgets.Label):

  def __init__(self, text, width):
    line = ""  
    cad = text
    width = width/5
    while len(cad) > width:
      cad2aux = cad[0:width]
      blankPos = cad2aux.rfind(" ")
      if blankPos > 0:
        line = line + cad[0:blankPos] + "\n"     
        cad = cad[blankPos+1:]
      else:  
        line = line + cad[0:width] + "\n"     
        cad = cad[width:]  
    line = line + cad    
    
    ocempgui.widgets.Label.__init__(self,line)
    self.multiline = True
    self.set_align(ocempgui.widgets.Constants.ALIGN_LEFT | ocempgui.widgets.Constants.ALIGN_TOP)

class LabelTransparent(ocempgui.widgets.Label):
  
  def __init__(self,label, style):
    self.label = label
    self.typeFont = style["font"]["name"] 
    self.sizeFont = style["font"]["size"]
    self.aliasFont = style["font"]["alias"]
    self.colorFont = style["fgcolor"][0]
    ocempgui.widgets.Label.__init__(self,label)

  def update(self):
    self.draw()

  def draw(self):
    #ocempgui.widgets.Label.draw(self)
    self._image = ocempgui.draw.String.draw_string (self.label, self.typeFont, self.sizeFont, self.aliasFont, self.colorFont)

    

class OcempImageMapTransparent(ocempgui.widgets.ImageMap):

  def __init__(self, image):
    ocempgui.widgets.ImageMap.__init__(self, image)
  
  def draw (self):
    self._image = self.picture
      

class OcempImageButtonTransparent(ocempgui.widgets.ImageButton):

  def __init__(self, image, label = None, tooltipShow = None, tooltipRemove = None):
    ocempgui.widgets.ImageButton.__init__(self, image)
    if tooltipShow and label:
      self.connect_signal (ocempgui.widgets.Constants.SIG_ENTER, tooltipShow, label)
    if tooltipShow and label and tooltipRemove:
      self.connect_signal (ocempgui.widgets.Constants.SIG_LEAVE, tooltipRemove)
    
  def draw(self):
    ocempgui.widgets.ImageButton.draw(self)
    self._image = self.picture

  def update(self): 
    self.draw()
  

class OcempImageFileList(ocempgui.widgets.FileList):
  
  def __init__(self, width, height):
    ocempgui.widgets.FileList.__init__(self, width, height)

  def _list_contents (self):
    items = ocempgui.widgets.components.ListItemCollection ()
    items.append (ocempgui.widgets.components.FileListItem (os.pardir, stat.S_IFDIR))
    stats = None
    files = []
    dirs = []
    dappend = dirs.append
    fappend = files.append
    entries = os.listdir (self._directory)
    isdir = os.path.isdir
    pjoin = os.path.join
        
    for filename in entries:
      if not filename.startswith("."):
        if isdir (pjoin (self._directory, filename)):
          dappend (filename)
        else:
          file, ext = os.path.splitext(filename)
          if ext in [".jpg",".JPG",".png",".PNG"]: 
            fappend (filename)
    dirs.sort ()
    files.sort ()
        
    map (items.append, [ocempgui.widgets.components.FileListItem (d, stat.S_IFDIR) for d in dirs])
    for filename in files:
      stats = os.stat (pjoin (self._directory, filename))
      items.append (ocempgui.widgets.components.FileListItem (filename, stats.st_mode))
    self.set_items (items)

  def getFileName(self):
    item = self.get_selected()
    if len(item):
      file = os.path.join (self.directory, item[0].text)
      if os.path.isfile(file):
        return file
    return None

class OcempContactListItem(ocempgui.widgets.components.FileListItem):

  def __init__(self, name):
    ocempgui.widgets.components.FileListItem.__init__(self, name, 0)
    filePath = DATA_PATH+"/book.png"
    self._icon = ocempgui.draw.Image.load_image(filePath)
    
    
class OcempImageContactList(OcempImageFileList):
  
  def __init__(self, width, height, contactList):
    self.contactList = contactList
    OcempImageFileList.__init__(self, width, height)

  def _list_contents (self):
    items = ocempgui.widgets.components.ListItemCollection ()
    for contact in self.contactList:
      items.append (OcempContactListItem (contact.getPlayer().username))
    self.set_items (items)

  def getSelectedName(self):
    item = self.get_selected()
    if len(item):
      return item[0].text
    return None


