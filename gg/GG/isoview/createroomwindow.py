# -*- coding: iso-8859-15 -*-

import pygame
import ocempgui.widgets
import GG.utils
import guiobjects
import os

class CreateRoomWindow:
  """ CreateRoomWindow class.
  Defines the create room window.
  """

  def __init__(self, session, player, hud):
    """ Class constructor.
    session: ggsession model.
    title: window title.
    player: active user.
    hud: hud object.
    """
    self.__objectsDict = session.getObjectsData()
    self.__player = player
    self.__hud = hud
    self.hide = True
    self.window = ocempgui.widgets.Window("Creación de habitaciones".decode("utf-8"))
    self.window.topleft = 400, 245
    self.window.zOrder = 10000
    self.selected = None
    self.editableFields = {}
    self.activeLabels = []
    self.__objectsArea = None
    self.tooltipWindow = None
    self.container = None
    self.images = None
    self.sizeX = None
    self.sizeY = None
    self.maxUsers = None
    self.label = None
    self.draw()
    
  def draw(self):
    """ Draws the window components.
    """    
    self.container = ocempgui.widgets.Box(358, 258)
    self.__paintBackground()
    self.__paintAttributes()
    self.__paintButtons()
    
  def setScreenPosition(self, posX, posY):
    """ Sets a new screen position.
    posX: x-axis position component.
    posY: y-axis position component.
    """    
    self.window.topleft = posX, posY  

  def getScreenPosition(self):
    """ Returns the window's screen position.
    """  
    return self.window.topleft

  def getSize(self):
    """ Returns the window's size.
    """  
    return self.container.width, self.container.height     

  def __paintBackground(self):
    """ Paints the background image.
    """  
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/editRoomWindow.png")
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0, 0
    self.container.add_child(imgBackground)
    self.window.child = self.container
     
  def __paintButtons(self):
    """ Paints the control buttons on screen.
    """  
    imgPath = os.path.join(GG.utils.HUD_PATH, "tiny_ok_button.png")
    createButton = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath), "Crear objeto contacto", self.showTooltip, self.removeTooltip)
    createButton.topleft = 150, 220
    createButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.createRoom)
    self.container.add_child(createButton)

  def __paintAttributes(self):
    """ Paints the room attribute values.
    """
    labelShift = [10, -15]
    spacing = 50
    iPos = 0
    
    label = guiobjects.OcempLabel("label", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    
    self.label = guiobjects.OcempEditLine()
    self.label.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.label.text = "habitacion 42"
    self.label.border = 1
    self.label.topleft = 10 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.label.set_minimum_size(150, 20)
    self.container.add_child(self.label)
    iPos += 1
    
    label = guiobjects.OcempLabel("size", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    
    self.sizeX = guiobjects.OcempEditLine()
    self.sizeX.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.sizeX.text = "8"
    self.sizeX.border = 1
    self.sizeX.topleft = 10 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.sizeX.set_minimum_size(50, 20)
    self.container.add_child(self.sizeX)
    
    self.sizeY = guiobjects.OcempEditLine()
    self.sizeY.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.sizeY.text = "8"
    self.sizeY.border = 1
    self.sizeY.topleft = 10 + 65 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.sizeY.set_minimum_size(50, 20)
    self.container.add_child(self.sizeY)
    
    label = guiobjects.OcempLabel("maxUsers", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + 190 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    
    self.maxUsers = guiobjects.OcempEditLine()
    self.maxUsers.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.maxUsers.text = "10"
    self.maxUsers.border = 1
    self.maxUsers.topleft = 10 + 190 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.maxUsers.set_minimum_size(50, 20)
    self.container.add_child(self.maxUsers)
    iPos += 1
    
    label = guiobjects.OcempLabel("images", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    
    height = 60
    self.images = guiobjects.OcempImageList(240, height, GG.utils.TILES, "tiles/")  
    self.images.topleft = 10 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    iPos += 1
    self.container.add_child(self.images)  
    self.activeLabels.append(self.images)
  
  def createRoom(self):
    """ Chechs the attribute values and creates a new room.
    """  
    if not self.images.getSelectedName():
      return  
    label = self.label.text
    try: 
      posX = int(self.sizeX.text)    
    except ValueError:
      self.__player.newChatMessage("Valor \"Dimension X\" incorrecto", 1)
      return
    try: 
      posY = int(self.sizeY.text)    
    except ValueError:
      self.__player.newChatMessage("Valor \"Dimension Y\" incorrecto", 1)
      return
    try: 
      maxUsers = int(self.maxUsers.text)    
    except ValueError:
      self.__player.newChatMessage("Valor \"Capacidad\" incorrecto", 1)
      return
    image = self.images.getSelectedName()
    self.__hud.createRoom(label, [posX, posY], [image], maxUsers)  
     
  def showTooltip(self, label):
    """ Shows the button tooltips.
    """  
    self.tooltipWindow = ocempgui.widgets.TooltipWindow (label)
    xPos, yPos = pygame.mouse.get_pos ()
    self.tooltipWindow.topleft = xPos + 8 - self.window.topleft[0], yPos - 5 - self.window.topleft[1]
    self.tooltipWindow.depth = 99
    self.tooltipWindow.zOrder = 30000
    self.container.add_child(self.tooltipWindow)
      
  def removeTooltip(self): 
    """ Removes a button tooltip.
    """  
    if self.tooltipWindow:
      self.container.remove_child(self.tooltipWindow)  
      self.tooltipWindow.destroy ()
      self.tooltipWindow = None
