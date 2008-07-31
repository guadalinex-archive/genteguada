import ocempgui.widgets
import ocempgui.widgets.base
import ocempgui.draw
import GG.genteguada
import pygame
from PIL import Image
import stat
import os
import GG.utils

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

# ===============================================================

class OcempLabel(ocempgui.widgets.Label):

  def __init__(self, text, width, style):
    """
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
    """
    self.label = text
    #self.typeFont = "Bitstream"
    self.typeFont = GG.utils.LOCAL_DATA_PATH+"/font/Domestic_Manners.ttf"
    self.sizeFont = style["font"]["size"]
    self.aliasFont = style["font"]["alias"]
    self.colorFont = style["fgcolor"][0]
    ocempgui.widgets.Label.__init__(self, self.label)
    
    self.multiline = True
    self.set_align(ocempgui.widgets.Constants.ALIGN_LEFT | ocempgui.widgets.Constants.ALIGN_TOP)

  def update(self):
    self.draw()

  def draw(self):
    #self._image = ocempgui.draw.String.draw_string (self.label, self.typeFont, self.sizeFont, self.aliasFont, self.colorFont, ocempgui.draw.Constants.FONT_STYLE_BOLD)
    self._image = ocempgui.draw.String.draw_string (self.label, self.typeFont, self.sizeFont, self.aliasFont, self.colorFont)

# ===============================================================

class OcempLabelNotTransparent(ocempgui.widgets.Label):

  def __init__(self, text, width):
    line = ""  
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
    
    ocempgui.widgets.Label.__init__(self,line)
    self.multiline = True
    self.set_align(ocempgui.widgets.Constants.ALIGN_LEFT | ocempgui.widgets.Constants.ALIGN_TOP)

# ===============================================================

class OcempImageMapTransparent(ocempgui.widgets.ImageMap):

  def __init__(self, image):
    ocempgui.widgets.ImageMap.__init__(self, image)
  
  def draw (self):
    self._image = self.picture
      
# ===============================================================

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
  
# ===============================================================

class OcempContactListItem(ocempgui.widgets.components.FileListItem):

  def __init__(self, name, image):
    ocempgui.widgets.components.FileListItem.__init__(self, name, 0)
    filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(image)
    path, file = os.path.split(filePath)
    size = 46,31 
    try:
      img = Image.open(filePath)
    except:
      return 
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(os.path.join(GG.utils.LOCAL_DATA_PATH,"imageLabel"+name+".png"))
    filePath = os.path.join(GG.utils.LOCAL_DATA_PATH,"imageLabel"+name+".png")
    self._icon = ocempgui.draw.Image.load_image(filePath)
    
# ===============================================================

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

# ===============================================================
  
class OcempImageContactList(OcempImageFileList):
  
  def __init__(self, width, height, contactList):
    self.contactList = contactList
    OcempImageFileList.__init__(self, width, height)

  def _list_contents (self):
    items = ocempgui.widgets.components.ListItemCollection ()
    for contact in self.contactList:
      player = contact.getPlayer()
      items.append (OcempContactListItem (player.username, player.getImageLabel()))
    self.set_items (items)

  def setContacts(self, agenda):
    self.contactList = agenda  
    items = ocempgui.widgets.components.ListItemCollection ()
    for contact in agenda.keys():
      items.append (OcempContactListItem (contact, agenda[contact]))
    self.set_items (items)

  def getSelectedName(self):
    item = self.get_selected()
    if len(item):
      return item[0].text
    return None

  def addMessageHintForContact(self, contact):
    for item in self.items:
      if item.text.find(contact.username) > -1:
        if item.text.find(" ") == -1:
          item.text = item.text + " (*)"
          return
        
  def restoreContactName(self):
    item = self.get_selected()
    if len(item):
      cad = item[0].text
      cad = cad[0:cad.find(" ")]
      item[0].text = cad

  def updateMaskPlayer(self, name, image):
    print "voy a buscar a name"
    for item in self.items:
      print item.text
      if item.text.find(name) > -1:
        print "Lo encontre "+name
        filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(image)
        path, file = os.path.split(filePath)
        size = 46,31 
        try:
          img = Image.open(filePath)
        except:
          return 
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(os.path.join(LOCAL_DATA_PATH,"imageLabel"+name+".png"))
        filePath = os.path.join(LOCAL_DATA_PATH,"imageLabel"+name+".png")
        item._icon = ocempgui.draw.Image.load_image(filePath)
        
# ===============================================================
  
class OcempImageObjectList(OcempImageFileList):
  
  def __init__(self, width, height, objectLabelList):
    self.objectLabelList = objectLabelList
    OcempImageFileList.__init__(self, width, height)

  def _list_contents (self):
    items = ocempgui.widgets.components.ListItemCollection ()
    for objectLabel in self.objectLabelList:
      items.append (OcempContactListItem (objectLabel, "chatEntry.png"))
    self.set_items (items)

  def getSelectedName(self):
    item = self.get_selected()
    if len(item):
      return item[0].text
    return None

# ===============================================================
  
class OcempImageList(OcempImageFileList):
  
  def __init__(self, width, height, imagesList):
    self.imagesList = imagesList
    OcempImageFileList.__init__(self, width, height)

  def _list_contents (self):
    items = ocempgui.widgets.components.ListItemCollection ()
    for image in self.imagesList:
      items.append (OcempContactListItem (image, "furniture/" + image))
    self.set_items (items)

  def getSelectedName(self):
    item = self.get_selected()
    if len(item):
      return item[0].text
    return None
    
# ===============================================================

def playSound(sound):
  sndPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.SOUND_PATH, sound))
  if not os.path.isfile(sndPath):
    return False
  if not pygame.mixer.get_busy():
    pygame.mixer.music.load(sndPath)
    pygame.mixer.music.play()

