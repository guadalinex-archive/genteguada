# -*- coding: utf-8 -*- 

import isoview
import ocempgui.widgets
import pygame
import GG
import guiobjects
import os

NEW_SIZE = [60, 60]

class IsoViewInventoryItem(isoview.IsoView):
  """ IsoViewInventoryItem class.
  Defines an inventory item view.
  """
    
  def __init__(self, model, screen, isohud, name = None):
    """ Class constructor.
    model: inventory item model.
    screen: screen handler.
    isohud: isometric view hud handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__spriteName = model.spriteInventory
    if name:
      self.__label = name
    else:
      self.__label = model.getName()
    self.__count = 0
    self.__isohud = isohud
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(model.spriteInventory)
    self.__img = guiobjects.getSprite(model.spriteInventory, None, 10001)
    
  def updateZOrder(self):
    """ Updates the item image zOrder value.
    """  
    self.__img.zOrder = 10001  
  
  def getImg(self):
    """ Returns the item's image.
    """  
    return self.__img  

  def setScreenPosition(self, pos):
    """ Sets a new position for the item's image.
    pos: new position.
    """
    self.__img.rect.topleft = pos  
  
  def getScreenPosition(self):
    """ Returns the item's image position.
    """
    return self.__img.rect.topleft  
  
  def getSpriteName(self):
    """ Returns the name of the sprite used to paint the item on the inventory.
    """
    return self.__spriteName

  def getLabel(self):
    """ Returns the itemp's label.
    """
    return self.__label
  
  def getCount(self):
    """ Returns the number of stacked items.
    """
    return self.__count
  
  def increaseCount(self):
    """ Increases by 1 the number of stacked items.
    """
    self.__count += 1
    
  def decreaseCount(self):
    """ Decreases by 1 the number of stacked items.
    """
    self.__count -= 1

  def draw(self, render):
    """ Draws an inventory item.
    render: widget container. 
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.__spriteName)
    tempFileName = os.path.join(GG.utils.LOCAL_DATA_PATH,"INVENTORY-"+str(self.__spriteName.replace(os.sep, "-")))
    guiobjects.generateImageSize(imgPath, NEW_SIZE, tempFileName)
    imgInventory = ocempgui.widgets.ImageButton(tempFileName)
    imgInventory.border = 0
    imgInventory.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.selected)
    render.get_managers()[0].add_high_priority_object(imgInventory, ocempgui.widgets.Constants.SIG_MOUSEDOWN)
    return imgInventory

  def selected(self): 
    """ Sets this item as selected.
    """
    self.__isohud.itemInventorySelected(self)
