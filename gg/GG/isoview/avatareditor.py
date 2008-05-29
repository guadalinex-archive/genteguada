import os
import sys
import time
import ocempgui.widgets
import GG.utils
import pygame
import pygame.locals
import pygame.transform



class AvatarEditor:
  """ AvatarEditor class.
  Defines the Avatar Editor
  """

  def __init__(self):
    """ Class constructor.
    """
    print "Iniciando Avatar Editor"
    self.activeWidget = []
    self.activeOption = 0
    self.avatarConfiguration = { "gender": "male", "headSize": "S",
                                "mask": "none", "hairStyle": 1,
                                "hairColor":  1, "skin": 1,
                                "bodySize": "none", "sleeve": 1,
                                "shirt": 3, "typeTrousers": 1,
                                "trousers": 5, "skirt": 7,
                                "shoes": 9}
    tLv0 = 0 , "headSize", "bodySize", "skin"
    tLv1 = 1 , "hairStyle", "hairColor", "shirt", "short", "sleeve", "typeTrousers", "trousers", "shoes"
    tLv2 = 2 , "hairStyle", "hairColor","skirt", "sleeve", "shoes"
    tLv3 = 3 , "mask"
    self.orderDrawAvatar = tLv0 ,tLv1, tLv2, tLv3

  def drawInGame(self):
    print "vamos a ver que hacemos"
    self.window = ocempgui.widgets.HFrame()
    self.window.topleft = 0,0
    self.window.set_minimum_size(GG.utils.SCREEN_SZ[0],GG.utils.SCREEN_SZ[1])
    img1 = ocempgui.widgets.ImageLabel(os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_DUMMY))
    img1.topleft = 528,114
    img2 = ocempgui.widgets.ImageLabel(os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_MASK))
    img2.topleft = 528,114
    #self.window.add_child(img1)
    #self.window.add_child(img2)
    return self.window,img1,img2


    """
    self.paintScreen()
    self.paintAvatar()
    self.renderer = ocempgui.widgets.Renderer()
    self.renderer.set_screen(self.screen)
    self.paintTags()
    self.paintCustomizeZone(self.activeOption)
    while True:
      time.sleep(0.4)
      self.input(pygame.event.get())
    """
    
  def paintScreen(self):
    """Paint the Avatar Editor background on screen.
    """
    print "Pinta la pantalla"
    #background = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
    #self.screen.fill(GG.utils.GUADALINEX_BLUE, background)
    
    self.paintLeftBackgroundScreen()
    
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.BACKGROUND_MIDDLE)
    self.backgroundMiddleImage = pygame.image.load(imgPath)
    self.screen.blit(self.backgroundMiddleImage, (288,0))
    
    self.paintRightBackgroundScreen()
    
    pygame.display.update()
    
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
    if item == "headSize":
      self.paintHeadSize(self.avatarConfiguration[item])
    elif item == "hairStyle":
      self.paintHairStyle(self.avatarConfiguration[item])
    elif item == "hairColor":
      self.paintHairColor(self.avatarConfiguration[item])
    elif item == "bodySize":
      self.paintBodySize(self.avatarConfiguration[item])
    elif item == "mask":
      self.paintMask(self.avatarConfiguration[item])
    elif item == "skin":
      self.paintSkin(self.avatarConfiguration[item])
    elif item == "shirt":
      self.paintShirt(self.avatarConfiguration[item])
    elif item == "sleeve":
      self.paintSleeve(self.avatarConfiguration[item])
    elif item == "typeTrousers":
      self.paintTypeTrousers(self.avatarConfiguration[item])
    elif item == "trousers":
      self.paintTrousers(self.avatarConfiguration[item])
    elif item == "shoes":
      self.paintShoes(self.avatarConfiguration[item])
    elif item == "skirt":
      self.paintSkirt(self.avatarConfiguration[item])
   
  def paintHeadSize(self, headSize):
    #TODO: Modificar ajustando al tamano de cabeza
    self.paintRightBackgroundScreen()
    if self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_DUMMY)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_DUMMY)
    headSizeItem = pygame.image.load(imgPath)
    self.screen.blit(headSizeItem, (528,114))
    pygame.display.update()
    
  def paintHairStyle(self, hairStyle):
    if self.avatarConfiguration["gender"] == "male":
      if hairStyle == 1:
        attributeHair = GG.utils.MALE_HAIR_1
      elif hairStyle == 2:
        attributeHair = GG.utils.MALE_HAIR_2
      elif hairStyle == 3:
        attributeHair = GG.utils.MALE_HAIR_3
      imgPath = os.path.join(GG.utils.DATA_PATH, attributeHair)
    else:
      if hairStyle == 1:
        attributeHair = GG.utils.FEMALE_HAIR_1
      elif hairStyle == 2:
        attributeHair = GG.utils.FEMALE_HAIR_2
      elif hairStyle == 3:
        attributeHair = GG.utils.FEMALE_HAIR_3
      imgPath = os.path.join(GG.utils.DATA_PATH, attributeHair)
    self.hairStyleItem = pygame.image.load(imgPath)
    self.updateColor(self.hairStyleItem, GG.utils.getRGBColor(GG.utils.HAIR_COLORS[self.avatarConfiguration["hairColor"]]))
    self.screen.blit(self.hairStyleItem, (528,114))
    pygame.display.update()
    
  def paintHairColor(self, hairColor):
    self.updateColor(self.hairStyleItem, GG.utils.getRGBColor(GG.utils.HAIR_COLORS[self.avatarConfiguration["hairColor"]]))
    self.screen.blit(self.hairStyleItem, (528,114))
    pygame.display.update()
    
  def paintBodySize(self, bodySize):
    #TODO: Modificar al tamano del cuerpo y del genero
    self.paintRightBackgroundScreen()
    if self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_DUMMY)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_DUMMY)
    bodySizeItem = pygame.image.load(imgPath)
    self.screen.blit(bodySizeItem, (528,114))
    pygame.display.update()
   
  def paintMask(self, skin):
    if self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_MASK)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_MASK)
    maskItem = pygame.image.load(imgPath)
    self.screen.blit(maskItem, (528,114))
    pygame.display.update()
    
  def paintSkin(self, skin):
    if self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_SKIN)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_SKIN)
    self.skinItem = pygame.image.load(imgPath)
    self.updateColor(self.skinItem, GG.utils.getRGBColor(GG.utils.SKIN_COLORS[self.avatarConfiguration["skin"]]))
    self.screen.blit(self.skinItem, (528,114))
    pygame.display.update()
  
  def paintShirt(self, shirt):
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_SHIRT)
    self.shirtItem = pygame.image.load(imgPath)
    self.updateColor(self.shirtItem, GG.utils.getRGBColor(GG.utils.COLORS[self.avatarConfiguration["shirt"]]))
    self.screen.blit(self.shirtItem, (528,114))
    pygame.display.update()
  
  def paintSleeve(self, sleeve):
    if sleeve == 1:
      if self.avatarConfiguration["gender"] == "male":
        imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_SLEEVE)
        shirtOrSkirt = "shirt"
      else:
        imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_SLEEVE)
        shirtOrSkirt = "skirt"
      self.sleeveItem = pygame.image.load(imgPath)
      self.updateColor(self.sleeveItem, GG.utils.getRGBColor(GG.utils.COLORS[self.avatarConfiguration[shirtOrSkirt]]))
      self.screen.blit(self.sleeveItem, (528,114))
      pygame.display.update()
  
  def paintTypeTrousers(self, typeTrousers):
    if typeTrousers == 1 and self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_TYPE_TROUSERS)
      self.typeTrousersItem = pygame.image.load(imgPath)
      self.updateColor(self.typeTrousersItem, GG.utils.getRGBColor(GG.utils.COLORS[self.avatarConfiguration["trousers"]]))
      self.screen.blit(self.typeTrousersItem, (528,114))
      pygame.display.update()
    
  def paintTrousers(self, sleeve):
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_TROUSERS)
    self.trousersItem = pygame.image.load(imgPath)
    self.updateColor(self.trousersItem, GG.utils.getRGBColor(GG.utils.COLORS[self.avatarConfiguration["trousers"]]))
    self.screen.blit(self.trousersItem, (528,114))
    pygame.display.update()
  
  def paintShoes(self, sleeve):
    if self.avatarConfiguration["gender"] == "male":
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_SHOES)
    else:
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_SHOES)
    self.shoesItem = pygame.image.load(imgPath)
    self.updateColor(self.shoesItem, GG.utils.getRGBColor(GG.utils.COLORS[self.avatarConfiguration["shoes"]]))
    self.screen.blit(self.shoesItem, (528,114))
    pygame.display.update()
    
  def paintSkirt(self, skirt):
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_SKIRT)
    self.skirtItem = pygame.image.load(imgPath)
    self.updateColor(self.skirtItem, GG.utils.getRGBColor(GG.utils.COLORS[self.avatarConfiguration["skirt"]]))
    self.screen.blit(self.skirtItem, (528,114))
    pygame.display.update()    
    
  def paintTags(self):
    """Paint the Tags Zone.
    """
    print "Pinta las pestanas"
    
    for pos in range(len(GG.utils.TAGS)):
      #img = pygame.image.load(os.path.join(GG.utils.DATA_PATH, GG.utils.TAGS[pos])).convert_alpha()
      imgTag = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.TAGS[pos]))
      #print dir(imgTag)
      imgTag.padding = 0
      imgTag.border = 0
      imgTag.border = ocempgui.widgets.Constants.BORDER_NONE
      imgTag.topleft = [288, GG.utils.TAG_OFFSET*pos]
      print imgTag.topleft
      imgTag.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.paintCustomizeZone, pos)
      self.renderer.add_widget(imgTag)
    
  def paintCustomizeZone(self,idTag):
    """Paint the Customize Zone.
    """
    print "Pinta la zona de personalizacion"
    self.removeWidgets()
    if idTag == 0:
      maleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_BTN))
      maleButton.border = 0
      maleButton.padding = 0
      maleButton.topleft = [73, 191]
      maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "male")
      self.renderer.add_widget(maleButton)
      self.activeWidget.append(maleButton)
      
      femaleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_BTN))
      femaleButton.border = 0
      femaleButton.padding = 0
      femaleButton.topleft = [73, 441]
      femaleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "female")
      self.renderer.add_widget(femaleButton)
      self.activeWidget.append(femaleButton)
      
    elif idTag == 1:
      if self.avatarConfiguration["gender"] == "male":
    #   self.paintSkinColorPalette(GG.utils.MALE_SKIN)
        self.paintSkinColorPalette()
      else:
    #   self.paintSkinColorPalette(GG.utils.FEMALE_SKIN)
        self.paintSkinColorPalette()
        
    elif idTag == 5:
      if self.avatarConfiguration["gender"] == "male":
    #   self.paintHairColorPalette(GG.utils.MALE_HAIR)
        self.paintHairColorPalette()
      else:
    #   self.paintHairColorPalette(GG.utils.FEMALE_HAIR)
        self.paintHairColorPalette()
        
    elif idTag == 6:
      #self.paintColorPalette(self.shirtItem)
      self.paintColorPalette("shirt")
      
    elif idTag == 7:
    #  self.paintColorPalette(GG.utils.MALE_TROUSERS)
      self.paintColorPalette("trousers")
      
    elif idTag == 8:
    #  self.paintColorPalette(GG.utils.FEMALE_SKIRT)
       self.paintColorPalette("skirt")
      
    elif idTag == 9:
      if self.avatarConfiguration["gender"] == "male":
    #    self.paintColorPalette(GG.utils.MALE_SHOES)
         self.paintColorPalette("shoes")
      else:
    #    self.paintColorPalette(GG.utils.FEMALE_SHOES)
        self.paintColorPalette("shoes")
    else:
      self.paintLeftBackgroundScreen()
      
  def removeWidgets(self):
    for widget in self.activeWidget:
      self.renderer.remove_widget(widget)
      widget.destroy()

  def paintGenderFrame(self):
    maleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_BTN))
    maleButton.border = 0
    maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "male")
    femaleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_BTN))
    femaleButton.border = 0
    femaleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "female")
    
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
      self.renderer.add_widget(yellowButton)
      self.activeWidget.append(yellowButton)
      orangeButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_ORANGE))
      orangeButton.border = 0
      orangeButton.padding = 0
      orangeButton.topleft = [baseX + sizeX + offset, baseY]
      orangeButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 2)
      self.renderer.add_widget(orangeButton)
      self.activeWidget.append(orangeButton)
      redButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_RED))
      redButton.border = 0
      redButton.padding = 0
      redButton.topleft = [baseX + sizeX * 2 + offset * 2, baseY]
      redButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 3)
      self.renderer.add_widget(redButton)
      self.activeWidget.append(redButton)
      pinkButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_PINK))
      pinkButton.border = 0
      pinkButton.padding = 0
      pinkButton.topleft = [baseX, baseY + sizeY + offset]
      pinkButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 4)
      self.renderer.add_widget(pinkButton)
      self.activeWidget.append(pinkButton)
      blueButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_BLUE))
      blueButton.border = 0
      blueButton.padding = 0
      blueButton.topleft = [baseX + sizeX + offset, baseY + sizeY + offset]
      blueButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 5)
      self.renderer.add_widget(blueButton)
      self.activeWidget.append(blueButton)
      purpleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_PURPLE))
      purpleButton.border = 0
      purpleButton.padding = 0
      purpleButton.topleft = [baseX + sizeX * 2 + offset * 2, baseY + sizeY + offset]
      purpleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 6)
      self.renderer.add_widget(purpleButton)
      self.activeWidget.append(purpleButton)
      greenButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_GREEN))
      greenButton.border = 0
      greenButton.padding = 0
      greenButton.topleft = [baseX, baseY + sizeY * 2 + offset * 2]
      greenButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 7)
      self.renderer.add_widget(greenButton)
      self.activeWidget.append(greenButton)
      whiteButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_WHITE))
      whiteButton.border = 0
      whiteButton.padding = 0
      whiteButton.topleft = [baseX + sizeX + offset, baseY + sizeY * 2 + offset * 2]
      whiteButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 8)
      self.renderer.add_widget(whiteButton)
      self.activeWidget.append(whiteButton)
      blackButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_BLACK))
      blackButton.border = 0
      blackButton.padding = 0
      blackButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, item, 9)
      blackButton.topleft = [baseX + sizeX * 2 + offset * 2, baseY + sizeY * 2 + offset * 2]
      self.renderer.add_widget(blackButton)
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
    self.renderer.add_widget(blondeButton)
    self.activeWidget.append(blondeButton)
    brownButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_BROWN))
    brownButton.border = 0
    brownButton.padding = 0
    brownButton.topleft = [baseX + sizeX + offset, baseY]
    brownButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "hairColor", 2)
    self.renderer.add_widget(brownButton)
    self.activeWidget.append(brownButton)
    blackButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.COLOR_BLACK))
    blackButton.border = 0
    blackButton.padding = 0
    blackButton.topleft = [baseX + sizeX * 2 + offset * 2, baseY]
    blackButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "hairColor", 3)
    self.renderer.add_widget(blackButton)
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
    self.renderer.add_widget(skin1Button)
    self.activeWidget.append(skin1Button)
    skin2Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_2))
    skin2Button.border = 0
    skin2Button.padding = 0
    skin2Button.topleft = [baseX + sizeX + offset, baseY]
    skin2Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 2)
    self.renderer.add_widget(skin2Button)
    self.activeWidget.append(skin2Button)
    skin3Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_3))
    skin3Button.border = 0
    skin3Button.padding = 0
    skin3Button.topleft = [baseX + sizeX * 2 + offset * 2, baseY]
    skin3Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 3)
    self.renderer.add_widget(skin3Button)
    self.activeWidget.append(skin3Button)
    skin4Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_4))
    skin4Button.border = 0
    skin4Button.padding = 0
    skin4Button.topleft = [baseX, baseY + sizeY + offset]
    skin4Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 4)
    self.renderer.add_widget(skin4Button)
    self.activeWidget.append(skin4Button)
    skin5Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_5))
    skin5Button.border = 0
    skin5Button.padding = 0
    skin5Button.topleft = [baseX + sizeX + offset, baseY + sizeY + offset]
    skin5Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 5)
    self.renderer.add_widget(skin5Button)
    self.activeWidget.append(skin5Button)
    skin6Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_6))
    skin6Button.border = 0
    skin6Button.padding = 0
    skin6Button.topleft = [baseX + sizeX * 2 + offset * 2, baseY + sizeY + offset]
    skin6Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 6)
    self.renderer.add_widget(skin6Button)
    self.activeWidget.append(skin6Button)
    skin7Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_7))
    skin7Button.border = 0
    skin7Button.padding = 0
    skin7Button.topleft = [baseX, baseY + sizeY * 2 + offset * 2]
    skin7Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 7)
    self.renderer.add_widget(skin7Button)
    self.activeWidget.append(skin7Button)
    skin8Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_8))
    skin8Button.border = 0
    skin8Button.padding = 0
    skin8Button.topleft = [baseX + sizeX + offset, baseY + sizeY * 2 + offset * 2]
    skin8Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 8)
    self.renderer.add_widget(skin8Button)
    self.activeWidget.append(skin8Button)
    skin9Button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.SKIN_9))
    skin9Button.border = 0
    skin9Button.padding = 0
    skin9Button.topleft = [baseX + sizeX * 2 + offset * 2, baseY + sizeY * 2 + offset * 2]
    skin9Button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateColorItem, "skin", 9)
    self.renderer.add_widget(skin9Button)
    self.activeWidget.append(skin9Button)
    
  def updateColorItem(self, item, color):
    self.avatarConfiguration[item] = color
    self.paintAvatar()
    
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
    pygame.display.set_caption("DEMO AVATAR GENERATOR")

if __name__=="__main__":
  a = AvatarEditor()
  a.draw()
  
