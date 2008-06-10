import os
import sys
import time
import GG.utils
import pygame
import pygame.locals
import pygame.transform

import ocempgui.widgets
import ocempgui.draw

class ImageMapTransparent(ocempgui.widgets.ImageMap):

  def __init__(self, image):
    ocempgui.widgets.ImageMap.__init__(self, image)
  
  def draw (self):
    self._image = self.picture

class ImageButtonTransparent(ocempgui.widgets.ImageButton):

  def __init__(self, image):
    ocempgui.widgets.ImageButton.__init__(self, image)
  
  #def draw (self):
    #ocempgui.widgets.ImageButton.draw(self)
    #self.set_state(1)
    #self.sensitive = True
    #self._image = self.picture
    #print self.sensitive

  def update (self):
    self._image = self.picture
    #ocempgui.widgets.ImageButton.update(self)
    #self.set_state(1)
    #self.parent.update()
    #self._image = self.picture
    #print self.sensitive

class AvatarEditor:
  """ AvatarEditor class.
  Defines the Avatar Editor
  """

  def __init__(self,render):
    """ Class constructor.
    """
    print "Iniciando Avatar Editor"
    self.firstTime = 1
    self.activeWidget = []
    self.activeOption = 0
    self.avatarConfiguration = { "gender": "male", "headSize": "S",
                                "mask": "none", "hairStyle": 1,
                                "hairColor":  1, "skin": 1,
                                "bodySize": "none", "sleeve": 0,
                                "shirt": 3, "typeTrousers": 0,
                                "trousers": 5, "skirt": 7,
                                "shoes": 9}
    tLv0 = 0, "body"
    tLv1 = 1, "shirt", "trousers", "shoes"
    tLv2 = 2, "skirt", "shoes"
    tLv3 = 3, "head"
    tLv4 = 4, "hair"
    tLv5 = 5, "mask"
    self.orderDrawAvatar = tLv0 ,tLv1, tLv2, tLv3, tLv4, tLv5

    #self.render = ocempgui.widgets.Renderer()
    self.render = render
    print dir(self.render)

  def processEvent(self,events):
    for event in events:
      if event.type == pygame.locals.QUIT:
        GG.genteguada.GenteGuada.getInstance().finish()
      if event.type == pygame.locals.KEYDOWN:
        if event.key == pygame.locals.K_ESCAPE:
          GG.genteguada.GenteGuada.getInstance().finish()
    self.render.distribute_events(*events)

  def updateFrame(self, ellapsedTime):
    """ Updates all sprites for a new frame.
    """
    #hay que dibujar la habitacion DESPUES del hud, para que las animaciones de los items 
    #se vean sobre el HUD y no debajo como ahora.
    self.window.update()


  def drawInGame(self):
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0],GG.utils.SCREEN_SZ[1])
    self.paintScreen()
    self.paintAvatar()
    self.paintTags()
    self.paintCustomizeZone(self.activeOption)
    self.window.set_depth(1)
    return self.window
    
  def paintScreen(self):
    """Paint the Avatar Editor background on screen.
    """
    print "Pinta la pantalla"
    #background = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
    #self.screen.fill(GG.utils.GUADALINEX_BLUE, background)

    #imgBackground = ocempgui.widgets.ImageLabel(os.path.join(GG.utils.DATA_PATH, "background.png"))
    #self.window.add_child(imgBackground)
    """
    self.paintLeftBackgroundScreen()
    
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.BACKGROUND_MIDDLE)
    self.backgroundMiddleImage = pygame.image.load(imgPath)
    self.screen.blit(self.backgroundMiddleImage, (288,0))
    
    self.paintRightBackgroundScreen()
    
    pygame.display.update()
    """
    
  def paintLeftBackgroundScreen(self):
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.BACKGROUND_LEFT)
    self.backgroundLeftImage = pygame.image.load(imgPath)
    self.screen.blit(self.backgroundLeftImage, (0,0))
    
  def paintRightBackgroundScreen(self):
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.BACKGROUND_RIGHT)
    self.backgroundRightImage = pygame.image.load(imgPath)
    self.screen.blit(self.backgroundRightImage, (385,0))
    
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
      self.paintSkirt(self.avatarConfiguration["sleeve"],self.avatarConfiguration["skirt"])

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
      #img = pygame.image.load(os.path.join(GG.utils.DATA_PATH, GG.utils.TAGS[pos])).convert_alpha()
      imgTag = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.TAGS[pos]))
      #imgTag = ImageButtonTransparent(os.path.join(GG.utils.DATA_PATH, GG.utils.TAGS[pos]))
      #print dir(imgTag)
      imgTag.padding = 0
      imgTag.border = 0
      imgTag.border = ocempgui.widgets.Constants.BORDER_NONE
      imgTag.topleft = [288, GG.utils.TAG_OFFSET*pos]
      #print imgTag.topleft
      imgTag.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.paintCustomizeZone, pos)
      imgTag._image = imgTag.picture
      #imgTag.connect_signal(ocempgui.widgets.Constants.SIG_MOUSEDOWN, self.casa, pos)
      #print dir(self.renderer)
      #render.get_managers()[0].add_high_priority_object(imgTag,ocempgui.widgets.Constants.SIG_MOUSEDOWN)
      #self.renderer.add_widget(imgTag)
      self.window.add_child(imgTag)

  def casa(self,p):
    print "hola"
    
  def paintCustomizeZone(self,idTag):
    """Paint the Customize Zone.
    """
    print "Pinta la zona de personalizacion"
    if idTag == self.activeOption and self.firstTime == 0:
      return
    
    self.removeWidgets()
    if idTag == 0:
      self.paintGenderFrame()
      self.activeOption = 0
      self.firstTime = 0
      """maleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_BTN))
      maleButton.border = 0
      maleButton.padding = 0
      maleButton.topleft = [73, 191]
      maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "male")
      self.window.add_child(maleButton)
      self.activeWidget.append(maleButton)
      
      femaleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_BTN))
      femaleButton.border = 0
      femaleButton.padding = 0
      femaleButton.topleft = [73, 441]
      femaleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "female")
      self.window.add_child(femaleButton)
      self.activeWidget.append(femaleButton)"""
      
    elif idTag == 1:
      if self.avatarConfiguration["gender"] == "male":
    #   self.paintSkinColorPalette(GG.utils.MALE_SKIN)
        self.paintSkinColorPalette()
      else:
    #   self.paintSkinColorPalette(GG.utils.FEMALE_SKIN)
        self.paintSkinColorPalette()
      self.activeOption = 1
        
    elif idTag == 5:
      if self.avatarConfiguration["gender"] == "male":
    #   self.paintHairColorPalette(GG.utils.MALE_HAIR)
        self.paintHairColorPalette()
      else:
    #   self.paintHairColorPalette(GG.utils.FEMALE_HAIR)
        self.paintHairColorPalette()
      self.activeOption = 5
        
    elif idTag == 6:
      #self.paintColorPalette(self.shirtItem)
      self.paintColorPalette("shirt")
      self.activeOption = 6
      
    elif idTag == 7:
    #  self.paintColorPalette(GG.utils.MALE_TROUSERS)
      self.paintColorPalette("trousers")
      self.activeOption = 7
      
    elif idTag == 8:
    #  self.paintColorPalette(GG.utils.FEMALE_SKIRT)
       self.paintColorPalette("skirt")
       self.activeOption = 8
      
    elif idTag == 9:
      if self.avatarConfiguration["gender"] == "male":
    #    self.paintColorPalette(GG.utils.MALE_SHOES)
         self.paintColorPalette("shoes")
      else:
    #    self.paintColorPalette(GG.utils.FEMALE_SHOES)
        self.paintColorPalette("shoes")
      self.activeOption = 9
    #else:
    #  self.paintLeftBackgroundScreen()
      
  def removeWidgets(self):
    for widget in self.activeWidget:
      if widget in self.window.children:
        self.window.remove_child(widget)
        widget.destroy()
    self.activeWidget = []


  def paintGenderFrame(self):
    """maleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_BTN))
    maleButton.border = 0
    maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "male")
    femaleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_BTN))
    femaleButton.border = 0
    femaleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "female")"""
    maleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_BTN))
    maleButton.border = 0
    maleButton.padding = 0
    maleButton.topleft = [73, 191]
    maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "male")
    self.window.add_child(maleButton)
    self.activeWidget.append(maleButton)
     
    femaleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_BTN))
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
    #pygame.display.update()
    
  def paintColorPalette(self, item):
      baseX = 60
      sizeX = 48
      baseY = 500
      sizeY = 27
      offset = 10
      yellowButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_YELLOW))
      yellowButton.border = 0
      yellowButton.padding = 0
      yellowButton.topleft = [baseX, baseY]
      yellowButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 1)
      self.window.add_child(yellowButton)
      self.activeWidget.append(yellowButton)
      orangeButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_ORANGE))
      orangeButton.border = 0
      orangeButton.padding = 0
      orangeButton.topleft = [baseX + sizeX + offset, baseY]
      orangeButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 2)
      self.window.add_child(orangeButton)
      self.activeWidget.append(orangeButton)
      redButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_RED))
      redButton.border = 0
      redButton.padding = 0
      redButton.topleft = [baseX + sizeX * 2 + offset * 2, baseY]
      redButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 3)
      self.window.add_child(redButton)
      self.activeWidget.append(redButton)
      pinkButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_PINK))
      pinkButton.border = 0
      pinkButton.padding = 0
      pinkButton.topleft = [baseX, baseY + sizeY + offset]
      pinkButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 4)
      self.window.add_child(pinkButton)
      self.activeWidget.append(pinkButton)
      blueButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_BLUE))
      blueButton.border = 0
      blueButton.padding = 0
      blueButton.topleft = [baseX + sizeX + offset, baseY + sizeY + offset]
      blueButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 5)
      self.window.add_child(blueButton)
      self.activeWidget.append(blueButton)
      purpleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_PURPLE))
      purpleButton.border = 0
      purpleButton.padding = 0
      purpleButton.topleft = [baseX + sizeX * 2 + offset * 2, baseY + sizeY + offset]
      purpleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 6)
      self.window.add_child(purpleButton)
      self.activeWidget.append(purpleButton)
      greenButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_GREEN))
      greenButton.border = 0
      greenButton.padding = 0
      greenButton.topleft = [baseX, baseY + sizeY * 2 + offset * 2]
      greenButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 7)
      self.window.add_child(greenButton)
      self.activeWidget.append(greenButton)
      whiteButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_WHITE))
      whiteButton.border = 0
      whiteButton.padding = 0
      whiteButton.topleft = [baseX + sizeX + offset, baseY + sizeY * 2 + offset * 2]
      whiteButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 8)
      self.window.add_child(whiteButton)
      self.activeWidget.append(whiteButton)
      blackButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_BLACK))
      blackButton.border = 0
      blackButton.padding = 0
      blackButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 9)
      blackButton.topleft = [baseX + sizeX * 2 + offset * 2, baseY + sizeY * 2 + offset * 2]
      self.window.add_child(blackButton)
      self.activeWidget.append(blackButton)
  
  def paintHairColorPalette(self):
    baseX = 60
    sizeX = 48
    baseY = 500
    sizeY = 27
    offset = 10
    blondeButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_BLONDE))
    blondeButton.border = 0
    blondeButton.padding = 0
    blondeButton.topleft = [baseX, baseY]
    blondeButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "hairColor", 1)
    self.window.add_child(blondeButton)
    self.activeWidget.append(blondeButton)
    brownButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_BROWN))
    brownButton.border = 0
    brownButton.padding = 0
    brownButton.topleft = [baseX + sizeX + offset, baseY]
    brownButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "hairColor", 2)
    self.window.add_child(brownButton)
    self.activeWidget.append(brownButton)
    blackButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_BLACK))
    blackButton.border = 0
    blackButton.padding = 0
    blackButton.topleft = [baseX + sizeX * 2 + offset * 2, baseY]
    blackButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "hairColor", 3)
    self.window.add_child(blackButton)
    self.activeWidget.append(blackButton)
    
  def paintSkinColorPalette(self):
    baseX = 60
    sizeX = 48
    baseY = 500
    sizeY = 27
    offset = 10
    skin1Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_1))
    skin1Button.border = 0
    skin1Button.padding = 0
    skin1Button.topleft = [baseX, baseY]
    skin1Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 1)
    self.window.add_child(skin1Button)
    self.activeWidget.append(skin1Button)
    skin2Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_2))
    skin2Button.border = 0
    skin2Button.padding = 0
    skin2Button.topleft = [baseX + sizeX + offset, baseY]
    skin2Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 2)
    self.window.add_child(skin2Button)
    self.activeWidget.append(skin2Button)
    skin3Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_3))
    skin3Button.border = 0
    skin3Button.padding = 0
    skin3Button.topleft = [baseX + sizeX * 2 + offset * 2, baseY]
    skin3Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 3)
    self.window.add_child(skin3Button)
    self.activeWidget.append(skin3Button)
    skin4Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_4))
    skin4Button.border = 0
    skin4Button.padding = 0
    skin4Button.topleft = [baseX, baseY + sizeY + offset]
    skin4Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 4)
    self.window.add_child(skin4Button)
    self.activeWidget.append(skin4Button)
    skin5Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_5))
    skin5Button.border = 0
    skin5Button.padding = 0
    skin5Button.topleft = [baseX + sizeX + offset, baseY + sizeY + offset]
    skin5Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 5)
    self.window.add_child(skin5Button)
    self.activeWidget.append(skin5Button)
    skin6Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_6))
    skin6Button.border = 0
    skin6Button.padding = 0
    skin6Button.topleft = [baseX + sizeX * 2 + offset * 2, baseY + sizeY + offset]
    skin6Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 6)
    self.window.add_child(skin6Button)
    self.activeWidget.append(skin6Button)
    skin7Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_7))
    skin7Button.border = 0
    skin7Button.padding = 0
    skin7Button.topleft = [baseX, baseY + sizeY * 2 + offset * 2]
    skin7Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 7)
    self.window.add_child(skin7Button)
    self.activeWidget.append(skin7Button)
    skin8Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_8))
    skin8Button.border = 0
    skin8Button.padding = 0
    skin8Button.topleft = [baseX + sizeX + offset, baseY + sizeY * 2 + offset * 2]
    skin8Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 8)
    self.window.add_child(skin8Button)
    self.activeWidget.append(skin8Button)
    skin9Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_9))
    skin9Button.border = 0
    skin9Button.padding = 0
    skin9Button.topleft = [baseX + sizeX * 2 + offset * 2, baseY + sizeY * 2 + offset * 2]
    skin9Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 9)
    self.window.add_child(skin9Button)
    self.activeWidget.append(skin9Button)
    
  def updateColorItem(self, item, color):
    self.avatarConfiguration[item] = color
    self.paintAvatarItem(item)
    
  def updateColor(self, item, color):
    size = item.get_rect()
    for x in range(0, size[2]):
      for y in range(0, size[3]):
        pixel = item.get_at((x,y))
        if pixel[3] != 0:
          item.set_at((x,y), color)
    
  def draw(self):
    self.initAvatarEditor()
    self.paintScreen()
    self.paintAvatar()
    self.renderer = ocempgui.widgets.Renderer()
    self.renderer.set_screen(self.screen)
    self.paintTags()
    self.paintCustomizeZone(self.activeOption)
    while True:
      time.sleep(0.4)
      self.input(pygame.event.get())
    
  def input(self,events):
    for event in events:
      if event.type == pygame.locals.QUIT:
        sys.exit(0)
    self.renderer.distribute_events(*events)

  def initAvatarEditor(self):
    #Iniciar las ventanas pygame
    pygame.init()
    #self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ,pygame.HWSURFACE|pygame.FULLSCREEN,0)
    self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ)
    print self.screen
    pygame.display.set_caption("DEMO AVATAR GENERATOR")

if __name__=="__main__":
  a = AvatarEditor()
  a.draw()
  
