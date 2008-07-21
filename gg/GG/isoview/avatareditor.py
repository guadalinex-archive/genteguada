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

  def __init__(self, render, parent, configuration):
    """ Class constructor.
    render: render object used for the ocempgui elements.
    parents: isometric view hud handler.
    configuration: avatar initial configuration.
    """
    self.activeWidget = []
    self.activeOption = ""
    self.avatarConfiguration = configuration 
    self.render = render
    self.parent = parent
    self.finish = False
    self.images = self.loadImagesAvatar()
    self.imagesTag = self.loadImagesTag()
    self.fileDialogShow = False
    self.buttonTooltips = {
        "boy":{"tooltip":"Avatar masculino"},
        "girl":{"tooltip":"Avatar femenino"},
        "summer":{"tooltip":"Ropa de verano"},
        "winter":{"tooltip":"Ropa de invierno"},
        "s":{"tooltip":"Talla S"},
        "m":{"tooltip":"Talla M"},
        "l":{"tooltip":"Talla L"},
        "xl":{"tooltip":"Talla XL"},
        "next":{"tooltip":"Siguiente"},
        "before":{"tooltip":"Anterior"},
        "undo":{"tooltip":"Deshacer"},
        "file":{"tooltip":"Abrir..."},
        "ok":{"tooltip":"Aceptar"},
        "cancel":{"tooltip":"Cancelar"},
    }

  def loadImagesAvatar(self):
    """ Loads the default avatar images.
    """  
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
    """ Loads the editor images.
    """  
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
    """ Handles the mouse and keyboard events.
    """  
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
    """ Draws all the editor elements on screen.    
    """  
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0],GG.utils.SCREEN_SZ[1])
    self.paintScreen()
    self.paintAvatar()
    self.paintTags()
    self.paintCustomizeZone()
    self.paintButtons()
    self.window.zOrder = 90000
    self.window.depth = 2
    return self.window
    
  def paintScreen(self):
    """Paints the Avatar Editor background on screen.
    """
    self.imgBackgroundLeft = GG.utils.OcempImageMapTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left.png"))
    self.window.add_child(self.imgBackgroundLeft)
    imgBackgroundRight = GG.utils.OcempImageMapTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_right.png"))
    imgBackgroundRight.topleft = 297,0
    self.window.add_child(imgBackgroundRight)

  def paintAvatar(self):
    """ Paints the avatar on screen.    
    """
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
    """ Deletes the avatar image.
    imgName: image file name.
    """  
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
    """ Sets a new avatar image.
    imgPath: image file path.
    imgName: image file name.
    """  
    img = ocempgui.draw.Image.load_image(imgPath)
    if not self.images[imgName]: 
      imgOcemp = GG.utils.OcempImageMapTransparent(img)
      imgOcemp.topleft = 528,114
      self.window.add_child(imgOcemp)
      self.images[imgName] = imgOcemp
    else:
      self.images[imgName].picture = img

  def paintBody(self):
    """ Paints the avatar's body.
    """
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], "skin", self.avatarConfiguration["skin"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "body")

  def paintShoes(self):
    """ Paints the avatar's shoes.
    """
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], "shoes", self.avatarConfiguration["shoes"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "shoes")

  def paintShirt(self):
    """ Paints the avatar's shirt.
    """
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], self.avatarConfiguration["typeShirt"]+"_shirt", self.avatarConfiguration["shirt"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "shirt")

  def paintTrousers(self):
    """ Paints the avatar's trousers.
    """
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], self.avatarConfiguration["typeTrousers"]+"_trousers", self.avatarConfiguration["trousers"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "trousers")

  def paintSkirt(self):
    """ Paints the avatar's skirt.
    """
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], self.avatarConfiguration["typeSkirt"]+"_skirt", self.avatarConfiguration["skirt"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "skirt")

  def paintHead(self):
    """ Paints the avatar's head.
    """
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], "head", self.avatarConfiguration["skin"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "head")

  def paintHair(self):
    """ Paints the avatar's hair.
    """
    imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], "hair_"+self.avatarConfiguration["hairStyle"], self.avatarConfiguration["hairColor"] + GG.utils.IMG_EXTENSION)
    self.newAvatarImage(imgPath, "hair")

  def paintMask(self):
    """ Paints the avatar's mask.
    """
    if self.avatarConfiguration["mask"]:
      imgPath = os.path.join(GG.utils.PATH_PHOTO_MASK, "imgUploadMask.png")
    else:
      imgPath = os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], "mask.png")
    self.newAvatarImage(imgPath, "mask")

  def paintTags(self):
    """Paints the Tags Zone.
    """
    imagesTagOrder = ["gender","skin","head","body","mask","hair","shirt","trousers","skirt","shoes"]
    pos = 0
    for img in imagesTagOrder:
      self.imagesTag[img].topleft = 296, pos * 76
      self.imagesTag[img].connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.paintCustomizeZone, img)
      self.window.add_child(self.imagesTag[img])
      pos += 1

  def changeImageTab(self, idTag):
    """ Changes the tab's image.
    idTag: new image id.
    """
    imgPath = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, self.activeOption+"_back.png")
    self.imagesTag[self.activeOption].picture = ocempgui.draw.Image.load_image(imgPath)
    imgPath = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, idTag+"_front.png")
    self.imagesTag[idTag].picture = ocempgui.draw.Image.load_image(imgPath)

  def changeBackgroundLeft(self, image):
    """ Changes the left background.
    image: new background.
    """  
    imgPath = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, image)
    self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(imgPath)

  def paintCustomizeZone(self,idTag = None):
    """Paints the Customize Zone.
    idTag: tag identifier. 
    """
    if self.fileDialogShow:
      return
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
      self.paintColorPalette(self.updateSkin, "skin", "skin")
    elif idTag == "head":
      self.changeBackgroundLeft("background_left.png")
      self.paintSizePalette(self.updateSizeHead)
    elif idTag == "body":
      self.changeBackgroundLeft("background_left.png")
      self.paintSizePalette(self.updateSizeBody)
    elif idTag == "mask": 
      self.changeBackgroundLeft("background_left.png")
      self.paintSelectionItem("mask")
      self.paintMaskOptions()
    elif idTag == "hair":
      self.changeBackgroundLeft("background_left_small_palette.png")
      self.paintColorPalette(self.updateHairColor, "hair", "hair")
    elif idTag == "shirt":
      self.changeBackgroundLeft("background_left_big_palette.png")
      self.paintColorPalette(self.updateShirtColor, "cloth", "shirt")
      self.paintWinterSelection("typeShirt")
    elif idTag == "trousers":
      self.changeBackgroundLeft("background_left_big_palette.png")
      self.paintColorPalette(self.updateTrouserColor, "cloth", "trousers")
      self.paintWinterSelection("typeTrousers")
    elif idTag == "skirt":
      self.changeBackgroundLeft("background_left_big_palette.png")
      self.paintColorPalette(self.updateSkirtColor, "cloth", "skirt")
      self.paintWinterSelection("typeSkirt")
    elif idTag == "shoes":
      self.changeBackgroundLeft("background_left_big_palette.png")
      self.paintColorPalette(self.updateShoesColor, "cloth", "shoes")

    self.activeOption = idTag
      
  def removeWidgets(self):
    """ Remove the screen active widgets.
    """  
    for widget in self.activeWidget:
      if widget in self.window.children:
        self.window.remove_child(widget)
        widget.destroy()
    self.activeWidget = []

  def paintGenderFrame(self):
    """ Paints the gender frames on screen.
    """  
    maleButton = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "boy_button.png"), self.buttonTooltips["boy"]['tooltip'], self.showTooltip, self.removeTooltip)
    maleButton.topleft = [73, 191]
    maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "boy")
    self.window.add_child(maleButton)
    self.activeWidget.append(maleButton)
     
    femaleButton = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "girl_button.png"), self.buttonTooltips["girl"]['tooltip'], self.showTooltip, self.removeTooltip)
    femaleButton.topleft = [73, 441]
    femaleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "girl")
    self.window.add_child(femaleButton)
    self.activeWidget.append(femaleButton)
    
  def updateGender(self, gender):
    """ Updates the Avatar Composite Zone with the appropiate gender.
    gender: new gender.
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
      self.delAvatarImage("head")
      self.delAvatarImage("hair")
      self.delAvatarImage("mask")
      self.paintHead()
      self.paintHair()
      self.paintMask()
  
  def paintColorPalette(self, method, type, tag):
    """ Paints the color palette on screen.
    method: method used to paint.
    type: palette type.
    tag: active tag.
    """  
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
    self.paintSelectionItem(tag)

  def paintSelectionItem(self, tag):
    """ Paints the selection item.
    tag: active tag.
    """  
    if tag == "skin":
      self.paintOptions(["skin.png"], "skin")
    elif tag == "mask":
      if self.avatarConfiguration["gender"] == "boy":
        self.paintOptions(["masko.png"], "mask")
      else:
        self.paintOptions(["maska.png"], "mask")

    elif tag == "hair":
      if self.avatarConfiguration["gender"] == "boy":
        self.paintOptions(["hair1o.png","hair2o.png","hair3o.png"], "hairStyle")
      else:
        self.paintOptions(["hair1a.png","hair2a.png","hair3a.png"], "hairStyle")
    elif tag == "shirt":
      self.paintOptions(["shirt.png"], "typeShirt")
    elif tag == "trousers":
      self.paintOptions(["trousers.png"], "typeTrousers")
    elif tag == "skirt":
      self.paintOptions(["skirt.png"], "typeSkirt")
    elif tag == "shoes":
      self.paintOptions(["shoes.png"], "shoes")

  def paintOptions(self, options, tag):
    """ Paints the tag options on screen.
    options: active options.
    tag: active tag.
    """  
    if len(options) > 1:
      img = options[int(self.avatarConfiguration[tag]) - 1]

      buttonLeft = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "left_button.png"), self.buttonTooltips["before"]['tooltip'], self.showTooltip, self.removeTooltip)
      buttonLeft.topleft = 30,400
      buttonLeft.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.moveOptions, "left", options, tag)
      self.window.add_child(buttonLeft)
      self.activeWidget.append(buttonLeft)
      buttonRight = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "right_button.png"), self.buttonTooltips["next"]['tooltip'], self.showTooltip, self.removeTooltip)
      buttonRight.topleft = 200,400
      buttonRight.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.moveOptions, "right", options, tag)
      self.window.add_child(buttonRight)
      self.activeWidget.append(buttonRight)
    else:
      img = options[0]

    if tag == "mask" and self.avatarConfiguration["mask"]:
      self.imgOptionsTab = GG.utils.OcempImageMapTransparent(os.path.join(GG.utils.PATH_PHOTO_MASK, "imgUpload.png"))
    else:
      self.imgOptionsTab = GG.utils.OcempImageMapTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, img))
    self.imgOptionsTab.topleft = 30,150
    self.activeWidget.append(self.imgOptionsTab)
    self.window.add_child(self.imgOptionsTab)
  
  def moveOptions(self, direction, options, tag):
    """ Shifts options on screen.
    direction: shift direction.
    options: options to be moved.
    tag: active tag.
    """  
    if direction == "left":
      if int(self.avatarConfiguration[tag]) == 1:
        return
      newImgIndex = int(self.avatarConfiguration[tag]) - 1
    else:
      if int(self.avatarConfiguration[tag]) == len(options):
        return
      newImgIndex = int(self.avatarConfiguration[tag]) + 1

    self.avatarConfiguration[tag] = str(newImgIndex)
    imgPath = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, options[int(self.avatarConfiguration[tag]) - 1])
    img = ocempgui.draw.Image.load_image(imgPath)
    self.imgOptionsTab.picture = img
    self.updateAvatar(tag)

  def updateAvatar(self, tag):
    """ Updates the avatar.
    tag: active tag.
    """  
    if tag == "hairStyle":
      self.paintHair()
    elif tag == "typeShirt":
      self.paintShirt()
    elif tag == "typeTrousers":
      self.paintTrousers()
    elif tag == "typeSkirt":
      self.paintSkirt()
      
  def paintWinterSelection(self, tag):
    """ Paints the winter mode for the selected tag items.
    tag: selected tag.
    """  
    buttonWinter = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "winter_button.png"), self.buttonTooltips["winter"]['tooltip'], self.showTooltip, self.removeTooltip)
    buttonWinter.topleft = 20,20
    buttonWinter.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.changeCloth, "long", tag)
    self.window.add_child(buttonWinter)
    self.activeWidget.append(buttonWinter)
    buttonSummer = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "summer_button.png"), self.buttonTooltips["summer"]['tooltip'], self.showTooltip, self.removeTooltip)
    buttonSummer.topleft = 150,20
    buttonSummer.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.changeCloth, "short", tag)
    self.window.add_child(buttonSummer)
    self.activeWidget.append(buttonSummer)

  def changeCloth(self, type, tag):
    """ Changes the avatar's clothes.
    type: clothes type.
    tag: active tag.
    """  
    self.avatarConfiguration[tag] = type
    self.updateAvatar(tag)

  def paintMaskOptions(self):
    """ Paints the mask options on screen.
    """  
    buttonMask = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "undo.png"), self.buttonTooltips["undo"]['tooltip'], self.showTooltip, self.removeTooltip)
    buttonMask.topleft = 30,500
    buttonMask.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.changeMask, "mask")
    self.window.add_child(buttonMask)
    self.activeWidget.append(buttonMask)
    buttonFileChooser = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "file_button.png"), self.buttonTooltips["file"]['tooltip'], self.showTooltip, self.removeTooltip)
    buttonFileChooser.topleft = 150,500
    buttonFileChooser.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.changeMask, "file")
    self.window.add_child(buttonFileChooser)
    self.activeWidget.append(buttonFileChooser)

  def changeMask(self, mask):
    """ Changes the mask image.
    mask: new mask mode.
    """  
    if self.fileDialogShow:
      return

    if mask == "file":
      self.fileDialogShow = True
      self.openFileDialog()
    else:
      if self.avatarConfiguration["gender"] == "boy":
        img = "masko.png"
      else:
        img = "maska.png"
      imgPath = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, img)
      img = ocempgui.draw.Image.load_image(imgPath)
      self.imgOptionsTab.picture = img 
      self.avatarConfiguration["mask"] = None

  def openFileDialog(self):
    """ Opens the OpenFile dialog.
    """  
    self.dialog = ocempgui.widgets.Box(373,372)
    self.dialog.topleft = 528, 205

    background = GG.utils.OcempImageMapTransparent(os.path.join(GG.utils.PATH_EDITOR_BACKGROUNDS, "uploadWindow.png"))
    self.dialog.add_child(background)
    
    self.listDir = GG.utils.OcempImageFileList(310,239)
    self.listDir.topleft = 31,60
    self.dialog.add_child(self.listDir)

    buttonOK = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "ok_button.png"), self.buttonTooltips["ok"]['tooltip'], self.parent.showTooltip, self.parent.removeTooltip)
    buttonOK.topleft = [233, 308]
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.closeFileDialog,"OK")
    self.dialog.add_child(buttonOK)
     
    buttonCancel = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "cancel_button.png"), self.buttonTooltips["cancel"]['tooltip'], self.parent.showTooltip, self.parent.removeTooltip)
    buttonCancel.topleft = [122, 308]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.closeFileDialog,"KO")
    self.dialog.add_child(buttonCancel)

    self.window.add_child (self.dialog)

  def closeFileDialog(self, result):
    """ Opens the close file dialog.
    result: file dialog result.
    """  
    filePath = None
    if result == "OK":
      filePath = self.listDir.getFileName()
    if filePath:
      self.showImage(filePath)
    self.window.remove_child(self.dialog)
    self.dialog.destroy()
    self.fileDialogShow = False

  def showImage(self, filePath):
    """ Show a loaded image.
    filePath: image path.
    """  
    from PIL import Image
    path, file = os.path.split(filePath)
    size = 244,244 
    try:
      img = Image.open(filePath)
    except:
      return 
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(os.path.join(GG.utils.PATH_PHOTO_MASK,"imgUpload.png"))
    imgPath = os.path.join(GG.utils.PATH_PHOTO_MASK,"imgUpload.png")
    img = ocempgui.draw.Image.load_image(imgPath)
    self.imgOptionsTab.picture = img
    self.generateMask("imgUpload.png")

  def generateMask(self,nameFile):
    """ Generates a new mask from an image file.
    nameFile: image file name.
    """  
    from PIL import Image
    imgPath = os.path.join(GG.utils.PATH_PHOTO_MASK, nameFile)
    imgMask = Image.open(os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"],self.avatarConfiguration["headSize"], "mask.png"))
    imgTemplate = Image.open(os.path.join(GG.utils.PATH_EDITOR_IMG, self.avatarConfiguration["gender"],self.avatarConfiguration["headSize"], "template.png"))
    imgUpload = Image.open(imgPath)
    size = GG.utils.MASK_SIZE[self.avatarConfiguration["headSize"]]
    imgUploadResized = imgUpload.resize(size, Image.ANTIALIAS)
    imgMask.paste(imgUploadResized,GG.utils.MASK_COORD[self.avatarConfiguration["headSize"]],imgTemplate)
    imgMask.save(os.path.join(GG.utils.PATH_PHOTO_MASK,"imgUploadMask.png"))
    self.avatarConfiguration["mask"] = "imgUploadMask.png"
    self.paintMask()

  def getPaletteButtons(self, type):
    """ Returns the selected palette buttons.
    type: selected palette.
    """  
    if type == "cloth":
      return [ [GG.utils.COLOR_YELLOW, GG.utils.COLOR_ORANGE, GG.utils.COLOR_RED], 
               [GG.utils.COLOR_PINK, GG.utils.COLOR_BLUE, GG.utils.COLOR_PURPLE], 
               [GG.utils.COLOR_GREEN, GG.utils.COLOR_WHITE, GG.utils.COLOR_BLACK] ] 
    elif type == "hair":
      return [ [GG.utils.COLOR_BLONDE, GG.utils.COLOR_BROWN, GG.utils.COLOR_BLACK] ]
    elif type == "skin":
      return [ [GG.utils.SKIN_1, GG.utils.SKIN_2, GG.utils.SKIN_3], 
               [GG.utils.SKIN_4, GG.utils.SKIN_5, GG.utils.SKIN_6], 
               [GG.utils.SKIN_7, GG.utils.SKIN_8, GG.utils.SKIN_9]]
    else:
      return []

  def updateColorItem(self, item, color):
    """ Updates an item color.
    item: item to be updated.
    color: new color.
    """  
    self.avatarConfiguration[item] = color
    self.paintAvatarItem(item)

  def updateSkin(self,color):
    """ Updates the avatar's skin color.
    color: new skin color.
    """  
    self.avatarConfiguration["skin"] = str(color)
    self.paintBody()
    self.paintHead()
  
  def updateHairColor(self,color):
    """ Updates the avatar's hair color.
    color: new hair color.
    """  
    self.avatarConfiguration["hairColor"] = str(color)
    self.paintHair()

  def updateShirtColor(self,color):
    """ Updates the avatar's shirt color.
    color: new shirt color.
    """  
    self.avatarConfiguration["shirt"] = str(color)
    self.paintShirt()

  def updateTrouserColor(self,color):
    """ Updates the avatar's trousers color.
    color: new trousers color.
    """  
    self.avatarConfiguration["trousers"] = str(color)
    self.paintTrousers()

  def updateSkirtColor(self,color):
    """ Updates the avatar's skirt color.
    color: new skirt color.
    """  
    self.avatarConfiguration["skirt"] = str(color)
    self.paintSkirt()

  def updateShoesColor(self,color):
    """ Updates the avatar's shoes color.
    color: new shoes color.
    """  
    self.avatarConfiguration["shoes"] = str(color)
    self.paintShoes()

  def paintSizePalette(self, method):
    """ Paints the avatar size palette.
    method: method used to paint the palette.
    """  
    baseX = 70
    baseY = 70
    sizeY = 150
    offset = 10
    buttons = ["s","m","l","xl"]
    for i in range(len(buttons)):
      button = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, buttons[i]+".png"), self.buttonTooltips[buttons[i]]['tooltip'], self.showTooltip, self.removeTooltip)
      button.topleft = [baseX , baseY + sizeY * i + offset * i]
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, method, buttons[i].upper())
      self.window.add_child(button)
      self.activeWidget.append(button)

  def updateSizeHead(self,size):
    """ Updates the head size.
    size: new head size.
    """  
    self.avatarConfiguration["headSize"] = size
    self.paintHead()
    self.paintHair()
    if (self.avatarConfiguration["mask"]):
      self.generateMask("imgUpload.png")
    self.paintMask()

  def updateSizeBody(self,size):
    """ Updates the body size.
    size: new body size.
    """  
    self.avatarConfiguration["bodySize"] = size
    self.paintBody()
    self.paintShoes()
    if self.avatarConfiguration["gender"] == "boy":
      self.paintShirt()
      self.paintTrousers()
    else:
      self.paintSkirt()

  def paintButtons(self):
    """ Paints the editor buttons.
    """
    buttonOK = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "ok_button.png"), self.buttonTooltips["ok"]['tooltip'], self.showTooltip, self.removeTooltip)
    buttonOK.topleft = [770, 30]
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.changeConfiguration)
    self.window.add_child(buttonOK)
     
    buttonCancel = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "cancel_button.png"), self.buttonTooltips["cancel"]['tooltip'], self.showTooltip, self.removeTooltip)
    buttonCancel.topleft = [890, 30]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.closeConfiguration)
    self.window.add_child(buttonCancel)

  def changeConfiguration(self):
    """ Closes the avatar editor and changes the avatar configuration.
    """  
    self.finish = True
    self.parent.closeDresser(self.avatarConfiguration)

  def closeConfiguration(self):
    """ Closes the avatar editor without saving the changes.
    """
    self.finish = True
    self.parent.closeDresser()
    
  def showTooltip(self, label):
    """ Shows tooltips for an ocempgui item.
    label: tooltip's label.
    """  
    self.tooltipWindow = ocempgui.widgets.TooltipWindow (label)
    x, y = pygame.mouse.get_pos ()
    self.tooltipWindow.topleft = x + 8, y - 5
    self.tooltipWindow.depth = 99 # Make it the topmost widget.
    self.tooltipWindow.zOrder = 30000
    self.window.add_child(self.tooltipWindow)
      
  def removeTooltip(self):
    """ Removes the active tooltip from screen.
    """  
    if self.tooltipWindow:
      self.window.remove_child(self.tooltipWindow)  
      self.tooltipWindow.destroy ()
      self.tooltipWindow = None
