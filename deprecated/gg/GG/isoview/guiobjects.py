# -*- coding: utf-8 -*-

import ocempgui.widgets
import ocempgui.widgets.base
import ocempgui.draw
import GG.genteguada
import pygame
from PIL import Image
import stat
import os
import GG.utils
import pygame.locals
import copy

# ======================= STYLES ===========================

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
          "textFieldChat" : { "font" : { "name" : "Bitstream", "size" : 20, "alias" : True },
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
          "textFieldLogin" : { "font" : { "name" : "Bitstream", "size" : 36, "alias" : True },
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
          "labelLogin" : { "font" : { "name" : "Bitstream", "size" : 48, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                          }
                            },   
          "labelLoading" : { "font" : { "name" : "Bitstream", "size" : 72, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                          }
                            },   
          "labelWaiting" : { "font" : { "name" : "Bitstream", "size" : 36, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                          }
                            },   

          "chatEntryWhite" : { "font" : { "name" : "Bitstream", "size" : 20, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                          }
                            },
          "chatEntryRed" : { "font" : { "name" : "Bitstream", "size" : 20, "alias" : True },
                             "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (120, 30, 30),
                                           ocempgui.widgets.Constants.STATE_ENTERED      : (120, 30, 30),
                                           ocempgui.widgets.Constants.STATE_ACTIVE       : (120, 30, 30),
                                           ocempgui.widgets.Constants.STATE_INSENSITIVE  : (120, 30, 30) 
                                         }
                            },
          "chatEntryGreen" : { "font" : { "name" : "Bitstream", "size" : 20, "alias" : True },
                               "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (30, 120, 30),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (30, 120, 30),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (30, 120, 30),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (30, 120, 30) 
                                          }
                            },
          "chatEntryBlue" : { "font" : { "name" : "Bitstream", "size" : 20, "alias" : True },
                              "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (30, 30, 120),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (30, 30, 120),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (30, 30, 120),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (30, 30, 120) 
                                          }
                            },
          "chatBalloonWhite" : { "font" : { "name" : "Bitstream", "size" : 20, "alias" : True }, 
                                "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (255, 255, 255),
                                           ocempgui.widgets.Constants.STATE_ENTERED      : (255, 255, 255),
                                           ocempgui.widgets.Constants.STATE_ACTIVE       : (255, 255, 255),
                                           ocempgui.widgets.Constants.STATE_INSENSITIVE  : (255, 255, 255) 
                                         },
                                "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                          }
                            },
          "chatBalloonBlue" : {"font" : { "name" : "Bitstream", "size" : 20, "alias" : True }, 
                               "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (200, 200, 255),
                                           ocempgui.widgets.Constants.STATE_ENTERED      : (200, 200, 255),
                                           ocempgui.widgets.Constants.STATE_ACTIVE       : (200, 200, 255),
                                           ocempgui.widgets.Constants.STATE_INSENSITIVE  : (200, 200, 255) 
                                         },
                                "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                          }
                            },
          "chatBalloonGreen" : { "font" : { "name" : "Bitstream", "size" : 20, "alias" : True },
                                 "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (200, 255, 200),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (200, 255, 200),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (200, 255, 200),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (200, 255, 200) 
                                          },
                                "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                          }
                            },
          "chatBalloonRed" : {  "font" : { "name" : "Bitstream", "size" : 20, "alias" : True },
                                "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (255, 200, 200),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (255, 200, 200),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (255, 200, 200),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (255, 200, 200) 
                                          },
                                "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                          }
                            },
          "userName" : {  "font" : { "name" : "Bitstream", "size" : 20, "alias" : True },
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
          "pointLabel" : {  "font" : { "name" : "Bitstream", "size" : 16, "alias" : True },
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
          #antes del cambio de tipo de letra el size era 22
          "dialogFont" : {  "font" : { "name" : "Bitstream", "size" : 18, "alias" : True },
                                "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 74, 153),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 74, 153) 
                                            }
                            }, 
          "hudLabel" : {  "font" : { "name" : "Bitstream", "size" : 20, "alias" : True },
                                "fgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (0, 0, 0),
                                             ocempgui.widgets.Constants.STATE_ENTERED      : (0, 0, 0),
                                             ocempgui.widgets.Constants.STATE_ACTIVE       : (0, 0, 0),
                                             ocempgui.widgets.Constants.STATE_INSENSITIVE  : (0, 0, 0) 
                                            },
                                "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (107, 177, 197),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (107, 177, 197),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (107, 177, 197),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (107, 177, 197) 
                                          }
                            },                          
            "itemLabel" : { "font" : { "name" : "Bitstream", "size" : 22, "alias" : True },
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
          "teleportLabel" : { "font" : { "name" : "Bitstream", "size" : 16, "alias" : True },
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
          "exchangeLabel" : { "font" : { "name" : "Bitstream", "size" : 20, "alias" : True },
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
          "buttonBar" :     { "font" : { "name" : "Bitstream", "size" : 20, "alias" : True }, 
                             "bgcolor" : { ocempgui.widgets.Constants.STATE_NORMAL       : (97, 171, 193),
                                            ocempgui.widgets.Constants.STATE_ENTERED      : (97, 171, 193),
                                            ocempgui.widgets.Constants.STATE_ACTIVE       : (97, 171, 193),
                                            ocempgui.widgets.Constants.STATE_INSENSITIVE  : (97, 171, 193) 
                                          }
                            },
          "buttonTopBar" :     { "font" : { "name" : "Bitstream", "size" : 20, "alias" : True }, 
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
          #antes del cambio de tipo de fuente era el size 20
          "quizLabel" : { "font" : { "name" : "Bitstream", "size" : 16, "alias" : True },
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


class GroupSprite(pygame.sprite.Group):
  """ GroupSprite class.
  Redefines an OrderedUpdates sprite group class.
  """
  
  def __init__(self, *sprites):
    """ Constructor method.
    *sprites: sprites list.
    """
    pygame.sprite.Group.__init__(self, *sprites)
    self.__oldSprites = {}
  
  def sprites(self):
    """ Order the group sprites according to their position.
    """
    keys = self.spritedict.keys()
    keys.sort(lambda x, y : (x.zOrder - y.zOrder))
    return keys


class OcempPanel(ocempgui.widgets.Box):
  """ OcempPanel class.
  Redefines an ocempgui Box class as a panel.
  """ 

  def __init__(self, width, height, topleft, imageBackground):
    """ Class constructor.
    width: panel width.
    height: panel height.
    topleft: panel top left position.
    imageBackground: panel background image.
    """  
    ocempgui.widgets.Box.__init__(self, width, height)
    self.topleft = topleft
    self.set_style(ocempgui.widgets.WidgetStyle(STYLES["buttonTopBar"]))
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(imageBackground)
    imgBackground = OcempImageMapTransparent(filePath)
    imgBackground.topleft = 1, 1
    self.add_child(imgBackground)

  def isInside(self, pos):
    """ Checks if one point is inside the panel.
    pos: point cords.
    """  
    if (self.topleft[0] <= pos[0] <= (self.topleft[0] + self.width)): 
      if (self.topleft[1] <= pos[1] <= (self.topleft[1] + self.height)):
        return True
    return False


class OcempLabel(ocempgui.widgets.Label):
  """ OcempLabel class.
  Redefines an ocempgui label class.
  """ 

  def __init__(self, text, style):
    """ Class constructor.
    text: label text.
    style: label text style.
    """
    try:
      self.label = text.decode("utf-8")
    except:
      self.label = text
    self.typeFont = os.path.join(GG.utils.LOCAL_DATA_PATH, "font", "Domestic_Manners.ttf")
    self.sizeFont = style["font"]["size"]
    self.aliasFont = style["font"]["alias"]
    self.colorFont = style["fgcolor"][0]
    ocempgui.widgets.Label.__init__(self, self.label)
    
    self.set_align(ocempgui.widgets.Constants.ALIGN_LEFT | ocempgui.widgets.Constants.ALIGN_TOP)

  def update(self):
    """ Updates the label text.
    """  
    self.draw()

  def draw(self):
    """ Draws the label text.
    """  
    self._image = ocempgui.draw.String.draw_string (self.label, self.typeFont, self.sizeFont, self.aliasFont, self.colorFont)


class OcempLabelNotTransparent(ocempgui.widgets.Label):
  """ OcempLabelNotTransparent class.
  Redefines an ocempgui label class as a not transparent label.
  """ 

  def __init__(self, text, width):
    """ Class constructor.
    text: label text.
    style: label text style.
    """  
    line = ""  
    try:
      cad = text.decode("utf-8")
    except:
      cad = text
    width = width/4
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
    
    ocempgui.widgets.Label.__init__(self, line)
    self.multiline = True
    self.set_align(ocempgui.widgets.Constants.ALIGN_LEFT | ocempgui.widgets.Constants.ALIGN_TOP)


class OcempImageMapTransparent(ocempgui.widgets.ImageMap):
  """ OcempImageMapTransparent class.
  Redefines an ocempgui image map class as transparent.
  """ 

  def __init__(self, image):
    """ Class constructor.
    image: image file name.
    """  
    ocempgui.widgets.ImageMap.__init__(self, image)
  
  def draw (self):
    """ Draws the image on screen.
    """  
    self._image = self.picture
      

class OcempImageButtonTransparent(ocempgui.widgets.ImageButton):
  """ OcempImageButtonTransparent class.
  Redefines an ocempgui image button class as a transparent one.
  """ 

  def __init__(self, image, label = None, tooltipShow = None, tooltipRemove = None):
    """ Class constructor.
    image: image file name.
    label: button label.
    tooltipShow: method used to show button's tooltip.
    tooltipRemove: method used to hide button's tooltip.
    """
    ocempgui.widgets.ImageButton.__init__(self, image)
    if tooltipShow and label:
      self.connect_signal (ocempgui.widgets.Constants.SIG_ENTER, tooltipShow, label)
    if tooltipShow and label and tooltipRemove:
      self.connect_signal (ocempgui.widgets.Constants.SIG_LEAVE, tooltipRemove)
    
  def draw(self):
    """ Draws button on screen.
    """  
    ocempgui.widgets.ImageButton.draw(self)
    self._image = self.picture

  def update(self): 
    """ Updates button picture on screen.
    """  
    self.draw()
  

class OcempContactListItem(ocempgui.widgets.components.FileListItem):
  """ OcempContactListItem class.
  Redefines an ocempgui file list item as a contact list item.
  """ 

  def __init__(self, name, image):
    """ Class constructor.
    name: contact name.
    image: contact image name.
    """
    ocempgui.widgets.components.FileListItem.__init__(self, name.decode("utf-8"), 0)
    filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(image)
    size = 46, 31 
    try:
      if not image == "chatEntry.png":
        generateImageSize(filePath, size, os.path.join(GG.utils.LOCAL_DATA_PATH, "imageLabel", name))
    except:
      return 
    if not image == "chatEntry.png":
      filePath = os.path.join(GG.utils.LOCAL_DATA_PATH, "imageLabel", name)
    else:
      filePath = os.path.join(GG.utils.LOCAL_DATA_PATH, "chatEntry.png")
    self._icon = ocempgui.draw.Image.load_image(filePath).convert_alpha()
    

class OcempImageFileList(ocempgui.widgets.FileList):
  """ OcempImageFileList class.
  Redefines an ocempgui file list item as an image item.
  """ 
  
  def __init__(self, width, height):
    """ Class constructor.
    width: item width.
    height: item height.
    """  
    ocempgui.widgets.FileList.__init__(self, width, height)

  def _list_contents (self):
    """ Creates and lists all list contents.
    """  
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
          fileNameSegment, ext = os.path.splitext(filename)
          if ext in [".jpg", ".JPG", ".png", ".PNG"]: 
            fappend (filename)
    dirs.sort ()
    files.sort ()
        
    map (items.append, [ocempgui.widgets.components.FileListItem (d, stat.S_IFDIR) for d in dirs])
    for filename in files:
      stats = os.stat (pjoin (self._directory, filename))
      items.append (ocempgui.widgets.components.FileListItem (filename, stats.st_mode))
    self.set_items (items)

  def getFileName(self):
    """ Returns the file name of the selected item.
    """  
    item = self.get_selected()
    if len(item):
      fileName = os.path.join (self.directory, item[0].text)
      if os.path.isfile(fileName):
        return fileName
    return None

  
class OcempImageContactList(OcempImageFileList):
  """ OcempImageContactList class.
  Defines a contact list composed by images & text.
  """  
  
  def __init__(self, width, height, contactList):
    """ Class constructor.
    width: list width.
    height: list height.
    contactList: contacts to be included on the list.
    """  
    self.contactList = contactList
    OcempImageFileList.__init__(self, width, height)

  def _list_contents (self):
    """ Creates and lists all list contacts.
    """  
    items = ocempgui.widgets.components.ListItemCollection ()
    for contact in self.contactList:
      items.append (OcempContactListItem (contact.getPlayer(), contact.getImageLabel()))
    self.set_items (items)

  def setContacts(self, agenda):
    """ Sets a new contact list.
    agenda: new contact list.
    """  
    self.contactList = agenda  
    items = ocempgui.widgets.components.ListItemCollection ()
    for contact in agenda.keys():
      items.append (OcempContactListItem (contact, agenda[contact]))
    self.set_items (items)

  def getSelectedName(self):
    """ Returns the name of the selected item.
    """  
    item = self.get_selected()
    if len(item):
      return item[0].text
    return None

  def addMessageHintForContact(self, contact):
    """ Adds a "message received" hin on a given contact.
    contact: message sender.
    """
    for item in self.items:
      if item.text.find(contact.username) > -1:
        if item.text.find(" ") == -1:
          item.text = item.text + " (*)"
          return
        
  def restoreContactName(self):
    """ Restores and removes the "message received" hint from selected contact.
    """  
    item = self.get_selected()
    if len(item):
      cad = item[0].text
      cad = cad[0:cad.find(" ")]
      item[0].text = cad

  def updateMaskPlayer(self, name, image):
    """ Updates a player's mask.
    name: player's name.
    image: mask image name.
    """  
    for item in self.items:
      if item.text.find(name) > -1:
        filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(image)
        size = 46, 31 
        try:
          generateImageSize(filePath, [46, 31], os.path.join(GG.utils.LOCAL_DATA_PATH, name))
        except:
          return 
        filePath = os.path.join(GG.utils.LOCAL_DATA_PATH, name)
        item._icon = ocempgui.draw.Image.load_image(filePath).convert_alpha()
        
  
class OcempImageObjectList(OcempImageFileList):
  """ OcempImageObjectList class.
  Defines an image object list.
  """ 
  
  def __init__(self, width, height, objectLabelList):
    """ Class constructor.
    width: list width.
    height: list width.
    objectLabelList: items label list.
    """  
    self.objectLabelList = objectLabelList
    OcempImageFileList.__init__(self, width, height)

  def _list_contents (self):
    """ Creates the list items.
    """  
    items = ocempgui.widgets.components.ListItemCollection ()
    self.objectLabelList.sort()
    for objectLabel in self.objectLabelList:
      items.append (OcempContactListItem (objectLabel, "chatEntry.png"))
    self.set_items (items)

  def getSelectedName(self):
    """ Returns the selected item's name.
    """  
    item = self.get_selected()
    if len(item):
      return item[0].text
    return None

  def selectItem(self, itemName):
    """ Selects a single item.
    itemName: item name.
    """  
    for item in self.items:
      if item.text == itemName:
        prevSelected = self.get_selected()
        if len(prevSelected):
          self._set_cursor(prevSelected[0], False)
        self._set_cursor(item, True)
        
  
class OcempImageList(OcempImageFileList):
  """ OcempImageList class.
  Defines an image list.
  """
  
  def __init__(self, width, height, imagesList, relativePath, otherPath= None):
    """ Class constructor.
    width: list width.
    height: list height.
    imagesList: images to be included on the list.
    relativePath: images path.
    """  
    self.imagesList = imagesList
    self.relativePath = relativePath
    self.otherPath = otherPath
    self.set_selectionmode(ocempgui.widgets.Constants.SELECTION_SINGLE)
    OcempImageFileList.__init__(self, width, height)
    
  def _list_contents (self):
    """ Creates the list items.
    """  
    items = ocempgui.widgets.components.ListItemCollection()
    for image in self.imagesList:
      if self.otherPath is not None:
        if os.path.isfile(os.path.join(GG.utils.DATA_PATH,self.otherPath, image)):
          items.append (OcempContactListItem (image, os.path.join(self.otherPath, image)))
        else:
          items.append (OcempContactListItem (image, os.path.join(self.relativePath, image)))
      else:
        items.append (OcempContactListItem (image, os.path.join(self.relativePath, image)))
    self.set_items (items)
    
  def getImagesList(self):
    """ Returns the image name list.
    """  
    return self.imagesList  

  def getSelectedName(self):
    """ Returns the selected item's name.
    """  
    item = self.get_selected()
    if len(item):
      return item[0].text
    return None

  def getSelectedNames(self):
    """ Returns the selected items names.
    """  
    retList = []
    items = self.get_selected()
    for singleItem in items:
      retList.append(singleItem.text)
    return retList

  def selectItem(self, itemName):
    """ Selects a single item.
    itemName: item name.
    """  
    for item in self.items:
      if item.text == itemName:
        prevSelected = self.get_selected()
        if len(prevSelected):
          self._set_cursor(prevSelected[0], False)
        self._set_cursor(item, True)
        return
  
  def selectItems(self, imgNames):
    """ Selects various item.
    itemName: item name.
    """  
    prevSelected = self.get_selected()
    for item in prevSelected:
      self._set_cursor(item, False)
    for item in self.items:
      if item.text in imgNames:
        self._set_cursor(item, True)


class OcempEditLine(ocempgui.widgets.Entry):
  """ OcempEditLine class.
  Redefines an ocempgui entry object as an edit line object.
  """  

  def __init__(self, text = ""):
    """ Class constructor.
    text: entry line initial text.
    """  
    ocempgui.widgets.Entry.__init__(self, text)

  def _input (self, event):
    """ Handles the events on the entry line.
    event: event info.
    """  
    handled = False
    if event.key == pygame.locals.K_ESCAPE:
      if self.editable:
        self._text = self._temp # Undo text input.
        self.run_signal_handlers (ocempgui.widgets.Constants.SIG_INPUT)
      handled = True
    elif event.key in (pygame.locals.K_RETURN, pygame.locals.K_KP_ENTER):
      if self.editable:
        self._temp = self.text
        self.run_signal_handlers (ocempgui.widgets.Constants.SIG_INPUT)
      handled = True
    # Move caret right and left on the corresponding key press.
    elif event.key == pygame.locals.K_RIGHT:
      if self._caret < len (self._text):
        self._caret += 1
      handled = True
    elif event.key == pygame.locals.K_LEFT:
      if self._caret > 0:
        self._caret -= 1
      handled = True
    # Go the start (home) of the text.
    elif event.key == pygame.locals.K_HOME:
      self._caret = 0
      handled = True
    # Go to the end (end) of the text.
    elif event.key == pygame.locals.K_END:
      self._caret = len (self._text)
      handled = True
    # The next statements directly influence the text, thus we have
    # to check, if it is editable or not.
    elif self.editable:
      # Delete at the position (delete).
      if event.key == pygame.locals.K_DELETE:
        if self._caret < len (self._text):
          self._text = self._text[:self._caret] + self._text[self._caret + 1:]
        handled = True
      # Delete backwards (backspace).
      elif event.key == pygame.locals.K_BACKSPACE:
        if self._caret > 0:
          self._text = self._text[:self._caret - 1] + self._text[self._caret:]
          self._caret -= 1
        handled = True
      # Non-printable characters or maximum exceeded.
      elif (len (event.unicode) == 0) or (ord (event.unicode) < 32):
        # Any unicode character smaller than 0x0020 (32, SPC) is
        # ignored as those are control sequences.
        return False
      # Any other case is okay, so show it.
      else:
        self._text = self._text[:self._caret] + event.unicode.encode("iso-8859-15") + self._text[self._caret:]
        #self._text = self._text[:self._caret] + event.unicode + self._text[self._caret:]
        self._caret += 1
      handled = True
    self.dirty = True
    return handled

# ===============================================================
# =========================== METHODS ===========================
# ===============================================================

def createButton(imgPath, topleft, tooltip, action, *params):
  """ Creates a transparent button.
  topleft: button topleft cords.
  tooltip: button tooltip.
  action: button triggered action after being pushed.
  params: button action params.
  """  
  imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath)
  if tooltip:
    button = OcempImageButtonTransparent(imgPath, tooltip[0], tooltip[1], tooltip[2])
  else:
    button = OcempImageButtonTransparent(imgPath)
  button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, action, *params)
  button.topleft = topleft
  return button

def generateImageSize(origFilePath, size, destFilePath):
  """ Copies and resizes an image.
  origFilePath: original image path.
  size: image name.
  destFilePath: image copy path.
  """  
  if not os.path.isdir(os.path.dirname(destFilePath)):
    GG.utils.createRecursiveDir(os.path.dirname(destFilePath))
  img = Image.open(origFilePath)
  img.thumbnail(size, Image.ANTIALIAS)
  img.save(destFilePath)

def playSound(sound):
  """ Plays a sound.
  sound: sound file name.
  """  
  sndPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.SOUND_PATH, sound))
  if not os.path.isfile(sndPath) or sndPath == GG.utils.IMG_ERROR:
    return False
  try:
    if not pygame.mixer.get_busy():
      pygame.mixer.music.load(sndPath)
      pygame.mixer.music.play()
  except:
    pass

def getSprite(imageName, topleft = None, zOrder = None):
  """ Loads a new sprite.
  imageName: sprite file name.
  loadRect: rectangle load flag.
  topleft: new sprite topleft.
  zOrder: sprite zOrder value.
  """  
  image = pygame.sprite.Sprite()
  imageFile = GG.genteguada.GenteGuada.getInstance().getDataPath(imageName)
  image.image = pygame.image.load(imageFile).convert_alpha()
  image.rect = image.image.get_rect()
  if topleft:
    image.rect.topleft = topleft
  if zOrder:
    image.zOrder = zOrder
  else:
    image.zOrder = 0    
  return image  

def getOffset(imageFile):
  im = Image.open(imageFile)
  sizeImage = im.size
  if sizeImage[0] > GG.utils.TILE_SZ[0]:
    offsetX = GG.utils.FLOOR_SHIFT[0] + ((sizeImage[0] - GG.utils.TILE_SZ[0]) / 2)
  else:
    offsetX = GG.utils.FLOOR_SHIFT[0]
  if sizeImage[1] > GG.utils.TILE_SZ[1]:
    offsetY = sizeImage[1] - GG.utils.TILE_SZ[1] + GG.utils.FLOOR_SHIFT[1]
  else:
    offsetY = GG.utils.FLOOR_SHIFT[1]
  return [offsetX, offsetY]

def getTopOffset(anchor ,imageFile):
  try:
    yTopOffset = GG.utils.STACKS_TOPANCHOR[os.path.split(imageFile)[-1]]
  except:
    yTopOffset = 0
  yTopAnchor = GG.utils.TILE_SZ[1] + anchor[1] + yTopOffset
  return [0,yTopAnchor]

def isInside(window, pos):
  if (window.topleft[0] <= pos[0] <= (window.topleft[0] + window.width)): 
    if (window.topleft[1] <= pos[1] <= (window.topleft[1] + window.height)):
      return True
  return False

