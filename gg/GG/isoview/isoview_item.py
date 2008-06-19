import pygame
import GG.utils
#import isoview
import animation
import positioned_view

class IsoViewItem(positioned_view.PositionedView):
  """ IsoViewItem class.
  Defines an item view.
  """
  
  def __init__(self, model, screen, room, parent):
    """ Class constructor.
    screen: screen handler.
    parent: isoview_hud handler.
    """
    positioned_view.PositionedView.__init__(self, model, screen)
    self.__ivroom = room
    self.__parent = parent
    self.__upperItem = None
    self.__lowerItem = None
    self.loadImage()
    self.getModel().subscribeEvent('position', self.positionChanged)
    #self.getModel().subscribeEvent('startPosition', self.startPositionChanged)
    #self.getModel().subscribeEvent('chat', parent.pruebaChat)
    #self.getModel().subscribeEvent('room', self.roomChanged)
        
  def loadImage(self):
    """ Loads the item's image.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.getModel().imagePath + self.getModel().spriteName)  
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = GG.utils.p3dToP2d(self.getModel().getPosition(), self.getModel().anchor)
        
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
    """ Returns a sprite.
    """
    return self.__img
  
  def setImg(self, img):
    """ Sets a new image for the item.
    img: image name.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.getModel().imagePath + img)
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    pygame.display.update()
    
  def setSprite(self, sprite):
    """ Sets a new sprite for the item
    sprite: new sprite.
    """
    self.__img.image = sprite
    
  # self.__upperItem
  
  def getUpperItem(self):
    return self.__upperItem

  def setUpperItem(self, item):
    self.__upperItem = item
  
  def getTopMostItem(self):
    if self.__upperItem == None:
      return self
    else:
      return self.__upperItem.getTopMostItem()
    
  def setTopMostItem(self, item):
    #self.lalala()
    if self.__upperItem == None:
      self.__upperItem = item
      item.setLowerItem(self)
    else:
      self.__upperItem.setTopMostItem(item)
    
  def removeTopMostItem(self):
    if self.__upperItem != None:
      if self.__upperItem.getUpperItem() == None:
        self.__upperItem.setLowerItem(None)
        self.__upperItem = None
      else:  
        self.__upperItem.removeTopMostItem()
          
  # self.__lowerItem
  
  def getLowerItem(self):
    return self.__lowerItem

  def setLowerItem(self, item):
    self.__lowerItem = item
    
  def selected(self):
    """ Changes the item's color and sets it as selected.
    """
    if self.__lowerItem != None:
      self.__lowerItem.selected()
    size = self.__img.rect
    color2 = [0, 0, 0]
    for x in range(0, size[2]):
      for y in range(0, size[3]):
        color = self.__img.image.get_at((x,y))
        if color[3] != 0:
          color2[0] = color[0] + GG.utils.COLOR_SHIFT
          if color2[0] > 255: color2[0] = 255
          color2[1] = color[1] + GG.utils.COLOR_SHIFT
          if color2[1] > 255: color2[1] = 255
          color2[2] = color[2] + GG.utils.COLOR_SHIFT
          if color2[2] > 255: color2[2] = 255
          self.__img.image.set_at((x,y), color2)
    pygame.display.update()

  def unselected(self):
    """ Restores the item's color and sets it as unselected.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.getModel().imagePath + self.getModel().spriteName)
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    if self.__lowerItem != None:
      self.__lowerItem.unselected()
    
  def getScreenPosition(self):
    #print self, self.__img.rect.topleft  
    return self.__img.rect.topleft
    
  def setScreenPosition(self, pos):
    self.__img.rect.topleft = pos
    
  def updateScreenPosition(self):
    if self.__lowerItem == None:
      return
    pos = self.getScreenPosition()
    self.setScreenPosition([pos[0], self.getAccumulatedHeight()])
    
  def getAccumulatedHeight(self):
    if self.__lowerItem == None:
      return self.__img.rect.topleft[1]
    else:
      acc = self.__lowerItem.getAccumulatedHeight()
      return acc - self.__img.rect[3] 
  
  def checkClickPosition(self, pos):
    rect = self.getImg().rect
    if rect[0] < pos[0] < (rect[0] + rect[2]):
      if rect[1] < pos[1] < (rect[1] + rect[3]):
        if self.getImg().image.get_at((pos[0] - rect[0], pos[1] - rect[1]))[3] != 0:
          return 1
    if self.__upperItem == None:
      return 0
    else:
      return self.__upperItem.checkClickPosition(pos)
    
  def positionChanged(self, event):
    """ Updates the item position and draws the room after receiving a position change event.
    event: even info.
    """
    GG.utils.playSound(GG.utils.SOUND_STEPS01)
    positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_WALKING_TIME, self, self.getScreenPosition(), \
                  GG.utils.p3dToP2d(event.getParams()["position"], self.getModel().anchor))
    self.setAnimation(positionAnim)
    self.getParent().getIsoviewRoom().setItemOnTile(None, event.getParams()["oldPosition"])
    self.getParent().getIsoviewRoom().setItemOnTile(self, event.getParams()["position"])
      
  def startPositionChanged(self, event):
    """ Updates the item position without animation and draws the room after receiving a position change event.
    event: even info.
    """
    self.setPositionAnimation(None)
    self.setImgPosition(GG.utils.p3dToP2d(event.getParams()['position'], self.getModel().anchor))
    self.getParent().getIsoviewRoom().setItemOnTile(None, event.getParams()["oldPosition"])
    self.getParent().getIsoviewRoom().setItemOnTile(self, event.getParams()["position"])
    
   
