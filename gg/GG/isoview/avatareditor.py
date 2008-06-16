import os
import sys
import time
import GG.utils
import pygame
import pygame.transform

from pygame.locals import * # faster name resolution

import ocempgui.widgets
import ocempgui.draw

class ImageMapTransparent(ocempgui.widgets.ImageMap):

  def __init__(self, image):
    ocempgui.widgets.ImageMap.__init__(self, image)
  
  def draw (self):
    self._image = self.picture
      
class MiImageButton(ocempgui.widgets.ImageButton):

  def __init__(self, image):
    ocempgui.widgets.ImageButton.__init__(self, image)

  def draw_bg(self):
    size = self.picture.get_size()
    return pygame.Surface(size)

class AvatarEditor:
  """ AvatarEditor class.
  Defines the Avatar Editor
  """

  def __init__(self,render,parent):
    """ Class constructor.
    """
    self.activeWidget = []
    self.activeOption = 0
    self.avatarConfiguration = { 
                                 "gender": "boy", 
                                 "headSize": "S",
                                 "mask": "mask", 
                                 "hairStyle": "1",
                                 "hairColor": "1", 
                                 "skin": "1",
                                 "bodySize": "S",
                                 "typeShirt": "short", 
                                 "shirt": "1", 
                                 "typeTrousers": "short",
                                 "trousers": "1", 
                                 "typeSkirt": "short",
                                 "skirt": "1",
                                 "shoes": "1"
                                }
    self.render = render
    self.parent = parent
    self.finish = False

    self.images = {
                    "body":None,
                    "shoes":None,
                    "shirt":None,
                    "trousers":None,
                    "skirt":None,
                    "head":None,
                    "hair":None,
                    "mask":None,
                  }

  def processEvent(self,events):
    for event in events:
      if event.type == QUIT:
        GG.genteguada.GenteGuada.getInstance().finish()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          GG.genteguada.GenteGuada.getInstance().finish()
    self.render.distribute_events(*events)

  def updateFrame(self, ellapsedTime):
    """ Updates all sprites for a new frame.
    """
    #hay que dibujar la habitacion DESPUES del hud, para que las animaciones de los items 
    #se vean sobre el HUD y no debajo como ahora.
    if not self.finish:
      self.window.update()

  def draw(self):
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0],GG.utils.SCREEN_SZ[1])
    self.paintScreen()
    self.paintAvatar()
    self.paintTags()
    self.paintCustomizeZone()
    self.window.set_depth(1)
    return self.window
    
  def paintScreen(self):
    """Paint the Avatar Editor background on screen.
    """
    imgBackground = ImageMapTransparent(os.path.join(GG.utils.DATA_PATH, "background.png"))
    self.window.add_child(imgBackground)

  def paintAvatar(self):
    self.paintBody()
    self.paintShoes()
    if self.avatarConfiguration["gender"] == "boy":
      self.paintShirt()
      self.paintTrousers()
    else:
      self.paintSkirt()
    self.paintHead()
    self.paintHair()
    self.paintMask()

  def delAvatarImage(self, imgName = None):
    if imgName:
      self.window.remove_child(self.images[imgName])
      self.images[imgName].destroy()
      self.images[imgName] = None
    else:
      for key in self.images:
        if self.images[key]:
          self.window.remove_child(self.images[key])
          self.images[key].destroy()
          self.images[key] = None  

  def newAvatarImage(self, imgPath, imgName):
    img = ocempgui.draw.Image.load_image(imgPath)
    if not self.images[imgName]: 
      imgOcemp = ImageMapTransparent(img)
      imgOcemp.topleft = 528,114
      self.window.add_child(imgOcemp)
      self.images[imgName] = imgOcemp
    else:
      self.images[imgName].picture = img

  def paintBody(self):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], "skin", self.avatarConfiguration["skin"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "body")

  def paintShoes(self):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], "shoes", self.avatarConfiguration["shoes"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "shoes")

  def paintShirt(self):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], self.avatarConfiguration["typeShirt"]+"_shirt", self.avatarConfiguration["shirt"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "shirt")

  def paintTrousers(self):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], self.avatarConfiguration["typeTrousers"]+"_trousers", self.avatarConfiguration["trousers"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "trousers")

  def paintSkirt(self):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], self.avatarConfiguration["typeSkirt"]+"_skirt", self.avatarConfiguration["skirt"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "skirt")

  def paintHead(self):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], "head", self.avatarConfiguration["skin"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "head")

  def paintHair(self):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], "hair_"+self.avatarConfiguration["hairStyle"], self.avatarConfiguration["hairColor"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "hair")

  def paintMask(self):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], self.avatarConfiguration["mask"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "mask")


  def paintTags(self):
    """Paint the Tags Zone.
    """
    print "Pinta las pestanas"
    for pos in range(len(GG.utils.TAGS)):
      #imgTag = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.TAGS[pos]))
      imgTag = MiImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.TAGS[pos]))
      imgTag.padding = 0
      imgTag.border = 0
      imgTag.border = ocempgui.widgets.Constants.BORDER_NONE
      #imgTag.topleft = [288, GG.utils.TAG_OFFSET*pos]
      imgTag.topleft = [320, GG.utils.TAG_OFFSET*pos]
      imgTag.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.paintCustomizeZone, pos)
      imgTag._image = imgTag.picture
      self.window.add_child(imgTag)
  
  def closeWindow(self):
    print "==> a cerrar"
    self.finish = True
    self.parent.closeDresser()
    
  def paintCustomizeZone(self,idTag = None):
    """Paint the Customize Zone.
    """
    if idTag == self.activeOption:
      return
    if not idTag:
      idTag = 0
    self.removeWidgets()
    if idTag == 0:
      self.paintGenderFrame()
      self.firstTime = 0
    elif idTag == 1:
      self.paintColorPalette(self.updateSkin, "skin")
    elif idTag == 5:
      self.paintColorPalette(self.updateHairColor, "hair")
    elif idTag == 6:
      self.paintColorPalette(self.updateShirtColor, "cloth")
    elif idTag == 7:
      self.paintColorPalette(self.updateTrouserColor, "cloth")
    elif idTag == 8:
      self.paintColorPalette(self.updateSkirtColor, "cloth")
    elif idTag == 9:
      self.paintColorPalette(self.updateShoesColor, "cloth")
    self.activeOption = idTag
      
  def removeWidgets(self):
    for widget in self.activeWidget:
      if widget in self.window.children:
        self.window.remove_child(widget)
        widget.destroy()
    self.activeWidget = []

  def paintGenderFrame(self):
    maleButton = MiImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_BTN))
    maleButton.border = 0
    maleButton.padding = 0
    maleButton.topleft = [73, 191]
    maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "boy")
    self.window.add_child(maleButton)
    self.activeWidget.append(maleButton)
     
    femaleButton = MiImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_BTN))
    femaleButton.border = 0
    femaleButton.padding = 0
    femaleButton.topleft = [73, 441]
    femaleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "girl")
    self.window.add_child(femaleButton)
    self.activeWidget.append(femaleButton)
    
  def updateGender(self, gender):
    """ Update the Avatar Composite Zone with the appropiate gender.
    """
    if not gender == self.avatarConfiguration["gender"]:
      self.avatarConfiguration["gender"] = gender
      self.paintBody()
      self.paintShoes()
      if self.avatarConfiguration["gender"] == "boy":
        self.delAvatarImage("skirt")
        self.paintShirt()
        self.paintTrousers()
      else:
        self.delAvatarImage("shirt")
        self.delAvatarImage("trousers")
        self.paintSkirt()
      self.paintHead()
      self.paintHair()
      self.paintMask()
      
  
  def paintColorPalette(self, method, type):
    baseX = 60
    sizeX = 48
    baseY = 500
    sizeY = 27
    offset = 10
    buttons = self.getPaletteButtons(type)
    for i in range(len(buttons)):
      for j in range(len(buttons[0])):
        button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, buttons[i][j]))
        button.border = 0
        button.padding = 0
        button.topleft = [baseX + sizeX * j + offset * j, baseY + sizeY * i + offset * i]
        button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, method, j + 1 + (i * 3))
        self.window.add_child(button)
        self.activeWidget.append(button)

  def getPaletteButtons(self, type):
    if type == "cloth":
      return [ [GG.utils.COLOR_YELLOW, GG.utils.COLOR_ORANGE, GG.utils.COLOR_RED], 
               [GG.utils.COLOR_PINK, GG.utils.COLOR_BLUE, GG.utils.COLOR_PURPLE], 
               [GG.utils.COLOR_GREEN, GG.utils.COLOR_WHITE, GG.utils.COLOR_BLACK] ]
    elif type == "hair":
      return [ [GG.utils.COLOR_BLONDE, GG.utils.COLOR_BROWN, GG.utils.COLOR_BLACK] ]
    elif type == "skin":
      return [ [GG.utils.SKIN_1, GG.utils.SKIN_2, GG.utils.SKIN_3], 
               [GG.utils.SKIN_4, GG.utils.SKIN_5, GG.utils.SKIN_6], 
               [GG.utils.SKIN_7, GG.utils.SKIN_8, GG.utils.SKIN_9] ]
    else:
      return []

  def updateColorItem(self, item, color):
    self.avatarConfiguration[item] = color
    self.paintAvatarItem(item)

  def updateSkin(self,color):
    self.avatarConfiguration["skin"] = str(color)
    self.paintBody()
    self.paintHead()
  
  def updateHairColor(self,color):
    self.avatarConfiguration["hairColor"] = str(color)
    self.paintHair()

  def updateShirtColor(self,color):
    self.avatarConfiguration["shirt"] = str(color)
    self.paintShirt()

  def updateTrouserColor(self,color):
    self.avatarConfiguration["trousers"] = str(color)
    self.paintTrousers()

  def updateSkirtColor(self,color):
    self.avatarConfiguration["skirt"] = str(color)
    self.paintSkirt()

  def updateShoesColor(self,color):
    self.avatarConfiguration["shoes"] = str(color)
    self.paintShoes()
