# -*- coding: utf-8 -*-

import pygame
import GG.utils
import isoview
import isoview_inventoryitem
import isoview_player
import ocempgui.widgets
import ocempgui.draw
import avatareditor
import animation
import exchangewindow
import guiobjects
import privatechatwindow
import webbrowser
import auxwindows


from pygame.locals import * # faster name resolution
import os

class FakeModel:
  """ FakeModel class.
  Used to create temporary screen animations without an associated item.
  """  
  def __init__(self, spriteInventory, label):
    self.spriteInventory = spriteInventory
    self.label = label

  def getName(self):
    return self.label

# ======================= CONSTANTS ===========================
BG_FULL_OR = [0, 0]
TILE_TARGET_SHIFT = [18, 18]
SELECTED_FLOOR_SHIFT = [55, -25]
HUD_OR = [0, GG.utils.GAMEZONE_SZ[1]]

CHAT_SZ = [753, 118]
CHAT_OR = [14, GG.utils.GAMEZONE_SZ[1]+14]
TEXT_BOX_OR = [CHAT_OR[0], GG.utils.GAMEZONE_SZ[1]+CHAT_SZ[1]+27]

INV_OR = [CHAT_SZ[0]+ 53, GG.utils.GAMEZONE_SZ[1]+28]
INV_ITEM_SZ = [60, 60]
INV_SZ = [INV_ITEM_SZ[0] * GG.utils.INV_ITEM_COUNT[0] + 10, 
          INV_ITEM_SZ[1] * GG.utils.INV_ITEM_COUNT[1] + 15]

ANIM_INVENTORY_TIME = 1000
ANIM_CHAT_TIME2 = 1000

BG_BLACK = "bg_black.png"
INTERFACE_LOWER = os.path.join(GG.utils.HUD_PATH, "interface_lowerv2.png")

TILE_SELECTED = os.path.join(GG.utils.TILE, "selected.png")
TILE_TARGET = os.path.join(GG.utils.TILE, "target.png")
# =============================================================

NOTIFICATION_IMAGE = os.path.join(GG.utils.HUD_PATH, "4.png")
MOVE_IN_IMAGE = os.path.join(GG.utils.HUD_PATH, "movein.png")
MOVE_OUT_IMAGE = os.path.join(GG.utils.HUD_PATH, "moveout.png")
LIFT_IMAGE = os.path.join(GG.utils.HUD_PATH, "lift.png")
DROP_IMAGE = os.path.join(GG.utils.HUD_PATH, "drop.png")
CLIMB_IMAGE = os.path.join(GG.utils.HUD_PATH, "climb.png")
CHAT_IMAGE = os.path.join(GG.utils.HUD_PATH, "chat.png")
PRIVATE_CHAT_IMAGE = os.path.join(GG.utils.HUD_PATH, "privatechat.png")
EXCHANGE_IMAGE = os.path.join(GG.utils.HUD_PATH, "exchange.png")
OPEN_IMAGE = os.path.join(GG.utils.HUD_PATH, "open.png")
WWW_IMAGE = os.path.join(GG.utils.HUD_PATH, "www.png")
CONTACT_IMAGE = os.path.join(GG.utils.HUD_PATH, "contact.png")
EXIT_IMAGE = os.path.join(GG.utils.HUD_PATH, "exit.png")
MAXIMIZE_IMAGE = os.path.join(GG.utils.HUD_PATH, "maximize.png")
MINIMIZE_IMAGE = os.path.join(GG.utils.HUD_PATH, "minimize.png")
SOUND_IMAGE = os.path.join(GG.utils.HUD_PATH, "sound.png")
MUTE_IMAGE = os.path.join(GG.utils.HUD_PATH, "mute.png")
TELEPORT_IMAGE = os.path.join(GG.utils.HUD_PATH, "teleport.png")
CREATE_ITEM_IMAGE = os.path.join(GG.utils.HUD_PATH, "addObject.png")
DELETE_ROOM_IMAGE = os.path.join(GG.utils.HUD_PATH, "removeRoom.png")
CREATE_ROOM_IMAGE = os.path.join(GG.utils.HUD_PATH, "addRoom.png")
JUMP_IMAGE = os.path.join(GG.utils.HUD_PATH, "jump.png")
KICK_IMAGE = os.path.join(GG.utils.HUD_PATH, "kick.png")
TINY_DELETE_IMAGE = os.path.join(GG.utils.HUD_PATH, "tinyRemove.png")
TINY_COPY_IMAGE = os.path.join(GG.utils.HUD_PATH, "tinyCopy.png")
EDIT_ROOM_IMAGE = os.path.join(GG.utils.HUD_PATH, "editGrid.png")
ROTATE_RIGHT_IMAGE = os.path.join(GG.utils.HUD_PATH, "spinright.png")
ROTATE_LEFT_IMAGE = os.path.join(GG.utils.HUD_PATH, "spinleft.png")
DRESSER_IMAGE = os.path.join(GG.utils.HUD_PATH, "dresser.png")
ADMIN_OPTIONS_BACKGROUND = os.path.join(GG.utils.HUD_PATH, "adminOptions.png")
#ROOM_OPTIONS_BACKGROUND = os.path.join(GG.utils.HUD_PATH, "roomActions.png")
ROOM_OPTIONS_UPPER_BACKGROUND = os.path.join(GG.utils.HUD_PATH, "editRoomUpper.png")
ROOM_OPTIONS_UPPER_USER_BACKGROUND = os.path.join(GG.utils.HUD_PATH, "editRoomUpperUser.png")
USER_ACTIONS_BACKGROUND = os.path.join(GG.utils.HUD_PATH, "actionsNotification.png")
TOOLBAR_IMAGE = os.path.join(GG.utils.LOCAL_DATA_PATH,"imgToolbar.png")
MASKUSER_IMAGE = os.path.join(GG.utils.LOCAL_DATA_PATH,"imgMaskUser.png")
CONTACT_WINDOW_BACKGROUND = os.path.join(GG.utils.BACKGROUNDS, "contactWindow.png")
OK_BUTTON_IMAGE = os.path.join(GG.utils.EDITOR, "ok_button.png")
CANCEL_BUTTON_IMAGE = os.path.join(GG.utils.EDITOR, "cancel_button.png")
ADMIN_IMAGE = os.path.join(GG.utils.HUD_PATH, "tools.png")
NOADMIN_IMAGE = os.path.join(GG.utils.HUD_PATH, "notools.png")

class IsoViewHud(isoview.IsoView): 
  """ IsoViewHud class.
  Defines the HUD.
  """
  
  #def __init__(self, model, screen, fullscreen, user, accesMode):
  def __init__(self, model, screen, fullscreen, user):
    """ Class constructor.
    model: ggsession model.
    screen: screen handler.
    fullscreen: sets the game as started on fullscreen or not.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__player = user
    self.__isoviewInventory = []
    inventoryData = self.__player.getInventory()
    self.room = self.__player.getRoom()
    self.roomName = self.room.getName()
    self.roomMaxUser = self.room.getMaxUsers()
    for key in inventoryData:
      self.__isoviewInventory.append(isoview_inventoryitem.IsoViewInventoryItem(inventoryData[key]["object"], screen, self, inventoryData[key]["name"]))
    self.__allSprites = guiobjects.GroupSprite()
    self.__isoviewRoom = None    
    self.__textArea = None
    self.__textField = None
    self.__windowInventory = None

    self.__privateChatWindow = privatechatwindow.PrivateChatWindow(self, self.__player)
    
    self.__fullScreen = fullscreen
    self.__sound = True
    self.__soundButton = None
    self.__adminButton = None
    self.__fullscreenButton = None
    self.__privateChatButton = None
    self.__buttonBarActions = None
    self.windowAdminActions = None
    model.subscribeEvent('chatAdded', self.chatAdded)
    subscriptionList = []
    subscriptionList.append(['quizAdded', self.quizAdded])
    subscriptionList.append(['room', self.roomChanged])
    subscriptionList.append(['liftItem', self.updateScreenItemPosition])
    subscriptionList.append(['dropItem', self.updateScreenItemPosition])
    subscriptionList.append(['addToInventory', self.addItemToInventory])
    subscriptionList.append(['removeFromInventory', self.inventoryRemoved])
    subscriptionList.append(['selectedItem', self.itemSelected])
    subscriptionList.append(['unselectedItem', self.itemUnselected])
    subscriptionList.append(['points', self.pointsAdded])
    subscriptionList.append(['clock', self.clockAdded])
    subscriptionList.append(['exp', self.expAdded])
    subscriptionList.append(['initExchange', self.initExchange])
    subscriptionList.append(['cancelExchange', self.cancelExchange])
    subscriptionList.append(['listExchange', self.addListExchange])
    subscriptionList.append(['contactDialog', self.newContactDialog])
    subscriptionList.append(['contactAdded', self.newContactAdded])
    subscriptionList.append(['privateChatReceived', self.privateChatReceived])
    subscriptionList.append(['removeContactRemote', self.removeContactRemote])
    subscriptionList.append(['avatarConfiguration', self.playerConfigurationChanged])
    subscriptionList.append(['contactMask', self.contactMaskChanged])
    subscriptionList.append(['finish', self.finishGame])
    subscriptionList.append(['destination', self.destinationChanged])
    self.__player.subscribeListEvent(subscriptionList)
    self.__selectedItem = None
    self.__selectedImage = guiobjects.getSprite(TILE_SELECTED)
    self.__targetTile = None
    self.__targetTileImage = guiobjects.getSprite(TILE_TARGET)
    self.__activeActions = []
    self.__restoreActiveActionButtonsList()
    self.__buttonActions = {
        "inventory":      {"image":MOVE_IN_IMAGE,       "action": self.itemToInventory,     "tooltip":"Al inventario (P)"},
        "copy":           {"image":MOVE_IN_IMAGE,       "action": self.itemCopyToInventory, "tooltip":"Al inventario (C)"},
        "gift":           {"image":MOVE_IN_IMAGE,       "action": self.itemCopyToInventoryRemove, "tooltip":"Al inventario"},
        "copyRemove":     {"image":MOVE_IN_IMAGE,       "action": self.itemCopyToInventoryRemove, "tooltip":"Al inventario"},
        "removeInventory":{"image":MOVE_OUT_IMAGE,      "action": self.itemOutInventory,    "tooltip":"Sacar del inventario (M)"},
        "jumpOver":       {"image":JUMP_IMAGE,          "action": self.itemToJumpOver,      "tooltip":"Saltar (J)"},
        "lift":           {"image":LIFT_IMAGE,          "action": self.itemToLift,          "tooltip":"Levantar (I)"},
        "drop":           {"image":DROP_IMAGE,          "action": self.itemToDrop,          "tooltip":"Soltar (Q)"},
        "climb":          {"image":CLIMB_IMAGE,         "action": self.itemToClimb,         "tooltip":"Subir (B)"},
        "clone":          {"image":MOVE_IN_IMAGE,       "action": self.itemToClone,         "tooltip":"Al inventario (Y)"},
        "talk":           {"image":CHAT_IMAGE,          "action": self.itemToTalk,          "tooltip":"Hablar (T)"},
        "talkAndGet":     {"image":CHAT_IMAGE,          "action": self.itemToTalkAndGet,    "tooltip":"Hablar (G)"},
        "exchange":       {"image":EXCHANGE_IMAGE,      "action": self.exchangeItemPlayer,  "tooltip":"Intercambiar (E)"},
        "open":           {"image":OPEN_IMAGE,          "action": self.itemToOpen,          "tooltip":"Abrir (O)"},
        "url":            {"image":WWW_IMAGE,           "action": self.itemToUrl,           "tooltip":"Ir a (W)"},
        "toExchange":     {"image":EXCHANGE_IMAGE,      "action": self.itemToExchange,      "tooltip":"Intercambiar (A)"},
        "giveCard":       {"image":CONTACT_IMAGE,       "action": self.itemToGiveCard,      "tooltip":"Dar tarjeta de visita (V)"},
        "money":          {"image":MOVE_IN_IMAGE,       "action": self.moneyToInventory,    "tooltip":"Recoger puntos (N)"},
        #"privateChat":    {"image":PRIVATE_CHAT_IMAGE,  "action": self.privateChat,         "tooltip":"Chat (H)"},
    }
    self.__hotkeys = {
        K_x: self.finishGame,         K_f: self.showFullScreen,       K_s: self.showSoundControl, 
        K_d: self.showDresser,        K_j: self.jump,                 K_r: self.turnRight, K_l: self.turnLeft, 
        K_p: self.itemToInventory,    K_c: self.itemCopyToInventory,  K_m: self.itemOutInventory, 
        K_i: self.itemToLift,         K_q: self.itemToDrop ,          K_b: self.itemToClimb , 
        K_y: self.itemToClone,        K_t: self.itemToTalk,           K_g: self.itemToTalkAndGet ,    
        K_e: self.exchangeItemPlayer, K_o: self.itemToOpen ,          K_w: self.itemToUrl ,         
        K_a: self.itemToExchange,     K_v: self.itemToGiveCard,       K_z: self.privateChatHandler, 
        K_n: self.moneyToInventory
    }
    self.__winWardrobe = None
    self.__exchangeWindow = None
    self.__activeWindow = False
    self.__activeContactDialog = None
    self.__tooltipWindow = None
    self.__ctrl = False
    self.__adminMenu = False
    self.__editRoomMenu = False
    self.__deleteConfirmDialog = None
    self.__isoviewRoom = self.room.defaultView(self.getScreen(), self)
    self.__isoviewRoom.updateScreenPositions()
    
    #self.__accessMode = accesMode 
    self.__accessMode = False 
    
    #if self.__accessMode:
    if self.__player.admin:
      adminInitData = model.getAdminInitData()
      self.__createItemsWindow = auxwindows.CreateItemsWindow(self, model, adminInitData["objectsData"])
      self.__createRoomWindow = auxwindows.CreateRoomWindow(self, self.__player, adminInitData["roomListInfo"])
      self.__editRoomWindow = auxwindows.EditRoomWindow(self, self.__player, self.room, self.roomName, self.roomMaxUser)
      self.__broadcastWindow = auxwindows.BroadcastWindow(self)
      self.__teleportWindow = auxwindows.TeleportWindow(self, adminInitData["roomListInfo"].keys())
      self.__deleteRoomWindow = auxwindows.DeleteRoomWindow(self, adminInitData["roomListInfo"].keys())
      self.__kickPlayerWindow = auxwindows.KickPlayerWindow(self, adminInitData["playerList"])
    else:
      self.__createItemsWindow = None  
      self.__createRoomWindow = None
      self.__editRoomWindow = None      
      self.__broadcastWindow = None  
      self.__teleportWindow = None
      self.__deleteRoomWindow = None
      self.__kickPlayerWindow = None
    self.addItemToRoomFromVoid(self.findIVItem(self.__player))  
    self.__player.setAccessMode(False)

    
  def processEvent(self, events):
    """ Processes the input events.
    events: events received.
    """  
    for event in events:
      event_type = event.type
      if event_type == QUIT:
        GG.genteguada.GenteGuada.getInstance().finish()
      elif event_type == KEYUP:
        if event.key == K_LCTRL or event.key == K_RCTRL:
          self.__ctrl = False
      elif event_type == KEYDOWN:
        if self.__ctrl:
          self.__processHotkeys(event)
        else:  
          if event.key == K_LCTRL or event.key == K_RCTRL:
            self.__ctrl = True 
          elif event.key == K_RETURN:
            self.__processEnterKey()
      elif event_type == MOUSEBUTTONDOWN:
        if self.__accessMode:
          if self.__adminMenu or not self.__createItemsWindow.hide:
            self.__moveItemPositionAdmin()
          elif not self.__windowOpen():
            self.__clickOnMap()
        elif not self.__windowOpen():
          self.__clickOnMap()
    self.widgetContainer.distribute_events(*events)
    
  def __processHotkeys(self, event):
    """ Processes the hotkeys and keyboard shortcuts.
    event: keyboard event type.
    """  
    if event.key in self.__hotkeys.keys():
      if self.__hotkeys[event.key] in self.__activeActions:
        self.__hotkeys[event.key]()

  def __processEnterKey(self):
    """ Processes the "enter" key event.
    """  
    if not self.__privateChatWindow.hide:
      self.__privateChatWindow.chatMessageEntered()
    else:
      self.chatMessageEntered()

  def __moveItemPositionAdmin(self):
    """ Changes an item position on the item edit window in admin access mode.
    """  
    cordX, cordY = pygame.mouse.get_pos()
    dest = self.getIsoviewRoom().findTileOnly([cordX, cordY])
    if not dest == [-1, -1]:
      if not self.__createItemsWindow.hide:
        if not self.__createItemsWindow.isInside([cordX, cordY]):  
          self.__createItemsWindow.setNewPosition(dest)    
      if self.__adminMenu and "Posicion" in self.editableFields.keys():
        if not guiobjects.isInside(self.windowAdminActions, [cordX, cordY]):
          self.editableFields["Posicion"][0].text = str(dest[0])
          self.editableFields["Posicion"][1].text = str(dest[1])
  
  def __clickOnMap(self):
    """ Processes a mouse click on the room.
    """  
    cordX, cordY = pygame.mouse.get_pos()
    if 0 <= cordY <= HUD_OR[1]:
      if self.__ctrl and self.__accessMode:
        dest = self.getIsoviewRoom().findTileOnly([cordX, cordY])
        if not dest == [-1, -1]:
          self.__isoviewRoom.getModel().clickedTileByAdmin(self.__player, dest)
      else:  
        dest, item = self.getIsoviewRoom().findTile([cordX, cordY])
        if not dest == [-1, -1]:
          self.__isoviewRoom.getModel().clickedByPlayer(self.__player, dest, item)

  def __windowOpen(self):
    """ Checks if there is an open window.
    """
    if self.__activeWindow:
      return True
    if self.__activeContactDialog or self.__deleteConfirmDialog:
      return True
    windowsList = [self.__kickPlayerWindow, self.__deleteRoomWindow, self.__teleportWindow, 
                   self.__privateChatWindow, self.__createItemsWindow, self.__broadcastWindow, 
                   self.__createRoomWindow, self.__editRoomWindow]
    for window in windowsList:
      if window:
        if not window.hide:
          return True
    return False
  
  def __closeAllWindow(self):
    windowsList = [self.__kickPlayerWindow, self.__deleteRoomWindow, self.__teleportWindow, 
                   self.__privateChatWindow, self.__createItemsWindow, self.__broadcastWindow, 
                   self.__createRoomWindow, self.__editRoomWindow]
    for window in windowsList:
      if window:
        if not window.hide:
          window.showOrHide()
    if self.__adminMenu:
      self.removeSprite(self.windowAdminActions)
      self.widgetContainer.remove_widget(self.windowAdminActions)
      self.__adminMenu = False

  def __restoreActiveActionButtonsList(self):
    """ Restores the active action button list.
    """  
    self.__activeActions = []  
    self.__activeActions.append(self.finishGame)
    self.__activeActions.append(self.showFullScreen)
    self.__activeActions.append(self.showAdminActions)
    self.__activeActions.append(self.showDresser)
    self.__activeActions.append(self.jump)
    self.__activeActions.append(self.turnRight)
    self.__activeActions.append(self.turnLeft)
    self.__activeActions.append(self.privateChatHandler)
    
  def getIVRoom(self):
    """ Returns the active room's isometric view.
    """  
    return self.__isoviewRoom

  def setActiveWindow(self, value):
    """ Sets the active quiz window with a new value
    """  
    self.__activeWindow = value
    
  def addSprite(self, sprite):
    """ Adds a new sprite to the sprite group.
    sprite: new sprite. 
    """  
    self.__allSprites.add(sprite)

  def removeSprite(self, sprite):
    """ Removes a sprite from the sprite group.
    sprite: sprite to be removed.
    """  
    self.__allSprites.remove(sprite)

  def getPlayer(self):
    """ Returns the active player.
    """  
    return self.__player
  
  def getSelectedItem(self):
    """ Returns the selected item.
    """  
    return self.__selectedItem

  def getSound(self):
    """ Returns the sound flag.
    """  
    return self.__sound

  def findIVItem(self, item):
    """ Returns the isometric view object that contains a given item.
    item: given item.
    """  
    if not self.__isoviewRoom:
      return None  
    for ivItem in self.__isoviewRoom.getIsoViewItems():
      if ivItem.getModel() == item:
        return ivItem
    return None

  def findIVInventoryItem(self, item):
    """ Returns the inventory isometric view object that contains a given item.
    item: given item.
    """  
    for ivItem in self.__isoviewInventory:
      if ivItem.getModel() == item:
        return ivItem
    return None
  
  def inventoryRemoved(self, event):
    """ Triggers after receiving an inventory removed item event.
    event: event info.
    """ 
    item = event.getParams()["item"]  
    ivInventItem = self.findIVInventoryItem(item)
    self.__isoviewInventory.remove(ivInventItem)
    self.paintItemsInventory()
      
  def updateScreenItemPosition(self, event):
    """ Triggers after receiving a lift item event.
    event: event info.
    """ 
    item = event.getParams()["item"]  
    pos = event.getParams()["position"]
    itemList = event.getParams()["itemList"]
    ivItem = self.__isoviewRoom.findIVItem(item)  
    if ivItem:
      self.__isoviewRoom.updateScreenPositionsOn(pos, itemList)  
      
  def addItemToInventory(self, event):
    """ Triggers after receiving an item added to inventory event.
    event: event info.
    """ 
    item = event.getParams()["item"]
    posOrigin = event.getParams()["position"]
    itemName = event.getParams()["itemName"]
    posX = len(self.__isoviewInventory)%GG.utils.INV_ITEM_COUNT[0]
    posY = len(self.__isoviewInventory)/GG.utils.INV_ITEM_COUNT[1]
    pos = [INV_OR[0] + (posX * INV_ITEM_SZ[0]), INV_OR[1] + (posY * INV_ITEM_SZ[1])]
    ivItem = self.findIVItem(item)
    invItem = isoview_inventoryitem.IsoViewInventoryItem(item, self.getScreen(), self, itemName)
    if ivItem:
      positionAnim = animation.ScreenPositionAnimation(ANIM_INVENTORY_TIME, ivItem, GG.utils.p3dToP2d(posOrigin, ivItem.anchor), pos, True)
      positionAnim.setOnStop(self.room.removeItem, item)
      positionAnim.setOnStop(self.removeSprite, ivItem.getImg())
    else:
      ivItem = item.defaultView(self.getScreen(), self.__isoviewRoom, self)
      self.__isoviewRoom.addIsoViewItem(ivItem)  
      positionAnim = animation.ScreenPositionAnimation(ANIM_INVENTORY_TIME, ivItem, GG.utils.p3dToP2d(posOrigin, [0, 0]), pos, True)
      positionAnim.setOnStop(self.removeSprite, ivItem.getImg())
    positionAnim.setOnStop(self.__isoviewInventory.append, invItem)
    positionAnim.setOnStop(self.paintItemsInventory, None)
    self.__isoviewRoom.itemUnselected(item)
    ivItem.setAnimation(positionAnim)
        
  def addItemToRoomFromInventory(self, ivItem, listItems = None):
    """ Removes an item from the inventory item list and creates an animation from the inventory to the room.
    ivItem: isoview item associated to the item model.
    """
    item = ivItem.getModel()
    itemPos = ivItem.getPosition()
    ivInventItem = self.findIVInventoryItem(item)
    if not listItems:
      listItems =  item.getTile().getItems()
    if ivItem:    
      posX = len(self.__isoviewInventory)%GG.utils.INV_ITEM_COUNT[0]
      posY = len(self.__isoviewInventory)/GG.utils.INV_ITEM_COUNT[1]
      pos = [INV_OR[0] + (posX * INV_ITEM_SZ[0]), INV_OR[1] + (posY * INV_ITEM_SZ[1])]
      positionAnim = animation.ScreenPositionAnimation(ANIM_INVENTORY_TIME, ivItem, pos, self.__isoviewRoom.getFutureScreenPosition(ivItem, itemPos, listItems), True)
      positionAnim.setOnStop(self.__isoviewRoom.updateScreenPositionsOn, itemPos, listItems)
      if self.__sound:
        positionAnim.setOnStop(guiobjects.playSound, GG.utils.SOUND_DROPITEM)     
      ivItem.setAnimation(positionAnim)
      if ivInventItem:
        self.__isoviewInventory.remove(ivInventItem)
        self.paintItemsInventory()
      
  def addItemToRoomFromVoid(self, ivItem, itemList = None):
    """ Creates an animation from the top of the screen to the room.
    ivItem: isoview item associated to the item model.
    """
    item = ivItem.getModel()
    itemPos = ivItem.getPosition()
    if not itemList:
      itemList = item.getItemsOnMyTile()
    endPos = self.__isoviewRoom.getFutureScreenPosition(ivItem, itemPos, itemList)
    if ivItem:
      positionAnim = animation.ScreenPositionAnimation(ANIM_INVENTORY_TIME, ivItem, [endPos[0], -500], endPos, True)
      ivItem.setAnimation(positionAnim)
      if isinstance(ivItem, isoview_player.IsoViewPlayer):
        movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, ivItem, ivItem.createFrameSet("walking_carrying"), ivItem.getPath())
        ivItem.setMovieAnimation(movieAnim)
      if self.__sound:
        positionAnim.setOnStop(guiobjects.playSound, GG.utils.SOUND_DROPITEM)     
      positionAnim.setOnStop(ivItem.stopFallingAndRestore, None)
      positionAnim.setOnStop(self.__isoviewRoom.updateScreenPositionsOn, itemPos, itemList)
      
  def draw(self):
    """ Updates the changed zones on the room view and draws the hud.
    """
    pygame.event.clear()
    self.__paintImgBlack()
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.getScreen())
    self.paintBackground()
    self.paintInventory()
    self.paintChat()
    self.paintTextBox()
    self.paintActionButtons()
    self.paintUserActions()
    if self.__accessMode:
      self.paintAdminOptions()
    self.__paintRoomInfo()
    self.hud.zOrder = 1
    self.addSprite(self.hud)
    self.widgetContainer.add_widget(self.hud)

  def __paintRoomInfo(self):
    """ Paints the room info.
    """  
    if self.__accessMode:
      self.roomInfo = guiobjects.OcempPanel(308, 31, [1,1], ROOM_OPTIONS_UPPER_BACKGROUND)
    else:  
      self.roomInfo = guiobjects.OcempPanel(308, 31, [1,1], ROOM_OPTIONS_UPPER_USER_BACKGROUND)
    self.roomLabel = guiobjects.OcempLabel(self.roomName, guiobjects.STYLES["itemLabel"])
    self.roomLabel.topleft = 30, -4
    self.roomInfo.add_child(self.roomLabel)
    if self.__accessMode:
      button = guiobjects.createButton(EDIT_ROOM_IMAGE, [1, 5], ["Editar habitación", self.showTooltip, self.removeTooltip], self.auxWindowHandler, self.__editRoomWindow)
      self.roomInfo.add_child(button)
    self.roomInfo.zOrder = 10000
    self.addSprite(self.roomInfo)
    self.widgetContainer.add_widget(self.roomInfo)

  def __paintImgBlack(self):
    """ Paints the game zone background.
    """  
    self.__bg = guiobjects.getSprite(BG_BLACK, BG_FULL_OR, -200)
    self.__allSprites.add(self.__bg)
    
  def updateFrame(self, events ,elapsedTime):
    """ Updates all sprites for a new timestamp.
    event: events info.
    elapsedTime: elapsedTime
    """
    self.processEvent(events)
    if self.__isoviewRoom:
      self.__isoviewRoom.updateFrame(elapsedTime)
    for item in self.__isoviewInventory:
      item.updateFrame(elapsedTime)  
    self.__allSprites.draw(self.getScreen())
    pygame.display.flip()
        
  def addIsoAnimation(self, isoviewAnim):
    """ Adds a new animation.
    isoviewAnim: new animation.
    """  
    self.__isoviewAnim.append(isoviewAnim)    
  
  def removeIsoAnimation(self, isoviewAnim):
    """ Removes an animation.
    isoviewAnim: animation to be removed.
    """  
    self.__isoviewAnim.remove(isoviewAnim)
    
  def roomChanged(self, event):
    """ Triggers after receiving a change room event.
    event: event info.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.stopAnimations()
      self.__isoviewRoom.unsubscribeAllEvents()
      if self.__sound:
        guiobjects.playSound(GG.utils.SOUND_OPENDOOR)
      spriteList = self.__isoviewRoom.getSpritesDict()
      for img in spriteList.keys():
        self.removeSprite(img)
      spriteList = self.__isoviewRoom.getBottomSpritesDict()
      for img in spriteList.keys():
        self.removeSprite(img)
      self.__isoviewRoom = None
      rect = pygame.Rect(0, 0, GG.utils.GAMEZONE_SZ[0], GG.utils.GAMEZONE_SZ[1])
      self.getScreen().fill((0, 0, 0), rect)
    if event.getParams()["room"]:
      self.room = event.getParams()["room"]
      self.roomName = event.getParams()["roomLabel"]
      self.__isoviewRoom = event.getParams()["room"].defaultView(self.getScreen(), self)
      self.__isoviewRoom.updateScreenPositions()
      self.roomLabel.label = event.getParams()["roomLabel"].decode("utf-8")
      self.roomLabel.set_text(event.getParams()["roomLabel"].decode("utf-8"))
      self.roomInfo.remove_child(self.roomLabel)
      self.roomInfo.add_child(self.roomLabel)
    if self.__isoviewRoom:
      ivItem = self.findIVItem(self.__player)
      self.__isoviewRoom.addIsoViewItem(ivItem)    
      self.addItemToRoomFromVoid(ivItem)
    
  def editRoom(self, maxUsers, newLabel, enabled, startRoom, newTile):
    """ Edits the active room.
    maxUsers: new max users limit.
    newLabel: new room label.
    enabled: sets the active room as enabled or disabled.
    startRoom: sets the active room as start room or not.
    newTile: new tile models.
    """  
    room = self.__isoviewRoom.getModel()      
    oldLabel = room.getName()
    if oldLabel != newLabel and self.getModel().getRoom(newLabel):
      self.__player.newChatMessage('La etiqueta de habitacion ya existe', 1)  
      self.__editRoomWindow.showOrHide()
      return   
    room.editRoom(maxUsers, newLabel, enabled, startRoom, newTile)
    if oldLabel != newLabel:
      self.getModel().labelChange(oldLabel, newLabel)
    self.getModel().setStartRoom(room, startRoom)  
    self.__editRoomWindow.showOrHide()
      
  def getIsoviewRoom(self):
    """ Returns the room isometric view.
    """
    return self.__isoviewRoom
           
  def paintBackground(self):
    """ Paints the HUD background on screen.
    """
    self.hud = guiobjects.OcempPanel(1024, 262, [HUD_OR[0], HUD_OR[1]- 50], INTERFACE_LOWER)
    labelChat = guiobjects.OcempLabel("Chat", guiobjects.STYLES["hudLabel"])
    labelChat.topleft = 17, 58
    self.hud.add_child(labelChat)
    
    labelProfile = guiobjects.OcempLabel("Mi perfil: ", guiobjects.STYLES["hudLabel"])
    labelProfile.topleft = 525, 75
    self.hud.add_child(labelProfile)
    
    labelInventory = guiobjects.OcempLabel("Inventario", guiobjects.STYLES["hudLabel"])
    labelInventory.topleft = 819, 58
    self.hud.add_child(labelInventory)

  def paintChat(self):
    """ Paints the chat window on screen.
    """
    self.__textArea = ocempgui.widgets.ScrolledWindow(490, 110)
    self.__textArea.set_scrolling(1)
    self.__textArea.topleft = CHAT_OR[0], 90
    self.__layoutTextArea = ocempgui.widgets.VFrame()
    self.__layoutTextArea.border = 0
    self.__layoutTextArea.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.__textArea.child = self.__layoutTextArea
    self.hud.add_child(self.__textArea)
  
  def paintTextBox(self):
    """ Paints the editable text box on screen.
    """
    self.__textField = guiobjects.OcempEditLine()
    self.__textField.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.__textField.border = 1
    self.__textField.topleft = 14, 210
    self.__textField.set_minimum_size(490, 20)
    self.hud.add_child(self.__textField)

  def paintInventory(self):
    """ Paints the inventory box and its items on it.    
    """
    self.__windowInventory = ocempgui.widgets.ScrolledWindow(186, 135)
    self.__windowInventory.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["inventoryArea"]))
    self.__windowInventory.border = ocempgui.widgets.Constants.BORDER_FLAT
    self.__windowInventory.topleft = 819, 90
    self.__windowInventory.set_depth(1)
    self.hud.add_child(self.__windowInventory)
    self.paintItemsInventory()

  def paintItemsInventory(self):
    """ Paints the inventory items.
    """
    self.__windowInventory.child = None
    self.__frameInventory = ocempgui.widgets.VFrame()
    self.__frameInventory.border = 0
    self.__frameInventory.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.__windowInventory.child = self.__frameInventory
    position = 0
    for inventoryitem in self.__isoviewInventory:
      self.paintItemOnInventory(inventoryitem, position)
      position += 1

  def itemInventorySelected(self, invIsoItem):
    """ Selects an item from the player's inventory.
    invIsoItem: selected item.
    """
    item = invIsoItem.getModel()
    self.__player.setSelectedItem(item, True)

  def itemOutInventory(self):
    """ Attempts to move an item from the inventory to the active room.
    """  
    self.__player.tryOutToInventory(self.__selectedItem)
    
  def paintItemOnInventory(self, invItem, position):
    """ Paints an item on the inventory.
    invItem: inventory item.
    position: inventory position that the item will be painted into.
    """
    if position % GG.utils.INV_ITEM_COUNT[0] == 0:
      self.hframe =  ocempgui.widgets.HFrame()
      self.hframe.border = 0
      self.hframe.add_child(invItem.draw(self.widgetContainer))
      self.__frameInventory.add_child(self.hframe)
    else:
      self.hframe.add_child(invItem.draw(self.widgetContainer))
  
  def printChatMessage(self, chatMessage):
    """ Puts a new chat message on screen.
    """  
    self.__layoutTextArea.add_child(chatMessage.draw())
    self.__textArea.vscrollbar.value = self.__textArea.vscrollbar.maximum
  
  def chatMessageEntered(self):
    """ Prints a new message on the chat window.
    """
    if self.__textField.text == "" or self.__textField.text.isspace():
      return
    #self.__player.getRoom().newChatMessage(self.__textField.text, self.__player, 0)
    self.__player.newChatMessageEntered(self.__textField.text)
    self.__textField.text = ""

  def chatAdded(self, event):
    """ Triggers after receiving a new chat message event.
    event: event info.
    """
    messageChat = event.getParams()['message']
    messageText = event.getParams()['text']
    messageHeader = event.getParams()['header']
    self.newChatMessage(messageChat, messageText, messageHeader)

  def newChatMessage(self, messageChat, messageText, messageHeader):
    """ Shows a new chat message on screen.
    messageChat: new chat message.
    """  
    ivMessageChat = messageChat.chatView(self.getScreen(), self, messageText, messageHeader)
    animTime = (len(messageText) / 12) * 1000
    if animTime < 2000:
      animTime = 2000 
    if messageChat.type == 3:
      animTime = animTime * 2   
    idleAnim = animation.IdleAnimation(animTime, ivMessageChat)
    positionAnim = animation.ScreenPositionAnimation(ANIM_CHAT_TIME2, ivMessageChat, ivMessageChat.getScreenPosition(), TEXT_BOX_OR, True)
    if not messageChat.type == 3:
      idleAnim.setOnStop(self.removeSprite, ivMessageChat.getTail())
    secAnim = animation.SecuenceAnimation()
    secAnim.addAnimation(idleAnim)
    secAnim.addAnimation(positionAnim)
    secAnim.setOnStop(self.printChatMessage, ivMessageChat)
    secAnim.setOnStop(self.__isoviewRoom.removeIsoViewItem, ivMessageChat)
    secAnim.setOnStop(self.removeSprite, ivMessageChat.getImg())
    ivMessageChat.setAnimation(secAnim)
    self.__isoviewRoom.addIsoViewChatItem(ivMessageChat)

  def quizAdded(self, event):
    """ Triggers after receiving a new quiz event.
    event: event info.
    """
    messageChat = event.getParams()['message']
    ivMessageChat = messageChat.chatView(self.getScreen(), self)
    self.__isoviewRoom.addIsoViewChatItem(ivMessageChat)
  
  def destinationChanged(self, event):
    """ Draws a destination marker on the room after a player destination change event.
    """  
    destination = event.getParams()['destination']
    ivPlayer = self.findIVItem(self.__player)
    ivPlayer.setDestination(destination)
    self.setMovementDestination(destination)

  def setMovementDestination(self, target):
    """ Adds a marker to the player's movement destination.
    target: movement destination.
    """  
    self.removeMovementDestination()
    self.__targetTileImage.rect.topleft = GG.utils.p3dToP2d(target, TILE_TARGET_SHIFT)
    self.__targetTileImage.zOrder = (pow(target[0], 2) + pow(target[1], 2))*10 - 1
    self.addSprite(self.__targetTileImage)        
    self.__targetTile = True  
    
  def removeMovementDestination(self):
    """ Removes the player's movement destination marker.
    """  
    try:
      self.removeSprite(self.__targetTileImage)  
    except KeyError:
        # This can happen if a sprite is removed before
        # update() has had a chance to be called.
      self.__targetTile = not self.__targetTile
      return
    self.__targetTile = not self.__targetTile
  
  def itemSelected(self, event):
    """ Triggers after receiving an item selected event.
    event: event info.
    """
    self.__selectedItem = event.getParams()['item']
    ivItem = self.findIVItem(self.__selectedItem)
    isTile = False
    if self.__accessMode:
      isTile = event.getParams()['isTile']
    itemName = event.getParams()['name']
    itemImageLabel = event.getParams()['imageLabel']
    highlight = event.getParams()['highlight']
    inventoryOnly = event.getParams()['inventoryOnly']
    options = event.getParams()['options']
    adminActions = event.getParams()['adminActions']
    if (not inventoryOnly and ivItem) or isTile:
      if highlight:  
        self.__isoviewRoom.itemSelected(self.__selectedItem)
      if isTile:
        selImgPos = self.__selectedItem.getPosition()
      else:
        selImgPos = ivItem.getPosition()
      self.__selectedImage.rect.topleft = GG.utils.p3dToP2d(selImgPos, SELECTED_FLOOR_SHIFT)
      self.addSprite(self.__selectedImage)        
    if (self.__accessMode and ivItem) or isTile:
      self.itemSelectedByAdmin(itemName, itemImageLabel, isTile, adminActions)
    if not isTile:
      self.itemSelectedByUser(itemName, itemImageLabel, options)
    
  def paintAdminOptions(self):
    """ Paints the admin action buttons on screen.
    """  
    self.adminOptions = guiobjects.OcempPanel(379, 95, [0, 431], ADMIN_OPTIONS_BACKGROUND)
    itemLabel = guiobjects.OcempLabel("Opciones avanzadas", guiobjects.STYLES["itemLabel"])
    itemLabel.topleft = 26, -4
    self.adminOptions.add_child(itemLabel)
    
    ACTIONS = [
      {"image":TELEPORT_IMAGE,    "action": self.auxWindowHandler,  "params":self.__teleportWindow,     "tooltip":"Teleportación"},
      {"image":CREATE_ITEM_IMAGE, "action": self.auxWindowHandler,  "params":self.__createItemsWindow,  "tooltip":"Panel de creación de objetos"},
      {"image":DELETE_ROOM_IMAGE, "action": self.auxWindowHandler,  "params":self.__deleteRoomWindow,   "tooltip":"Eliminar habitación"},
      {"image":CREATE_ROOM_IMAGE, "action": self.auxWindowHandler,  "params":self.__createRoomWindow,   "tooltip":"Crear habitación"},
      {"image":KICK_IMAGE,        "action": self.auxWindowHandler,  "params":self.__kickPlayerWindow,   "tooltip":"Expulsar jugador"},
      {"image":CHAT_IMAGE,        "action": self.auxWindowHandler,  "params":self.__broadcastWindow,    "tooltip":"Mensaje general"},
    ]
    
    i = 0
    for buttonData in ACTIONS:
      if buttonData["params"]:
        button = guiobjects.createButton(buttonData['image'], [13 + i*61, 40], [buttonData['tooltip'], self.showTooltip, self.removeTooltip], buttonData['action'], buttonData["params"])
      else:
        button = guiobjects.createButton(buttonData['image'], [13 + i*61, 40], [buttonData['tooltip'], self.showTooltip, self.removeTooltip], buttonData['action'])
      self.adminOptions.add_child(button)
      i += 1
    self.adminOptions.zOrder = 10000
    self.addSprite(self.adminOptions)
    self.widgetContainer.add_widget(self.adminOptions)
    
  def auxWindowHandler(self, window):
    """ Shows or hides the selected window.
    window: selected window.
    """  
    if window:
      if window == self.__kickPlayerWindow:
        if not self.__deleteRoomWindow.hide:
          self.__deleteRoomWindow.showOrHide()
        if not self.__teleportWindow.hide:
          self.__teleportWindow.showOrHide()
      if window == self.__deleteRoomWindow:
        if not self.__kickPlayerWindow.hide:
          self.__kickPlayerWindow.showOrHide()
        if not self.__teleportWindow.hide:
          self.__teleportWindow.showOrHide()
      if window == self.__teleportWindow:
        if not self.__deleteRoomWindow.hide:
          self.__deleteRoomWindow.showOrHide()
        if not self.__kickPlayerWindow.hide:
          self.__kickPlayerWindow.showOrHide()
      window.showOrHide()

  def applyKickPlayer(self, playerLabel):
    """ Teleports the player to another room.
    """  
    if not playerLabel:
      self.__player.newChatMessage("Escoja un jugador para expulsar", 1)
      return  
    player = self.getModel().getSpecificPlayer(playerLabel)
    if not player:
      self.__player.newChatMessage("Jugador no encontrado", 1)
      return  
    if player.username == self.__player.username:
      self.__player.newChatMessage("No puedes expulsarte a ti mismo", 1)
      return
    player.kick()

  def applyTeleport(self, roomLabel):
    """ Teleports the player to another room.
    roomLabel: new room's label.
    """  
    if not roomLabel:
      self.__player.newChatMessage("Escoja un destino para el teletransporte", 1)
      return  
    room = self.getModel().getRoom(roomLabel)
    if not room:
      self.__player.newChatMessage("La habitación seleccionada no existe", 1)
      return  
    pos = self.__player.getPosition()
    pos = room.getNearestEmptyCell(pos)
    
    if room.isFull():
      self.__player.newChatMessage("La habitación esta completa. Volvere a intentarlo mas tarde", 1)
      return
    itemList = self.__player.getTile().getItemsFrom(self.__player)
    for item in itemList:
      item.changeRoom(room, pos)
  
  def applyDeleteRoom(self, roomLabel):
    """ Deletes the selected room.
    roomLabel: room to be deleted.
    """  
    if not roomLabel:
      self.__player.newChatMessage("Escoja una habitación para eliminar", 1)
      return  
    room = self.getModel().getRoom(roomLabel)
    pos = self.__player.getPosition()
    pos = room.getNearestEmptyCell(pos)
    
    players = room.getPlayers()
    if not len(players) == 0:
      self.__player.newChatMessage("Error: la habitación seleccionada contiene jugadores", 1)
      return
    if GG.genteguada.GenteGuada.getInstance().deleteRoom(roomLabel):
      self.__player.newChatMessage("Habitación eliminada con éxito", 1)
    else:
      self.__player.newChatMessage("Error: habitación no encontrada", 1)  
     
  def itemSelectedByAdmin(self, itemName, itemImageLabel, isTile, adminActions):
    """ Paints the selected item actions admin pannel.
    itemName: selected item's name.
    itemImageLabel: selected item's image name.
    isTile: sets the selected item as tile or not.
    adminActions: item's available admin actions.
    """  
    actions = adminActions
    if not actions:
      return
    self.windowAdminActions = ocempgui.widgets.Window("Edición de objetos".decode("utf-8"))
    self.windowAdminActions.topleft = [GG.utils.SCREEN_SZ[0] - 151, 1]
    self.windowAdminActions.zOrder = 15000
    YShift = 50
    self.buttonBarAdminActions = guiobjects.OcempPanel(150, 427, [1, 1], GG.utils.ADMIN_ACTIONS_LARGE_BACKGROUND)
    self.windowAdminActions.child = self.buttonBarAdminActions
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(itemImageLabel)
    guiobjects.generateImageSize(filePath, [23,23], TOOLBAR_IMAGE)
    img = guiobjects.OcempImageButtonTransparent(TOOLBAR_IMAGE)
    img.topleft = 5, 6
    self.buttonBarAdminActions.add_child(img)
    itemLabel = guiobjects.OcempLabel(itemName, guiobjects.STYLES["teleportLabel"])
    itemLabel.topleft = 35, 0
    self.buttonBarAdminActions.add_child(itemLabel)
    self.editableFields = {}
    iPos = 0
    for key in sorted(actions.keys()):
      label = guiobjects.OcempLabel(key, guiobjects.STYLES["teleportLabel"])
      label.topleft = 10, 30 + iPos*YShift
      self.buttonBarAdminActions.add_child(label)
      if key == "image":
        height = 300
        listTiles = GG.utils.TILES + ["cont_hor.png","cont_vert.png","disc_hor.png","disc_vert.png"];
        self.tileImages = guiobjects.OcempImageList(145, height, listTiles, GG.utils.TILE)  
        self.tileImages.topleft = 5, 40 + iPos*YShift + 27
        self.buttonBarAdminActions.add_child(self.tileImages)  
        self.editableFields[key] = self.tileImages
        iPos += 2
      else:  
        fCount = 0
        fields = []
        for field in actions[key]:
          entryLabel = guiobjects.OcempEditLine()
          entryLabel.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
          try:
            entryLabel.text = field.decode("utf-8")  
          except:
            try:
              entryLabel.text = field
            except:
              entryLabel.text = str(field)
          entryLabel.border = 1
          entryLabel.topleft = 10 + fCount*65, 40 + iPos*YShift + 22
          if len(actions[key]) == 1:
            entryLabel.set_minimum_size(125, 20)
          else:    
            entryLabel.set_minimum_size(60, 20)
          self.buttonBarAdminActions.add_child(entryLabel)
          fields.append(entryLabel)
          fCount += 1
        self.editableFields[key] = fields
        iPos += 1
    buttonsHeight = 292 + 60   
    if not isTile:
      deleteButton = guiobjects.createButton(TINY_DELETE_IMAGE, [80, 0 + buttonsHeight], ["Eliminar objeto", self.showTooltip, self.removeTooltip], self.removeSelectedItemConfirmation)
      self.buttonBarAdminActions.add_child(deleteButton)
      copyButton = guiobjects.createButton(TINY_COPY_IMAGE, [10, 0 + buttonsHeight], ["Copiar objeto", self.showTooltip, self.removeTooltip], self.copySelectedItem)
      self.buttonBarAdminActions.add_child(copyButton)
    okButton = guiobjects.createButton(GG.utils.TINY_OK_IMAGE, [10, 35 + buttonsHeight], ["Aplicar cambios", self.showTooltip, self.removeTooltip], self.applyChanges)
    self.buttonBarAdminActions.add_child(okButton)
    cancelButton = guiobjects.createButton(GG.utils.TINY_CANCEL_IMAGE, [80, 35 + buttonsHeight], ["Descartar cambios", self.showTooltip, self.removeTooltip], self.discardChanges)
    self.buttonBarAdminActions.add_child(cancelButton)
    self.addSprite(self.windowAdminActions)
    self.widgetContainer.add_widget(self.windowAdminActions)
    self.__adminMenu = True
  
  def itemSelectedByUser(self, itemName, itemImageLabel, options):
    """ Paints the user action buttons.
    itemName: selected item's name.
    itemImageLabel: selected item's image name.
    options: item's available options.
    """  
    if not len(options):
      return
    self.__buttonBarActions = guiobjects.OcempPanel(259, 95, [GG.utils.SCREEN_SZ[0] - 260, 431], USER_ACTIONS_BACKGROUND)
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(itemImageLabel)
    guiobjects.generateImageSize(filePath, [23,23], TOOLBAR_IMAGE)
    img = guiobjects.OcempImageButtonTransparent(TOOLBAR_IMAGE)
    img.topleft = 5, 6
    self.__buttonBarActions.add_child(img)
    itemLabel = guiobjects.OcempLabel(itemName, guiobjects.STYLES["itemLabel"])
    itemLabel.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["itemLabel"]))
    itemLabel.topleft = 35, 0
    self.__buttonBarActions.add_child(itemLabel)
    i = 0
    self.__restoreActiveActionButtonsList()
    for action in options:
      button = guiobjects.createButton(self.__buttonActions[action]['image'], [195 - i*60, 40], [self.__buttonActions[action]['tooltip'], self.showTooltip, self.removeTooltip], self.__buttonActions[action]['action'])
      self.__buttonBarActions.add_child(button)
      i += 1
    self.__buttonBarActions.zOrder = 10000
    self.addSprite(self.__buttonBarActions)
    self.widgetContainer.add_widget(self.__buttonBarActions)

  def discardChanges(self):
    """ Discards the selected item's changes and closes the item's edit window.
    """  
    if self.__selectedItem:
      self.__player.setUnselectedItem()
      self.itemUnselected()

  def itemUnselected(self, event=None):
    """ Triggers after receiving an item unselected event.
    event: event info.
    """
    if self.__selectedItem:
      item = self.__selectedItem
      self.__selectedItem = None
      self.removeSprite(self.__selectedImage)
      self.__dropActionsItembuttons()
      if self.__isoviewRoom:
        self.__isoviewRoom.itemUnselected(item)
      self.__restoreActiveActionButtonsList()     
    
  def itemUnselectedSoft(self, item):
    """ Triggers after receiving an item unselected event.
    event: event info.
    """
    if not self.__selectedItem:
      return
    if not item.getName() == self.__selectedItem.getName():
      return
    self.itemUnselected()

  def pointsAdded(self, event):
    """ Updates the points label after receiving a points added event.
    event: event info.
    """
    self.__pointsLabel.label = "GuadaPuntos: " + str(event.getParams()["points"])
    self.__pointsLabel.set_text("GuadaPuntos: " + str(event.getParams()["points"]))
    self.hud.remove_child(self.__pointsLabel)
    self.hud.add_child(self.__pointsLabel)
    
  def clockAdded(self, event):
    """ Updates the exp label after receiving an exp added event.
    event: event info.
    """  
    self.__labelOld.label = "ClockPuntos: " + str(event.getParams()["clock"])
    self.__labelOld.set_text("ClockPuntos: " + str(event.getParams()["clock"]))
    self.hud.remove_child(self.__labelOld)
    self.hud.add_child(self.__labelOld)
    
  def expAdded(self, event):
    """ Updates the exp label after receiving an exp added event.
    event: event info.
    """  
    self.__expLabel.label = "Experiencia: " + str(event.getParams()["exp"])
    self.__expLabel.set_text("Experiencia: " + str(event.getParams()["exp"]))
    self.hud.remove_child(self.__expLabel)
    self.hud.add_child(self.__expLabel)

  def paintActionButtons(self):
    """ Paints the general action buttons.
    """
    ACTIONS = [
      {"image":EXIT_IMAGE,      "action": self.finishGame,        "tooltip":"Finalizar (X)"},
      {"image":MAXIMIZE_IMAGE,  "action": self.showFullScreen,    "tooltip":"Maximizar o minimizar pantalla (F)"},
      {"image":SOUND_IMAGE,     "action": self.showSoundControl,  "tooltip":"Controles de sonido (S)"},
      {"image":ADMIN_IMAGE,     "action": self.showAdminActions,  "tooltip":"Cambiar/eliminar vista administrador"}
    ]
    if self.__fullScreen:
      ACTIONS[1]["image"] = MINIMIZE_IMAGE
    i = 0
    for buttonData in ACTIONS:
      if buttonData['action'] == self.showAdminActions and not self.__player.admin:
        break
      button = guiobjects.createButton(buttonData['image'], [16 + i*60, 10], [buttonData['tooltip'], self.showTooltip, self.removeTooltip], buttonData['action'])
      if buttonData['action'] == self.showAdminActions:
        self.__adminButton = button
      if buttonData['action'] == self.showFullScreen:
        self.__fullscreenButton = button
      elif  buttonData['action'] == self.showSoundControl:
        self.__soundButton = button
      i += 1
      self.hud.add_child(button)

  def showAdminActions(self):
    if self.__accessMode:
      self.__accessMode = False
      self.__player.setAccessMode(False)
      self.removeSprite(self.adminOptions)
      self.widgetContainer.remove_widget(self.adminOptions)
      self.__closeAllWindow()
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(ADMIN_IMAGE)
    else: 
      self.__accessMode = True
      self.__player.setAccessMode(True)
      self.paintAdminOptions()
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(NOADMIN_IMAGE)
    self.itemUnselected()
    self.removeSprite(self.roomInfo)
    self.widgetContainer.remove_widget(self.roomInfo)
    self.__paintRoomInfo()
    self.__adminButton.picture = ocempgui.draw.Image.load_image(imgPath)
    self.hud.remove_child(self.__adminButton)
    self.hud.add_child(self.__adminButton)
      
  def newBroadcastMessage(self, line):
    """ Sends a new broadcast message.
    line: new message.
    """  
    self.getModel().newBroadcastMessage(line)
  
  def createRoom(self, label, size, img, maxUsers, enabled, startRoom, copyRoom=None):
    """ Creates a new room and teleports the admin there.
    label: room label.
    size: room size.
    img: room's default tile image.
    maxUsers: max users per room.
    enabled: sets the room as enabled or disabled.
    startRoom: sets the room as start room or not.
    copyRoom: room to be copied.
    """  
    if self.getModel().getRoom(label):
      self.__player.newChatMessage("La etiqueta de habitación ya existe.", 1)
      return
    room = GG.genteguada.GenteGuada.getInstance().createRoom(label, size, img, maxUsers, enabled, startRoom, copyRoom)
    if not room:
      self.__player.newChatMessage("La etiqueta de habitación ya existe.", 1)
      return
    pos = room.getNearestEmptyCell(self.__player.getPosition())
    itemList = self.__player.getTile().getItemsFrom(self.__player)
    for item in itemList:
      item.changeRoom(room, pos)
        
  def privateChatHandler(self):
    """ Handles the private chat window.
    """  
    self.__privateChatWindow.showOrHide()

  def changeChatButton(self):
    """ Changes the private chat button appearance.
    """  
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(PRIVATE_CHAT_IMAGE)
    self.__privateChatButton.picture = ocempgui.draw.Image.load_image(imgPath)
    self.hud.remove_child(self.__privateChatButton)
    self.hud.add_child(self.__privateChatButton)

  def showTooltip(self, label):
    """ Shows the selected button tooltip.
    label: tooltip label.
    """  
    self.__tooltipWindow = ocempgui.widgets.TooltipWindow (label.decode("utf-8"))
    x, y = pygame.mouse.get_pos ()
    szX, szY = self.__tooltipWindow.size
    if (x + 8 + szX) > GG.utils.GAMEZONE_SZ[0]:
      self.__tooltipWindow.topleft = GG.utils.GAMEZONE_SZ[0] - szX, y - 5
    else:
      self.__tooltipWindow.topleft = x + 8, y - 5
    self.__tooltipWindow.depth = 99 # Makes it the topmost widget.
    self.__tooltipWindow.zOrder = 30000
    self.addSprite(self.__tooltipWindow)
      
  def removeTooltip(self):
    """ Removes the active tooltip.
    """
    if self.__tooltipWindow:
      self.removeSprite(self.__tooltipWindow)  
      self.__tooltipWindow.destroy ()
      self.__tooltipWindow = None
  
  def showDresser(self):
    """ Shows the avatar configuration window.
    """  
    wardrobe = avatareditor.AvatarEditor(self, self.__player.getAvatarConfiguration())
    self.__winWardrobe = wardrobe.draw()
    self.addSprite(self.__winWardrobe)
    self.widgetContainer.add_widget(self.__winWardrobe)
    self.__activeWindow = True
    
  def closeDresser(self, configuration=None):
    """ Closes the avatar configuration window.
    configuration: avatar configuration.
    """  
    if configuration:
      self.__player.newChatMessage("Hemos mandado a confeccionar tu nuevo traje, en cuanto este listo, te lo cambiaremos por el que tienes",1)
      self.setAvatarConfiguration(configuration)
    self.widgetContainer.remove_widget(self.__winWardrobe)  
    self.removeSprite(self.__winWardrobe)
    self.__winWardrobe.destroy()
    self.__winWardrobe = None
    self.__activeWindow = False
    
  def setAvatarConfiguration(self, configuration):
    """ Sets a new avatar configuration.
    configuration: new avatar configuration.
    """
    GG.genteguada.GenteGuada.getInstance().uploadAvatarConfiguration(configuration, self.__player)
    
  def turnRight(self):
    """ Turns the player to the right.
    """  
    if not self.findIVItem(self.__player).hasAnimation():
      self.__player.turnRight()
    
  def turnLeft(self):
    """ Turns the player to the left.
    """  
    if not self.findIVItem(self.__player).hasAnimation():
      self.__player.turnLeft()
    
  def showSoundControl(self):
    """ Enables or disables the sound effects.
    """
    if self.__sound:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(MUTE_IMAGE)
      self.__soundButton.picture = ocempgui.draw.Image.load_image(imgPath)
    else:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(SOUND_IMAGE)
      self.__soundButton.picture = ocempgui.draw.Image.load_image(imgPath)
    self.hud.remove_child(self.__soundButton)
    self.hud.add_child(self.__soundButton)
    self.__sound = not self.__sound
    
  def finishGame(self, event = None):
    """ Finishes the game.
    """  
    GG.genteguada.GenteGuada.getInstance().finish()

    
  def showFullScreen(self):
    """ Toggles the fullscreen mode.
    """
    #TODO solo funciona en linux con las X, para e
    if self.__fullScreen:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(MAXIMIZE_IMAGE)
      self.__fullscreenButton.picture = ocempgui.draw.Image.load_image(imgPath)
    else:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(MINIMIZE_IMAGE)
      self.__fullscreenButton.picture = ocempgui.draw.Image.load_image(imgPath)
    self.hud.remove_child(self.__fullscreenButton)
    self.hud.add_child(self.__fullscreenButton)
    self.__fullScreen = not self.__fullScreen
    pygame.display.toggle_fullscreen()
    
  def paintUserActions(self):
    """ Paints the user action buttons.
    """
    ACTIONS = [
      {"image":PRIVATE_CHAT_IMAGE,  "action": self.privateChatHandler,  "tooltip":"Abre o cierra chat privado (Z)"},
      {"image":ROTATE_RIGHT_IMAGE,  "action": self.turnRight,           "tooltip":"Rotar derecha (R)"},
      {"image":ROTATE_LEFT_IMAGE,   "action": self.turnLeft,            "tooltip":"Rotar izquierda (L)"},
      {"image":JUMP_IMAGE,          "action": self.jump,                "tooltip":"Saltar (J)"},
      {"image":DRESSER_IMAGE,       "action": self.showDresser,         "tooltip":"Cambiar configuración avatar (D)"},
    ]
    i = 0
    for buttonData in ACTIONS:
      button = guiobjects.createButton(buttonData['image'], [950 - i * 60 , 10], [buttonData["tooltip"], self.showTooltip, self.removeTooltip], buttonData['action'])
      self.hud.add_child(button)
      i += 1
      if buttonData['action'] == self.privateChatHandler:
        self.__privateChatButton = button
    expPackage = self.__player.getExpInforPackage()
    image = expPackage["imageLabel"]
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(image)
    guiobjects.generateImageSize(filePath, [64, 64], MASKUSER_IMAGE)
    self.imgMask = guiobjects.OcempImageButtonTransparent(MASKUSER_IMAGE)
    self.imgMask.topleft = 524, 110
    self.hud.add_child(self.imgMask)
    labelUserName = guiobjects.OcempLabel(self.__player.username, guiobjects.STYLES["userName"])
    labelUserName.topleft = 622, 75
    self.hud.add_child(labelUserName)
    self.__pointsLabel = guiobjects.OcempLabel("GuadaPuntos: " + str(expPackage["points"]), guiobjects.STYLES["pointLabel"])
    self.__pointsLabel.topleft = 590, 110
    self.hud.add_child(self.__pointsLabel)
    self.__labelOld = guiobjects.OcempLabel("ClockPuntos: " + str(expPackage["playedTime"]), guiobjects.STYLES["pointLabel"])
    self.__labelOld.topleft = 590, 135
    self.hud.add_child(self.__labelOld)
    self.__expLabel = guiobjects.OcempLabel("Experiencia: " + str(expPackage["exp"]), guiobjects.STYLES["pointLabel"])
    self.__expLabel.topleft = 590, 160
    self.hud.add_child(self.__expLabel)

  def jump(self):
    """ Makes the player jump.
    """  
    #self.getModel().getSystem().deletePlayer("pepa")
    #self.getModel().getSystem().deleteGift("recopetin")
    if not self.findIVItem(self.__player).hasAnimation():
      self.__player.jump()

  def itemToJumpOver(self):
    """ Makes the player jump over an item.
    """  
    self.__player.jumpOver()

  def __dropActionsItembuttons(self):
    """ Removes the action buttons from the screen.
    """
    self.removeTooltip()
    self.__dropUserOptions()
    if self.__adminMenu:
      self.__dropAdminOptions()

  def __dropUserOptions(self):
    """ Removes the user's option buttons from the screen.
    """
    if self.__buttonBarActions:
      for child in self.__buttonBarActions.children:
        self.__buttonBarActions.remove_child(child)
        child.destroy()
      self.widgetContainer.remove_widget(self.__buttonBarActions)
      self.__buttonBarActions.destroy()
      self.__buttonBarActions = None

  def __dropAdminOptions(self):
    """ Removes the admin's option buttons from the screen.
    """
    for child in self.buttonBarAdminActions.children:
      self.buttonBarAdminActions.remove_child(child)
      child.destroy()
    self.widgetContainer.remove_widget(self.windowAdminActions)
    self.windowAdminActions.destroy()
    self.windowAdminActions = None
    self.__adminMenu = False

  def itemToInventory(self):
    """ Brings an item from the room to the player's inventory.
    """
    if self.__selectedItem:
      self.__player.tryToInventory(self.__selectedItem)

  def moneyToInventory(self):
    """ Picks up money from the room and deletes the money object.
    """  
    if self.__selectedItem:
      ivItem = self.findIVItem(self.__selectedItem)
      ivItem.updateZOrder(40000)
      positionAnim = animation.ScreenPositionAnimation(ANIM_INVENTORY_TIME, ivItem, ivItem.getScreenPosition(), [565, 90+568], True)
      positionAnim.setOnStop(self.__isoviewRoom.getModel().removeItem, self.__selectedItem)
      if self.__player.tryToPocket(self.__selectedItem):
        ivItem.setAnimation(positionAnim)
    
  def itemCopyToInventory(self):
    """ Brings an item from the room to the player's inventory.
    """
    if self.__selectedItem:
      self.__player.tryToInventoryCopy(self.__selectedItem)

  def itemCopyToInventoryRemove(self):
    """ Brings an item from the room to the player's inventory.
    """
    if self.__selectedItem:
      self.__player.tryToInventoryCopy(self.__selectedItem)
      self.room.removeItem(self.__selectedItem)

  def itemToClone(self):
    """ Clones an item from the room and inserts it on the player's inventory
    """
    clone = self.__selectedItem.getClone()
    self.__player.addInventory(clone)
    self.itemUnselected()
    
  def itemToTalkAndGet(self):
    """ Talks to an item and gets another one.
    """
    if self.__selectedItem:
      item = self.__player.talkAndGetFrom(self.__selectedItem)
 
  def itemToTalk(self):
    """ Talks to an item.
    """
    self.__player.talkTo(self.__selectedItem)

  def exchangeItemPlayer(self):
    """ Shows the trade window.
    """
    self.__player.initExchangeTo(self.__selectedItem)
    
  def itemToOpen(self):
    """ Attempts to open a teleporter item.
    """
    self.__player.open(self.__selectedItem)

  def itemToUrl(self):
    """ Attempts to open an url adress.
    """
    if self.__fullScreen:
      self.__fullScreen = False
      pygame.display.toggle_fullscreen()
    webbrowser.open(self.__selectedItem.getUrl())
    self.itemUnselected()

  def itemToLift(self):
    """ Picks an item and takes it ove the player's head.
    """
    self.__player.lift(self.__selectedItem)
    
  def itemToDrop(self):
    """ Drops a picked item in front of the player.
    """  
    self.__player.drop(self.__selectedItem)
    #self.itemUnselected()

  def initExchange(self, event):
    """ Starts the exchange project after receiving an exchange event.
    event: event info.
    """  
    itemList = event.getParams()["itemList"]
    if len(itemList):
      step = 2
    else:
      step = 1
    self.__exchangeWindow = exchangewindow.ExchangeWindow(self, step, itemList)
    self.__exchangeWindow.draw()
    self.addSprite(self.__exchangeWindow.window)
    self.widgetContainer.add_widget(self.__exchangeWindow.window)
    self.__activeWindow = True
    
  def itemToExchange(self):
    """ Attempts to exchange an item with another player.
    """  
    self.__exchangeWindow.addItemOut(self.__selectedItem)
    self.__player.setUnselectedItem()

  def cancelExchange(self, event):
    """ Cancels the exchange process after receiving a cancel exchange event.
    event: event info.
    """  
    self.widgetContainer.remove_widget(self.__exchangeWindow.window)
    self.removeSprite(self.__exchangeWindow.window)
    self.__exchangeWindow = None
    self.__activeWindow = False

  def addListExchange(self, event):
    """ Adds an item to the exchange list after receiving an event.
    event: event info.
    """  
    itemList = event.getParams()["list"]
    self.__exchangeWindow.addInList(itemList) 

  def itemToClimb(self):
    """ Climbs over an item.
    """
    self.__player.climb(self.__selectedItem)
    self.itemUnselected()
    
  def itemToGiveCard(self):
    """ Gives a contact card to another player.
    """  
    self.__selectedItem.checkContact(self.__player)
    self.itemUnselected()
    
  def newContactDialog(self, event):
    """ Shows the new contact confirmation dialog after receiving an event.
    event: event info.
    """  
    if self.__activeContactDialog:
      return  
    newContact = event.getParams()["contact"]
    self.confirmDialog = guiobjects.OcempPanel(300, 120, [1, 1], CONTACT_WINDOW_BACKGROUND)
    cad = "Intercambiar tarjetas con " + newContact.username 
    questionLabel = guiobjects.OcempLabel(cad, guiobjects.STYLES["dialogFont"])
    questionLabel.topleft = 22, 20 
    self.confirmDialog.add_child(questionLabel)
    okButton = guiobjects.createButton(OK_BUTTON_IMAGE, [20, 55], None, self.giveContactCard, event.getParams()['contact'])
    cancelButton = guiobjects.createButton(CANCEL_BUTTON_IMAGE, [170, 55], None, self.dropContactDialog)
    self.confirmDialog.add_child(okButton)
    self.confirmDialog.add_child(cancelButton)
    self.confirmDialog.zOrder = 20000
    self.addSprite(self.confirmDialog)
    self.widgetContainer.add_widget(self.confirmDialog)
    self.__activeContactDialog = event.getParams()['contact']
    
  def giveContactCard(self, contact):
    """ Gives a contact card to another player.
    contact: new contact.
    """ 
    contact.addContact(self.__player)
    self.__player.addContact(contact)
    self.dropContactDialog()
      
  def dropContactDialog(self):
    """ Hides the private contacts window.
    """  
    self.removeSprite(self.confirmDialog)
    self.widgetContainer.remove_widget(self.confirmDialog)
    self.__activeContactDialog = None
    self.itemUnselected()
    
  def newContactAdded(self, event):
    """ Updates the contacts window after receiving a contact added event.
    event: event info.
    """  
    self.__privateChatWindow.updateContactList()
    
  def privateChatReceived(self, event):
    """ Triggers after receiving a new private chat message event.
    event: event info.
    """  
    chat = event.getParams()['chat']
    player = event.getParams()['player']
    if self.__privateChatWindow.hide == True:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(NOTIFICATION_IMAGE)
      self.__privateChatButton.picture = ocempgui.draw.Image.load_image(imgPath)
      self.hud.remove_child(self.__privateChatButton)
      self.hud.add_child(self.__privateChatButton)
      mail = FakeModel("book.png", "correo")
      posOrigin = [0, 0]
      pos = [960, 540]
      invItem = isoview_inventoryitem.IsoViewInventoryItem(mail, self.getScreen(), self)
      positionAnim = animation.ScreenPositionAnimation(ANIM_INVENTORY_TIME*2, invItem, posOrigin, pos, True)
      self.addSprite(invItem.getImg())
      self.__isoviewInventory.append(invItem)
      positionAnim.setOnStop(self.removeSprite, invItem.getImg())  
      positionAnim.setOnStop(self.__isoviewInventory.remove, invItem)
      invItem.setAnimation(positionAnim)
    self.__privateChatWindow.incomingChatMessage(chat, player)
      
  def removeContactRemote(self, event):
    """ Triggers after receiving a remove contact event from another player.
    event: event info.
    """  
    contact = event.getParams()['contact']
    self.__privateChatWindow.removeContactRemote(contact)      

  def unsubscribeAllEvents(self):
    """ Unsubscribes the active room and the isoview hud object from all events.
    """  
    if self.__isoviewRoom:
      self.__isoviewRoom.unsubscribeAllEvents()
    self.__player.unsubscribeEventObserver(self)
    isoview.IsoView.unsubscribeAllEvents(self) 
  
  def playerConfigurationChanged(self, event):
    """ Triggers after receiving a player avatar configuration change event.
    event: event info.
    """  
    image = event.getParams()['imageLabel']
    os.remove(GG.genteguada.GenteGuada.getInstance().getDataPath(image))
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(image)
    guiobjects.generateImageSize(filePath, [64, 64], MASKUSER_IMAGE)
    img = ocempgui.draw.Image.load_image(MASKUSER_IMAGE)
    self.imgMask.picture = img
    self.hud.remove_child(self.imgMask)
    self.hud.add_child(self.imgMask)

  def contactMaskChanged(self, event):
    """ Triggers after receiving a contact mask change event.
    event: event info.
    """  
    contactName =  event.getParams()['playerName']
    image = event.getParams()['imageLabel']
    self.__privateChatWindow.contactsArea.updateMaskPlayer(contactName, image)

  def applyChanges(self):
    """ Applies the changes to the selected item attributes.
    """  
    result = {}
    selectedItem = self.__selectedItem
    for key in self.editableFields:
      if key in ["Posicion", "Posicion salida"]:
        result[key] = [self.editableFields[key][0].text,self.editableFields[key][1].text]
      elif key == "image":
        result[key] = self.editableFields[key].getSelectedName()
      else:
        result[key] = self.editableFields[key][0].text
    pos = selectedItem.applyChanges(result, self.__player, self.room)
    if pos:
      self.__selectedImage.rect.topleft = GG.utils.p3dToP2d(pos, SELECTED_FLOOR_SHIFT)
    return 
    
  def removeSelectedItemConfirmation(self):
    """ Shows the confirmation dialog to delete the selected item.
    """  
    self.__deleteConfirmDialog = guiobjects.OcempPanel(300, 120, [1, 1], CONTACT_WINDOW_BACKGROUND)
    questionLabel = guiobjects.OcempLabel("Eliminar objeto seleccionado", guiobjects.STYLES["dialogFont"])
    questionLabel.topleft = 38, 20 
    self.__deleteConfirmDialog.add_child(questionLabel)
     
    okButton = guiobjects.createButton(OK_BUTTON_IMAGE, [20, 55], None, self.removeSelectedItem)
    cancelButton = guiobjects.createButton(CANCEL_BUTTON_IMAGE, [170, 55], None, self.dropRemoveSelectedDialog)
    self.__deleteConfirmDialog.add_child(okButton)
    self.__deleteConfirmDialog.add_child(cancelButton)
    self.__deleteConfirmDialog.zOrder = 20000
    self.addSprite(self.__deleteConfirmDialog)
    self.widgetContainer.add_widget(self.__deleteConfirmDialog)
    
  def removeSelectedItem(self):
    """ Removes selected item from the game.
    """  
    item = self.__selectedItem
    self.dropRemoveSelectedDialog()
    self.__isoviewRoom.getModel().removeItem(item)
    
  def dropRemoveSelectedDialog(self):
    """ Closes the remove item dialog.
    """  
    self.itemUnselected()
    self.removeSprite(self.__deleteConfirmDialog)
    self.widgetContainer.remove_widget(self.__deleteConfirmDialog)
    self.__deleteConfirmDialog = None

  def changeAvatarImages(self, avatar, path, timestamp):
    """ Changes the player's avatar images.
    avatar: player's avatar.
    path: new image path.
    """  
    if self.__isoviewRoom:
      self.__isoviewRoom.changeAvatarImages(avatar, path, timestamp) 

  def reloadImage(self, img):
    """ Reloads the selected image.
    img: selected image.
    """  
    self.removeSprite(img)
    self.addSprite(img)  

  def copySelectedItem(self):
    """ Copies the selected room item.
    """  
    try: 
      posX = int(self.editableFields['Posicion'][0].text)    
      posY = int(self.editableFields['Posicion'][1].text)    
    except ValueError:
      self.__player.newChatMessage('Valor "Posicion" incorrecto', 1)
      return
    position = self.__isoviewRoom.getModel().getNearestEmptyCell([posX, posY])
    if position:
      objectSelected = self.__selectedItem
      self.itemUnselected()
      itemCopy = self.getModel().copyObject(objectSelected,self.__isoviewRoom.getModel(),position,self.__player)
      self.__player.setSelectedItem(itemCopy)
    else:
      self.__player.newChatMessage("No hay sitio en la habitación", 1)
