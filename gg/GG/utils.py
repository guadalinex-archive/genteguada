import math
import os
import pygame

if os.path.isdir("gg/GG/data"):
  DATA_PATH = "gg/GG/data"
else:
  DATA_PATH = "/usr/share/pixmaps/genteguada-client"

VERSION = "GenteGuada 0.0.3.1"
TICK_DELAY = 0.1
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
CHAT_SZ = [400, 160]
CHAT_OR = [20, GAMEZONE_SZ[1]+20]
BG_FULL_OR = [0, 0]

ANIMATIONS = 5
MAX_FRAMES = 5
ANIM_DELAY = 0.2
SPEED = 55.901699437

BG_FULL = "fondo.png"
BG_FULL2 = "fondo2.png"
TILE_STONE = "tile_stone.png"
PLAYER_SPRITE1 = "black_mage.gif"
PLAYER_SPRITE2 = "black_mage_red.gif"
OAK_SPRITE = "oak.png"
NINO_SZ = [64, 100]
NINO_SPRITE = "nino.png"
NINA_SPRITE = "nina.png"
OBJ_BOOK_SPRITE1 = "book.png"
SIN30R = math.sin(math.radians(30))
COS30R = math.cos(math.radians(30))

HUD_COLOR_BASE = [177, 174, 200]
HUD_COLOR_BORDER1 = [104, 102, 119]
HUD_COLOR_BORDER2 = [138, 136, 160]
HUD_COLOR_BORDER3 = [202, 199, 231]
CHAT_COLOR_BG = [61, 61, 91]
CHAT_COLOR_FONT = [216, 216, 216]

HEADING = {0: "none", 1: "up", 2: "down", 3: "left", 4: "right",
           5: "topleft", 6: "bottomright", 7: "bottomleft", 8: "topright"}

STATE = {1: "standing", 2: "walking"}

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
