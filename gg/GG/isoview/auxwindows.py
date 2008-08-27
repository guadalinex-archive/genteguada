# -*- coding: utf-8 -*-

import GG.utils
import guiobjects
import ocempgui.widgets
import os

BROADCAST_BACKGROUND = os.path.join(GG.utils.BACKGROUNDS, "broadcastWIndow.png")
EDIT_ROOM_BACKGROUND = os.path.join(GG.utils.BACKGROUNDS, "editRoomWindow.png")
CREATE_ITEM_BACKGROUND = os.path.join(GG.utils.BACKGROUNDS, "createObjectWindow.png")

class AuxBox:
  
  def __init__(self, hud):
    self.hide = True
    self.window = None
    self.hud = hud
    self.draw()

  def draw(self):
    pass

  def showOrHide(self):
    if self.hide:
      self.updateListItem()
      self.hud.addSprite(self.window)
      self.hud.widgetContainer.add_widget(self.window)
    else:
      self.hud.removeSprite(self.window)
      self.hud.widgetContainer.remove_widget(self.window)
      self.removeTooltip()
      self.hud.itemUnselected()
      self.hud.dropActionsItembuttons()
    self.hide = not self.hide

  def showTooltip(self, label):
    self.hud.showTooltip(label)
  
  def removeTooltip(self):
    self.hud.removeTooltip()

  def accept(self):
    pass


class TeleportWindow(AuxBox):

  def __init__(self, hud):
    self.title = "Escoja destino"
    self.tooltipLabel = "Teleportar"
    self.listItems = hud.getModel().getRoomLabels()
    AuxBox.__init__(self, hud)

  def draw(self):
    self.window = ocempgui.widgets.Box(150, 300)
    self.window.topleft = [GG.utils.SCREEN_SZ[0] - 151, 129]
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.ADMIN_ACTIONS_BACKGROUND)
    self.window.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["buttonTopBar"]))
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0, 0
    self.window.add_child(imgBackground)
    titleLabel = guiobjects.OcempLabel(self.title.decode("utf-8"), guiobjects.STYLES["teleportLabel"])
    titleLabel.topleft = 4, 0
    self.window.add_child(titleLabel)
    self.listItems = guiobjects.OcempImageObjectList(110, 205, self.listItems)
    self.listItems.topleft = 20, 40
    self.window.add_child(self.listItems) 
    okButton = guiobjects.createButton(GG.utils.TINY_OK_IMAGE, [10, 262], [self.tooltipLabel, self.showTooltip, self.removeTooltip], self.accept)
    self.window.add_child(okButton)
    cancelButton = guiobjects.createButton(GG.utils.TINY_CANCEL_IMAGE, [80, 262], ["Cerrar menu", self.showTooltip, self.removeTooltip], self.showOrHide)
    self.window.add_child(cancelButton)
    self.window.zOrder = 10000

  def accept(self):
    roomLabel = self.listItems.getSelectedName()
    self.showOrHide()
    self.hud.applyTeleport(roomLabel)

  def updateListItem(self):
    self.window.remove_child(self.listItems)
    self.listItems.destroy()
    self.listItems = self.hud.getModel().getRoomLabels()
    self.listItems = guiobjects.OcempImageObjectList(110, 205, self.listItems)
    self.listItems.topleft = 20, 40
    self.window.add_child(self.listItems) 


class DeleteRoomWindow(TeleportWindow):

  def __init__(self, hud):
    TeleportWindow.__init__(self, hud)

  def draw(self):
    self.title = "Eliminar habitación"
    self.tooltipLabel = "Eliminar habitación"
    TeleportWindow.draw(self)

  def accept(self):
    roomLabel = self.listItems.getSelectedName()
    self.showOrHide()
    self.hud.applyDeleteRoom(roomLabel)


class KickPlayerWindow(TeleportWindow):

  def __init__(self, hud):
    TeleportWindow.__init__(self, hud)

  def draw(self):
    self.title = "Escaja jugador"
    self.tooltipLabel = "Expulsar jugador"
    self.listItems = self.hud.getModel().getPlayersList()
    TeleportWindow.draw(self)

  def accept(self):
    playerLabel = self.listItems.getSelectedName()
    self.showOrHide()
    self.hud.applyKickPlayer(playerLabel)

  def updateListItem(self):
    self.window.remove_child(self.listItems)
    self.listItems.destroy()
    self.listItems = self.hud.getModel().getPlayersList()
    self.listItems = guiobjects.OcempImageObjectList(110, 205, self.listItems)
    self.listItems.topleft = 20, 40
    self.window.add_child(self.listItems) 

class AuxWindow:

  def __init__(self, hud, title, topleft):
    self.hide = True
    self.window = ocempgui.widgets.Window(title.decode("utf-8"))
    self.window.topleft = topleft
    self.window.zOrder = 15000
    self.hud = hud
    self.container = None
    self.draw()

  def draw(self):
    pass

  def showOrHide(self):
    if self.hide:
      self.hud.addSprite(self.window)
      self.hud.widgetContainer.add_widget(self.window)
      cordX, cordY = self.window.topleft
      if cordX < 0:
        cordX = 0
      elif (cordX + self.container.width) > GG.utils.GAMEZONE_SZ[0]:
        cordX = GG.utils.GAMEZONE_SZ[0] - self.container.width  
      if cordY < 0:
        cordY = 0
      elif (cordY + self.container.height) > GG.utils.GAMEZONE_SZ[1]:
        cordY = GG.utils.GAMEZONE_SZ[1] - self.container.height - 75
      self.window.topleft = cordX, cordY
    else:
      self.removeTooltip()
      self.hud.removeSprite(self.window)
      self.hud.widgetContainer.remove_widget(self.window)
    self.hide = not self.hide

  def showTooltip(self, label):
    self.hud.showTooltip(label)
  
  def removeTooltip(self):
    self.hud.removeTooltip()

  def accept(self):
    pass

 
class BroadcastWindow(AuxWindow):

  def __init__(self, hud):
    self.__textField = None
    AuxWindow.__init__(self, hud, "Mensajes de sistema", [0,0])

  def draw(self):
    """ Draws window components on screen.
    """  
    self.container = ocempgui.widgets.Box(303, 123)
    self.__paintBackground()
    self.__paintChat()
    self.__paintSendButton()

  def __paintBackground(self):
    """ Paints the window background.
    """  
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(BROADCAST_BACKGROUND)
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0, 0
    self.container.add_child(imgBackground)
    self.window.child = self.container
    labelChat = guiobjects.OcempLabel("Mensaje", guiobjects.STYLES["userName"])
    labelChat.topleft = 115, 10
    self.container.add_child(labelChat)

  def __paintChat(self):
    """ Paints the chat area.
    """  
    self.__textField = guiobjects.OcempEditLine()
    self.__textField.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.__textField.border = 1
    self.__textField.topleft = 30, 50
    self.__textField.set_minimum_size(240, 20)
    self.container.add_child(self.__textField)  
    
  def __paintSendButton(self):
    """ Paints the send broadcast message button.
    """  
    sendButton = guiobjects.createButton(GG.utils.TINY_OK_IMAGE, [120, 80], ["Enviar mensaje", self.showTooltip, self.removeTooltip], self.accept)
    self.container.add_child(sendButton)

  def accept(self):
    self.hud.newBroadcastMessage(self.__textField.text)
    self.__textField.text = ""


class CreateRoomWindow(AuxWindow):

  def __init__(self, hud, player):
    self.__player = player
    self.activeLabels = []
    self.images = None
    self.sizeX = None
    self.sizeY = None
    self.maxUsers = None
    self.label = None
    AuxWindow.__init__(self, hud, "Creación de habitaciones", [400,245])
  
  def draw(self):
    """ Draws the window components.
    """    
    self.container = ocempgui.widgets.Box(358, 258)
    self.__paintBackground()
    self.__paintAttributes()
    self.__paintButtons()

  def __paintBackground(self):
    """ Paints the background image.
    """  
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(EDIT_ROOM_BACKGROUND)
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0, 0
    self.container.add_child(imgBackground)
    self.window.child = self.container
     
  def __paintButtons(self):
    """ Paints the control buttons on screen.
    """ 
    createButton = guiobjects.createButton(GG.utils.TINY_OK_IMAGE, [150, 220], ["Crear habitación", self.showTooltip, self.removeTooltip], self.accept)
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

  def accept(self):
    if not self.images.getSelectedName():
      return  
    label = self.label.text
    try: 
      posX = int(self.sizeX.text)    
    except ValueError:
      self.__player.newChatMessage('Valor "Dimension X" incorrecto', 1)
      return
    try: 
      posY = int(self.sizeY.text)    
    except ValueError:
      self.__player.newChatMessage('Valor "Dimension Y" incorrecto', 1)
      return
    try: 
      maxUsers = int(self.maxUsers.text)    
    except ValueError:
      self.__player.newChatMessage('Valor "Capacidad" incorrecto', 1)
      return
    image = self.images.getSelectedName()
    self.showOrHide()
    self.hud.createRoom(label, [posX, posY], [image], maxUsers)


class CreateItemsWindow(AuxWindow):

  def __init__(self, hud, session):
    self.__session = session
    self.__objectsDict = session.getObjectsData()
    self.editableFields = {}
    self.activeLabels = []
    self.__objectsArea = None
    self.images = None
    AuxWindow.__init__(self, hud, "Creación de objetos", [0,0])

  def draw(self):
    """ Draws the window components.
    """  
    self.container = ocempgui.widgets.Box(373, 390)
    self.__paintBackground()
    self.__paintObjectsList()
    self.__paintButtons()

  def __paintBackground(self):
    """ Paints the background image.
    """  
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(CREATE_ITEM_BACKGROUND)
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0, 0
    self.container.add_child(imgBackground)
    self.window.child = self.container
    itemsLabel = guiobjects.OcempLabel("Objetos", guiobjects.STYLES["pointLabel"])
    itemsLabel.topleft = 20, 10
    self.container.add_child(itemsLabel)
    itemsPropertiesLabel = guiobjects.OcempLabel("Propiedades del objeto", guiobjects.STYLES["pointLabel"])
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
    createButton = guiobjects.createButton(GG.utils.TINY_OK_IMAGE, [20, 340], ["Crear objeto", self.showTooltip, self.removeTooltip], self.accept)
    self.container.add_child(createButton)

    defaultButton = guiobjects.createButton(GG.utils.TINY_CANCEL_IMAGE, [90, 340], ["Restaurar valores por defecto", self.showTooltip, self.removeTooltip], self.__restoreDefault)
    self.container.add_child(defaultButton)

  def __selectionChange(self):
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
      label = guiobjects.OcempLabel(key, guiobjects.STYLES["itemLabel"])
      label.topleft = 10 + labelShift[0], 25 + iPos*spacing + labelShift[1]
      self.container.add_child(label)
      self.activeLabels.append(label)
      if key == "images":
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

  def accept(self):
    name = self.__objectsArea.getSelectedName()
    if not name:
      return  
    self.showOrHide()  
    data = {}
    keys = self.editableFields.keys()
    for key in keys:
      if key == "images":
        data[key] = self.editableFields[key].getSelectedName()
      else:      
        values = []
        for field in self.editableFields[key]:
          values.append(field.text)
        data[key] = values
    self.__session.createObject(name, data)

  def __restoreDefault(self):
    if self.__objectsArea.getSelectedName(): 
      self.__selectionChange()  

