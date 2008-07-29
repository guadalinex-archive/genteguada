# -*- coding: iso-8859-15 -*-

import pygame
import ocempgui.widgets
import GG.utils
import guiobjects

class CreateItemsWindow:

  def __init__(self, title, player, hud):
    self.__player = player
    self.__hud = hud
    self.hide = False
    self.window = ocempgui.widgets.Window(title)
    self.window.topleft = 0, 0
    self.window.zOrder = 10000
    self.player = player
    self.selected = None
    self.draw()

  def draw(self):
    self.container = ocempgui.widgets.Box(373,372)
    self.__paintBackground()
    """
    self.__paintContactList()
    self.__paintDeleteButton()
    self.__paintChat()
    self.__paintChatArea()
    return self.window  
    """

  def setScreenPosition(self, x, y):
    self.window.topleft = x, y  

  def getScreenPosition(self):
    return self.window.topleft

  def getSize(self):
    return self.container.width, self.container.height     

  def __paintBackground(self):
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/privateChatWindow.png")
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0,0
    self.container.add_child(imgBackground)
    self.window.child = self.container
    
    itemsLabel = guiobjects.OcempLabel("Objetos", 280, guiobjects.STYLES["userName"])
    itemsLabel.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["userName"]))
    itemsLabel.topleft = 20, 20
    self.container.add_child(itemsLabel)
    
    itemsPropertiesLabel = guiobjects.OcempLabel("Propiedades del objeto", 280, guiobjects.STYLES["userName"])
    itemsPropertiesLabel.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["userName"]))
    itemsPropertiesLabel.topleft = 150, 20
    self.container.add_child(itemsPropertiesLabel)
  