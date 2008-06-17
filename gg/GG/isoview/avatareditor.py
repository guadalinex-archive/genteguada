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

  """
  def draw_bg(self):
    rect_image = self.picture.get_rect ()
    width = rect_image.width
    height = rect_image.height
    return self.picture
  def draw_bg(self):
    print self.state
    return self.picture
    size = self.picture.get_size()
    area = pygame.Surface(size)
    #area.fill([97,171,193,0])
    return area 
  """
  def draw(self):
    ocempgui.widgets.ImageButton.draw(self)
    self._image = self.picture
    """
    rect = self.picture.get_rect ()
    self._image = self.picture
    topleft = self.rect.topleft
    self._rect = rect
    self._rect.topleft = topleft
    self._oldrect = self.rect
    """
  def update(self): 
    self.draw()

class AvatarEditor:
  """ AvatarEditor class.
  Defines the Avatar Editor
  """

  def __init__(self,render,parent):
    """ Class constructor.
    """
    self.activeWidget = []
    self.activeOption = ""
    self.avatarConfiguration = { 
                                 "gender": "boy", 
                                 "headSize": "S",
                                 "mask": "mask", 
                                 "hairStyle": "1",
                                 "hairColor": "1", 
                                 "skin": "1",
                                 "bodySize": "S",
                                 "typeShirt": "short", 
                                 "shirt": "3", 
                                 "typeTrousers": "short",
                                 "trousers": "5", 
                                 "typeSkirt": "short",
                                 "skirt": "3",
                                 "shoes": "9"
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
    self.imagesTag = self.loadImagesTag()

  def loadImagesTag(self):
    dict = {}
    dict["gender"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "gender_front.png"))
    dict["skin"] =  MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skin_back.png"))
    dict["head"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "head_back.png"))
    dict["body"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "body_back.png"))
    dict["mask"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "mask_back.png"))
    dict["hair"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "hair_back.png"))
    if self.avatarConfiguration["gender"] == "boy":
      dict["shirt"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shirt_back.png"))
      dict["trousers"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "trousers_back.png"))
      dict["skirt"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skirt_disabled.png"))
    else:
      dict["shirt"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shirt_disabled.png"))
      dict["trousers"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "trousers_disabled.png"))
      dict["skirt"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skirt_back.png"))
    dict["shoes"] = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shoes_back.png"))
    return dict


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
    self.imgBackgroundLeft = ImageMapTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left.png"))
    self.window.add_child(self.imgBackgroundLeft)
    imgBackgroundRight = ImageMapTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_right.png"))
    imgBackgroundRight.topleft = 297,0
    self.window.add_child(imgBackgroundRight)

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
    imagesTagOrder = ["gender","skin","head","body","mask","hair","shirt","trousers","skirt","shoes"]
    pos = 0
    for img in imagesTagOrder:
      self.imagesTag[img].border = 0
      self.imagesTag[img].padding = 0
      self.imagesTag[img].border = ocempgui.widgets.Constants.BORDER_NONE
      self.imagesTag[img].topleft = 296, pos * 76
      self.imagesTag[img].connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.paintCustomizeZone, img)
      self.window.add_child(self.imagesTag[img])
      pos += 1

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
      idTag = "gender"
    else:
      self.imagesTag[self.activeOption]._image = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, self.activeOption+"_back.png"))
      self.imagesTag[idTag]._image =  ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, idTag+"_front.png"))
    self.removeWidgets()
    if idTag == "gender":
      self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left.png"))
      self.paintGenderFrame()
    elif idTag == "skin":
      self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left_big_palette.png"))
      self.paintColorPalette(self.updateSkin, "skin")
    elif idTag == "head":
      self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left.png"))
    elif idTag == "body":
      self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left.png"))
    elif idTag == "mask": 
      self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left.png"))
    elif idTag == "hair":
      self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left_small_palette.png"))
      self.paintColorPalette(self.updateHairColor, "hair")
    elif idTag == "shirt":
      self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left_big_palette.png"))
      self.paintColorPalette(self.updateShirtColor, "cloth")
    elif idTag == "trousers":
      self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left_big_palette.png"))
      self.paintColorPalette(self.updateTrouserColor, "cloth")
    elif idTag == "skirt":
      self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left_big_palette.png"))
      self.paintColorPalette(self.updateSkirtColor, "cloth")
    elif idTag == "shoes":
      self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left_big_palette.png"))
      self.paintColorPalette(self.updateShoesColor, "cloth")
    self.activeOption = idTag
      
  def removeWidgets(self):
    for widget in self.activeWidget:
      if widget in self.window.children:
        self.window.remove_child(widget)
        widget.destroy()
    self.activeWidget = []

  def paintGenderFrame(self):
    maleButton = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "boy_button.png"))
    maleButton.border = 0
    maleButton.padding = 0
    maleButton.topleft = [73, 191]
    maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "boy")
    self.window.add_child(maleButton)
    self.activeWidget.append(maleButton)
     
    femaleButton = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "girl_button.png"))
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
        self.imagesTag["shirt"].picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shirt_back.png"))
        self.imagesTag["trousers"].picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "trousers_back.png"))
        self.imagesTag["skirt"].picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skirt_disabled.png"))
        self.delAvatarImage("skirt")
        self.paintShirt()
        self.paintTrousers()
      else:
        self.imagesTag["shirt"].picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shirt_disabled.png"))
        self.imagesTag["trousers"].picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "trousers_disabled.png"))
        self.imagesTag["skirt"].picture = ocempgui.draw.Image.load_image(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skirt_back.png"))
        self.delAvatarImage("shirt")
        self.delAvatarImage("trousers")
        self.paintSkirt()
      self.paintHead()
      self.paintHair()
      self.paintMask()
      
  
  def paintColorPalette(self, method, type):
    baseX = 35
    sizeX = 70
    baseY = 510
    sizeY = 45
    offset = 10
    buttons = self.getPaletteButtons(type)
    for i in range(len(buttons)):
      for j in range(len(buttons[0])):
        button = MiImageButton(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, buttons[i][j]))
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
