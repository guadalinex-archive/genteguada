# -*- coding: iso-8859-15 -*-

import pygame
import ocempgui.widgets
import GG.utils
import guiobjects

class CreateItemsWindow:

  def __init__(self, session, title, player, hud):
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
    self.draw()

  def draw(self):
    self.container = ocempgui.widgets.Box(373,372)
    self.__paintBackground()
    self.__paintObjectsList()
    self.__paintButtons()
    
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
  
  def __paintObjectsList(self):
    objectsLabels = self.__objectsDict.keys()
    objectsLabels.sort()
    self.__objectsArea = guiobjects.OcempImageObjectList(130, 270, objectsLabels)
    self.__objectsArea.topleft = 20, 40
    self.__objectsArea.connect_signal (ocempgui.widgets.Constants.SIG_SELECTCHANGED, self.__selectionChange)
    self.container.add_child(self.__objectsArea)  
   
  def __paintButtons(self):
    createButton = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.HUD_PATH + "tiny_ok_button.png"), "Crear objeto contacto", self.showTooltip, self.removeTooltip)
    createButton.topleft = 20, 325
    createButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.createObject)
    self.container.add_child(createButton)

    defaultButton = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.HUD_PATH + "tiny_cancel_button.png"), "Restaurar a valores por defecto", self.showTooltip, self.removeTooltip)
    defaultButton.topleft = 90, 325
    defaultButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.restoreDeafultValues)
    self.container.add_child(defaultButton)

  def __selectionChange(self):
    labelShift = [150, 0]
    spacing = 50
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
      label = guiobjects.OcempLabel(key, 290, guiobjects.STYLES["itemLabel"])
      label.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["itemLabel"]))
      label.topleft = 10 + labelShift[0], 40 + iPos*spacing + labelShift[1]
      self.container.add_child(label)
      self.activeLabels.append(label)
        
      fCount = 0
      fields = []
      for field in attrDict[key]:
        entryLabel = ocempgui.widgets.Entry()
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
    
  def createObject(self):
    if not self.__objectsArea.getSelectedName():
      return  
    self.__hud.createItemstHandler()  
    name = self.__objectsArea.getSelectedName()
    #data = []
    data = {}
    keys = self.editableFields.keys().sort()
    for key in keys:
      values = []
      for field in self.editableFields[key]:
        values.append(field.text)
      #data.append([key, values])
      data[key] = values
    self.__session.createObject(name, data)  
      
  def restoreDeafultValues(self):
    if self.__objectsArea.getSelectedName(): 
      self.__selectionChange()  
    
  def showTooltip(self, label):
    self.tooltipWindow = ocempgui.widgets.TooltipWindow (label)
    x, y = pygame.mouse.get_pos ()
    self.tooltipWindow.topleft = x + 8 - self.window.topleft[0], y - 5 - self.window.topleft[1]
    self.tooltipWindow.depth = 99
    self.tooltipWindow.zOrder = 30000
    self.container.add_child(self.tooltipWindow)
      
  def removeTooltip(self): 
    if self.tooltipWindow:
      self.container.remove_child(self.tooltipWindow)  
      self.tooltipWindow.destroy ()
      self.tooltipWindow = None
