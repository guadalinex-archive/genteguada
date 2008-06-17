import os
import sys
import time
import GG.utils
import pygame
import pygame.transform

from pygame.locals import * # faster name resolution

import ocempgui.widgets
import ocempgui.draw

class AvatarEditor:
  """ AvatarEditor class.
  Defines the Avatar Editor
  """

  def __init__(self,render,parent,configuration):
    """ Class constructor.
    """
    self.activeWidget = []
    self.activeOption = ""
    self.avatarConfiguration = configuration 
    self.render = render
    self.parent = parent
    self.finish = False
    self.images = self.loadImagesAvatar()
    self.imagesTag = self.loadImagesTag()

  def loadImagesAvatar(self):
    dict = {}
    dict["body"] = None
    dict["shoes"] = None
    dict["shirt"] = None
    dict["trousers"] = None
    dict["skirt"] = None
    dict["head"] = None
    dict["hair"] = None
    dict["mask"] = None
    return dict

  def loadImagesTag(self):
    dict = {}
    dict["gender"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "gender_front.png"))
    dict["skin"] =  GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skin_back.png"))
    dict["head"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "head_back.png"))
    dict["body"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "body_back.png"))
    dict["mask"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "mask_back.png"))
    dict["hair"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "hair_back.png"))
    if self.avatarConfiguration["gender"] == "boy":
      dict["shirt"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shirt_back.png"))
      dict["trousers"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "trousers_back.png"))
      dict["skirt"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skirt_disabled.png"))
    else:
      dict["shirt"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shirt_disabled.png"))
      dict["trousers"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "trousers_disabled.png"))
      dict["skirt"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skirt_back.png"))
    dict["shoes"] = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shoes_back.png"))
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
    self.paintButtons()
    self.window.set_depth(1)
    return self.window
    
  def paintScreen(self):
    """Paint the Avatar Editor background on screen.
    """
    self.imgBackgroundLeft = GG.utils.OcempImageMapTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left.png"))
    self.window.add_child(self.imgBackgroundLeft)
    imgBackgroundRight = GG.utils.OcempImageMapTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_right.png"))
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
      imgOcemp = GG.utils.OcempImageMapTransparent(img)
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
      self.imagesTag[img].topleft = 296, pos * 76
      self.imagesTag[img].connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.paintCustomizeZone, img)
      self.window.add_child(self.imagesTag[img])
      pos += 1

  def changeImageTab(self, idTag):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, self.activeOption+"_back.png")
    self.imagesTag[self.activeOption].picture = ocempgui.draw.Image.load_image(imgPath)
    imgPath = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, idTag+"_front.png")
    self.imagesTag[idTag].picture = ocempgui.draw.Image.load_image(imgPath)

  def changeBackgroundLeft(self, image):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, image)
    self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(imgPath)

  def paintCustomizeZone(self,idTag = None):
    """Paint the Customize Zone.
    """
    if idTag == self.activeOption:
      return
    
    if idTag == "skirt" and self.avatarConfiguration["gender"] == "boy":
      return 

    if self.avatarConfiguration["gender"] == "girl" and idTag in ["shirt","trousers"]:
      return

    if not idTag:
      idTag = "gender"
    else:
      self.changeImageTab(idTag)
      
    self.removeWidgets()

    if idTag == "gender":
      self.changeBackgroundLeft("background_left.png")
      self.paintGenderFrame()

    elif idTag == "skin":
      self.changeBackgroundLeft("background_left_big_palette.png")
      self.paintColorPalette(self.updateSkin, "skin")

    elif idTag == "head":
      self.changeBackgroundLeft("background_left.png")
      self.paintSizePalette(self.updateSizeHead)

    elif idTag == "body":
      self.changeBackgroundLeft("background_left.png")
      self.paintSizePalette(self.updateSizeBody)

    elif idTag == "mask": 
      self.changeBackgroundLeft("background_left.png")

    elif idTag == "hair":
      self.changeBackgroundLeft("background_left_small_palette.png")
      self.paintColorPalette(self.updateHairColor, "hair")

    elif idTag == "shirt":
      self.changeBackgroundLeft("background_left_big_palette.png")
      self.paintColorPalette(self.updateShirtColor, "cloth")

    elif idTag == "trousers":
      self.changeBackgroundLeft("background_left_big_palette.png")
      self.paintColorPalette(self.updateTrouserColor, "cloth")

    elif idTag == "skirt":
      self.changeBackgroundLeft("background_left_big_palette.png")
      self.paintColorPalette(self.updateSkirtColor, "cloth")

    elif idTag == "shoes":
      self.changeBackgroundLeft("background_left_big_palette.png")
      self.paintColorPalette(self.updateShoesColor, "cloth")

    self.activeOption = idTag
      
  def removeWidgets(self):
    for widget in self.activeWidget:
      if widget in self.window.children:
        self.window.remove_child(widget)
        widget.destroy()
    self.activeWidget = []

  def paintGenderFrame(self):
    maleButton = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "boy_button.png"))
    maleButton.topleft = [73, 191]
    maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "boy")
    self.window.add_child(maleButton)
    self.activeWidget.append(maleButton)
     
    femaleButton = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "girl_button.png"))
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
    if type == "hair":
      baseY = 515
    else:
      baseY = 510
    sizeY = 45
    offset = 10
    buttons = self.getPaletteButtons(type)
    for i in range(len(buttons)):
      for j in range(len(buttons[0])):
        button = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, buttons[i][j]))
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

  def paintSizePalette(self, method):
    baseX = 70
    baseY = 70
    sizeY = 150
    offset = 10
    buttons = ["s","m","l","xl"]
    for i in range(len(buttons)):
      button = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, buttons[i]+".png"))
      button.topleft = [baseX , baseY + sizeY * i + offset * i]
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, method, buttons[i].upper())
      self.window.add_child(button)
      self.activeWidget.append(button)

  def updateSizeHead(self,size):
    self.avatarConfiguration["headSize"] = size
    self.paintHead()
    self.paintHair()
    self.paintMask()

  def updateSizeBody(self,size):
    self.avatarConfiguration["bodySize"] = size
    self.paintBody()
    self.paintShoes()
    if self.avatarConfiguration["gender"] == "boy":
      self.paintShirt()
      self.paintTrousers()
    else:
      self.paintSkirt()


  def paintButtons(self):
    buttonOK = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "ok_button.png"))
    buttonOK.topleft = [780, 710]
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.changeConfiguration)
    self.window.add_child(buttonOK)
     
    buttonCancel = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "cancel_button.png"))
    buttonCancel.topleft = [900, 710]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.closeConfiguration)
    self.window.add_child(buttonCancel)

  def changeConfiguration(self):
    self.finish = True
    self.parent.closeDresser(self.avatarConfiguration)

  def closeConfiguration(self):
    self.finish = True
    self.parent.closeDresser()


