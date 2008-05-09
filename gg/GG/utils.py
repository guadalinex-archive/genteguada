import math
import os
import pygame

if os.path.isdir("gg/GG/data"):
  DATA_PATH = "gg/GG/data"
else:
  DATA_PATH = "/usr/share/pixmaps/genteguada"

VERSION = "GenteGuada 0.0.3.1"
TICK_DELAY = 0.1
#TILE_SZ = [100, 50]
TILE_SZ = [120, 60]
#TILE2TILE = 55.901699437
#tile2tile = math.sqrt(pow(TILE_SZ[0],2)+pow(TILE_SZ[1],2))
CHAR_SZ = [50, 50]
CHAR_POS = [0, 0, 0]
#SCREEN_SZ = [800, 600]
SCREEN_SZ = [1024, 768]
SCREEN_OR = [SCREEN_SZ[0]/2, 20]
#FLOOR_SHIFT = [50, -20]
FLOOR_SHIFT = [55, -30]
SCENE_SZ = [8, 8]
#GAMEZONE_SZ = [800, 400]
GAMEZONE_SZ = [1024, 568]
#HUD_SZ = [800, 200]
HUD_SZ = [1024, 200]
HUD_OR = [0, GAMEZONE_SZ[1]]
CHAT_SZ = [400, 120]
CHAT_OR = [20, GAMEZONE_SZ[1]+20]
TEXT_BOX_SZ = [400, 30]
TEXT_BOX_OR = [CHAT_OR[0], GAMEZONE_SZ[1]+CHAT_SZ[1]+30]
INV_OR = [40 + CHAT_SZ[0], GAMEZONE_SZ[1]+20]
INV_ITEM_SZ = [50, 50]
INV_ITEM_COUNT = [5, 3]
INV_SZ = [INV_ITEM_SZ[0]*INV_ITEM_COUNT[0], INV_ITEM_SZ[1]*INV_ITEM_COUNT[1]]
BG_FULL_OR = [0, 0]

ANIMATIONS = 5
MAX_FRAMES = 20
ANIM_DELAY = 0.05
SPEED = 55.901699437

BG_FULL = "fondo.png"
BG_FULL2 = "fondo2.png"
BG_BLACK = "black.png"
#TILE_STONE = "tile_stone.png"
TILE_STONE = "baldosaIsometricTile.tga"
TILE_WATER = "aguaIsometricTile.tga"
PLAYER_SPRITE1 = "black_mage.gif"
PLAYER_SPRITE2 = "black_mage_red.gif"
OAK_SPRITE = "oak.png"
PENGUIN_SPRITE = "andatuz_01.png"
NINO_SZ = [64, 100]
NINO_SPRITE = "nino_right.png"
NINA_SPRITE = "nina.png"
BOOK_SPRITE = "book.png"
BOOK_SPRITE_INV = "book.png"
DOOR_DOWN_SPRITE = "door_down.png"
SIN30R = math.sin(math.radians(30))
COS30R = math.cos(math.radians(30))

HUD_COLOR_BASE = [177, 174, 200]
HUD_COLOR_BORDER1 = [104, 102, 119]
HUD_COLOR_BORDER2 = [138, 136, 160]
HUD_COLOR_BORDER3 = [202, 199, 231]
CHAT_COLOR_BG = [61, 61, 91]
CHAT_COLOR_FONT = [216, 216, 216]
INV_COLOR_BG = [0, 0, 0]
TEXT_BOX_COLOR_BG = [255, 255, 255]

HEADING = {0: "none", 1: "up", 2: "down", 3: "left", 4: "right",
           5: "topleft", 6: "bottomright", 7: "bottomleft", 8: "topright"}

STATE = {1: "standing", 2: "walking"}

NINO_SPRITES = {"up": "nino_up.png", "down": "nino_down.png", "left": "nino_left.png",
                "right": "nino_right.png", "topleft": "nino_topleft.png", "bottomright": "nino_bottomright.png",
                "bottomleft": "nino_bottomleft.png", "topright": "nino_topright.png"}

NINA_SPRITES = {"up": "nina.png", "down": "nina.png", "left": "nina.png",
                "right": "nina.png", "topleft": "nina.png", "bottomright": "nina.png",
                "bottomleft": "nina.png", "topright": "nina.png"}

def getNextDirection(pos1, pos2):
  """ Obtiene la siguiente posicion en el trayecto entre 2 puntos.
  pos1: posicion de inicio.
  pos2: posicion de destino.
  """
  if pos1[0] < pos2[0]:
    if pos1[2] < pos2[2]:
      return "bottomright"
    elif pos1[2] > pos2[2]:
      return "topright"
    else:
      return "right"
  elif pos1[0] > pos2[0]:
    if pos1[2] < pos2[2]:
      return "bottomleft"
    elif pos1[2] > pos2[2]:
      return "topleft"
    else:
      return "left"
  elif pos1[0] == pos2[0]:
    if pos1[2] < pos2[2]:
      return "down" 
    elif pos1[2] > pos2[2]:
      return "up"
  return "down"

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
  if heading == "up" and pos[2] <> 0:
    return [pos[0], pos[1], pos[2] - 1]
  elif heading == "down" and pos[2] <> (SCENE_SZ[1] - 1):
    return [pos[0], pos[1], pos[2] + 1]
  elif heading == "left" and pos[0] <> 0:
    return [pos[0] - 1, pos[1], pos[2]]
  elif heading == "right" and pos[0] <> (SCENE_SZ[0] - 1):
    return [pos[0] + 1, pos[1], pos[2]]
  elif heading == "topleft" and pos[0] <> 0 and pos[2] <> 0:
    return [pos[0] - 1, pos[1], pos[2] - 1]
  elif heading == "bottomright" and pos[0] <> (SCENE_SZ[0] - 1) and pos[2] <> (SCENE_SZ[1] - 1):
    return [pos[0] + 1, pos[1], pos[2] + 1]
  elif heading == "bottomleft" and pos[0] <> 0 and pos[2] <> (SCENE_SZ[1] - 1):
    return [pos[0] - 1, pos[1], pos[2] + 1]
  elif heading == "topright" and pos[2] <> 0 and pos[0] <> (SCENE_SZ[0] - 1):
    return [pos[0] + 1, pos[1], pos[2] - 1]
  return [-1, -1, -1]
    
class TextRectException:
  
  def __init__(self, message = None):
    self.message = message
  def __str__(self):
    return self.message
      
def renderTextRect(string, font, rect, text_color, bgColor, justification=0):
  """Returns a surface containing the passed text string, reformatted
  to fit within the given rect, word-wrapping as necessary. The text
  will be anti-aliased.
  
  Takes the following arguments:
  string - the text you wish to render. \n begins a new line.
  font - a Font object
  rect - a rectstyle giving the size of the surface requested.
  text_color - a three-byte tuple of the rgb value of the
               text color. ex (0, 0, 0) = BLACK
  bgColor - a three-byte tuple of the rgb value of the surface.
  justification - 0 (default) left-justified
                  1 horizontally centered
                  2 right-justified

  Returns the following values:

  Success - a surface object with the text rendered onto it.
  Failure - raises a TextRectException if the text won't fit onto the surface.
  """
   
  finalLines = []
  requestedLines = string.splitlines()

  # Create a series of lines that will fit on the provided
  # rectangle.

  for requestedLine in requestedLines:
    if font.size(requestedLine)[0] > rect.width:
      words = requestedLine.split(' ')
      # if any of our words are too long to fit, return.
      for word in words:
        if font.size(word)[0] >= rect.width:
          raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
      # Start a new line
      accumulatedLine = ""
      for word in words:
        testLine = accumulatedLine + word + " "
        # Build the line while the words fit.    
        if font.size(testLine)[0] < rect.width:
          accumulatedLine = testLine
        else:
          finalLines.append(accumulatedLine)
          accumulatedLine = word + " "
      finalLines.append(accumulatedLine)
    else:
      finalLines.append(requestedLine)

  # Let's try to write the text out on the surface.

  surface = pygame.Surface(rect.size)
  surface.fill(bgColor)

  accumulatedHeight = 0
  for line in finalLines:
    if accumulatedHeight + font.size(line)[1] >= rect.height:
      raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
    if line != "":
      tempsurface = font.render(line, 1, text_color)
      if justification == 0:
        surface.blit(tempsurface, (0, accumulatedHeight))
      elif justification == 1:
        surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulatedHeight))
      elif justification == 2:
        surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulatedHeight))
      else:
        raise TextRectException, "Invalid justification argument: " + str(justification)
    accumulatedHeight += font.size(line)[1]

  return surface
