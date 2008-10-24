# -*- coding: utf-8 -*-

import os
import GG.utils
import pygame
import guiobjects

from pygame.locals import * # faster name resolution

import ocempgui.widgets
import ocempgui.draw

from PIL import Image

# ======================= CONSTANTS ===========================
PATH_EDITOR_IMG = "editor"
IMG_EXTENSION = ".png"
MASK_SIZE = {"S":[112, 105], "M":[124, 116], "L":[134, 127], "XL":[146, 137]}
MASK_COORD = {"S":(91, 114), "M":(86, 111), "L":(80, 105), "XL":(74, 100)}
COLOR_YELLOW = "yellow.png"
COLOR_ORANGE = "orange.png"
COLOR_RED = "red.png"
COLOR_PINK = "pink.png"
COLOR_BLUE = "blue.png"
COLOR_PURPLE = "purple.png"
COLOR_GREEN = "green.png"
COLOR_WHITE = "white.png"
COLOR_BLACK = "black.png"
COLOR_BLONDE = "blonde.png"
COLOR_BROWN = "brown.png"
SKIN_1 = "skin_1.png"
SKIN_2 = "skin_2.png"
SKIN_3 = "skin_3.png"
SKIN_4 = "skin_4.png"
SKIN_5 = "skin_5.png"
SKIN_6 = "skin_6.png"
SKIN_7 = "skin_7.png"
SKIN_8 = "skin_8.png"
SKIN_9 = "skin_9.png"

MASK_UPLOAD = os.path.join(GG.utils.PATH_PHOTO_MASK, "imgUploadMask.png")
IMG_UPLOAD = os.path.join(GG.utils.PATH_PHOTO_MASK, "imgUpload.png")


BACKGROUND_LEFT = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_left.png")
BACKGROUND_RIGHT = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "background_right.png")
WINDOW_UPLOAD = os.path.join(GG.utils.BACKGROUNDS, "uploadWindow.png")

BUTTON_UNDO = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "undo.png")
BUTTON_FILE = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "file_button.png")
BUTTON_BOY = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "boy_button.png")
BUTTON_GIRL = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "girl_button.png")
BUTTON_OK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "ok_button.png")
BUTTON_CANCEL = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "cancel_button.png")
BUTTON_LEFT = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "left_button.png")
BUTTON_RIGHT = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "right_button.png")
BUTTON_WINTER = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "winter_button.png")
BUTTON_SUMMER = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "summer_button.png")

SHIRT_BACK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shirt_back.png")
SHIRT_DISABLED = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shirt_disabled.png")
TROUSERS_BACK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "trousers_back.png")
TROUSERS_DISABLED = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "trousers_disabled.png")
SKIRT_BACK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skirt_back.png")
SKIRT_DISABLED = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skirt_disabled.png")
SHOES_BACK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "shoes_back.png")

GENDER_FRONT = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "gender_front.png")
SKIN_BACK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "skin_back.png")
HEAD_BACK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "head_back.png")
BODY_BACK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "body_back.png")
MASK_BACK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "mask_back.png")
HAIR_BACK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "hair_back.png")

# =============================================================

class AvatarEditor:
  """ AvatarEditor class.
  Defines the Avatar Editor
  """

  def __init__(self, parent, configuration):
    """ Class constructor.
    render: render object used for the ocempgui elements.
    parents: isometric view hud handler.
    configuration: avatar initial configuration.
    """
    self.activeWidget = []
    self.activeOption = ""
    self.avatarConfiguration = configuration 
    self.parent = parent
    self.images = self.loadImagesAvatar()
    self.imagesTag = self.loadImagesTag()
    self.fileDialogShow = False
    self.listDir = None
    self.imgOptionsTab = None
    self.tooltipWindow = None
    self.window = None
    self.dialog = None
    self.imgBackgroundLeft = None
    self.buttonTooltips = {
        "boy":    "Avatar masculino",
        "girl":   "Avatar femenino",
        "summer": "Ropa de verano",
        "winter": "Ropa de invierno",
        "s":      "Talla S",
        "m":      "Talla M",
        "l":      "Talla L",
        "xl":     "Talla XL",
        "next":   "Siguiente",
        "before": "Anterior",
        "undo":   "Deshacer",
        "file":   "Abrir...",
        "ok":     "Aceptar",
        "cancel": "Cancelar"
    }

  def loadImagesAvatar(self):
    """ Loads the default avatar images.
    """  
    dictionary = {}
    dictionary["body"] = None
    dictionary["shoes"] = None
    dictionary["shirt"] = None
    dictionary["trousers"] = None
    dictionary["skirt"] = None
    dictionary["head"] = None
    dictionary["hair"] = None
    dictionary["mask"] = None
    return dictionary

  def loadImagesTag(self):
    """ Loads the editor images.
    """  
    dictionary = {}
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GENDER_FRONT)
    dictionary["gender"] = guiobjects.OcempImageButtonTransparent(imgPath)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(SKIN_BACK)
    dictionary["skin"] =  guiobjects.OcempImageButtonTransparent(imgPath)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(HEAD_BACK)
    dictionary["head"] = guiobjects.OcempImageButtonTransparent(imgPath)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(BODY_BACK)
    dictionary["body"] = guiobjects.OcempImageButtonTransparent(imgPath)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(MASK_BACK)
    dictionary["mask"] = guiobjects.OcempImageButtonTransparent(imgPath)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(HAIR_BACK)
    dictionary["hair"] = guiobjects.OcempImageButtonTransparent(imgPath)
    if self.avatarConfiguration["gender"] == "boy":
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(SHIRT_BACK)
      dictionary["shirt"] = guiobjects.OcempImageButtonTransparent(imgPath)
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(TROUSERS_BACK)
      dictionary["trousers"] = guiobjects.OcempImageButtonTransparent(imgPath)
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(SKIRT_BACK)
      dictionary["skirt"] = guiobjects.OcempImageButtonTransparent(imgPath)
    else:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(SHIRT_DISABLED)
      dictionary["shirt"] = guiobjects.OcempImageButtonTransparent(imgPath)
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(TROUSERS_DISABLED)
      dictionary["trousers"] = guiobjects.OcempImageButtonTransparent(imgPath)
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(SKIRT_BACK)
      dictionary["skirt"] = guiobjects.OcempImageButtonTransparent(imgPath)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(SHOES_BACK)
    dictionary["shoes"] = guiobjects.OcempImageButtonTransparent(imgPath)
    return dictionary

  def draw(self):
    """ Draws all the editor elements on screen.    
    """  
    pygame.event.clear()
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0], GG.utils.SCREEN_SZ[1])
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
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(BACKGROUND_LEFT)
    self.imgBackgroundLeft = guiobjects.OcempImageMapTransparent(imgPath)
    self.window.add_child(self.imgBackgroundLeft)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(BACKGROUND_RIGHT)
    imgBackgroundRight = guiobjects.OcempImageMapTransparent(imgPath)
    imgBackgroundRight.topleft = 297, 0
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
      imgOcemp = guiobjects.OcempImageMapTransparent(img)
      imgOcemp.topleft = 528, 114
      self.window.add_child(imgOcemp)
      self.images[imgName] = imgOcemp
    else:
      self.images[imgName].picture = img

  def paintBody(self):
    """ Paints the avatar's body.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], "skin", self.avatarConfiguration["skin"] + IMG_EXTENSION))
    self.newAvatarImage(imgPath, "body")

  def paintShoes(self):
    """ Paints the avatar's shoes.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], "shoes", self.avatarConfiguration["shoes"] + IMG_EXTENSION))
    self.newAvatarImage(imgPath, "shoes")

  def paintShirt(self):
    """ Paints the avatar's shirt.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], self.avatarConfiguration["typeShirt"]+"_shirt", self.avatarConfiguration["shirt"] + IMG_EXTENSION))
    self.newAvatarImage(imgPath, "shirt")

  def paintTrousers(self):
    """ Paints the avatar's trousers.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], self.avatarConfiguration["typeTrousers"]+"_trousers", self.avatarConfiguration["trousers"] + IMG_EXTENSION))
    self.newAvatarImage(imgPath, "trousers")

  def paintSkirt(self):
    """ Paints the avatar's skirt.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["bodySize"], self.avatarConfiguration["typeSkirt"]+"_skirt", self.avatarConfiguration["skirt"] + IMG_EXTENSION))
    self.newAvatarImage(imgPath, "skirt")

  def paintHead(self):
    """ Paints the avatar's head.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], "head", self.avatarConfiguration["skin"] + IMG_EXTENSION))
    self.newAvatarImage(imgPath, "head")

  def paintHair(self):
    """ Paints the avatar's hair.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], "hair_"+self.avatarConfiguration["hairStyle"], self.avatarConfiguration["hairColor"] + IMG_EXTENSION))
    self.newAvatarImage(imgPath, "hair")

  def paintMask(self):
    """ Paints the avatar's mask.
    """
    if self.avatarConfiguration["mask"]:
      if not os.path.isfile(MASK_UPLOAD):
        image = self.parent.getPlayer().getImageLabel()
        filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(image)
        guiobjects.generateImageSize(filePath, [244, 244], IMG_UPLOAD)
        self.generateMask("imgUpload.png")
      imgPath = MASK_UPLOAD
    else:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], "mask.png"))
    self.newAvatarImage(imgPath, "mask")

  def paintTags(self):
    """Paints the Tags Zone.
    """
    imagesTagOrder = ["gender", "skin", "head", "body", "mask", "hair", "shirt", "trousers", "skirt", "shoes"]
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
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, self.activeOption + "_back.png"))
    self.imagesTag[self.activeOption].picture = ocempgui.draw.Image.load_image(imgPath)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, idTag + "_front.png"))
    self.imagesTag[idTag].picture = ocempgui.draw.Image.load_image(imgPath)

  def changeBackgroundLeft(self, image):
    """ Changes the left background.
    image: new background.
    """  
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, image))
    self.imgBackgroundLeft.picture = ocempgui.draw.Image.load_image(imgPath)

  def paintCustomizeZone(self, idTag = None):
    """Paints the Customize Zone.
    idTag: tag identifier. 
    """
    if self.fileDialogShow:
      return
    if idTag == self.activeOption:
      return
    if idTag == "skirt" and self.avatarConfiguration["gender"] == "boy":
      return 
    if self.avatarConfiguration["gender"] == "girl" and idTag in ["shirt", "trousers"]:
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
    maleButton = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_BOY), self.buttonTooltips["boy"], self.showTooltip, self.removeTooltip)
    maleButton.topleft = [73, 191]
    maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "boy")
    self.window.add_child(maleButton)
    self.activeWidget.append(maleButton)
     
    femaleButton = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_GIRL), self.buttonTooltips["girl"], self.showTooltip, self.removeTooltip)
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
        self.imagesTag["shirt"].picture = ocempgui.draw.Image.load_image(GG.genteguada.GenteGuada.getInstance().getDataPath(SHIRT_BACK))
        self.imagesTag["trousers"].picture = ocempgui.draw.Image.load_image(GG.genteguada.GenteGuada.getInstance().getDataPath(TROUSERS_BACK))
        self.imagesTag["skirt"].picture = ocempgui.draw.Image.load_image(GG.genteguada.GenteGuada.getInstance().getDataPath(SKIRT_DISABLED))
        self.delAvatarImage("skirt")
        self.paintShirt()
        self.paintTrousers()
      else:
        self.imagesTag["shirt"].picture = ocempgui.draw.Image.load_image(GG.genteguada.GenteGuada.getInstance().getDataPath(SHIRT_DISABLED))
        self.imagesTag["trousers"].picture = ocempgui.draw.Image.load_image(GG.genteguada.GenteGuada.getInstance().getDataPath(TROUSERS_DISABLED))
        self.imagesTag["skirt"].picture = ocempgui.draw.Image.load_image(GG.genteguada.GenteGuada.getInstance().getDataPath(SKIRT_BACK))
        self.delAvatarImage("shirt")
        self.delAvatarImage("trousers")
        self.paintSkirt()
      self.delAvatarImage("head")
      self.delAvatarImage("hair")
      self.delAvatarImage("mask")
      self.paintHead()
      self.paintHair()
      self.paintMask()
  
  def paintColorPalette(self, method, paletteType, tag):
    """ Paints the color palette on screen.
    method: method used to paint.
    paletteType: palette type.
    tag: active tag.
    """  
    baseX = 35
    sizeX = 70
    if paletteType == "hair":
      baseY = 515
    else:
      baseY = 510
    sizeY = 45
    offset = 10
    buttons = self.getPaletteButtons(paletteType)
    for i in range(len(buttons)):
      for j in range(len(buttons[0])):
        button = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, buttons[i][j])))
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
        self.paintOptions(["hair1o.png", "hair2o.png", "hair3o.png"], "hairStyle")
      else:
        self.paintOptions(["hair1a.png", "hair2a.png", "hair3a.png"], "hairStyle")
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
      buttonLeft = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_LEFT), self.buttonTooltips["before"], self.showTooltip, self.removeTooltip)
      buttonLeft.topleft = 30, 400
      buttonLeft.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.moveOptions, "left", options, tag)
      self.window.add_child(buttonLeft)
      self.activeWidget.append(buttonLeft)
      buttonRight = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_RIGHT), self.buttonTooltips["next"], self.showTooltip, self.removeTooltip)
      buttonRight.topleft = 200, 400
      buttonRight.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.moveOptions, "right", options, tag)
      self.window.add_child(buttonRight)
      self.activeWidget.append(buttonRight)
    else:
      img = options[0]
    if tag == "mask" and self.avatarConfiguration["mask"]:
      if not os.path.isfile(IMG_UPLOAD):
        image = self.parent.getPlayer().getImageLabel()
        filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(image)
        guiobjects.generateImageSize(filePath, [244, 244], IMG_UPLOAD)
      self.imgOptionsTab = guiobjects.OcempImageMapTransparent(IMG_UPLOAD)
    else:
      self.imgOptionsTab = guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, img)))
    self.imgOptionsTab.topleft = 30, 150
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
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, options[int(self.avatarConfiguration[tag]) - 1]))
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
    buttonWinter = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_WINTER), self.buttonTooltips["winter"], self.showTooltip, self.removeTooltip)
    buttonWinter.topleft = 20, 20
    buttonWinter.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.changeCloth, "long", tag)
    self.window.add_child(buttonWinter)
    self.activeWidget.append(buttonWinter)
    buttonSummer = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_SUMMER), self.buttonTooltips["summer"], self.showTooltip, self.removeTooltip)
    buttonSummer.topleft = 150, 20
    buttonSummer.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.changeCloth, "short", tag)
    self.window.add_child(buttonSummer)
    self.activeWidget.append(buttonSummer)

  def changeCloth(self, clothType, tag):
    """ Changes the avatar's clothes.
    clothType: clothes type.
    tag: active tag.
    """  
    self.avatarConfiguration[tag] = clothType
    self.updateAvatar(tag)

  def paintMaskOptions(self):
    """ Paints the mask options on screen.
    """  
    buttonMask = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_UNDO), self.buttonTooltips["undo"], self.showTooltip, self.removeTooltip)
    buttonMask.topleft = 30, 500
    buttonMask.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.changeMask, "mask")
    self.window.add_child(buttonMask)
    self.activeWidget.append(buttonMask)
    buttonFileChooser = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_FILE), self.buttonTooltips["file"], self.showTooltip, self.removeTooltip)
    buttonFileChooser.topleft = 150, 500
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
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, img))
      img = ocempgui.draw.Image.load_image(imgPath)
      self.imgOptionsTab.picture = img 
      self.avatarConfiguration["mask"] = None
      self.paintMask()

  def openFileDialog(self):
    """ Opens the OpenFile dialog.
    """  
    self.dialog = ocempgui.widgets.Box(373, 372)
    self.dialog.topleft = 528, 205

    background = guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(WINDOW_UPLOAD))
    self.dialog.add_child(background)
    
    self.listDir = guiobjects.OcempImageFileList(310, 239)
    self.listDir.topleft = 31, 60
    self.dialog.add_child(self.listDir)

    buttonOK = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_OK), self.buttonTooltips["ok"], self.parent.showTooltip, self.parent.removeTooltip)
    buttonOK.topleft = [233, 308]
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.closeFileDialog,"OK")
    self.dialog.add_child(buttonOK)
     
    buttonCancel = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_CANCEL), self.buttonTooltips["cancel"], self.parent.showTooltip, self.parent.removeTooltip)
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
    size = 244, 244 
    try:
      guiobjects.generateImageSize(filePath, [244, 244], IMG_UPLOAD)
    except:
      return 
    imgPath = IMG_UPLOAD
    img = ocempgui.draw.Image.load_image(imgPath)
    self.imgOptionsTab.picture = img
    self.generateMask("imgUpload.png")

  def generateMask(self, nameFile):
    """ Generates a new mask from an image file.
    nameFile: image file name.
    """  
    imgPath = os.path.join(GG.utils.PATH_PHOTO_MASK, nameFile)
    imgMask = Image.open(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], "mask.png")))
    imgTemplate = Image.open(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(PATH_EDITOR_IMG, self.avatarConfiguration["gender"], self.avatarConfiguration["headSize"], "template.png")))
    imgUpload = Image.open(imgPath)
    size = MASK_SIZE[self.avatarConfiguration["headSize"]]
    imgUploadResized = imgUpload.resize(size, Image.ANTIALIAS)
    imgMask.paste(imgUploadResized, MASK_COORD[self.avatarConfiguration["headSize"]], imgTemplate)
    imgMask.save(MASK_UPLOAD)
    self.avatarConfiguration["mask"] = "imgUploadMask.png"
    self.paintMask()

  def getPaletteButtons(self, paletteType):
    """ Returns the selected palette buttons.
    paletteType: selected palette.
    """  
    if paletteType == "cloth":
      return [ [COLOR_YELLOW, COLOR_ORANGE, COLOR_RED], 
               [COLOR_PINK, COLOR_BLUE, COLOR_PURPLE], 
               [COLOR_GREEN, COLOR_WHITE, COLOR_BLACK] ] 
    elif paletteType == "hair":
      return [ [COLOR_BLONDE, COLOR_BROWN, COLOR_BLACK] ]
    elif paletteType == "skin":
      return [ [SKIN_1, SKIN_2, SKIN_3], 
               [SKIN_4, SKIN_5, SKIN_6], 
               [SKIN_7, SKIN_8, SKIN_9]]
    else:
      return []

  def updateColorItem(self, item, itemColor):
    """ Updates an item color.
    item: item to be updated.
    itemColor: new color.
    """  
    self.avatarConfiguration[item] = itemColor
    self.paintAvatarItem(item)

  def updateSkin(self, skinColor):
    """ Updates the avatar's skin color.
    skinColor: new skin color.
    """  
    self.avatarConfiguration["skin"] = str(skinColor)
    self.paintBody()
    self.paintHead()
  
  def updateHairColor(self, hairColor):
    """ Updates the avatar's hair color.
    hairColor: new hair color.
    """  
    self.avatarConfiguration["hairColor"] = str(hairColor)
    self.paintHair()

  def updateShirtColor(self, shirtColor):
    """ Updates the avatar's shirt color.
    shirtColor: new shirt color.
    """  
    self.avatarConfiguration["shirt"] = str(shirtColor)
    self.paintShirt()

  def updateTrouserColor(self, trouserColor):
    """ Updates the avatar's trousers color.
    trouserColor: new trousers color.
    """  
    self.avatarConfiguration["trousers"] = str(trouserColor)
    self.paintTrousers()

  def updateSkirtColor(self, skirtColor):
    """ Updates the avatar's skirt color.
    skirtColor: new skirt color.
    """  
    self.avatarConfiguration["skirt"] = str(skirtColor)
    self.paintSkirt()

  def updateShoesColor(self, shoesColor):
    """ Updates the avatar's shoes color.
    shoesColor: new shoes color.
    """  
    self.avatarConfiguration["shoes"] = str(shoesColor)
    self.paintShoes()

  def paintSizePalette(self, method):
    """ Paints the avatar size palette.
    method: method used to paint the palette.
    """  
    baseX = 70
    baseY = 70
    sizeY = 150
    offset = 10
    buttons = ["s", "m", "l", "xl"]
    for i in range(len(buttons)):
      button = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, buttons[i] + ".png")), self.buttonTooltips[buttons[i]], self.showTooltip, self.removeTooltip)
      button.topleft = [baseX , baseY + sizeY * i + offset * i]
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, method, buttons[i].upper())
      self.window.add_child(button)
      self.activeWidget.append(button)

  def updateSizeHead(self, size):
    """ Updates the head size.
    size: new head size.
    """  
    self.avatarConfiguration["headSize"] = size
    self.paintHead()
    self.paintHair()
    if (self.avatarConfiguration["mask"]):
      self.generateMask("imgUpload.png")
    self.paintMask()

  def updateSizeBody(self, size):
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

    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_OK)
    buttonOK = guiobjects.OcempImageButtonTransparent(imgPath, self.buttonTooltips["ok"], self.showTooltip, self.removeTooltip)
    buttonOK.topleft = [770, 30]
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.changeConfiguration)
    self.window.add_child(buttonOK)

    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_CANCEL)
    buttonCancel = guiobjects.OcempImageButtonTransparent(imgPath, self.buttonTooltips["cancel"], self.showTooltip, self.removeTooltip)
    buttonCancel.topleft = [890, 30]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.closeConfiguration)
    self.window.add_child(buttonCancel)

  def changeConfiguration(self):
    """ Closes the avatar editor and changes the avatar configuration.
    """  
    self.parent.closeDresser(self.avatarConfiguration)

  def closeConfiguration(self):
    """ Closes the avatar editor without saving the changes.
    """
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
