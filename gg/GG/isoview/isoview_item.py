# -*- coding: utf-8 -*- 

import os
import pygame
import GG.utils
import animation
import positioned_view
import guiobjects

# ======================= CONSTANTS ===========================
COLOR_SHIFT = 80
NEW_SIZE = [40, 40]
# =============================================================

class IsoViewItem(positioned_view.PositionedView):
  """ IsoViewItem class.
  Defines an item view.
  """
  
  def __init__(self, model, screen, room, parent, position=None, imagePath=None):
    """ Class constructor.
    model: isometric view model.
    screen: screen handler.
    room: item's isometric room object.
    parent: isoview_hud handler.
    position: isometric view's initial position. 
    imagePath: item's image path.
    """
    positioned_view.PositionedView.__init__(self, model, screen)
    self.__ivroom = room
    self.__parent = parent
    
    infoPackage = model.getItemBuildPackage()
    if position:
      self.__position = position
    else:    
      self.__position = infoPackage["position"]
    self.__imagePath = infoPackage["imagepath"]
    
    self.__img = None
    self.loadImage(imagePath)
    self.getModel().subscribeEvent('position', self.positionChanged)
        
  def loadImage(self, imagePath=None):
    """ Loads the item's image.
    imagePath: item's image path.
    """
    if imagePath is None:
      imageName = os.path.join(self.getModel().getImagePath(), self.getModel().spriteName)
    else:
      imageName = os.path.join(imagePath, self.getModel().spriteName)  
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(imageName)  
    pos = self.__position
    scrPos = GG.utils.p3dToP2d(pos, self.getModel().anchor)
    zOrder = (pow(pos[0], 2) + pow(pos[1], 2))*10
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = scrPos
    self.__img.zOrder = zOrder
    #self.__img = guiobjects.loadSprite(imageName, True, scrPos, zOrder)
            
  def getPosition(self):
    """ Returns the item's position on the room.
    """  
    return self.__position
            
  def updateZOrder(self, value=None):
    """ Updates the zOrder value, used to properly order sprites for painting.
    value: zOrder value.
    """  
    if value == None:
      pos = self.__position
      self.__img.zOrder = (pow(pos[0], 2) + pow(pos[1], 2))*10
    else:
      self.__img.zOrder = value
  
  def updateZOrderFor(self, pos):
    """ Updates the zOrder value, used to properly order sprites for painting.
    value: zOrder value.
    """  
    self.__img.zOrder = (pow(pos[0], 2) + pow(pos[1], 2))*10
        
  def getZOrder(self):
    """ Returns the zOrder value of item's image.
    """  
    return self.__img.zOrder
        
  def getParent(self):
    """ Returns the isoview hud handler.
    """
    return self.__parent
  
  def getIVRoom(self):
    """ Returns the isometric view room object.
    """
    return self.__ivroom
  
  def setIVRoom(self, ivroom):
    """ Sets a new isoview room for the item.
    ivroom: new isoview room.
    """
    self.__ivroom = ivroom
  
  def getImg(self):
    """ Returns the item's image.
    """
    return self.__img   
  
  def setImg(self, img, path=None):
    """ Sets a new image for the item.
    img: image name.
    path: image path.
    """
    if path:
      imageName = os.path.join(path, img)
    else:
      imageName = os.path.join(self.getModel().getImagePath(), img)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(imageName)
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    self.__img.dirty = 1
    
  def setSprite(self, sprite):
    """ Sets a new sprite for the item
    sprite: new sprite.
    """
    self.__img.image = sprite
    self.__img.dirty = 1
  
  def setRect(self, rect):
    """ Sets a new rect for the item image.
    rect: new rect.
    """
    self.__img.rect = rect
    
  def selected(self):
    """ Changes the item's color and sets it as selected.
    """
    size = self.__img.rect
    color2 = [0, 0, 0]
    for x in range(0, size[2]):
      for y in range(0, size[3]):
        color = self.__img.image.get_at((x, y))
        if color[3] != 0:
          color2[0] = color[0] + COLOR_SHIFT
          if color2[0] > 255: 
            color2[0] = 255
          color2[1] = color[1] + COLOR_SHIFT
          if color2[1] > 255: 
            color2[1] = 255
          color2[2] = color[2] + COLOR_SHIFT
          if color2[2] > 255: 
            color2[2] = 255
          self.__img.image.set_at((x, y), color2)
    
  def unselected(self):
    """ Restores the item's color and sets it as unselected.
    """
    imageName = os.path.join(self.__imagePath, self.getModel().spriteName)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(imageName)
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    #self.__img = guiobjects.loadSprite(imageName, False, None, None)
    
  def getScreenPosition(self):
    """ Returns the item's screen position.
    """  
    return self.__img.rect.topleft
    
  def setScreenPosition(self, pos):
    """ Sets a new screen position for the item.
    pos: new screen position.
    """  
    self.__img.rect.topleft = pos
    
  def updateScreenPosition(self, height):
    """ Updates the item's screen position.
    height: added height.
    """  
    pos = self.getScreenPosition()
    self.setScreenPosition([pos[0], pos[1] - height])
    
  def checkClickPosition(self, pos):
    """ Checks if the user clicked on the item's image.
    pos: click position.
    """  
    rect = self.getImg().rect
    if rect[0] < pos[0] < (rect[0] + rect[2]):
      if rect[1] < pos[1] < (rect[1] + rect[3]):
        if self.getImg().image.get_at((pos[0] - rect[0], pos[1] - rect[1]))[3] != 0:
          return 1
    return 0
    
  def setPosition(self, pos):
    """ Stores a local copy for item's position.
    pos: item's position.
    """  
    self.__position = pos  
    
  def positionChanged(self, event):
    """ Updates the item position and draws the room after receiving a position change event.
    event: even info.
    """
    self.__position = event.getParams()['position']
    oldPos = event.getParams()['oldPosition']
    itemList = event.getParams()['itemList']
    
    """
    import isoview_player
    
    if not isinstance(self, isoview_player.IsoViewPlayer):
      tmpPos = GG.utils.p3dToP2d(oldPos, self.getModel().anchor)
      scrPos = self.getScreenPosition()
      self.setScreenPosition([tmpPos[0], scrPos[1]])
      #self.setScreenPosition(tmpPos)
    """  
    
    destination = self.__ivroom.getFutureScreenPosition(self, self.__position, itemList)
    positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_WALKING_TIME, self, self.__img.rect.topleft, destination)
    if self.__parent.getSound():
      guiobjects.playSound(GG.utils.SOUND_STEPS01)
    self.setAnimation(positionAnim)
      
  def startPositionChanged(self, event):
    """ Updates the item position without animation and draws the room after receiving a position change event.
    event: even info.
    """
    self.__position = event.getParams()['position']
    self.setPositionAnimation(None)
    self.setImgPosition(GG.utils.p3dToP2d(event.getParams()['position'], self.getModel().anchor))
    
  def stopFallingAndRestore(self):
    """ DO NOT delete
    """
    pass  

  def isPlayer(self):
    """ Checks if this item is a player or not.
    """
    return False  

# =============================================================

class IsoViewResizedItem(IsoViewItem):
  """ IsoViewResizedItem class.
  Defines an item view.
  """
  
  def __init__(self, model, screen, room, parent, position=None, image=None):
    """ Class constructor.
    model: isometric view model.
    screen: screen handler.
    room: item's isometric room object.
    parent: isoview_hud handler.
    position: isometric view's initial position. 
    imagePath: item's image path.
    """
    if image:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(model.getImagePath(), model.spriteName))
      tempFileName = model.spriteName.replace(os.sep, "-")
      guiobjects.generateImageSize(imgPath, NEW_SIZE, os.path.join(GG.utils.LOCAL_DATA_PATH,tempFileName))
    IsoViewItem.__init__(self, model, screen, room, parent)
    