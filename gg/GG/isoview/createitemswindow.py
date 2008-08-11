# -*- coding: iso-8859-15 -*-

import pygame
import ocempgui.widgets
import GG.utils
import guiobjects

class CreateItemsWindow:
  """ CreateItemsWindow class.
  Defines the create item window.
  """

  def __init__(self, session, title, player, hud):
    """ Class constructor.
    session: ggsession model.
    title: window title.
    player: active user.
    hud: hud object.
    """
    self.__session = session
    self.__objectsDict = session.getObjectsData()
    self.__player = player
    self.__hud = hud
    self.hide = False
    self.window = ocempgui.widgets.Window(title)
    self.window.topleft = 0, 0
    self.window.zOrder = 10000
    self.player = player
    self.selected = None
    self.editableFields = {}
    self.activeLabels = []
    self.__objectsArea = None
    self.tooltipWindow = None
    self.container = None
    self.images = None
    self.draw()

  def draw(self):
    """ Draws the window components.
    """  
    self.container = ocempgui.widgets.Box(373, 390)
    self.__paintBackground()
    self.__paintObjectsList()
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
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/createObjectWindow.png")
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0, 0
    self.container.add_child(imgBackground)
    self.window.child = self.container
    
    #itemsLabel = guiobjects.OcempLabel("Objetos", guiobjects.STYLES["userName"])
    itemsLabel = guiobjects.OcempLabel("Objetos", guiobjects.STYLES["pointLabel"])
    #itemsLabel.topleft = 20, 20
    itemsLabel.topleft = 20, 10
    self.container.add_child(itemsLabel)
    
    #itemsPropertiesLabel = guiobjects.OcempLabel("Propiedades del objeto", guiobjects.STYLES["userName"])
    itemsPropertiesLabel = guiobjects.OcempLabel("Propiedades del objeto", guiobjects.STYLES["pointLabel"])
    #itemsPropertiesLabel.topleft = 150, 20
    itemsPropertiesLabel.topleft = 160, 10
    self.container.add_child(itemsPropertiesLabel)
  
  def __paintObjectsList(self):
    """ Paints the item list.
    """  
    objectsLabels = self.__objectsDict.keys()
    objectsLabels.sort()
    self.__objectsArea = guiobjects.OcempImageObjectList(130, 270, objectsLabels)
    self.__objectsArea.topleft = 20, 50
    self.__objectsArea.connect_signal (ocempgui.widgets.Constants.SIG_SELECTCHANGED, self.__selectionChange)
    self.container.add_child(self.__objectsArea)  
   
  def __paintButtons(self):
    """ Paints the control buttons on screen.
    """  
    createButton = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.HUD_PATH + "tiny_ok_button.png"), "Crear objeto contacto", self.showTooltip, self.removeTooltip)
    createButton.topleft = 20, 340
    createButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.createObject)
    self.container.add_child(createButton)

    defaultButton = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.HUD_PATH + "tiny_cancel_button.png"), "Restaurar a valores por defecto", self.showTooltip, self.removeTooltip)
    defaultButton.topleft = 90, 340
    defaultButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.restoreDeafultValues)
    self.container.add_child(defaultButton)

  def __selectionChange(self):
    """ Updates the selected item info ater a selection change.
    """  
    labelShift = [153, 10]
    spacing = 45
    self.editableFields = []
    name = self.__objectsArea.getSelectedName()
    attrDict = self.__objectsDict[name]
    
    for label in self.activeLabels:
      self.container.remove_child(label)
    self.activeLabels = []  
    self.editableFields = {}
    
    iPos = 0
    keys = attrDict.keys()
    keys.sort()
    
    for key in keys:
    
      #label = guiobjects.OcempLabel(key, guiobjects.STYLES["itemLabel"])
      label = guiobjects.OcempLabel(key, guiobjects.STYLES["itemLabel"])
      #label.topleft = 10 + labelShift[0], 40 + iPos*spacing + labelShift[1]
      label.topleft = 10 + labelShift[0], 25 + iPos*spacing + labelShift[1]
      self.container.add_child(label)
      self.activeLabels.append(label)
      
      if key == "images":
        #height = len(attrDict[key])*20
        height = 60
        self.images = guiobjects.OcempImageList(190, height, attrDict[key], "furniture/")  
        self.images.topleft = 10 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
        iPos += 1
        self.container.add_child(self.images)  
        self.activeLabels.append(self.images)
        self.editableFields[key] = self.images
      else:  
        
        fCount = 0
        fields = []
        for field in attrDict[key]:
          entryLabel = guiobjects.OcempEditLine()
          entryLabel.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
          entryLabel.text = str(field)
          entryLabel.border = 1
          entryLabel.topleft = 10 + fCount*65 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
          if len(attrDict[key]) == 1:
            entryLabel.set_minimum_size(125, 20)
          else:    
            entryLabel.set_minimum_size(50, 20)
          self.container.add_child(entryLabel)
          self.activeLabels.append(entryLabel)
        
          fields.append(entryLabel)
          fCount += 1
        self.editableFields[key] = fields
      iPos += 1
    
  def paintImagesList(self):
    """ Paints the image list.
    """  
    objectsLabels = self.__objectsDict.keys()
    objectsLabels.sort()
    self.__objectsArea = guiobjects.OcempImageObjectList(130, 270, objectsLabels)
    self.__objectsArea.topleft = 20, 40
    self.__objectsArea.connect_signal (ocempgui.widgets.Constants.SIG_SELECTCHANGED, self.__selectionChange)
    self.container.add_child(self.__objectsArea)  
    
  def createObject(self):
    """ Gathers the item attribute values and returns them.
    """  
    if not self.__objectsArea.getSelectedName():
      return  
    self.__hud.createItemsHandler()  
    name = self.__objectsArea.getSelectedName()
    data = {}
    keys = self.editableFields.keys()
    for key in keys:
      if key == "images":
        data[key] = self.editableFields[key].getSelectedName()
      else:      
        values = []
        for field in self.editableFields[key]:
          values.append(field.text)
        #data.append([key, values])
        data[key] = values
    self.__session.createObject(name, data)  
      
  def restoreDeafultValues(self):
    """ Restores the item attribute values.
    """  
    if self.__objectsArea.getSelectedName(): 
      self.__selectionChange()  
    
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
