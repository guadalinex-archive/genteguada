# -*- coding: utf-8 -*-

import math
import os
import stat

# ======================= GENERAL PATHS ===========================

#imageinit
if os.path.isdir("gg/GG/initimage"):
  INIT_IMAGE_PATH = "gg/GG/initimage"
else:
  INIT_IMAGE_PATH = "/usr/share/pixmaps/genteguada/initimage"

#cache
if os.path.isdir("gg/GG/cache"):
  LOCAL_DATA_PATH = "gg/GG/cache"
else:
  LOCAL_DATA_PATH = "/usr/share/pixmaps/genteguada/cache"

#resources
if os.path.isdir("gg/GG/data"):
  DATA_PATH = "gg/GG/data"
else:
  DATA_PATH = "/usr/share/pixmaps/genteguada/data"

DIR_FILES_CLIENT_ERROR = os.path.join(DATA_PATH, "clienterror")

#PATHS IMAGE
INTERFACE_PATH = "interface"
FURNITURE_PATH = "furniture"
SOUND_PATH = "sound"
MASKS_PATH = "masks"
INTERFACE_AVATARS = "avatars"
MASKS_DIR = os.path.join(INTERFACE_AVATARS, MASKS_PATH)
TILE = "tiles"
ICONS_PATH = os.path.join(DATA_PATH,"icons")
IMAGES_GIFT = "imagesgift"
IMAGES_GIFT_PATH = os.path.join(DATA_PATH, "imagesgift")
SAVE_DATA = os.path.join(DATA_PATH, "savedata")
HUD_PATH = os.path.join(INTERFACE_PATH, "hud")
NINO_PATH = os.path.join(INTERFACE_AVATARS, "default_boy")
NINA_PATH = os.path.join(INTERFACE_AVATARS, "default_girl")
QUESTIONS_PATH = os.path.join(DATA_PATH, "questions")
BACKGROUNDS = os.path.join(INTERFACE_PATH,"backgrounds")
EDITOR = os.path.join(INTERFACE_PATH,"editor")
ADMIN_ACTIONS_BACKGROUND = os.path.join(HUD_PATH, "adminActions.png")
ADMIN_ACTIONS_LARGE_BACKGROUND = os.path.join(HUD_PATH, "adminActionsLarge.png")
TINY_OK_IMAGE = os.path.join(HUD_PATH, "tiny_ok_button.png")
TINY_CANCEL_IMAGE = os.path.join(HUD_PATH, "tiny_cancel_button.png")

PATH_EDITOR_INTERFACE = os.path.join(INTERFACE_PATH,"editor")
FILE_BUTTON_IMAGE = os.path.join(HUD_PATH, "tiny_file_button.png")
OK_BUTTON_IMAGE = os.path.join(PATH_EDITOR_INTERFACE, "ok_button.png")
CANCEL_BUTTON_IMAGE = os.path.join(PATH_EDITOR_INTERFACE, "cancel_button.png")

UPLOAD_BACKGROUND = os.path.join(BACKGROUNDS, "uploadWindow.png")

DIR_ERROR = os.path.join(LOCAL_DATA_PATH, "error")
IMG_ERROR = os.path.join(LOCAL_DATA_PATH, "error", "error.png")
DIR_FONT = os.path.join(LOCAL_DATA_PATH, "font")

# ======================= CONSTANTS ===========================
# Screen & General values
TILE_SZ = [120, 60]
CHAR_SZ = [50, 50]
SCREEN_SZ = [1024, 768]
SCREEN_OR = [SCREEN_SZ[0]/2 -8, 5]
FLOOR_SHIFT = [55, -30]
GAMEZONE_SZ = [SCREEN_SZ[0], 578]

# Chat & iventory
INV_ITEM_COUNT = [3, 2]

# Animation values
TICK_DELAY = 0.45
ANIM_WALKING_COUNT = 10
ANIM_WALKING_TIME = int(TICK_DELAY*ANIM_WALKING_COUNT*100)
TEXT_COLOR = {"black": 0, "blue": 1}

# Player headings.
HEADING = {0: None, 1: "up", 2: "down", 3: "left", 4: "right", 5: "topleft", 6: "bottomright", 7: "bottomleft", 8: "topright"}
# Player states.
STATE = {1: "standing", 2: "walking", 3: "standing_carrying", 4: "walking_carrying", 5: "standing_sleeping"}

# ======================= SPRITES ===========================
IMAGE_CHAT_MESSAGE = "chatEntry.png"

# Avatar editor
PATH_PHOTO_MASK = os.path.join(LOCAL_DATA_PATH, "mask") 

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

TAGS = [GENDER_TAG, SKIN_TAG, HEAD_TAG, BODY_TAG, MASK_TAG, HAIR_TAG, SHIRT_TAG, SHORT_TAG, SKIRT_TAG, SHOES_TAG]



#================== TILES ============================================================================

TILES_BEACH = ["arena1.png","arena2.png","arena3.png","arena4.png", "costaTileCornerDown.png" , "costaTileCornerUp.png","costaTileCornerLeft.png" ,"costaTileCornerRight.png"] 
TILES_DESERT = ["desierto1.png","desierto2.png","desierto3.png"] 
TILES_GRAVEL = ["gravilla1.png"] 
TILES_ALBERO = ["albero1.png","albero2.png"] 
TILES_GRASS = ["hierba1.png","hierba2.png"] 
TILES_SNOW = ["nieve1.png","nieve2.png"] 
TILES_TERRAZO = ["terrazo1.png"] 
TILES_MUD = ["barro1.png","barro2.png","barro3.png"] 
TILES_MOZARABE = ["mozarabe1.png","mozarabe2.png"] 
TILES_FOOTBALL = ["futbol1.png","futbol2.png","futbol3.png"] 
TILES_CHESS = ["ajedrez1.png","ajedrez1b.png","ajedrez2.png","ajedrez2b.png"]
TILES_SEA = ["mar_piedra.png"]
TILES_RIVER = ["aguaRio.png","rio_piedra.png","costaRiverTileCornerDown.png","costaRiverTileCornerUp.png","costaRiverTileCornerLeft.png","costaRiverTileCornerRight.png","costaTileRiverDown.png","costaTileRiverUp.png","costaTileRiverRight.png","costaTileRiverLeft.png","costaBarroRioCornerDown.png","costaBarroRioCornerLeft.png",
"costaBarroRioCornerRight.png","costaBarroRioCornerUp.png","costaBarroTileRioDown.png","costaBarroTileRioUp.png","costaBarroTileRioLeft.png","costaBarroTileRioRight.png","costaNieveRioRight.png","costaNieveRioLeft.png","costaNieveRioUp.png","costaNieveRioDown.png","costaNieveRioCornerDown.png","costaNieveRioCornerUp.png",
"costaNieveRioCornerRight.png","costaNieveRioCornerLeft.png"]



PRESSED_TILE = os.path.join("tiles","actuador.png")

TILES = TILES_SEA + TILES_BEACH + TILES_DESERT + TILES_GRAVEL + TILES_ALBERO + TILES_GRASS + TILES_SNOW + TILES_TERRAZO + TILES_MUD + TILES_MOZARABE + TILES_FOOTBALL + TILES_CHESS + TILES_RIVER + ["asfalto.png","actuador.png"]

#================== WALL ============================================================================

CORNER_BRICK = os.path.join(FURNITURE_PATH, "esquina2.png")
BRICK_LEFT = os.path.join(FURNITURE_PATH, "ladrillo_2.png")
BRICK_UP = os.path.join(FURNITURE_PATH, "ladrillo_2b.png")

CORNER_STONE = os.path.join(FURNITURE_PATH, "esquina_piedra.png")
STONE_LEFT = os.path.join(FURNITURE_PATH, "piedra.png")
STONE_UP = os.path.join(FURNITURE_PATH, "piedrab.png")

CORNER_WOOD = os.path.join(FURNITURE_PATH, "esquina_madera.png")
WOOD_LEFT = os.path.join(FURNITURE_PATH, "madera.png")
WOOD_UP = os.path.join(FURNITURE_PATH, "madera_b.png")

CORNER_BUSH = os.path.join(FURNITURE_PATH, "esquina_arbusto.png")
BUSH_LEFT = os.path.join(FURNITURE_PATH, "muroArbusto.png")
BUSH_UP = os.path.join(FURNITURE_PATH, "arbusto_b.png")

CORNER_WIRE = os.path.join(FURNITURE_PATH, "esquina_alambre.png")
WIRE_LEFT = os.path.join(FURNITURE_PATH, "alambre.png")
WIRE_UP = os.path.join(FURNITURE_PATH, "alambre_b.png")

WALLS = ["esquina2.png","ladrillo_2.png","ladrillo_2b.png","esquina_piedra.png","piedra.png","piedrab.png","esquina_madera.png","madera.png","madera_b.png","esquina_arbusto.png","muroArbusto.png","arbusto_b.png","esquina_alambre.png","alambre.png","alambre_b.png"]

#=============== DECORATORS ==================================================================

FIR = os.path.join(FURNITURE_PATH, "abeto.png")
BUSH = os.path.join(FURNITURE_PATH, "arbusto.png")
CACTUS_1 = os.path.join(FURNITURE_PATH, "cactus1.png")
CACTUS_2 = os.path.join(FURNITURE_PATH, "cactus2.png")
COLUMN = os.path.join(FURNITURE_PATH, "columna.png")
SHELF_1 = os.path.join(FURNITURE_PATH, "estanteria1.png")
SHELF_2 = os.path.join(FURNITURE_PATH, "estanteria2.png")
LAMP = os.path.join(FURNITURE_PATH, "farola.png")
FONT = os.path.join(FURNITURE_PATH, "fuente.png")
ORANGETREE = os.path.join(FURNITURE_PATH, "naranjo.png")
OLIVETREE = os.path.join(FURNITURE_PATH, "olivo.png")
RACK = os.path.join(FURNITURE_PATH, "perchero.png")
PINE_1 = os.path.join(FURNITURE_PATH, "pino.png")
PINE_2 = os.path.join(FURNITURE_PATH, "pino2.png")
ROCK3 = os.path.join(FURNITURE_PATH, "roca3.png")
COW = os.path.join(FURNITURE_PATH, "vaca.png")
COW_2 = os.path.join(FURNITURE_PATH, "vaca2.png")
COW_violet= os.path.join(FURNITURE_PATH, "vaca_morada.png")
COW_2_violet= os.path.join(FURNITURE_PATH, "vaca2_morada.png")
LINCE = os.path.join(FURNITURE_PATH, "lince.png")

DECORATORS = ["abeto.png","arbusto.png","cactus1.png","cactus2.png","columna.png","estanteria1.png","estanteria2.png","farola.png","fuente.png","naranjo.png","olivo.png","perchero.png","pino.png","pino2.png","roca3.png","vaca.png","vaca2.png","lince.png","vaca_morada.png","vaca2_morada.png"]

#=============== STACKS ==================================================================

HAY = os.path.join(FURNITURE_PATH, "heno.png")
TABLE = os.path.join(FURNITURE_PATH, "mesa.png")
WEIGHS = os.path.join(FURNITURE_PATH, "pesa.png")
BOX = os.path.join(FURNITURE_PATH, "caja.png")
ROCK2 = os.path.join(FURNITURE_PATH, "roca2.png")
POT = os.path.join(FURNITURE_PATH, "maceta.png")
CHAIR2 = os.path.join(FURNITURE_PATH, "silla2.png")
CHAIR1 = os.path.join(FURNITURE_PATH, "silla1.png")

STACKS_TOPANCHOR = {}
STACKS_TOPANCHOR["heno.png"] = -12
STACKS_TOPANCHOR["mesa.png"] = -12
STACKS_TOPANCHOR["pesa.png"] = -12
STACKS_TOPANCHOR["caja.png"] = -12
STACKS_TOPANCHOR["roca2.png"] = -25
STACKS_TOPANCHOR["maceta.png"] = -12
STACKS_TOPANCHOR["silla2.png"] = -100
STACKS_TOPANCHOR["silla1.png"] = -100

STACKS = ["heno.png","mesa.png","pesa.png","caja.png","roca2.png","maceta.png","silla2.png","silla1.png"]


#=============== KEYS ==================================================================

KEY_BLUE_2 = os.path.join(FURNITURE_PATH, "llave_azul2.png")
KEY_BLUE_1 = os.path.join(FURNITURE_PATH, "llave_azul.png")
KEY_BRONZE = os.path.join(FURNITURE_PATH, "llave_bronce.png")
KEY_GOLDEN = os.path.join(FURNITURE_PATH, "llave_dorada.png")
KEY_RED = os.path.join(FURNITURE_PATH, "llave_roja.png")
KEY_VIOLET = os.path.join(FURNITURE_PATH, "llave_violeta.png")
KEY_GREEN = os.path.join(FURNITURE_PATH, "llave_verde.png")

KEYS = ["llave_azul2.png","llave_azul.png","llave_bronce.png","llave_dorada.png","llave_roja.png","llave_violeta.png","llave_verde.png"]


#=============== INVENTORY ==================================================================

GIFT = os.path.join(FURNITURE_PATH, "regalo.png")
MUSHROOMS = os.path.join(FURNITURE_PATH, "setas.png")
SARDINES = os.path.join(FURNITURE_PATH, "sardinas.png")
ROCK1 = os.path.join(FURNITURE_PATH, "roca1.png")
CD = os.path.join(FURNITURE_PATH, "cd_guadalinex.png")
CRAB = os.path.join(FURNITURE_PATH, "cangrejo.png")
CLAM = os.path.join(FURNITURE_PATH, "almeja.png")


INVENTORYS = ["regalo.png","setas.png","sardinas.png","roca1.png","cd_guadalinex.png","cangrejo.png","almeja.png"]

#=============== MONEY ==================================================================

TICKET_5 = os.path.join(FURNITURE_PATH, "5Guadapuntos.png")
TICKET_10 = os.path.join(FURNITURE_PATH, "10Guadapuntos.png")
TICKET_50 = os.path.join(FURNITURE_PATH, "50Guadapuntos.png")
CURRENCY = os.path.join(FURNITURE_PATH, "moneda.png")

MONEY_VALUE = {}
MONEY_VALUE["5Guadapuntos.png"] = 5
MONEY_VALUE["10Guadapuntos.png"] = 10
MONEY_VALUE["50Guadapuntos.png"] = 50
MONEY_VALUE["moneda.png"] = 1

MONEY_LABEL = {}
MONEY_LABEL["5Guadapuntos.png"] = "Billete 5"
MONEY_LABEL["10Guadapuntos.png"] = "Billete 10"
MONEY_LABEL["50Guadapuntos.png"] = "Billete 50"
MONEY_LABEL["moneda.png"] = "Moneda 1"

MONEYS = ["5Guadapuntos.png","10Guadapuntos.png","50Guadapuntos.png","moneda.png"]

#=============== COAST ==================================================================

COAST_UP = os.path.join(FURNITURE_PATH, "costaUp.png")
COAST_DOWN = os.path.join(FURNITURE_PATH, "costaDown.png")
COAST_LEFT = os.path.join(FURNITURE_PATH, "costaLeft.png")
COAST_RIGHT = os.path.join(FURNITURE_PATH, "costaRight.png")

COAST_LEFT = os.path.join(FURNITURE_PATH, "mar.png")

COAST_UP_2 = os.path.join(FURNITURE_PATH, "costa2Up.png")
COAST_DOWN_2 = os.path.join(FURNITURE_PATH, "costa2Down.png")
COAST_LEFT_2 = os.path.join(FURNITURE_PATH, "costa2Left.png")
COAST_RIGHT_2 = os.path.join(FURNITURE_PATH, "costa2Right.png")

COAST_CORNER_UP = os.path.join(FURNITURE_PATH, "costaCornerUp.png")
COAST_CORNER_DOWN = os.path.join(FURNITURE_PATH, "costaCornerDown.png")
COAST_CORNER_RIGHT = os.path.join(FURNITURE_PATH, "costaCornerRight.png")
COAST_CORNER_LEFT = os.path.join(FURNITURE_PATH, "costaCornerLeft.png")

COAST_RIVER_CORNER_DOWN = os.path.join(FURNITURE_PATH, "costaRioCornerDown.png")
COAST_RIVER_CORNER_LEFT = os.path.join(FURNITURE_PATH, "costaRioCornerLeft.png")
COAST_RIVER_CORNER_RIGHT = os.path.join(FURNITURE_PATH, "costaRioCornerRight.png")
COAST_RIVER_CORNER_UP = os.path.join(FURNITURE_PATH, "costaRioCornerUp.png")

COAST_RIVER_CORNER2_RIGHT = os.path.join(FURNITURE_PATH, "costaRightPico.png")

COAST_RIVER_DOWN = os.path.join(FURNITURE_PATH, "costaRioDown.png")
COAST_RIVER_LEFT = os.path.join(FURNITURE_PATH, "costaRioLeft.png")
COAST_RIVER_RIGHT = os.path.join(FURNITURE_PATH, "costaRioRight.png")
COAST_RIVER_UP = os.path.join(FURNITURE_PATH, "costaRioUp.png")

COAST_RIVER_PICO_DOWN = os.path.join(FURNITURE_PATH, "costaRioPicoDown.png")
COAST_RIVER_PICO_LEFT = os.path.join(FURNITURE_PATH, "costaRioPicoLeft.png")
COAST_RIVER_PICO_RIGHT = os.path.join(FURNITURE_PATH, "costaRioPicoRight.png")
COAST_RIVER_PICO_UP = os.path.join(FURNITURE_PATH, "costaRioPicoUp.png")

COAST_MUD_RIVER_CORNER_DOWN = os.path.join(FURNITURE_PATH, "costaBarroRioCornerDown.png")
COAST_MUD_RIVER_CORNER_LEFT = os.path.join(FURNITURE_PATH, "costaBarroRioCornerLeft.png")
COAST_MUD_RIVER_CORNER_RIGHT = os.path.join(FURNITURE_PATH, "costaBarroRioCornerRight.png")
COAST_MUD_RIVER_CORNER_UP = os.path.join(FURNITURE_PATH, "costaBarroRioCornerUp.png")

COAST_MUD_RIVER_DOWN = os.path.join(FURNITURE_PATH, "costaBarroRioDown.png")
COAST_MUD_RIVER_LEFT = os.path.join(FURNITURE_PATH, "costaBarroRioLeft.png")
COAST_MUD_RIVER_RIGHT = os.path.join(FURNITURE_PATH, "costaBarroRioRight.png")
COAST_MUD_RIVER_UP = os.path.join(FURNITURE_PATH, "costaBarroRioUp.png")

COAST_MUD_RIVER_PICO_DOWN = os.path.join(FURNITURE_PATH, "costaBarroRioPicoDown.png")
COAST_MUD_RIVER_PICO_LEFT = os.path.join(FURNITURE_PATH, "costaBarroRioPicoLeft.png")
COAST_MUD_RIVER_PICO_RIGHT = os.path.join(FURNITURE_PATH, "costaBarroRioPicoRight.png")
COAST_MUD_RIVER_PICO_UP = os.path.join(FURNITURE_PATH, "costaBarroRioPicoUp.png")

COAST_WATER_RIVER = os.path.join(FURNITURE_PATH, "aguaRio.png")
COAST_WATER_RIVER1 = os.path.join(FURNITURE_PATH, "aguaRio1.png")
COAST_WATER_RIVER2 = os.path.join(FURNITURE_PATH, "aguaRio2.png")
COAST_WATER_RIVER3 = os.path.join(FURNITURE_PATH, "aguaRio3.png")
COAST_WATER_RIVER4 = os.path.join(FURNITURE_PATH, "aguaRio4.png")
COAST_WATER_RIVER5 = os.path.join(FURNITURE_PATH, "aguaRio5.png")
COAST_WATER_RIVER6 = os.path.join(FURNITURE_PATH, "aguaRio6.png")


COASTS = ["costaUp.png","costaDown.png","costaLeft.png","costaRight.png","costa2Up.png","costa2Down.png","costa2Left.png","costa2Right.png","costaCornerUp.png", "costaCornerDown.png","costaCornerRight.png","costaCornerLeft.png","costaRioCornerDown.png","costaRioCornerLeft.png","costaRioCornerRight.png",
"costaRioCornerUp.png","costaRioDown.png","costaRioLeft.png","costaRioRight.png","costaRioUp.png","costaBarroRioCornerDown.png","costaBarroRioCornerLeft.png",
"costaBarroRioCornerRight.png","costaBarroRioCornerUp.png","costaBarroRioDown.png","costaBarroRioLeft.png","costaBarroRioRight.png","costaBarroRioUp.png"
,"aguaRio.png","aguaRio1.png","aguaRio2.png","aguaRio3.png","aguaRio4.png","aguaRio5.png","aguaRio6.png","costaRioPicoDown.png","costaRioPicoLeft.png",
"costaRioPicoRight.png","costaRioPicoUp.png","costaBarroRioPicoDown.png","costaBarroRioPicoLeft.png","costaBarroRioPicoRight.png","costaBarroRioPicoUp.png", 
"costaNieveRioRight.png","costaNieveRioLeft.png","costaNieveRioUp.png","costaNieveRioDown.png","costaNieveRioCornerDown.png","costaNieveRioCornerUp.png",
"costaNieveRioCornerRight.png","costaNieveRioCornerLeft.png", "costaNieveRioPicoDown.png","costaNieveRioPicoUp.png","costaNieveRioPicoLeft.png","costaNieveRioPicoRight.png"]



#=============== RIVER ==================================================================

RIVER_CORNER_RIGHT_DOWN = os.path.join(FURNITURE_PATH, "rioCurvaDchDown.png")
RIVER_CORNER_RIGHT_UP = os.path.join(FURNITURE_PATH, "rioCurvaDchUp.png")
RIVER_CORNER_LEFT_DOWN = os.path.join(FURNITURE_PATH, "rioCurvaIzqDown.png")
RIVER_CORNER_LEFT_UP = os.path.join(FURNITURE_PATH, "rioCurvaIzqUp.png")

RIVER_FINISH_UP = os.path.join(FURNITURE_PATH, "rioFinalUp.png")
RIVER_FINISH_DOWN = os.path.join(FURNITURE_PATH, "rioFinalDown.png")
RIVER_FINISH_LEFT = os.path.join(FURNITURE_PATH, "rioFinalLeft.png")
RIVER_FINISH_RIGHT = os.path.join(FURNITURE_PATH, "rioFinalRight.png")

RIVER_RECT_UP = os.path.join(FURNITURE_PATH, "rioRectoUp.png")
RIVER_RECT_LEFT = os.path.join(FURNITURE_PATH, "rioRectoLeft.png")

RIVER_ROCK = os.path.join(FURNITURE_PATH, "mar_saltable.png")

RIVERS = ["rioCurvaDchDown.png","rioCurvaDchUp.png","rioCurvaIzqDown.png","rioCurvaIzqUp.png","rioFinalUp.png","rioFinalDown.png","rioFinalLeft.png","rioFinalRight.png","rioRectoUp.png","rioRectoLeft.png", "mar.png","mar_saltable.png"]


#=============== DOORS ==================================================================

DOOR_CORINTHIAN_UP = os.path.join(FURNITURE_PATH, "puertaCorintiaUp.png")
DOOR_CORINTHIAN_LEFT = os.path.join(FURNITURE_PATH, "puertaCorintiaLeft.png")
DOOR_CORINTHIAN_DOWN = os.path.join(FURNITURE_PATH, "puertaCorintiaDown.png")
DOOR_CORINTHIAN_RIGHT = os.path.join(FURNITURE_PATH, "puertaCorintiaRight.png")

DOOR_DORIC_UP = os.path.join(FURNITURE_PATH, "puertaDoricaUp.png")
DOOR_DORIC_LEFT = os.path.join(FURNITURE_PATH, "puertaDoricaLeft.png")
DOOR_DORIC_DOWN = os.path.join(FURNITURE_PATH, "puertaDoricaDown.png")
DOOR_DORIC_RIGHT = os.path.join(FURNITURE_PATH, "puertaDoricaRight.png")

DOOR_IONIAN_UP = os.path.join(FURNITURE_PATH, "puertaJonicaUp.png")
DOOR_IONIAN_LEFT = os.path.join(FURNITURE_PATH, "puertaJonicaLeft.png")
DOOR_IONIAN_DOWN = os.path.join(FURNITURE_PATH, "puertaJonicaDown.png")
DOOR_IONIAN_RIGHT = os.path.join(FURNITURE_PATH, "puertaJonicaRight.png")

DOOR_SALOMONIC_UP = os.path.join(FURNITURE_PATH, "puertaSalomonicaUp.png")
DOOR_SALOMINIC_LEFT = os.path.join(FURNITURE_PATH, "puertaSalomonicaLeft.png")
DOOR_SALOMINIC_DOWN = os.path.join(FURNITURE_PATH, "puertaSalomonicaDown.png")
DOOR_SALOMINIC_RIGHT = os.path.join(FURNITURE_PATH, "puertaSalomonicaRight.png")

DOOR_WALL_UP = os.path.join(FURNITURE_PATH, "puertaMuroUp.png")
DOOR_WALL_LEFT = os.path.join(FURNITURE_PATH, "puertaMuroLeft.png")
DOOR_WALL_DOWN = os.path.join(FURNITURE_PATH, "puertaMuroDown.png")
DOOR_WALL_RIGHT = os.path.join(FURNITURE_PATH, "puertaMuroRight.png")

DOOR_ROAD_UP = os.path.join(FURNITURE_PATH, "puertaCarreteraUp.png")
DOOR_ROAD_LEFT = os.path.join(FURNITURE_PATH, "puertaCarreteraLeft.png")
DOOR_ROAD_DOWN = os.path.join(FURNITURE_PATH, "puertaCarreteraDown.png")
DOOR_ROAD_RIGHT = os.path.join(FURNITURE_PATH, "puertaCarreteraRight.png")

DOOR_FENCE_UP = os.path.join(FURNITURE_PATH, "puertaVallaUp.png")
DOOR_FENCE_LEFT = os.path.join(FURNITURE_PATH, "puertaVallaLeft.png")
DOOR_FENCE_DOWN = os.path.join(FURNITURE_PATH, "puertaVallaDown.png")
DOOR_FENCE_RIGHT = os.path.join(FURNITURE_PATH, "puertaVallaRight.png")

DOOR_DOWN = os.path.join(FURNITURE_PATH, "downArrow.png")
DOOR_UP = os.path.join(FURNITURE_PATH, "upArrow.png")
DOOR_LEFT = os.path.join(FURNITURE_PATH, "leftArrow.png")
DOOR_RIGHT = os.path.join(FURNITURE_PATH, "rightArrow.png")

DOORS = ["puertaCorintiaUp.png","puertaCorintiaLeft.png","puertaDoricaUp.png","puertaDoricaLeft.png","puertaJonicaUp.png","puertaJonicaLeft.png","puertaSalomonicaUp.png","puertaSalomonicaLeft.png","puertaMuroUp.png","puertaMuroLeft.png","puertaCarreteraUp.png","puertaCarreteraLeft.png","downArrow.png","upArrow.png","leftArrow.png","rightArrow.png","puertaVallaUp.png","puertaVallaLeft.png","puertaCorintiaDown.png","puertaCorintiaRight.png","puertaDoricaDown.png","puertaDoricaRight.png","puertaJonicaDown.png","puertaJonicaRight.png","puertaSalomonicaDown.png","puertaSalomonicaRight.png","puertaCarreteraDown.png","puertaCarreteraRight.png","puertaMuroDown.png","puertaMuroRight.png","puertaVallaDown.png","puertaVallaRight.png"]


#=============== PANNELS ==================================================================

PANNEL_UP = os.path.join(FURNITURE_PATH, "panelUp.png")
PANNEL_LEFT = os.path.join(FURNITURE_PATH, "panelLeft.png")



PANNEL_UP = os.path.join(FURNITURE_PATH, "panelUpEdukanda.png")
PANNEL_LEFT = os.path.join(FURNITURE_PATH, "panelLeftEdukanda.png")

PANNEL_UP = os.path.join(FURNITURE_PATH, "panelUpGuadaSoft.png")
PANNEL_LEFT = os.path.join(FURNITURE_PATH, "panelLeftGuadaSoft.png")

PANNEL_UP = os.path.join(FURNITURE_PATH, "panelUpkiddia.png")
PANNEL_LEFT = os.path.join(FURNITURE_PATH, "panelLeftkiddia.png")

PANNEL_UP = os.path.join(FURNITURE_PATH, "panelUpWikanda.png")
PANNEL_LEFT = os.path.join(FURNITURE_PATH, "panelLeftWikanda.png")

PANNEL_UP = os.path.join(FURNITURE_PATH, "panelUpGuadalinfo.png")
PANNEL_LEFT = os.path.join(FURNITURE_PATH, "panelLeftGuadalinfo.png")

PANNEL_UP = os.path.join(FURNITURE_PATH, "panelUpGuadalinex_ant.png")
PANNEL_LEFT = os.path.join(FURNITURE_PATH, "panelLeftGuadalinex_ant.png")

PANNEL_UP = os.path.join(FURNITURE_PATH, "panelUpGuadaV6.png")
PANNEL_LEFT = os.path.join(FURNITURE_PATH, "panelLeftGuadaV6.png")


PANNELS = ["panelUp.png","panelLeft.png","panelUpEdukanda.png","panelLeftEdukanda.png","panelUpGuadaSoft.png","panelLeftGuadaSoft.png","panelUpkiddia.png","panelLeftkiddia.png","panelUpWikanda.png","panelLeftWikanda.png","panelUpGuadalinfo.png","panelLeftGuadalinfo.png","panelUpGuadalinex_ant.png","panelLeftGuadalinex_ant.png","panelUpGuadaV6.png","panelLeftGuadaV6.png"]


#=============== WEBS ==================================================================

WEBS = WALLS + DECORATORS + STACKS + KEYS + INVENTORYS + DOORS + PANNELS

#=============== RANDOMS ==================================================================

RANDOMS = KEYS + INVENTORYS

#=============== ANDATUZ ==================================================================

ANDATUZ_DOWN = os.path.join(FURNITURE_PATH, "andatuzDown.png")
ANDATUZ_RIGHT = os.path.join(FURNITURE_PATH, "andatuzRight.png")
ANDATUZ_UP = os.path.join(FURNITURE_PATH, "andatuzUp.png")

ANDATUZ_TALKER_LEFT = os.path.join(FURNITURE_PATH, "andatuzHabladorLeft.png")
ANDATUZ_TALKER_UP = os.path.join(FURNITURE_PATH, "andatuzHabladorUp.png")

ANDATUZ_GIVER_LEFT = os.path.join(FURNITURE_PATH, "andatuzGenerosoLeft.png")
ANDATUZ_GIVER_UP = os.path.join(FURNITURE_PATH, "andatuzGenerosoUp.png")

ANDATUZ_QUIZ_LEFT = os.path.join(FURNITURE_PATH, "andatuzPreguntonLeft.png")
ANDATUZ_QUIZ_UP = os.path.join(FURNITURE_PATH, "andatuzPreguntonUp.png")

PENGUINS = ["andatuzDown.png","andatuzRight.png","andatuzUp.png"]
PENGUINS_TALKERS = ["andatuzHabladorUp.png","andatuzHabladorLeft.png"]
PENGUINS_GIVERS = ["andatuzGenerosoUp.png","andatuzGenerosoLeft.png"]
PENGUINS_QUIZS = ["andatuzPreguntonUp.png","andatuzPreguntonLeft.png"]

ALL_PENGUINS = PENGUINS + PENGUINS_TALKERS + PENGUINS_GIVERS + PENGUINS_QUIZS

PENGUINS_GIF = KEYS + INVENTORYS 
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
  """ Returns a jump destination given a player heading and position, and room size.
  pos: player position.
  heading: player heading.
  size: room size.
  """  
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

def getSpriteName(state, heading, frame, timestamp):
  """ Returns a composed sprite file name created using a player and current timestamp.
  state: player's state.
  heading: player's heading.
  frame: frame number.
  timestamp: current system timestamp.
  """  
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
  if frame == 0:
    fileName = state + "_" + heading + "_00" + str(maxFrames)
  elif frame < 10:
    fileName = state + "_" + heading + "_000" + str(frame)
  else:  
    fileName = state + "_" + heading + "_00" + str(frame)
  return fileName + tail

def getNextDirection(pos1, pos2):
  """ Obtiene la siguiente posicion en el trayecto entre 2 puntos.
  pos1: posicion de inicio.
  pos2: posicion de destino.
  """
  retVar = "down"
  if pos1 == pos2:
    return None
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
    
def p2pDistance(point1, point2):
  """ Calculates the distance between 2 points.
  point1: starting point.
  point2: ending point.
  """
  if point1 == point2: 
    return 0
  return '%.3f' % math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[1] - point1[1]), 2))
    
def p3dToP2d(cord3d, anchor):
  """ Returns the physical 2d coordinates of a 3d virtual point.
  cord3d: 3d virtual point.
  anchor: point's anchor on screen.
  """
  corX2d = SCREEN_OR[0]
  corY2d = SCREEN_OR[1]
  corX2d += (cord3d[0]*(TILE_SZ[0]/2)) - (cord3d[1]*(TILE_SZ[1])) 
  corY2d += (cord3d[0]*(TILE_SZ[0]/4)) + (cord3d[1]*(TILE_SZ[1]/2)) 
  corX2d -= anchor[0]
  corY2d -= anchor[1]
  return corX2d, corY2d
 
def compare(x, y):
  """ Checks two images and compares their zOrder attribute values.
  x: first image.
  y: second image.
  """  
  return y.zOrder - x.zOrder

def createRecursiveDir(newdir):
  if os.path.isdir(newdir):
    pass
  elif os.path.isfile(newdir):
    raise OSError("Un fichero con el mismo nombre que el directorio , '%s', ya existe." % newdir)
  else:
    head, tail = os.path.split(newdir)
    if head and not os.path.isdir(head):
      createRecursiveDir(head)
    if tail:
      os.mkdir(newdir)

def clearCache(dir, limitTime):
  toRemove = []
  for fileName in os.listdir(dir):
    pathFile = os.path.join(dir, fileName) 
    if os.path.isdir(pathFile) and not pathFile in [DIR_ERROR, DIR_FONT, PATH_PHOTO_MASK, os.path.join(LOCAL_DATA_PATH, ".svn")]:
      clearCache(pathFile, limitTime)
    elif os.path.isfile(pathFile):
      accessTime = os.stat(pathFile)[stat.ST_ATIME]
      if accessTime < limitTime:
        toRemove.append(fileName)
  for fileName in toRemove:
    pathFile = os.path.join(dir, fileName) 
    os.remove(pathFile)
  #if len(os.listdir(dir)) == 0:
  #  os.rmdir(dir)

