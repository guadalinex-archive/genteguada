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

def generateImageSize(origFilePath, size, destFilePath):
  img = Image.open(origFilePath)
  img.thumbnail(size, Image.ANTIALIAS)
  img.save(destFilePath)




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

# ===============================================================
# ===============================================================
# ===============================================================

class LayeredUpdates(pygame.sprite.AbstractGroup):
    """LayeredUpdates Group handles layers, that draws like OrderedUpdates.
    pygame.sprite.LayeredUpdates(*spites, **kwargs): return LayeredUpdates
    
    This group is fully compatible with pygame.sprite.Sprite.

    New in pygame 1.8.0
    """
    
    def __init__(self, *sprites, **kwargs):
        """
        You can set the default layer through kwargs using 'default_layer'
        and an integer for the layer. The default layer is 0.
        
        If the sprite you add has an attribute layer then that layer will
        be used.
        If the **kwarg contains 'layer' then the sprites passed will be 
        added to that layer (overriding the sprite.layer attribute).
        If neither sprite has attribute layer nor kwarg then the default
        layer is used to add the sprites.
        """
        self._spritelayers = {}
        self._spritelist = []
        pygame.sprite.AbstractGroup.__init__(self)
        if kwargs.has_key('default_layer'):
            self._default_layer = kwargs['default_layer']
        else:
            self._default_layer = 0
            
        self.add(*sprites, **kwargs)
    
    def add_internal(self, sprite, layer=None):
        """
        Do not use this method directly. It is used by the group to add a
        sprite internally.
        """
        self.spritedict[sprite] = pygame.Rect(0, 0, 0, 0) # add a old rect
        
        if layer is None:
            if hasattr(sprite, '_layer'):
                layer = sprite._layer
            else:
                layer = self._default_layer
                
                
        self._spritelayers[sprite] = layer
        if hasattr(sprite, '_layer'):
            sprite._layer = layer
    
        # add the sprite at the right position
        # bisect algorithmus
        sprites = self._spritelist # speedup
        sprites_layers = self._spritelayers
        leng = len(sprites)
        low = 0
        high = leng-1
        mid = low
        while(low<=high):
            mid = low + (high-low)/2
            if(sprites_layers[sprites[mid]]<=layer):
                low = mid+1
            else:
                high = mid-1
        # linear search to find final position
        while(mid<leng and sprites_layers[sprites[mid]]<=layer):
            mid += 1
        sprites.insert(mid, sprite)
        
    def add(self, *sprites, **kwargs):
        """add a sprite or sequence of sprites to a group
        LayeredUpdates.add(*sprites, **kwargs): return None

        If the sprite(s) have an attribute layer then that is used 
        for the layer. If kwargs contains 'layer' then the sprite(s) 
        will be added to that argument (overriding the sprite layer 
        attribute). If neither is passed then the sprite(s) will be
        added to the default layer.
        """
        layer = None
        if kwargs.has_key('layer'):
            layer = kwargs['layer']
        if sprites is None or len(sprites)==0:
            return
        for sprite in sprites:
            # It's possible that some sprite is also an iterator.
            # If this is the case, we should add the sprite itself,
            # and not the objects it iterates over.
            if isinstance(sprite, pygame.sprite.Sprite):
                if not self.has_internal(sprite):
                    self.add_internal(sprite, layer)
                    sprite.add_internal(self)
            else:
                try:
                    # See if sprite is an iterator, like a list or sprite
                    # group.
                    for spr in sprite:
                        self.add(spr, **kwargs)
                except (TypeError, AttributeError):
                    # Not iterable, this is probably a sprite that happens
                    # to not subclass Sprite. Alternately, it could be an
                    # old-style sprite group.
                    if hasattr(sprite, '_spritegroup'):
                        #for spr in sprite.sprites():
                        for spr in self.sprites():
                            if not self.has_internal(spr):
                                self.add_internal(spr, layer)
                                spr.add_internal(self)
                    elif not self.has_internal(sprite):
                        self.add_internal(sprite, layer)
                        sprite.add_internal(self)
    
    def remove_internal(self, sprite):
        """
        Do not use this method directly. It is used by the group to 
        add a sprite.
        """
        self._spritelist.remove(sprite)
        # these dirty rects are suboptimal for one frame
        self.lostsprites.append(self.spritedict[sprite]) # dirty rect
        if hasattr(sprite, 'rect'):
            self.lostsprites.append(sprite.rect) # dirty rect
        
        self.spritedict.pop(sprite, 0)
        self._spritelayers.pop(sprite)
    
    """
    def sprites(self):
        return list(self._spritelist)
    """
    
    def sprites(self):
        """ Order the group sprites according to their position.
        """
        #keys = list(self._spritelist).keys()
        keys = self.spritedict.keys()
        keys.sort(lambda x, y : (x.zOrder - y.zOrder))
        return keys
    
    def draw(self, surface):
        """draw all sprites in the right order onto the passed surface.
        LayeredUpdates.draw(surface): return Rect_list
        """
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        #for spr in self.sprites():
        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect)
            if rec is 0:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty

    def get_sprites_at(self, pos):
        """returns a list with all sprites at that position.
        LayeredUpdates.get_sprites_at(pos): return colliding_sprites

        Bottom sprites first, top last.
        """
        _sprites = self._spritelist
        rect = Rect(pos, (0, 0))
        colliding_idx = rect.collidelistall(_sprites)
        colliding = []
        colliding_append = colliding.append
        for i in colliding_idx:
            colliding_append(_sprites[i])
        return colliding

    def get_sprite(self, idx):
        """returns the sprite at the index idx from the groups sprites
        LayeredUpdates.get_sprite(idx): return sprite

        Raises IndexOutOfBounds if the idx is not within range.
        """
        return self._spritelist[idx]
    
    def remove_sprites_of_layer(self, layer_nr):
        """removes all sprites from a layer and returns them as a list
        LayeredUpdates.remove_sprites_of_layer(layer_nr): return sprites
        """
        sprites = self.get_sprites_from_layer(layer_nr)
        self.remove(sprites)
        return sprites
        

    #---# layer methods
    def layers(self):
        """returns a list of layers defined (unique), sorted from botton up.
        LayeredUpdates.layers(): return layers
        """
        layers = set()
        for layer in self._spritelayers.values():
            layers.add(layer)
        return list(layers)

    def change_layer(self, sprite, new_layer):
        """changes the layer of the sprite
        LayeredUpdates.change_layer(sprite, new_layer): return None

        sprite must have been added to the renderer. It is not checked.
        """
        sprites = self._spritelist # speedup
        sprites_layers = self._spritelayers # speedup
        
        sprites.remove(sprite) 
        sprites_layers.pop(sprite)
        
        # add the sprite at the right position
        # bisect algorithmus
        leng = len(sprites)
        low = 0
        high = leng-1
        mid = low
        while(low<=high):
            mid = low + (high-low)/2
            if(sprites_layers[sprites[mid]]<=new_layer):
                low = mid+1
            else:
                high = mid-1
        # linear search to find final position
        while(mid<leng and sprites_layers[sprites[mid]]<=new_layer):
            mid += 1
        sprites.insert(mid, sprite)
        if hasattr(sprite, 'layer'):
            sprite.layer = new_layer
        
        # add layer info
        sprites_layers[sprite] = new_layer
            
    def get_layer_of_sprite(self, sprite):
        """
        Returns the layer that sprite is currently in. If the sprite is not 
        found then it will return the default layer.
        """
        return self._spritelayers.get(sprite, self._default_layer)
    
    def get_top_layer(self):
        """returns the top layer
        LayeredUpdates.get_top_layer(): return layer
        """
        return self._spritelayers[self._spritelist[-1]]
    
    def get_bottom_layer(self):
        """returns the bottom layer
        LayeredUpdates.get_bottom_layer(): return layer
        """
        return self._spritelayers[self._spritelist[0]]
    
    def move_to_front(self, sprite):
        """brings the sprite to front layer
        LayeredUpdates.move_to_front(sprite): return None

        Brings the sprite to front, changing sprite layer to topmost layer
        (added at the end of that layer).
        """
        self.change_layer(sprite, self.get_top_layer())
        
    def move_to_back(self, sprite):
        """moves the sprite to the bottom layer
        LayeredUpdates.move_to_back(sprite): return None

        Moves the sprite to the bottom layer, moving it behind
        all other layers and adding one additional layer.
        """
        self.change_layer(sprite, self.get_bottom_layer()-1)
        
    def get_top_sprite(self):
        """returns the topmost sprite
        LayeredUpdates.get_top_sprite(): return Sprite
        """
        return self._spritelist[-1]
    
    def get_sprites_from_layer(self, layer):
        """returns all sprites from a layer, ordered by how they where added
        LayeredUpdates.get_sprites_from_layer(layer): return sprites

        Returns all sprites from a layer, ordered by how they where added.
        It uses linear search and the sprites are not removed from layer.
        """
        sprites = []
        sprites_append = sprites.append
        sprite_layers = self._spritelayers
        for spr in self._spritelist:
            if sprite_layers[spr] == layer: 
                sprites_append(spr)
            elif sprite_layers[spr]>layer:# break after because no other will 
                                          # follow with same layer
                break
        return sprites
        
    def switch_layer(self, layer1_nr, layer2_nr):
        """switches the sprites from layer1 to layer2
        LayeredUpdates.switch_layer(layer1_nr, layer2_nr): return None

        The layers number must exist, it is not checked.
        """
        sprites1 = self.remove_sprites_of_layer(layer1_nr)
        for spr in self.get_sprites_from_layer(layer2_nr):
            self.change_layer(spr, layer1_nr)
        self.add(sprites1, layer=layer2_nr)
        
# ===============================================================

class LayeredDirty(LayeredUpdates):
    """LayeredDirty Group is for DirtySprites.  Subclasses LayeredUpdates.
    pygame.sprite.LayeredDirty(*spites, **kwargs): return LayeredDirty
        
    This group requires pygame.sprite.DirtySprite or any sprite that 
    has the following attributes: 
        image, rect, dirty, visible, blendmode (see doc of DirtySprite).

    It uses the dirty flag technique and is therefore faster than the 
    pygame.sprite.RenderUpdates if you have many static sprites.  It 
    also switches automatically between dirty rect update and full 
    screen drawing, so you do no have to worry what would be faster.

    Same as for the pygame.sprite.Group.
    You can specify some additional attributes through kwargs:
        _use_update: True/False   default is False
        _default_layer: default layer where sprites without a layer are added.
        _time_threshold: treshold time for switching between dirty rect mode 
            and fullscreen mode, defaults to 1000./80  == 1000./fps

    New in pygame 1.8.0
    """
    
    def __init__(self, *sprites, **kwargs):
        """Same as for the pygame.sprite.Group.
        pygame.sprite.LayeredDirty(*spites, **kwargs): return LayeredDirty

        You can specify some additional attributes through kwargs:
        _use_update: True/False   default is False
        _default_layer: the default layer where the sprites without a layer are
                        added.
        _time_threshold: treshold time for switching between dirty rect mode and
                        fullscreen mode, defaults to 1000./80  == 1000./fps
        """
        LayeredUpdates.__init__(self, *sprites, **kwargs)
        self._clip = None
        
        self._use_update = False
        
        self._time_threshold = 1000./80. # 1000./ fps
        
        
        self._bgd = None
        for key, val in kwargs.items():
            if key in ['_use_update', '_time_threshold', '_default_layer']:
                if hasattr(self, key):
                    setattr(self, key, val)

    def add_internal(self, sprite, layer=None):
        """Do not use this method directly. It is used by the group to add a
        sprite internally.
        """
        sprite.dirty = 1
        sprite.blendmode = 0
        sprite.source_rect = None
        sprite.visible = 1
        sprite._visible = 1
        sprite.layer = 0
        
        # check if all attributes needed are set
        if not hasattr(sprite, 'dirty'):
            raise AttributeError()
        if not hasattr(sprite, "visible"):
            raise AttributeError()
        if not hasattr(sprite, "blendmode"):
            raise AttributeError()
        
        #if not isinstance(sprite, DirtySprite):
        #    raise TypeError()
        
        if sprite.dirty == 0: # set it dirty if it is not
            sprite.dirty = 1
        
        LayeredUpdates.add_internal(self, sprite, layer)
        
    def draw(self, surface, bgd=None):
        """draw all sprites in the right order onto the passed surface.
        LayeredDirty.draw(surface, bgd=None): return Rect_list

        You can pass the background too. If a background is already set, 
        then the bgd argument has no effect.
        """
        # speedups
        _orig_clip = surface.get_clip()
        _clip = self._clip
        if _clip is None:
            _clip = _orig_clip
                
        _surf = surface
        
        _sprites = LayeredUpdates.sprites(self)
        #_sprites = self._spritelist
        _old_rect = self.spritedict
        _update = self.lostsprites
        _update_append = _update.append
        _ret = None
        _surf_blit = _surf.blit
        _rect = pygame.Rect
        if bgd is not None:
            self._bgd = bgd
        _bgd = self._bgd
        
        _surf.set_clip(_clip)
        # -------
        # 0. deside if normal render of flip
        start_time = pygame.time.get_ticks()
        if self._use_update: # dirty rects mode
            # 1. find dirty area on screen and put the rects into _update
            # still not happy with that part
            for spr in _sprites:
                if 0 < spr.dirty:
                    # chose the right rect
                    if spr.source_rect:
                        _union_rect = _rect(spr.rect.topleft, spr.source_rect.size)
                    else:
                        _union_rect = _rect(spr.rect)
                        
                    _union_rect_collidelist = _union_rect.collidelist
                    _union_rect_union_ip = _union_rect.union_ip
                    i = _union_rect_collidelist(_update)
                    while -1 < i:
                        _union_rect_union_ip(_update[i])
                        del _update[i]
                        i = _union_rect_collidelist(_update)
                    _update_append(_union_rect.clip(_clip))
                    
                    _union_rect = _rect(_old_rect[spr])
                    _union_rect_collidelist = _union_rect.collidelist
                    _union_rect_union_ip = _union_rect.union_ip
                    i = _union_rect_collidelist(_update)
                    while -1 < i:
                        _union_rect_union_ip(_update[i])
                        del _update[i]
                        i = _union_rect_collidelist(_update)
                    _update_append(_union_rect.clip(_clip))
            # can it be done better? because that is an O(n**2) algorithm in
            # worst case
                    
            # clear using background
            if _bgd is not None:
                for rec in _update:
                    _surf_blit(_bgd, rec, rec)
                
            # 2. draw
            for spr in _sprites:
                if 1 > spr.dirty:
                    if spr._visible:
                        # sprite not dirty, blit only the intersecting part
                        _spr_rect = spr.rect
                        if spr.source_rect is not None:
                            _spr_rect = Rect(spr.rect.topleft, spr.source_rect.size)
                        _spr_rect_clip = _spr_rect.clip
                        for idx in _spr_rect.collidelistall(_update):
                            # clip
                            clip = _spr_rect_clip(_update[idx])
                            _surf_blit(spr.image, clip, \
                                       (clip[0]-_spr_rect[0], \
                                            clip[1]-_spr_rect[1], \
                                            clip[2], \
                                            clip[3]))
                else: # dirty sprite
                    if spr._visible:
                        _old_rect[spr] = _surf_blit(spr.image, spr.rect)
                    if spr.dirty == 1:
                        spr.dirty = 0
            _ret = list(_update)
        else: # flip, full screen mode
            if _bgd is not None:
                _surf_blit(_bgd, (0, 0))
            for spr in _sprites:
                if spr._visible:
                    #_old_rect[spr] = _surf_blit(spr.image, spr.rect, spr.source_rect, spr.blendmode)
                    _old_rect[spr] = _surf_blit(spr.image, spr.rect)
            _ret = [_rect(_clip)] # return only the part of the screen changed
            
        
        # timing for switching modes
        # how to find a good treshold? it depends on the hardware it runs on
        end_time = pygame.time.get_ticks()
        if end_time-start_time > self._time_threshold:
            self._use_update = False
        else:
            self._use_update = True
            
##        # debug
##        print "               check: using dirty rects:", self._use_update
            
        # emtpy dirty reas list
        _update[:] = []
        
        # -------
        # restore original clip
        _surf.set_clip(_orig_clip)
        return _ret

    def clear(self, surface, bgd):
        """used to set background
        Group.clear(surface, bgd): return None
        """
        self._bgd = bgd

    def repaint_rect(self, screen_rect): 
        """repaints the given area
        LayeredDirty.repaint_rect(screen_rect): return None

        screen_rect is in screencoordinates.
        """
        self.lostsprites.append(screen_rect.clip(self._clip))
        
    def set_clip(self, screen_rect=None):
        """ clip the area where to draw. Just pass None (default) to reset the clip
        LayeredDirty.set_clip(screen_rect=None): return None
        """
        if screen_rect is None:
            self._clip = pygame.display.get_surface().get_rect()
        else:
            self._clip = screen_rect
        self._use_update = False
        
    def get_clip(self):
        """clip the area where to draw. Just pass None (default) to reset the clip
        LayeredDirty.get_clip(): return Rect
        """
        return self._clip
    
    def change_layer(self, sprite, new_layer):
        """changes the layer of the sprite
        change_layer(sprite, new_layer): return None

        sprite must have been added to the renderer. It is not checked.
        """
        LayeredUpdates.change_layer(self, sprite, new_layer)
        if sprite.dirty == 0:
            sprite.dirty = 1
            

    def set_timing_treshold(self, time_ms):
        """sets the treshold in milliseconds
        set_timing_treshold(time_ms): return None

        Default is 1000./80 where 80 is the fps I want to switch to full screen mode.
        """
        self._time_threshold = time_ms

# ===============================================================
# ===============================================================
# ===============================================================

class GroupSprite(pygame.sprite.Group):
#class GroupSprite(pygame.sprite.LayeredDirty):
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
    """ Adds new sprites to the group.
    """  
    for sprite in sprites:
      if hasattr(sprite, "zOrder"):
        if sprite.zOrder != None:
          pygame.sprite.Group.add(self, sprite)
        else:  
          raise "ERROR: zOrder = None"  
      else:    
        raise "ERROR: sprite sin zOrder"

# ===============================================================

class OcempPanel(ocempgui.widgets.Box):

  def __init__(self, width, height, topleft, imageBackground):
    ocempgui.widgets.Box.__init__(self, width, height)
    self.topleft = topleft
    self.set_style(ocempgui.widgets.WidgetStyle(STYLES["buttonTopBar"]))
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(imageBackground)
    imgBackground = OcempImageMapTransparent(filePath)
    imgBackground.topleft = 1, 1
    self.add_child(imgBackground)


class OcempLabel(ocempgui.widgets.Label):

  def __init__(self, text, style):
    self.label = text
    self.typeFont = GG.utils.LOCAL_DATA_PATH+"/font/Domestic_Manners.ttf"
    self.sizeFont = style["font"]["size"]
    self.aliasFont = style["font"]["alias"]
    self.colorFont = style["fgcolor"][0]
    ocempgui.widgets.Label.__init__(self, self.label)
    
    self.set_align(ocempgui.widgets.Constants.ALIGN_LEFT | ocempgui.widgets.Constants.ALIGN_TOP)

  def update(self):
    self.draw()

  def draw(self):
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
    
    ocempgui.widgets.Label.__init__(self, line)
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
    size = 46, 31 
    try:
      generateImageSize(filePath, [46, 31], os.path.join(GG.utils.LOCAL_DATA_PATH, "imageLabel" + name + ".png"))
    except:
      return 
    filePath = os.path.join(GG.utils.LOCAL_DATA_PATH, "imageLabel" + name + ".png")
    self._icon = ocempgui.draw.Image.load_image(filePath).convert_alpha()
    
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
    item = self.get_selected()
    if len(item):
      fileName = os.path.join (self.directory, item[0].text)
      if os.path.isfile(fileName):
        return fileName
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
  
  def __init__(self, width, height, imagesList, relativePath):
    self.imagesList = imagesList
    self.relativePath = relativePath
    OcempImageFileList.__init__(self, width, height)

  def _list_contents (self):
    items = ocempgui.widgets.components.ListItemCollection ()
    for image in self.imagesList:
      items.append (OcempContactListItem (image, self.relativePath + image))
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


class OcempEditLine(ocempgui.widgets.Entry):

  def __init__(self, text = ""):
    ocempgui.widgets.Entry.__init__(self, text)

  def _input (self, event):
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
        self._caret += 1
      handled = True

    self.dirty = True
    return handled

def createButton(imgPath, topleft, tooltip, action, *params):
  imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath)
  if tooltip:
    button = OcempImageButtonTransparent(imgPath, tooltip[0], tooltip[1], tooltip[2])
  else:
    button = OcempImageButtonTransparent(imgPath)
  button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, action, *params)
  button.topleft = topleft
  return button



