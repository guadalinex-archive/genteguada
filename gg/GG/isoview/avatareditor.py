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
                                 "mask": "mask.png", 
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
    tLv0 = 0, "body"
    tLv1 = 1, "shirt", "trousers", "shoes"
    tLv2 = 2, "skirt", "shoes"
    tLv3 = 3, "head"
    tLv4 = 4, "hair"
    tLv5 = 5, "mask"
    self.orderDrawAvatar = tLv0 ,tLv1, tLv2, tLv3, tLv4, tLv5
    self.render = render
    self.parent = parent
    self.finish = False

    self.images = {
                    "body":None,
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
    self.paintNewAvatar()
    #self.paintAvatar()
    self.paintTags()
    self.paintCustomizeZone()
    self.window.set_depth(1)
    return self.window
    
  def paintScreen(self):
    """Paint the Avatar Editor background on screen.
    """
    imgBackground = ImageMapTransparent(os.path.join(GG.utils.DATA_PATH, "background.png"))
    self.window.add_child(imgBackground)

  def paintNewAvatar(self):
    self.paintNewBody()

  def paintNewBody(self):
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG + GG.utils.MALE_SKIN, str(color) + GG.utils.IMG_EXTENSION)

    if self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH + GG.utils.MALE_SKIN, str(color) + GG.utils.IMG_EXTENSION)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_DUMMY)
    img = ocempgui.draw.Image.load_image(imgPath)
    bodySizeItem = ImageMapTransparent(img)
    bodySizeItem.topleft = 528,114
    self.window.add_child(bodySizeItem)

  def paintAvatar(self):
    """Paint the Composite Avatar Zone.
    """
    print "Pinta el avatar"

    for tuple in self.orderDrawAvatar:
      if tuple[0] != 1 and tuple[0] != 2: 
        for item in tuple:
          print item
          self.paintAvatarItem(item)
      elif  tuple[0] == 1 and self.avatarConfiguration["gender"] == "male":
        print "avatar masculino"
        for item in tuple:
          print item
          self.paintAvatarItem(item)
      elif  tuple[0] == 2 and self.avatarConfiguration["gender"] == "female":
        print "avatar femenino"
        for item in tuple:
          print item
          self.paintAvatarItem(item)

  def paintAvatarItem(self, item):
    """Paint each Avatar Item.
    """
    if item == "head":
      self.paintHead(self.avatarConfiguration["headSize"], self.avatarConfiguration["skin"])
    elif item == "hair":
      self.paintHair(self.avatarConfiguration["hairStyle"], self.avatarConfiguration["hairColor"])
    elif item == "body":
      self.paintBody(self.avatarConfiguration["bodySize"], self.avatarConfiguration["skin"])
    elif item == "mask":
      self.paintMask(self.avatarConfiguration[item])
    elif item == "shirt":
      self.paintShirt(self.avatarConfiguration["sleeve"], self.avatarConfiguration["shirt"])
    elif item == "trousers":
      self.paintTrousers(self.avatarConfiguration["typeTrousers"],self.avatarConfiguration["trousers"])
    elif item == "shoes":
      self.paintShoes(self.avatarConfiguration["shoes"])
    elif item == "skirt":
      self.paintSkirt(self.avatarConfiguration["skirt"])
      #self.paintSkirt(self.avatarConfiguration["sleeve"],self.avatarConfiguration["skirt"])

  def paintHead(self, size, color):
    #TODO: Modificar ajustando al tamano de cabeza
    if self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH + GG.utils.MALE_HEAD, str(color) + GG.utils.IMG_EXTENSION)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_DUMMY)
    img = ocempgui.draw.Image.load_image(imgPath)
    headSizeItem = ImageMapTransparent(img)
    headSizeItem.topleft = 528,114
    self.window.add_child(headSizeItem)

  def paintHair(self, style, color):
    if self.avatarConfiguration["gender"] == "male":
      if style == 1:
        hairPath = GG.utils.MALE_HAIR_1 
      elif style == 2:
        hairPath = GG.utils.MALE_HAIR_2
      elif style == 3:
        hairPath = GG.utils.MALE_HAIR_3
      imgPath = os.path.join(GG.utils.DATA_PATH + hairPath, str(color) + GG.utils.IMG_EXTENSION )
    else:
      if style == 1:
        hairPath = GG.utils.FEMALE_HAIR_1
      elif style == 2:
        hairPath = GG.utils.FEMALE_HAIR_2
      elif style == 3:
        hairPath = GG.utils.FEMALE_HAIR_3
      imgPath = os.path.join(GG.utils.DATA_PATH, hairPath)
    img = ocempgui.draw.Image.load_image(imgPath)
    self.hairStyleItem = ImageMapTransparent(img)
    self.hairStyleItem.topleft = 528,114
    self.window.add_child(self.hairStyleItem)
    
  def paintBody(self, size, color):
    #TODO: Modificar al tamano del cuerpo y del genero
    if self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH + GG.utils.MALE_SKIN, str(color) + GG.utils.IMG_EXTENSION)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_DUMMY)
    img = ocempgui.draw.Image.load_image(imgPath)
    bodySizeItem = ImageMapTransparent(img)
    bodySizeItem.topleft = 528,114
    self.window.add_child(bodySizeItem)
   
  def paintMask(self, skin):
    if self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH + GG.utils.MALE_MASK, "mask" + GG.utils.IMG_EXTENSION)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_MASK)
    img = ocempgui.draw.Image.load_image(imgPath)
    maskItem = ImageMapTransparent(img)
    maskItem.topleft = 528,114
    self.window.add_child(maskItem)
  
  def paintShirt(self, type, color):
    if type == 1:
      imgPath = os.path.join(GG.utils.DATA_PATH + GG.utils.MALE_LONG_SHIRT, str(color) + GG.utils.IMG_EXTENSION)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH + GG.utils.MALE_SHORT_SHIRT, str(color) + GG.utils.IMG_EXTENSION)
    img = ocempgui.draw.Image.load_image(imgPath)
    self.shirtItem= ImageMapTransparent(img)
    self.shirtItem.topleft = 528,114
    self.window.add_child(self.shirtItem)
    
  def paintTrousers(self, type, color):
    if type == 1:
      imgPath = os.path.join(GG.utils.DATA_PATH + GG.utils.MALE_LONG_TROUSERS, str(color) + GG.utils.IMG_EXTENSION)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH + GG.utils.MALE_SHORT_TROUSERS, str(color) + GG.utils.IMG_EXTENSION)
    img = ocempgui.draw.Image.load_image(imgPath)
    self.trousersItem = ImageMapTransparent(img)
    self.trousersItem.topleft = 528,114
    self.window.add_child(self.trousersItem)
  
  def paintShoes(self, color):
    if self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH + GG.utils.MALE_SHOES, str(color) + GG.utils.IMG_EXTENSION)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_SHOES)
    img = ocempgui.draw.Image.load_image(imgPath)
    self.shoesItem = ImageMapTransparent(img)
    self.shoesItem.topleft = 528,114
    self.window.add_child(self.shoesItem)
    
  def paintSkirt(self, skirt):
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_SKIRT)
    img = ocempgui.draw.Image.load_image(imgPath)
    self.skirtItem = ImageMapTransparent(img)
    self.skirtItem.topleft = 528,114
    self.window.add_child(self.skirtItem)
    
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
      self.paintColorPalette("skin", "skin")
    elif idTag == 5:
      self.paintColorPalette("hairColor", "hair")
    elif idTag == 6:
      self.paintColorPalette("shirt", "cloth")
    elif idTag == 7:
      self.paintColorPalette("trousers", "cloth")
    elif idTag == 8:
      self.paintColorPalette("skirt", "cloth")
    elif idTag == 9:
      self.paintColorPalette("shoes","cloth")
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
    maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "male")
    self.window.add_child(maleButton)
    self.activeWidget.append(maleButton)
     
    femaleButton = MiImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_BTN))
    femaleButton.border = 0
    femaleButton.padding = 0
    femaleButton.topleft = [73, 441]
    femaleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "female")
    self.window.add_child(femaleButton)
    self.activeWidget.append(femaleButton)
    
  def updateGender(self, gender):
    """ Update the Avatar Composite Zone with the appropiate gender.
    """
    if gender == "male":
      print "genero actualizado"
      self.avatarConfiguration["gender"] = "male"
      self.paintAvatar()
    elif gender == "female":
      print "genero actualizado"
      self.avatarConfiguration["gender"] = "female"
      self.paintAvatar()
  
  def paintColorPalette(self, item, type):
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
        button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, j + 1 + (i * 3))
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
    
