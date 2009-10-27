# -*- coding: utf-8 -*-

import GG.utils
import guiobjects
import ocempgui.widgets
import os
import copy
import time
import shutil

BROADCAST_BACKGROUND = os.path.join(GG.utils.BACKGROUNDS, "broadcastWIndow.png")
EDIT_ROOM_BACKGROUND = os.path.join(GG.utils.BACKGROUNDS, "editRoomWindow.png")
EDIT_ROOM_LARGE_BACKGROUND = os.path.join(GG.utils.BACKGROUNDS, "editRoomWindowLarge.png")
CREATE_ITEM_BACKGROUND = os.path.join(GG.utils.BACKGROUNDS, "createObjectWindow.png")
ROOM_OPTIONS_LOWER_BACKGROUND = os.path.join(GG.utils.HUD_PATH, "editRoomLower.png")

FURNITURE = "furniture"

class AuxBox:
  """ AuxBox class.
  Defines an auxiliary box used to show and get info on screen.
  """
  
  def __init__(self, hud):
    """ Class constructor.
    hud: isometric view hud handler.
    """  
    self.hide = True
    self.window = None
    self.hud = hud
    self.draw()

  def draw(self):
    """ Drawing method, redefined on subclasses.
    """  
    pass

  def showOrHide(self):
    """ Shows or hides the auxiliary window.
    """  
    if self.hide:
      self.updateListItem()
      self.hud.addSprite(self.window)
      self.hud.widgetContainer.add_widget(self.window)
    else:
      self.hud.removeSprite(self.window)
      self.hud.widgetContainer.remove_widget(self.window)
      self.removeTooltip()
      self.hud.itemUnselected()
    self.hide = not self.hide

  def showTooltip(self, label):
    """ Shows the item's tooltip.
    label: tooltip's label.
    """
    self.hud.showTooltip(label)
  
  def removeTooltip(self):
    """ Removes the item's tooltip from screen.
    """  
    self.hud.removeTooltip()

  def accept(self):
    """ Accepts all info, redefined on sublasses.
    """  
    pass

  def isInside(self, pos):
    """ Checks wether one point is located or not inside the item.
    pos: point.
    """  
    if (self.window.topleft[0] <= pos[0] <= (self.window.topleft[0] + self.window.width)): 
      if (self.window.topleft[1] <= pos[1] <= (self.window.topleft[1] + self.window.height)):
        return True
    return False


class TeleportWindow(AuxBox):
  """ TeleportWindow class.
  Defines an teleport window on screen.
  """
  
  def __init__(self, hud, listRoomLabels):
    """ Class constructor.
    hud: isometric view hud handler.
    """  
    self.title = "Escoja destino"
    self.tooltipLabel = "Teleportar"
    self.listItems = listRoomLabels
    AuxBox.__init__(self, hud)

  def draw(self):
    """ Draws the item parts on screen.
    """  
    self.window = guiobjects.OcempPanel(150, 300, [GG.utils.SCREEN_SZ[0] - 151, 129], GG.utils.ADMIN_ACTIONS_BACKGROUND)
    titleLabel = guiobjects.OcempLabel(self.title, guiobjects.STYLES["teleportLabel"])
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
    """ Gets the teleport data and processes it.
    """  
    roomLabel = self.listItems.getSelectedName()
    self.showOrHide()
    self.hud.applyTeleport(roomLabel.encode("utf-8"))

  def updateListItem(self):
    """ Updates the room's list.
    """  
    self.window.remove_child(self.listItems)
    self.listItems.destroy()
    self.listItems = self.hud.getModel().getRoomLabels()
    self.listItems = guiobjects.OcempImageObjectList(110, 205, self.listItems)
    self.listItems.topleft = 20, 40
    self.window.add_child(self.listItems) 


class DeleteRoomWindow(TeleportWindow):
  """ DeleteRoomWindow class.
  Defines the delete room window.
  """

  def __init__(self, hud, listRoomLabels):
    """ Class constructor.
    hud: isometric view hud handler.
    """  
    TeleportWindow.__init__(self, hud, listRoomLabels)

  def draw(self):
    """ Draws the window parts.
    """  
    self.title = "Eliminar habitación"
    self.tooltipLabel = "Eliminar habitación"
    TeleportWindow.draw(self)

  def accept(self):
    """ Gathers and processes all data.
    """
    roomLabel = self.listItems.getSelectedName()
    self.showOrHide()
    self.hud.applyDeleteRoom(roomLabel)


class KickPlayerWindow(TeleportWindow):
  """ KickPlayerWindow class.
  Defines the kick player window.
  """  

  def __init__(self, hud, playerList):
    """ Class constructor.
    hud: isometric view hud handler.
    """  
    TeleportWindow.__init__(self, hud, playerList)

  def draw(self):
    """ Draws all window parts on screen.
    """  
    self.title = "Escoja jugador"
    self.tooltipLabel = "Expulsar jugador"
    #self.listItems = self.hud.getModel().getPlayersList()
    TeleportWindow.draw(self)

  def accept(self):
    """ Gathers and processes all data.
    """  
    playerLabel = self.listItems.getSelectedName()
    self.showOrHide()
    self.hud.applyKickPlayer(playerLabel)

  def updateListItem(self):
    """ Updates the players list.
    """  
    self.window.remove_child(self.listItems)
    self.listItems.destroy()
    self.listItems = self.hud.getModel().getPlayersList()
    self.listItems = guiobjects.OcempImageObjectList(110, 205, self.listItems)
    self.listItems.topleft = 20, 40
    self.window.add_child(self.listItems) 


class AuxWindow:
  """ AuxWindow class.
  Defines an auxiliary window used to show and get info on screen.
  """
  
  def __init__(self, hud, title, topleft):
    """ Class constructor.
    hud: isometric view hud handler.
    title: window title.
    topleft: topleft window cords.
    """  
    self.hide = True
    self.window = ocempgui.widgets.Window(title.decode("utf-8"))
    self.window.topleft = topleft
    self.window.zOrder = 15000
    self.hud = hud
    self.container = None
    self.draw()

  def draw(self):
    """ Draws this window on screen. Redefined on subclasses.
    """  
    pass

  def showOrHide(self):
    """ Shows or hides this window.
    """  
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
    """ Shows this window's tooltip on screen.
    label: tooltip's label.
    """  
    self.hud.showTooltip(label)
  
  def removeTooltip(self):
    """ Removes this window's tooltip from screen.
    """  
    self.hud.removeTooltip()

  def accept(self):
    """ Redefined on subclasses.
    """  
    pass

  def isInside(self, pos):
    """ Checks wether one point is located or not inside the item.
    pos: point.
    """  
    if (self.window.topleft[0] <= pos[0] <= (self.window.topleft[0] + self.window.width)): 
      if (self.window.topleft[1] <= pos[1] <= (self.window.topleft[1] + self.window.height)):
        return True
    return False

 
class BroadcastWindow(AuxWindow):
  """ BroadcastWindow class.
  Defines a broadcast window used to send messages to all connected players.
  """

  def __init__(self, hud):
    """ Class constructor.
    hud: isometric view hud handler.
    """
    self.__textField = None
    AuxWindow.__init__(self, hud, "Mensajes de sistema", [0,0])

  def draw(self):
    """ Draws window components on screen.
    """  
    self.__paintBackground()
    self.__paintChat()
    self.__paintSendButton()

  def __paintBackground(self):
    """ Paints the window background.
    """  
    self.container = guiobjects.OcempPanel(303, 123, [1, 1], BROADCAST_BACKGROUND)
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
    """ Paints the broadcast send message button.
    """  
    sendButton = guiobjects.createButton(GG.utils.TINY_OK_IMAGE, [120, 80], ["Enviar mensaje", self.showTooltip, self.removeTooltip], self.accept)
    self.container.add_child(sendButton)

  def accept(self):
    """ Sends a new broadcast message.
    """  
    self.hud.newBroadcastMessage(self.__textField.text)
    self.__textField.text = ""


class EditRoomWindow(AuxWindow):
  """ EditRoomWindow class.
  Defines the edit room window.
  """

  def __init__(self, hud, player, room, roomName, roomMaxUser):
    """ Class constructor.
    hud: isometric view hud handler.
    player: active player.
    """
    self.__hud = hud
    self.__player = player
    self.room = room
    self.roomMaxUser = roomMaxUser
    self.imageName = room.getTile([0, 0]).spriteName
    self.imageName = self.imageName[self.imageName.rfind(os.sep)+1:]
    self.activeLabels = []
    self.images = None
    self.maxUsers = None
    self.label = None
    self.container = None
    self.editRoomMaxUsers = None
    self.newTileImages = None
    self.roomLabelText = roomName
    AuxWindow.__init__(self, hud, "Edición de habitaciones", [0, 32])

  def showOrHide(self):
    """ Shows or hides the edit room window.
    """  
    if self.hide:
      self.editRoomMaxUsers.text = str(self.roomMaxUser)  
      self.roomLabel.text = self.__hud.roomName.decode("utf-8")
      self.imageName = self.__hud.room.getTile([0, 0]).spriteName
      self.imageName = self.imageName[self.imageName.rfind(os.sep)+1:]
      self.newTileImages.selectItem(self.imageName)
    AuxWindow.showOrHide(self)
  
  def draw(self):
    """ Draws window components on screen.
    """  
    self.__paintBackground()
    self.__paintFields()
    self.__paintButtons()
    
  def __paintBackground(self):
    """ Paints the background image.
    """  
    self.container = guiobjects.OcempPanel(300, 270, [1, 1], ROOM_OPTIONS_LOWER_BACKGROUND)
    self.window.child = self.container
    
  def __paintFields(self):
    """ Paints data fields on the window.
    """  
    iPos = 0
    spacing = 50
    labelShift = [5, -20]
    label = guiobjects.OcempLabel("users", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    self.editRoomMaxUsers = guiobjects.OcempEditLine()
    self.editRoomMaxUsers.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.editRoomMaxUsers.text = str(self.roomMaxUser)
    self.editRoomMaxUsers.border = 1
    self.editRoomMaxUsers.topleft = 10 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.editRoomMaxUsers.set_minimum_size(50, 20)
    self.container.add_child(self.editRoomMaxUsers)
    
    label = guiobjects.OcempLabel("label", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + 70 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    self.roomLabel = guiobjects.OcempEditLine()
    self.roomLabel.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.roomLabel.text = self.roomLabelText
    self.roomLabel.border = 1
    self.roomLabel.topleft = 10 + 70 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.roomLabel.set_minimum_size(90, 20)
    self.container.add_child(self.roomLabel)
    iPos += 1
        
    label = guiobjects.OcempLabel("enabled", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    self.enabledChecker = ocempgui.widgets.CheckButton()
    self.enabledChecker.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    if self.room.getEnabled():
      self.enabledChecker.activate()
    self.enabledChecker.border = 1
    self.enabledChecker.topleft = 10 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.container.add_child(self.enabledChecker)
    
    label = guiobjects.OcempLabel("startRoom", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + 120 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    self.startRoomChecker = ocempgui.widgets.CheckButton()
    self.startRoomChecker.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    if self.room.getStartRoom():
      self.startRoomChecker.activate()
    self.startRoomChecker.border = 1
    self.startRoomChecker.topleft = 10 + 120 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.container.add_child(self.startRoomChecker)
    iPos += 1
            
    label = guiobjects.OcempLabel("tiles", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    self.newTileImages = guiobjects.OcempImageList(240, 80, GG.utils.TILES, GG.utils.TILE)  
    self.newTileImages.topleft = 10 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.newTileImages.set_selectionmode(ocempgui.widgets.Constants.SELECTION_MULTIPLE)
    self.container.add_child(self.newTileImages)  
    iPos += 1
    
  def __paintButtons(self):
    """ Paints modify and discard buttons on screen.
    """  
    editButton = guiobjects.createButton(GG.utils.TINY_OK_IMAGE, [50, 230], ["Modificar habitación", self.showTooltip, self.removeTooltip], self.applyEditRoom)
    self.container.add_child(editButton)
    cancelButton = guiobjects.createButton(GG.utils.TINY_CANCEL_IMAGE, [180, 230], ["Descartar edición", self.showTooltip, self.removeTooltip], self.discardEditRoom)
    self.container.add_child(cancelButton)
    self.container.zOrder = 10000
    
  def applyEditRoom(self):
    """ Edits the room using the data provided by the user.
    """
    try: 
      maxUsers = int(self.editRoomMaxUsers.text)
    except ValueError:
      self.__player.newChatMessage('Valor "maxUsers" incorrecto', 1)
      return
    if maxUsers < 1:
      self.__player.newChatMessage('Valor "maxUsers" incorrecto', 1)
      return
    enabled = self.enabledChecker.active
    startRoom = self.startRoomChecker.active
    newTile = self.newTileImages.getSelectedNames()
    self.__hud.editRoom(maxUsers, self.roomLabel.text, enabled, startRoom, newTile)
    
  def discardEditRoom(self):
    """ Discards changes and closes window.
    """  
    self.showOrHide() 
  

class CreateRoomWindow(AuxWindow):
  """ CreateRoomWindow class.
  Defines the create room window.
  """  

  def __init__(self, hud, player, roomsInfo):
    """ Class constructor.
    hud: isometric view hud handler.
    player: active player.
    """
    self.__player = player
    self.activeLabels = []
    self.images = None
    self.sizeX = None
    self.sizeY = None
    self.maxUsers = None
    self.label = None
    self.dictInfoRooms = roomsInfo
    self.rooms = roomsInfo.values()
    self.listItems = roomsInfo.keys()
    AuxWindow.__init__(self, hud, "Creación de habitaciones", [400,320])
    
  def showOrHide(self):
    """ Shows or hides the create room window. 
    """
    if self.hide:
      self.container.remove_child(self.listRooms)
      self.__paintRoomList()
    AuxWindow.showOrHide(self)
    
  def draw(self):
    """ Draws the window components.
    """    
    self.__paintBackground()
    self.__paintAttributes()
    self.__paintRoomList()
    self.__paintButtons()

  def __paintBackground(self):
    """ Paints the background image.
    """  
    self.container = guiobjects.OcempPanel(420, 320, [1, 1], EDIT_ROOM_LARGE_BACKGROUND)
    self.window.child = self.container
     
  def __paintRoomList(self):
    """ Paints the room list on screen.
    """     
    labelShift = [10, -15]
    self.listRooms = guiobjects.OcempImageObjectList(110, 170, self.listItems)
    self.listRooms.topleft = 275 + labelShift[0], 58 + labelShift[1] 
    self.listRooms.connect_signal (ocempgui.widgets.Constants.SIG_SELECTCHANGED, self.__selectionChange)
    self.container.add_child(self.listRooms) 
     
  def __paintButtons(self):
    """ Paints the control buttons on screen.
    """ 
    createButton = guiobjects.createButton(GG.utils.TINY_OK_IMAGE, [150, 275], ["Crear habitación", self.showTooltip, self.removeTooltip], self.accept)
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
    label.topleft = 10 + 130 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    
    self.maxUsers = guiobjects.OcempEditLine()
    self.maxUsers.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.maxUsers.text = "10"
    self.maxUsers.border = 1
    self.maxUsers.topleft = 10 + 130 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.maxUsers.set_minimum_size(50, 20)
    self.container.add_child(self.maxUsers)
    iPos += 1
    
    label = guiobjects.OcempLabel("enabled", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    self.enabledChecker = ocempgui.widgets.CheckButton()
    self.enabledChecker.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.enabledChecker.activate()
    self.enabledChecker.border = 1
    self.enabledChecker.topleft = 10 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.container.add_child(self.enabledChecker)
    
    label = guiobjects.OcempLabel("startRoom", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + 120 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    self.startRoomChecker = ocempgui.widgets.CheckButton()
    self.startRoomChecker.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.startRoomChecker.border = 1
    self.startRoomChecker.topleft = 10 + 120 + labelShift[0], 40 + iPos*spacing + 18 + labelShift[1]
    self.container.add_child(self.startRoomChecker)
    iPos += 1
    
    label = guiobjects.OcempLabel("images", guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + labelShift[0], 25 + iPos*spacing + labelShift[1]
    self.container.add_child(label)
    
    height = 60
    self.images = guiobjects.OcempImageList(240, height, GG.utils.TILES, "tiles")  
    self.images.topleft = 10 + labelShift[0], 40 + iPos*spacing + 25 + labelShift[1]
    self.images.set_selectionmode(ocempgui.widgets.Constants.SELECTION_MULTIPLE)
    iPos += 1
    self.container.add_child(self.images)  
    self.activeLabels.append(self.images)
    
    label = guiobjects.OcempLabel("copy data...", guiobjects.STYLES["itemLabel"])
    label.topleft = 275 + labelShift[0], 25 + labelShift[1]
    self.container.add_child(label)
    
  def __selectionChange(self):
    """ Changes the default values, according to the selected room.
    """
    name = self.listRooms.getSelectedName().encode("utf-8")
    for key in self.listItems:
      if name == key:
        room = self.dictInfoRooms[key] 
        self.sizeX.text = str(room.size[0])  
        self.sizeY.text = str(room.size[1])  
        self.maxUsers.text = str(room.getMaxUsers())
        imgNames = []
        for singleSprite in room.spriteFull:
          imgNames.append(singleSprite[singleSprite.rfind(os.sep)+1:])  
        self.images.selectItems(imgNames)
        self.enabledChecker.set_active(room.getEnabled())
        self.startRoomChecker.set_active(room.getStartRoom())
          
  def accept(self):
    """ Gets and checks all data to create a new room.
    """  
    if not self.images.getSelectedName():
      return  
    label = self.label.text
    try: 
      posX = int(self.sizeX.text)    
    except ValueError:
      self.__player.newChatMessage('Valor "Dimension X" incorrecto', 1)
      return
    if not (4 <= posX <= 8):
      self.__player.newChatMessage('"Dimension X" debe ser un valor entre 4 y 8', 1)
      return
    try: 
      posY = int(self.sizeY.text)    
    except ValueError:
      self.__player.newChatMessage('Valor "Dimension Y" incorrecto', 1)
      return
    if not (4 <= posY <= 8):
      self.__player.newChatMessage('"Dimension Y" debe ser un valor entre 4 y 8', 1)
      return
    try: 
      maxUsers = int(self.maxUsers.text)    
    except ValueError:
      self.__player.newChatMessage('Valor "Capacidad" incorrecto', 1)
      return
    if not (1 <= maxUsers <= 15):
      self.__player.newChatMessage('"maxUsers" debe ser un valor entre 1 y 15', 1)
      return
    image = self.images.getSelectedNames()
    if not len(image):
      self.__player.newChatMessage('Debe elegir al menos un modelo de suelo', 1)
      return
    room = None
    roomList = self.listRooms.get_selected()
    if len(roomList):
      for singleRoom in self.rooms:
        if singleRoom.getName() == roomList[0].text:
          room = singleRoom
    enabled = self.enabledChecker.active      
    startRoom = self.startRoomChecker.active
    self.hud.createRoom(label, [posX, posY], image, maxUsers, enabled, startRoom, room)
    self.showOrHide()
    

class CreateItemsWindow(AuxWindow):
  """ CreateItemsWindow class.
  Defines the create item window.
  """  

  def __init__(self, hud, session, objectsData):
    """ Class constructor.
    hud: isometric view hud handler.
    session: game session object.
    """  
    self.__session = session
    self.__objectsDict = objectsData
    self.editableFields = {}
    self.activeLabels = []
    self.__objectsArea = None
    self.images = None
    self.labelShift = [153, 10]
    self.spacing = 45
    AuxWindow.__init__(self, hud, "Creación de objetos", [0,0])

  def draw(self):
    """ Draws the window components.
    """  
    self.__paintBackground()
    self.__paintObjectsList()
    self.__paintButtons()

  def __paintBackground(self):
    """ Paints the background image.
    """  
    self.container = guiobjects.OcempPanel(373, 410, [1, 1], CREATE_ITEM_BACKGROUND)
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
    """ Changes the default values, according to the selected item.
    """
    name = self.__objectsArea.getSelectedName()
    if not name:
      return  
    self.editableFields = []
    attrDict = self.__objectsDict[name]
    for label in self.activeLabels:
      self.container.remove_child(label)
      label.destroy()
    self.activeLabels = []  
    self.editableFields = {}
    iPos = 0
    keys = attrDict.keys()
    if "position" in keys:
      self.__paintDoubleTextField(iPos, "Posición", attrDict["position"], "position")
      iPos += 1
    if "label" in keys:
      self.__paintTextField(iPos, "Etiqueta", attrDict["label"], "label")
      iPos += 1
    if "destinationRoom" in keys:
      self.__paintTextField(iPos, "Habitación destino", attrDict["destinationRoom"], "destinationRoom")
      iPos += 1
    if "exitPosition" in keys:
      self.__paintDoubleTextField(iPos, "Posición de salida", attrDict["exitPosition"], "exitPosition")
      iPos += 1
    if "key" in keys:
      self.__paintTextField(iPos, "Etiqueta llave", attrDict["key"], "key")
      iPos += 1
    if "pointsGiver" in keys:
      self.__paintTextField(iPos, "Etiqueta Andatuz", attrDict["pointsGiver"], "pointsGiver")
      iPos += 1
    if "numEntradasForo" in keys:
      self.__paintTextField(iPos, "Entradas en el foro", attrDict["numEntradasForo"], "numEntradasForo")
      iPos += 1
    if "pressedTile1" in keys:
      self.__paintDoubleTextField(iPos, "Celda presionada", attrDict["pressedTile1"], "pressedTile1")
      iPos += 1
    if "pressedTile2" in keys:
      self.__paintDoubleTextField(iPos, "Celda presionada", attrDict["pressedTile2"], "pressedTile2")
      iPos += 1
    if "url" in keys:
      self.__paintTextField(iPos, "Dirección web", attrDict["url"], "url")
      iPos += 1
    if "filePath" in keys:
      self.__paintTextField(iPos, "Directorio preguntas", attrDict["filePath"], "filePath")
      iPos += 1
    if "message" in keys:
      self.__paintTextField(iPos, "Mensaje", attrDict["message"], "message")
      iPos += 1
    if "gift" in keys:
      self.__paintTextField(iPos, "Regalo", attrDict["gift"], "gift")
      iPos += 1
    if "label_gift" in keys:
      self.__paintTextField(iPos, "Etiqueta Regalo", attrDict["label_gift"], "label_gift")
      iPos += 1
    if "imagesGift" in keys:
      self.__paintImageGift(iPos, attrDict["imagesGift"])
    if "images" in keys:
      self.__paintImage(iPos, attrDict["images"])
    if "images_trader" in keys:
      self.__paintImageTrader(iPos, attrDict["images_trader"])

  def __paintTextField(self, iPos, title, label, key):
    self.__paintTitleField(title, iPos)
    entryLabel = self.__paintLongField(label, iPos)
    self.editableFields[key] = [entryLabel]

  def __paintImage(self, iPos, images):
    self.__paintTitleField("Imagenes", iPos)
    imagesArea = self.__paintImagesField(iPos, images, FURNITURE)
    self.editableFields["images"] = imagesArea

  def __paintImageTrader(self, iPos, images):
    self.__paintTitleField("Imagenes", iPos)
    imagesArea = self.__paintImagesField(iPos, images, FURNITURE, GG.utils.IMAGES_GIFT)
    self.editableFields["images_trader"] = imagesArea

  def __paintImageGift(self, iPos, images):
    self.imagesGiftList = images 
    self.__paintTitleField("Regalo", iPos)
    imagesArea = self.__paintImagesField(iPos, images, GG.utils.IMAGES_GIFT)
    fileChooser = self.__paintButtonFileChooser(iPos+4)
    self.editableFields["imagesGift"] = imagesArea

  def __paintButtonFileChooser(self, iPos):
    buttonFileChooser = guiobjects.createButton(GG.utils.FILE_BUTTON_IMAGE, [10 + self.labelShift[0], 40 + iPos * self.spacing + 40 + self.labelShift[1]], ["subir imagen", self.showTooltip, self.removeTooltip], self.openFileDialog)
    self.container.add_child(buttonFileChooser)
    self.activeLabels.append(buttonFileChooser)
    return buttonFileChooser

  def __paintDoubleTextField(self, iPos, title, values, key):
    self.__paintTitleField(title, iPos)
    entryPosX = self.__paintSortField(values[0], iPos, 0)
    entryPosY = self.__paintSortField(values[1], iPos, 1)
    self.editableFields[key] = [entryPosX, entryPosY]
 
  def __paintImagesField(self, iPos, images, imagesDir, otherImageDir = None):
    self.imagesArea = guiobjects.OcempImageList(190, self.__getImagesFieldHeight(iPos, imagesDir), sorted(images), imagesDir, otherImageDir)  
    self.imagesArea.topleft = 10 + self.labelShift[0], 40 + iPos * self.spacing + 18 + self.labelShift[1]
    self.container.add_child(self.imagesArea)  
    self.activeLabels.append(self.imagesArea)
    return self.imagesArea

  def __getImagesFieldHeight(self, iPos, dir):
    if iPos == 1:
      return 250
    elif iPos == 2:
      if dir == GG.utils.IMAGES_GIFT:
        return 180
      else:
        return 220
    elif iPos == 3: 
      return 180
    elif iPos == 4:
      return 150
    elif iPos == 5:
      return 100
    elif iPos == 6:
      return 60
    return 60

  def __paintTitleField(self, title, iPos):
    label = guiobjects.OcempLabel(title, guiobjects.STYLES["itemLabel"])
    label.topleft = 10 + self.labelShift[0], 25 + iPos * self.spacing + self.labelShift[1]
    self.container.add_child(label)
    self.activeLabels.append(label)

  def __paintSortField(self, text, iPos, margin):
    entryLabel = guiobjects.OcempEditLine()
    entryLabel.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    entryLabel.text = str(text)
    entryLabel.border = 1
    entryLabel.topleft = 10 + margin * 65 + self.labelShift[0], 40 + iPos * self.spacing + 18 + self.labelShift[1]
    entryLabel.set_minimum_size(50, 20)
    self.container.add_child(entryLabel)
    self.activeLabels.append(entryLabel)
    return entryLabel

  def __paintLongField(self, text, iPos):
    entryLabel = guiobjects.OcempEditLine()
    entryLabel.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    entryLabel.text = str(text)
    entryLabel.border = 1
    entryLabel.topleft = 10 + self.labelShift[0], 40 + iPos * self.spacing + 18 + self.labelShift[1]
    entryLabel.set_minimum_size(180, 20)
    self.container.add_child(entryLabel)
    self.activeLabels.append(entryLabel)
    return entryLabel

  def openFileDialog(self):
    """ Opens the file explorer dialog.
    """  
    self.dialog = guiobjects.OcempPanel(373, 372, [528, 100], GG.utils.UPLOAD_BACKGROUND)
    self.dialog.zOrder = 10000
    self.listDir = guiobjects.OcempImageFileList(310, 239)
    self.listDir.topleft = 31, 60
    self.dialog.add_child(self.listDir)
    buttonOK = guiobjects.createButton(GG.utils.OK_BUTTON_IMAGE, [233, 308], ["aceptar", self.showTooltip, self.removeTooltip], self.closeFileDialog,"OK")
    self.dialog.add_child(buttonOK)
    buttonCancel = guiobjects.createButton(GG.utils.CANCEL_BUTTON_IMAGE, [122, 308], ["cerrar", self.showTooltip, self.removeTooltip], self.closeFileDialog,"KO")
     
    self.dialog.add_child(buttonCancel)
    self.hud.addSprite(self.dialog)
    self.hud.widgetContainer.add_widget(self.dialog)

  def closeFileDialog(self, action):
    """ Closes the file explorer dialog.
    """  
    if action == "OK":
      filePath = None
      filePath = self.listDir.getFileName()
      if filePath:
        self.origFilePath = filePath
        GG.genteguada.GenteGuada.getInstance().asyncUploadFile(filePath, self.uploadImageFinish, "imagesgift")
    self.removeTooltip()
    self.hud.removeSprite(self.dialog)
    self.hud.widgetContainer.remove_widget(self.dialog)

  def uploadImageFinish(self, resultado):
    """ Reloads the item pannel after an image upload finishes.
    """  
    if resultado:
      fileName = os.path.join("imagesgift",resultado)
      shutil.copy(self.origFilePath, os.path.join(GG.utils.LOCAL_DATA_PATH, fileName))
      self.imagesGiftList.append(resultado)
      self.container.remove_child(self.imagesArea)
      self.activeLabels.remove(self.imagesArea)
      del self.editableFields["imagesGift"]
      self.imagesArea.destroy()
      self.imagesArea = guiobjects.OcempImageList(190, 180, sorted(self.imagesGiftList), GG.utils.IMAGES_GIFT)  
      self.imagesArea.topleft = 10 + self.labelShift[0], 40 + 2 * self.spacing + 18 + self.labelShift[1]
      self.container.add_child(self.imagesArea)  
      self.activeLabels.append(self.imagesArea)
      self.editableFields["imagesGift"] = self.imagesArea

  def accept(self):
    """ Gets and checks all data to create a new room.
    """  
    name = self.__objectsArea.getSelectedName()
    if not name:
      return  
    self.showOrHide()  
    data = {}
    keys = self.editableFields.keys()
    for key in keys:
      if key in ["images","imagesGift","images_trader"]:
        data[key] = self.editableFields[key].getSelectedName()
      else:      
        values = []
        for field in self.editableFields[key]:
          values.append(field.text)
        data[key] = values
    self.__session.createObject(name, data)

  def __restoreDefault(self):
    """ Restore default values.
    """  
    if self.__objectsArea.getSelectedName(): 
      self.__selectionChange()  
      
  def setNewPosition(self, pos):
    """ Sets a new position for the created item.
    """  
    if "position" in self.editableFields.keys():
      self.editableFields["position"][0].text = str(pos[0])  
      self.editableFields["position"][1].text = str(pos[1])
