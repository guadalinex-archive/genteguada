# -*- coding: iso-8859-15 -*-

import pygame
import GG.utils
import isoview
import isoview_inventoryitem
import ocempgui.widgets
import ocempgui.draw
import copy
import random
import avatareditor
import animation
import exchangewindow
import privatechatwindow

from pygame.locals import * # faster name resolution


class IsoViewHud(isoview.IsoView): 
  """ IsoViewHud class.
  Defines the HUD.
  """
  
  def __init__(self, model, screen, parent, fullscreen):
    """ Class constructor.
    model: ggsession model.
    screen: screen handler.
    parent: session handler.
    fullscreen: sets the game as started on fullscreen or not.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__isoviewInventory = []
    self.__player = self.getModel().getPlayer()
    
    self.__allSprites = GG.utils.GroupSprite()
    
    bgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.BG_BLACK)
    self.__bg = pygame.sprite.Sprite()
    self.__bg.image = pygame.image.load(bgPath).convert_alpha()
    self.__bg.rect = self.__bg.image.get_rect()
    self.__bg.rect.topleft = GG.utils.BG_FULL_OR
    self.__bg.zOrder = -2
    
    self.__isoviewRoom = self.__player.getRoom().defaultView(self.getScreen(), self)
    self.textArea = None
    self.__textField = None
    self.windowInventory = None
    self.privateChatWindow = privatechatwindow.PrivateChatWindow("Chat Privado", self.__player)
    self.privateChatWindow.hide = True
    
    if fullscreen:
      self.__fullScreen = True
    else:
      self.__fullScreen = False
    self.__sound = True
    
    self.__soundButton = None
    self.__fullscreenButton = None
    self.__privateChatButton = None
    
    self.__img = pygame.sprite.Sprite()
    #self.__img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.INTERFACE_LOWER)).convert_alpha()
    self.__img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.HUD_PATH + GG.utils.INTERFACE_LOWER)).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = GG.utils.HUD_OR[0],GG.utils.HUD_OR[1] - 70
    self.__img.zOrder = -1
    
    model.subscribeEvent('chatAdded', self.chatAdded)
    self.__player.subscribeEvent('quizAdded', self.quizAdded)
    self.__player.subscribeEvent('room', self.roomChanged)
    #elf.__player.subscribeEvent('addInventory', self.inventoryAdded)
    self.__player.subscribeEvent('liftItem', self.liftItem)
    self.__player.subscribeEvent('dropItem', self.dropItem)
    self.__player.subscribeEvent('addToInventory', self.addItemToInventory)
    self.__player.subscribeEvent('removeFromInventory', self.inventoryRemoved)
    self.__player.subscribeEvent('selectedItem', self.itemSelected)
    self.__player.subscribeEvent('unselectedItem', self.itemUnselected)
    self.__player.subscribeEvent('points', self.pointsAdded)
    self.__player.subscribeEvent('clock', self.clockAdded)
    self.__player.subscribeEvent('exp', self.expAdded)
    self.__player.subscribeEvent('initExchange', self.initExchange)
    self.__player.subscribeEvent('cancelExchange', self.cancelExchange)
    self.__player.subscribeEvent('listExchange', self.addListExchange)
    self.__player.subscribeEvent('contactDialog', self.newContactDialog)
    self.__player.subscribeEvent('contactAdded', self.newContactAdded)
    self.__player.subscribeEvent("privateChatReceived", self.privateChatReceived)
    self.__player.subscribeEvent("removeContactRemote", self.removeContactRemote)
    
    self.__selectedItem = None
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("tiles/" + GG.utils.TILE_SELECTED)  
    self.__selectedImage = pygame.sprite.Sprite()
    self.__selectedImage.image = pygame.image.load(imgPath).convert_alpha()
    self.__selectedImage.rect = self.__selectedImage.image.get_rect()
    
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("tiles/" + GG.utils.TILE_TARGET)  
    self.__targetTile = None
    self.__targetTileImage = pygame.sprite.Sprite()
    self.__targetTileImage.image = pygame.image.load(imgPath).convert_alpha()
    self.__targetTileImage.rect = self.__targetTileImage.image.get_rect()
    
    self.__activeActions = []
    self.restoreActiveActionButtonsList()
    
    self.buttonActions = {
        "inventory":{"image":"interface/hud/movein.png", "action": self.itemToInventory, "tooltip":"Al inventario (P)"},
        "copy":{"image":"interface/hud/movein.png", "action": self.itemCopyToInventory, "tooltip":"Al inventario (C)"},
        "removeInventory":{"image":"interface/hud/moveout.png", "action": self.itemOutInventory, "tooltip":" Sacar del inventario (M)"},
        "lift":{"image":"interface/hud/lift.png", "action": self.itemToLift, "tooltip":"Levantar (I)"},
        "drop":{"image":"interface/hud/drop.png", "action": self.itemToDrop, "tooltip":"Soltar (Q)"},
        "climb":{"image":"interface/hud/climb.png", "action": self.itemToClimb, "tooltip":"Subir (B)"},
        "clone":{"image":"interface/hud/movein.png", "action": self.itemToClone, "tooltip":"Al inventario (Y)"},
        "push":{"image":"interface/hud/push.png", "action": self.itemToPush, "tooltip":"Empujar (K)"},
        "up":{"image":"interface/hud/lift.png", "action": self.itemToUp, "tooltip": "Subir (P)"},
        "talk":{"image":"interface/hud/chat.png", "action": self.itemToTalk, "tooltip":"Hablar (T)"},
        "talkAndGet":{"image":"interface/hud/chat.png", "action": self.itemToTalkAndGet, "tooltip":"Hablar (G)"},
        "privateChat":{"image":"interface/hud/privatechat.png", "action": self.privateChat, "tooltip":"Chat (H)"},
        "exchange":{"image":"interface/hud/exchange.png", "action": self.exchangeItemPlayer, "tooltip":"Intercambiar (E)"},
        "open":{"image":"interface/hud/open.png", "action": self.itemToOpen, "tooltip":"Abrir (O)"},
        "url":{"image":"interface/hud/www.png", "action": self.itemToUrl, "tooltip":"Ir a (W)"},
        "toExchange":{"image":"interface/hud/exchange.png", "action": self.itemToExchange, "tooltip":"Intercambiar (A)"},
        "giveCard":{"image":"interface/hud/contact.png", "action": self.itemToGiveCard, "tooltip":"Dar tarjeta de visita (V)"},
        "money":{"image":"interface/hud/movein.png", "action": self.moneyToInventory, "tooltip":"Recoger puntos (N)"}
    }
    
    self.hotkeys = {K_x: self.finishGame, K_f: self.showFullScreen, K_s: self.showSoundControl, \
                    K_d: self.showDresser, K_j: self.jump, K_r: self.turnRight, K_l: self.turnLeft, \
                    K_p: self.itemToInventory, K_c: self.itemCopyToInventory, K_m: self.itemOutInventory, \
                    K_i: self.itemToLift , K_q: self.itemToDrop , K_b: self.itemToClimb , \
                    K_y: self.itemToClone , K_k: self.itemToPush , K_p: self.itemToUp , \
                    K_t: self.itemToTalk , K_g: self.itemToTalkAndGet , K_h: self.privateChat , \
                    K_e: self.exchangeItemPlayer , K_o: self.itemToOpen , K_w: self.itemToUrl , \
                    K_a: self.itemToExchange, K_v: self.itemToGiveCard, K_z: self.privateChatHandler, \
                    K_n: self.moneyToInventory}
                          
    self.winWardrobe = None
    self.wardrobe = None
    self.exchangeWindow = None
    self.activeExchageWindow = False
    self.activeQuizWindow = False
    self.activeContactDialog = None
    self.tooltipWindow = None
    self.ctrl = 0
  
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
          self.ctrl = 0
      elif event_type == KEYDOWN:
        if self.ctrl:
          if event.key in self.hotkeys.keys():
            if self.hotkeys[event.key] in self.__activeActions:
              self.hotkeys[event.key]()
        else:  
          if event.key == K_LCTRL or event.key == K_RCTRL:
            self.ctrl = 1  
          if event.key == K_ESCAPE:
            GG.genteguada.GenteGuada.getInstance().finish()
          elif event.key == K_RETURN: 
            if self.privateChatWindow:
              if not self.privateChatWindow.hide:
                self.privateChatWindow.chatMessageEntered()
              else:
                self.chatMessageEntered()
            else:
              self.chatMessageEntered()
      elif event_type == MOUSEBUTTONDOWN:
        if not self.windowOpen():
          cordX, cordY = pygame.mouse.get_pos()
          if 0 <= cordY <= GG.utils.HUD_OR[1]:
            dest, item = self.getIsoviewRoom().findTile([cordX, cordY])
            if not dest == [-1, -1, -1]:
              self.__isoviewRoom.getModel().clickedByPlayer(self.__player, dest, item)
    self.widgetContainer.distribute_events(*events)

  def windowOpen(self):
    """ Checks if there is an open window.
    """  
    if self.activeExchageWindow:
      return True
    if self.activeQuizWindow:
      return True
    if self.privateChatWindow:
      if not self.privateChatWindow.hide:
        return True
    if self.activeContactDialog:
      return True
    return False

  def restoreActiveActionButtonsList(self):
    """ Restore the active action button list.
    """  
    self.__activeActions = []  
    self.__activeActions.append(self.finishGame)
    self.__activeActions.append(self.showFullScreen)
    self.__activeActions.append(self.showSoundControl)
    self.__activeActions.append(self.showDresser)
    self.__activeActions.append(self.jump)
    self.__activeActions.append(self.turnRight)
    self.__activeActions.append(self.turnLeft)
    self.__activeActions.append(self.privateChatHandler)
    
  def compareSelectedItem(self, item):
    """ Compares a given item with the selected item.
    item: item to be compared.
    """  
    if self.__selectedItem:  
      return self.__selectedItem.checkSimilarity(item)
    else:
      return False

  def setActiveQuizWindow(self, value):
    """ Sets the active quiz window with a new value
    """  
    self.activeQuizWindow = value
    
  def getActiveQuizWindow(self):
    """ Returns the active quiz window.
    """  
    return self.activeQuizWindow

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
      
  def liftItem(self, event):
    """ Triggers after receiving a lift item event.
    event: event info.
    """ 
    item = event.getParams()["item"]  
    pos = event.getParams()["position"]
    ivItem = self.__isoviewRoom.findIVItem(item)  
    if ivItem != None:
      self.__isoviewRoom.updateScreenPositionsOn(pos)  
    
  def dropItem(self, event):
    """ Triggers after receiving a drop item event.
    event: event info.
    """ 
    item = event.getParams()["item"]  
    pos = event.getParams()["position"]
    ivItem = self.__isoviewRoom.findIVItem(item)  
    if ivItem != None:
      self.__isoviewRoom.updateScreenPositionsOn(pos)  
      
  def addItemToInventory(self, event):
    """ Triggers after receiving an item added to inventory event.
    event: event info.
    """ 
    item = event.getParams()["item"]
    posOrigin = event.getParams()["position"]
    posX = len(self.__isoviewInventory)%GG.utils.INV_ITEM_COUNT[0]
    posY = len(self.__isoviewInventory)/GG.utils.INV_ITEM_COUNT[1]
    pos = [GG.utils.INV_OR[0] + (posX * GG.utils.INV_ITEM_SZ[0]), GG.utils.INV_OR[1] + (posY * GG.utils.INV_ITEM_SZ[1])]
    ivItem = self.findIVItem(item)
    invItem = isoview_inventoryitem.IsoViewInventoryItem(item, self.getScreen(), self)
    if ivItem != None:
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            GG.utils.p3dToP2d(posOrigin, item.anchor), pos, True)
      positionAnim.setOnStop(item.getRoom().removeItem, item)
      positionAnim.setOnStop(self.removeSprite, ivItem.getImg())
    else:
      ivItem = item.defaultView(self.getScreen(), self.__isoviewRoom, self)
      self.__isoviewRoom.addIsoViewItem(ivItem)  
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            GG.utils.p3dToP2d(posOrigin, [0, 0]), pos, True)
      positionAnim.setOnStop(self.removeSprite, ivItem.getImg())
    positionAnim.setOnStop(self.__isoviewInventory.append, invItem)
    positionAnim.setOnStop(self.paintItemsInventory, None)
    self.__isoviewRoom.itemUnselected(item)
    self.__player.setUnselectedItem()
    ivItem.setAnimation(positionAnim)
        
  def addItemToRoomFromInventory(self, ivItem):
    """ Removes an item from the inventory item list and creates an animation from the inventory to the room.
    event: event info.
    """
    item = ivItem.getModel()
    itemPos = ivItem.getPosition()
    ivInventItem = self.findIVInventoryItem(item)
    if ivItem:    
      posX = len(self.__isoviewInventory)%GG.utils.INV_ITEM_COUNT[0]
      posY = len(self.__isoviewInventory)/GG.utils.INV_ITEM_COUNT[1]
      pos = [GG.utils.INV_OR[0] + (posX * GG.utils.INV_ITEM_SZ[0]), GG.utils.INV_OR[1] + (posY * GG.utils.INV_ITEM_SZ[1])]
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            pos, self.__isoviewRoom.getFutureScreenPosition(ivItem, itemPos), True)
      positionAnim.setOnStop(self.__isoviewRoom.updateScreenPositionsOn, itemPos)
      ivItem.setAnimation(positionAnim)
      if ivInventItem != None:
        self.__isoviewInventory.remove(ivInventItem)
        self.paintItemsInventory()
      if self.__sound:  
        GG.utils.playSound(GG.utils.SOUND_DROPITEM)
      
  def addItemToRoomFromVoid(self, ivItem):
    """ Creates an animation from the top of the screen to the room.
    event: event info.
    """
    item = ivItem.getModel()
    print item
    itemPos = ivItem.getPosition()
    endPos = self.__isoviewRoom.getFutureScreenPosition(ivItem, itemPos)
    if ivItem:
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            [endPos[0], 0], endPos, True)
      positionAnim.setOnStop(self.__isoviewRoom.updateScreenPositionsOn, itemPos)
      ivItem.setAnimation(positionAnim)
      if self.__sound:  
        GG.utils.playSound(GG.utils.SOUND_DROPITEM)
  
  def draw(self):
    """ Updates the changed zones on the room view and draws the hud.
    """
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.getScreen())
    self.paintBackground()
    self.paintInventory()
    self.paintChat()
    self.paintTextBox()
    self.paintActionButtons()
    self.paintUserActions()

    self.hud.zOrder = 1
    #self.hud.depth = 1
    self.addSprite(self.hud)
    self.widgetContainer.add_widget(self.hud)


  def updateFrame(self, ellapsedTime):
    """ Updates all sprites for a new timestamp.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.updateFrame(ellapsedTime)
    
    screen = self.getScreen()
    bg_image = self.__bg.image
    self.__allSprites.clear(screen, bg_image)
    self.__allSprites.draw(screen)
    
    pygame.display.update()

  def roomChanged(self, event):
    """ Triggers after receiving a change room event.
    event: event info.
    """
    print "I"
    if self.__isoviewRoom:
      self.__isoviewRoom.stopAnimations()
      self.__isoviewRoom.unsubscribeAllEvents()
      print "II"
      if self.__sound:
        GG.utils.playSound(GG.utils.SOUND_OPENDOOR)

      list = self.__isoviewRoom.getSpritesDict()
      print "III"
      for img in list.keys():
        self.removeSprite(img)
      list = self.__isoviewRoom.getBottomSpritesDict()
      print "VI"
      for img in list.keys():
        self.removeSprite(img)
      
      self.__isoviewRoom = None
      print "V"
      rect = pygame.Rect(0, 0, GG.utils.GAMEZONE_SZ[0], GG.utils.GAMEZONE_SZ[1])
      self.getScreen().fill((0, 0, 0), rect)
      print "VI"
    if not event.getParams()["room"] is None:
      self.__isoviewRoom = event.getParams()["room"].defaultView(self.getScreen(), self)
      print "VII"
      
  def getIsoviewRoom(self):
    """ Returns the room isometric view.
    """
    return self.__isoviewRoom
           
  # Paint methods
    
  def paintBackground(self):
    """ Paints the HUD background on screen.
    """
    self.hud = ocempgui.widgets.Box(1024,262)
    self.hud.topleft = GG.utils.HUD_OR[0], GG.utils.HUD_OR[1]- 50

    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.HUD_PATH + GG.utils.INTERFACE_LOWER)
    self.imgBackground = GG.utils.OcempImageMapTransparent(filePath)
    self.imgBackground.topleft = 1,1
    self.hud.add_child(self.imgBackground)
    
    labelChat = GG.utils.LabelTransparent("Chat", GG.utils.STYLES["hudLabel"])
    labelChat.topleft = 17, 70
    self.hud.add_child(labelChat)
    
    labelProfile = GG.utils.LabelTransparent("Mi perfil: ", GG.utils.STYLES["hudLabel"])
    labelProfile.topleft = 555, 90
    self.hud.add_child(labelProfile)
    
    labelInventory = GG.utils.LabelTransparent("Inventario", GG.utils.STYLES["hudLabel"])
    labelInventory.topleft = 819, 70
    self.hud.add_child(labelInventory)

  def paintChat(self):
    """ Paints the chat window on screen.
    """
    myOwnStyle = ocempgui.widgets.WidgetStyle ({
            "bgcolor" : ocempgui.widgets.WidgetStyle ({ ocempgui.widgets.Constants.STATE_NORMAL : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_ENTERED : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_ACTIVE : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_INSENSITIVE : (255, 0, 255) }),
           "fgcolor" : ocempgui.widgets.WidgetStyle ({ ocempgui.widgets.Constants.STATE_NORMAL : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_ENTERED : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_ACTIVE : (255, 0, 255),
                                       ocempgui.widgets.Constants.STATE_INSENSITIVE : (255, 0, 255) }),
            "lightcolor" : ocempgui.widgets.WidgetStyle ({ ocempgui.widgets.Constants.STATE_NORMAL : (0, 0, 0),
                                          ocempgui.widgets.Constants.STATE_ENTERED : (0, 0, 0),
                                          ocempgui.widgets.Constants.STATE_ACTIVE : (0, 0, 0),
                                          ocempgui.widgets.Constants.STATE_INSENSITIVE : (0, 0, 0) }),
            "darkcolor" : ocempgui.widgets.WidgetStyle ({ ocempgui.widgets.Constants.STATE_NORMAL : (0, 0, 0),
                                         ocempgui.widgets.Constants.STATE_ENTERED : (0, 0, 0),
                                         ocempgui.widgets.Constants.STATE_ACTIVE : (0, 0, 0),
                                         ocempgui.widgets.Constants.STATE_INSENSITIVE : (0, 0, 0) }),
            "bordercolor" : ocempgui.widgets.WidgetStyle ({ ocempgui.widgets.Constants.STATE_NORMAL : (0, 0, 0),
                                           ocempgui.widgets.Constants.STATE_ENTERED : (0, 0, 0),
                                           ocempgui.widgets.Constants.STATE_ACTIVE : (0, 0, 0),
                                           ocempgui.widgets.Constants.STATE_INSENSITIVE : (0, 0, 0) }),
            "shadowcolor": ((0, 0, 0), (0, 0, 0)),
            "image" : ocempgui.widgets.WidgetStyle ({ ocempgui.widgets.Constants.STATE_NORMAL : None,
                                     ocempgui.widgets.Constants.STATE_ENTERED : None,
                                     ocempgui.widgets.Constants.STATE_ACTIVE : None,
                                     ocempgui.widgets.Constants.STATE_INSENSITIVE : None }),
            "font" : ocempgui.widgets.WidgetStyle ({ "name" : "Bitstream",
                                    "size" : 0,
                                    "alias" : False,
                                    "style" : 0 }),
            "shadow" : 0
            })
    self.textArea = ocempgui.widgets.ScrolledWindow(490, 110)
    self.textArea.set_style(myOwnStyle)
    self.textArea.update()
    self.textArea.set_scrolling(1)
    self.textArea.topleft = GG.utils.CHAT_OR[0], 90
    self.__layoutTextArea= ocempgui.widgets.VFrame()
    self.__layoutTextArea.border = 0
    self.__layoutTextArea.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.textArea.child = self.__layoutTextArea
    self.hud.add_child(self.textArea)
  
  def paintTextBox(self):
    """ Paints the editable text box on screen.
    """
    self.__textField = ocempgui.widgets.Entry()
    self.__textField.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["textFieldChat"]))
    self.__textField.border = 1
    self.__textField.topleft = 14, 210
    self.__textField.set_minimum_size(490, 20)
    self.hud.add_child(self.__textField)

  def paintInventory(self):
    """ Paints the inventory box and its items on it.    
    """
    self.windowInventory = ocempgui.widgets.ScrolledWindow(186, 135)
    self.windowInventory.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["inventoryArea"]))
    self.windowInventory.border = ocempgui.widgets.Constants.BORDER_FLAT
    self.windowInventory.topleft = 819, 90
    self.windowInventory.set_depth(1)
    self.hud.add_child(self.windowInventory)
    self.paintItemsInventory()

  def paintItemsInventory(self):
    """ Paints the inventory items.
    """
    self.windowInventory.child = None
    self.__frameInventory = ocempgui.widgets.VFrame()
    self.__frameInventory.border = 0
    self.__frameInventory.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.windowInventory.child = self.__frameInventory
    position = 0
    for inventoryitem in self.__isoviewInventory:
      self.paintItemOnInventory(inventoryitem, position)
      position += 1

  def itemInventorySelected(self, invIsoItem):
    """ Selects an item from the player's inventory.
    invIsoItem: selected item.
    """
    item = invIsoItem.getModel()
    self.__player.setSelectedItem(item)

  def itemOutInventory(self):
    """ Attempts to move an item from the inventory to the active room.
    """  
    if self.__selectedItem.inventoryOnly():
      self.__player.newChatMessage("Mejor no. Creo que puede ser util mas adelante.", 2) 
      self.paintItemsInventory()
    else:   
      self.__player.addToRoomFromInventory(self.__selectedItem)
    self.__player.setUnselectedItem()
    
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
    self.textArea.vscrollbar.value = self.textArea.vscrollbar.maximum
  
  def getStyleMessageChat(self):
    """ Returns the chat current style.
    """
    listStyle = ["chatEntryBlack","chatEntryRed","chatEntryGreen","chatEntryBlue"]
    return GG.utils.STYLES[listStyle[random.randint(0,len(listStyle)-1)]]
    
  def chatMessageEntered(self):
    """ Prints a new message on the chat window.
    """
    if self.__textField.text == "":
      return
    self.__player.getRoom().newChatMessage(self.__textField.text, self.__player, 0)
    self.__textField.text = ""

  def chatAdded(self, event):
    """ Triggers after receiving a new chat message event.
    event: event info.
    """
    messageChat = event.getParams()['message']
    ivMessageChat = messageChat.chatView(self.getScreen(), self)
    cad = messageChat.getHour() + " [" + messageChat.getSender() + "]: " + messageChat.getMessage()

    animTime = (len(messageChat.getMessage()) / 12) * 1000
    if animTime < 2000:
      animTime = 2000 
    
    idleAnim = animation.IdleAnimation(animTime, ivMessageChat)
    positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_CHAT_TIME2, ivMessageChat, \
                            ivMessageChat.getScreenPosition(), GG.utils.TEXT_BOX_OR, True)
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
        
  def setMovementDestination(self, target):
    """ Adds a marker to the player's movement destination.
    target: movement destination.
    """  
    self.removeMovementDestination()
    self.__targetTileImage.rect.topleft = GG.utils.p3dToP2d(target, GG.utils.TILE_TARGET_SHIFT)
    self.__targetTileImage.zOrder = (pow(target[0], 2) + pow(target[2], 2))*10 - 1
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
      pass
    self.__targetTile = not self.__targetTile
    
  def itemSelected(self,event):
    """ Triggers after receiving an item selected event.
    event: event info.
    """
    self.__selectedItem = event.getParams()['item']
    highlight = event.getParams()['highlight']
    if not self.__selectedItem.inventoryOnly():
      if self.__selectedItem.getRoom():
        if highlight:  
          self.__isoviewRoom.itemSelected(self.__selectedItem)
        selImgPos = self.__selectedItem.getPosition()
        self.__selectedImage.rect.topleft = GG.utils.p3dToP2d(selImgPos, GG.utils.SELECTED_FLOOR_SHIFT)
        
        #self.__selectedImage.rect.topleft = [self.__selectedImage.rect.topleft[0], self.__selectedImage.rect.topleft[1] + 5]
        
        #self.__selectedImage.zOrder = (pow(selImgPos[0], 2) + pow(selImgPos[2], 2))*10 - 1
        self.__selectedImage.zOrder = 0
        self.addSprite(self.__selectedImage)        
    
    options = self.__selectedItem.getOptions()
    self.buttonBarActions = ocempgui.widgets.Box(259,95)
    self.buttonBarActions.topleft = [GG.utils.SCREEN_SZ[0] - 260, 431]
    
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/actionsNotification.png")
    self.buttonBarActions.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["buttonTopBar"]))
    imgBackground = GG.utils.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0,0
    self.buttonBarActions.add_child(imgBackground)
    
    img = self.__selectedItem.getImageLabel()
        
    from PIL import Image
    import os
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(img)
    img = Image.open(filePath)
    size = 23,23
    img.thumbnail(size,Image.ANTIALIAS)
    img.save(os.path.join(GG.utils.LOCAL_DATA_PATH,"imgToolbar.png"))
    imgPath = os.path.join(GG.utils.LOCAL_DATA_PATH,"imgToolbar.png")
    img = GG.utils.OcempImageButtonTransparent(imgPath)
    img.topleft = 5,6
    self.buttonBarActions.add_child(img)
    
    itemLabel = GG.utils.OcempLabel(self.__selectedItem.getName(),290, GG.utils.STYLES["itemLabel"])
    
    itemLabel.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["itemLabel"]))
    itemLabel.topleft = 35,10
    self.buttonBarActions.add_child(itemLabel)
    i = 0
    self.restoreActiveActionButtonsList()
    for action in options:
      #button = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(self.buttonActions[action]['image']))
      filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.buttonActions[action]['image'])
      button = GG.utils.OcempImageButtonTransparent(filePath, self.buttonActions[action]['tooltip'], self.showTooltip, self.removeTooltip)
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.buttonActions[action]['action'])
      self.__activeActions.append(self.buttonActions[action]['action'])
      button.topleft = 195 - i*60 ,40
      self.buttonBarActions.add_child(button)
      i+=1
      
    self.buttonBarActions.zOrder = 10000
    self.addSprite(self.buttonBarActions)
    self.widgetContainer.add_widget(self.buttonBarActions)

  def itemUnselected(self,event=None):
    """ Triggers after receiving an item unselected event.
    event: event info.
    """
    if self.__selectedItem:
      #print "B: ", self.__selectedItem  
      if self.__isoviewRoom:
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.removeSprite(self.__selectedImage)
        self.restoreActiveActionButtonsList()     
    self.dropActionsItembuttons()

  def itemUnselectedSoft(self, item):
    """ Triggers after receiving an item unselected event.
    event: event info.
    """
    if not self.__selectedItem:
      return
    if not item.getName() == self.__selectedItem.getName():
      return
    
    if self.__selectedItem:
      #print "B: ", self.__selectedItem  
      if self.__isoviewRoom:
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.removeSprite(self.__selectedImage)
        self.restoreActiveActionButtonsList()     
    self.dropActionsItembuttons()

  def pointsAdded(self, event):
    """ Updates the points label after receiving a points added event.
    """
    self.__pointsLabel.label = "GuadaPuntos: " + str(event.getParams()["points"])
    self.__pointsLabel.set_text("GuadaPuntos: " + str(event.getParams()["points"]))
    self.hud.remove_child(self.__pointsLabel)
    self.hud.add_child(self.__pointsLabel)
    
  def clockAdded(self, event):
    """ Updates the exp label after receiving an exp added event.
    """  
    self.__labelOld.label = "ClockPuntos: " + str(event.getParams()["clock"])
    self.__labelOld.set_text("ClockPuntos: " + str(event.getParams()["clock"]))
    self.hud.remove_child(self.__labelOld)
    self.hud.add_child(self.__labelOld)
    
  def expAdded(self, event):
    """ Updates the exp label after receiving an exp added event.
    """  
    self.__expLabel.label = "Experiencia: " + str(event.getParams()["exp"])
    self.__expLabel.set_text("Experiencia: " + str(event.getParams()["exp"]))
    self.hud.remove_child(self.__expLabel)
    self.hud.add_child(self.__expLabel)

  def paintActionButtons(self):
    """ Paints the general action buttons.
    """
    if not self.__fullScreen:
      ACTIONS = [
                {"image":"interface/hud/exit.png", "action": self.finishGame, "tooltip":"Finalizar (X)"},
                {"image":"interface/hud/maximize.png", "action": self.showFullScreen, "tooltip":"Maximizar o minimizar pantalla (F)"},
                {"image":"interface/hud/sound.png", "action": self.showSoundControl, "tooltip":"Controles de sonido (S)"},
                ]
    else:
      ACTIONS = [
                {"image":"interface/hud/exit.png", "action": self.finishGame, "tooltip":"Finalizar (X)"},
                {"image":"interface/hud/minimize.png", "action": self.showFullScreen, "tooltip":"Maximizar o minimizar pantalla (F)"},
                {"image":"interface/hud/sound.png", "action": self.showSoundControl, "tooltip":"Controles de sonido (S)"},
                ]
    
    i = 0
    for buttonData in ACTIONS:
      filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image'])
      button = GG.utils.OcempImageButtonTransparent(filePath, buttonData['tooltip'], self.showTooltip, self.removeTooltip)
      button.topleft = 16 + i*60 ,10
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, buttonData['action'])
      if buttonData['action'] == self.showFullScreen:
        self.__fullscreenButton = button
      elif  buttonData['action'] == self.showSoundControl:
        self.__soundButton = button
      i+=1
      self.hud.add_child(button)
      
  def privateChatHandler(self):
    """ Shows or hides the private chat window.
    """  
    if not self.privateChatWindow:
      self.showPrivateChat()
    else:
      if self.privateChatWindow.hide:
        self.showPrivateChat()
      else:
        self.hidePrivateChat()
      
  def showPrivateChat(self):
    """ Shows the private chat window.
    """  
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/privatechat.png")
    self.__privateChatButton.picture = ocempgui.draw.Image.load_image(imgPath)
    self.hud.remove_child(self.__privateChatButton)
    self.hud.add_child(self.__privateChatButton)
    
    self.addSprite(self.privateChatWindow.window)
    self.widgetContainer.add_widget(self.privateChatWindow.window)
    x, y = self.privateChatWindow.getScreenPosition()
    width, height = self.privateChatWindow.getSize()
    cordX = x
    cordY = y
    if x < 0:
      cordX = 0
    if y < 0:
      cordY = 0
    if (x + width) > GG.utils.GAMEZONE_SZ[0]:
      cordX = GG.utils.GAMEZONE_SZ[0] - width  
    if (y + height) > GG.utils.GAMEZONE_SZ[1]:
      cordY = GG.utils.GAMEZONE_SZ[1] - height - 75
    self.privateChatWindow.setScreenPosition(cordX, cordY)  
    self.privateChatWindow.hide = False
    
  def hidePrivateChat(self):
    """ Hides the private chat window.
    """  
    self.removeSprite(self.privateChatWindow.window)
    self.widgetContainer.remove_widget(self.privateChatWindow.window)
    self.privateChatWindow.hide = True
  
  def showTooltip(self, label):
    """ Shows the selected button tooltip.
    label: tooltip label.
    """  
    self.tooltipWindow = ocempgui.widgets.TooltipWindow (label)
    x, y = pygame.mouse.get_pos ()
    szX, szY = self.tooltipWindow.size
    if (x + 8 + szX) > GG.utils.GAMEZONE_SZ[0]:
      self.tooltipWindow.topleft = GG.utils.GAMEZONE_SZ[0] - szX, y - 5
    else:
      self.tooltipWindow.topleft = x + 8, y - 5
    self.tooltipWindow.depth = 99 # Make it the topmost widget.
    self.tooltipWindow.zOrder = 30000
    self.addSprite(self.tooltipWindow)
      
  def removeTooltip(self):
    """ Removes the active tooltip.
    """  
    if self.tooltipWindow:
      self.removeSprite(self.tooltipWindow)  
      self.tooltipWindow.destroy ()
      self.tooltipWindow = None
  
  def showDresser(self):
    """ Shows the avatar configuration window.
    """  
    self.wardrobe = avatareditor.AvatarEditor(self.widgetContainer, self, self.__player.getAvatarConfiguration())
    self.winWardrobe = self.wardrobe.draw()
    self.addSprite(self.winWardrobe)
    self.widgetContainer.add_widget(self.winWardrobe)
    #GG.genteguada.GenteGuada.getInstance().activeScreen = self.wardrobe
    
  def closeDresser(self, configuration = None):
    """ Closes the avatar configuration window.
    configuration: avatar configuration.
    """  
    if configuration:
      self.setAvatarConfiguration(configuration)
    #GG.genteguada.GenteGuada.getInstance().activeScreen = self

    self.widgetContainer.remove_widget(self.winWardrobe)  
    self.winWardrobe.depth = 1
    self.removeSprite(self.winWardrobe)
    self.winWardrobe.destroy()
    #self.winWardrobe = None
    
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
    
  def showTools(self):
    """ Shows the tools window.
    """  
    pass

  def showSoundControl(self):
    """ Enables or disables the sound effects.
    """
    if self.__sound:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/mute.png")
      self.__soundButton.picture = ocempgui.draw.Image.load_image(imgPath)
    else:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/sound.png")
      self.__soundButton.picture = ocempgui.draw.Image.load_image(imgPath)
    self.hud.remove_child(self.__soundButton)
    self.hud.add_child(self.__soundButton)
    self.__sound = not self.__sound
    
  def showHelp(self):
    """ Shows the help menu.
    """
    pass

  def finishGame(self):
    """ Finishes the game.
    """  
    GG.genteguada.GenteGuada.getInstance().finish()
    
  def showFullScreen(self):
    """ Toggles the fullscreen mode.
    """
    #TODO solo funciona en linux con las X, para e
    if self.__fullScreen:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/maximize.png")
      self.__fullscreenButton.picture = ocempgui.draw.Image.load_image(imgPath)
    else:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/minimize.png")
      self.__fullscreenButton.picture = ocempgui.draw.Image.load_image(imgPath)
    self.hud.remove_child(self.__fullscreenButton)
    self.hud.add_child(self.__fullscreenButton)
    self.__fullScreen = not self.__fullScreen
    pygame.display.toggle_fullscreen()
    
  def paintUserActions(self):
    """ Paints the user action buttons.
    """
    ACTIONS = [
                {"image":"interface/hud/privatechat.png", "action": self.privateChatHandler, "tooltip":"Abre o cierra chat privado (Z)"},
                {"image":"interface/hud/spinright.png", "action": self.turnRight, "tooltip":"Rotar derecha (R)"},
                {"image":"interface/hud/spinleft.png", "action": self.turnLeft, "tooltip":"Rotar izquierda (L)"},
                {"image":"interface/hud/jump.png", "action": self.jump, "tooltip":"Saltar (J)"},
                {"image":"interface/hud/dresser.png", "action": self.showDresser, "tooltip":"Cambiar configuracion avatar (D)"},
              ]
    i = 0
    for buttonData in ACTIONS:
      filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image'])
      button = GG.utils.OcempImageButtonTransparent(filePath, buttonData['tooltip'], self.showTooltip, self.removeTooltip)
      button.topleft = 950 - i * 60 , 10
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, buttonData['action'])
      self.hud.add_child(button)
      i += 1
      if buttonData['action'] == self.privateChatHandler:
        self.__privateChatButton = button

    from PIL import Image
    import os
    image = self.__player.getImageLabel()
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(image)
    img = Image.open(filePath)
    size = 64,64
    img.thumbnail(size,Image.ANTIALIAS)
    img.save(os.path.join(GG.utils.LOCAL_DATA_PATH,"imgMaskUser.png"))
    imgPath = os.path.join(GG.utils.LOCAL_DATA_PATH,"imgMaskUser.png")
    img = GG.utils.OcempImageButtonTransparent(imgPath)
    img.topleft = 548,110
    self.hud.add_child(img)

    labelUserName = GG.utils.LabelTransparent(self.__player.username, GG.utils.STYLES["userName"])
    labelUserName.topleft = 638, 90
    self.hud.add_child(labelUserName)
    
    self.__pointsLabel = GG.utils.OcempLabel("GuadaPuntos: 0", 140, GG.utils.STYLES["userName"])
    self.__pointsLabel.topleft = 627, 120
    self.hud.add_child(self.__pointsLabel)

    self.__labelOld = GG.utils.OcempLabel("ClockPuntos: 0", 140, GG.utils.STYLES["userName"])
    self.__labelOld.topleft = 627, 140
    self.hud.add_child(self.__labelOld)

    self.__expLabel = GG.utils.OcempLabel("Experiencia: 1", 140, GG.utils.STYLES["userName"])
    self.__expLabel.topleft = 627, 160
    self.hud.add_child(self.__expLabel)

  def jump(self):
    """ Makes the player jump.
    """  
    if not self.findIVItem(self.__player).hasAnimation():
      self.__player.jump()

  #definicion de las acciones y botones en funcion del item seleccionado
  
  def dropActionsItembuttons(self):
    """ Removes the action buttons from the screen.
    """
    if self.__selectedItem == None:
      return
    self.removeTooltip()
    self.__selectedItem = None
    self.removeSprite(self.__selectedImage)        
    
    children = copy.copy(self.buttonBarActions.children)
    for child in children:
      self.buttonBarActions.remove_child(child)
      child.destroy()
    self.widgetContainer.remove_widget(self.buttonBarActions)
    self.buttonBarActions.destroy()

  def itemToInventory(self):
    """ Brings an item from the room to the player's inventory.
    """
    if self.__selectedItem == None:
      return
    self.__player.addToInventoryFromRoom(self.__selectedItem)
    self.__player.setUnselectedItem()    

  def moneyToInventory(self):
    if self.__selectedItem == None:
      return
    self.__selectedItem.addPointsTo(self.__player)
    self.__isoviewRoom.getModel().removeItem(self.__selectedItem)
    self.__player.setUnselectedItem()

  def itemCopyToInventory(self):
    """ Brings an item from the room to the player's inventory.
    """
    if self.__selectedItem == None:
      return
    item, pos = self.__selectedItem.getCopyFor(self.__player)
    if item != None:
      self.__player.addToInventoryFromVoid(item, pos)
    self.__player.setUnselectedItem()
 
  def itemToClone(self):
    """ Clones an item from the room and inserts it on the player's inventory
    """
    clone = self.__selectedItem.getClone()
    self.__player.addInventory(clone)
    self.itemUnselected()
    
  def itemToTalkAndGet(self):
    """ Talks to an item and gets another one.
    """
    if self.__selectedItem == None:
      return
    item = self.__player.talkAndGetFrom(self.__selectedItem)
    if item:
      self.__player.addToInventoryFromVoid(item, self.__player.getPosition())          
    self.itemUnselected()
    self.dropActionsItembuttons()
 
  def itemToPush(self):
    """ Unused method.
    """  
    self.itemUnselected()

  def itemToUp(self):
    """ Unused method.
    """  
    self.itemUnselected()

  def privateChat(self):
    """ Unused method.
    """  
    self.__player.setUnselectedItem()
    
  def itemToTalk(self):
    """ Talks to an item.
    """
    self.__player.talkTo(self.__selectedItem)
    self.itemUnselected()

  def exchangeItemPlayer(self):
    """ Shows the trade window.
    """
    self.__player.initExchangeTo(self.__selectedItem)
    
  def itemToOpen(self):
    """ Attempts to open a teleporter item.
    """
    self.__player.open(self.__selectedItem)
    self.itemUnselected()

  def itemToUrl(self):
    """ Attempts to open an url adress.
    """
    import webbrowser
    if self.__fullScreen:
      self.__fullScreen = False
      pygame.display.toggle_fullscreen()
    webbrowser.open(self.__selectedItem.url)
    self.itemUnselected()

  def itemToLift(self):
    """ Picks an item and takes it ove the player's head.
    """
    self.__player.lift(self.__selectedItem)
    self.itemUnselected()
    if self.__selectedItem:
      if self.__isoviewRoom:  
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.__selectedItem = None
        self.removeSprite(self.__selectedImage)        
    self.dropActionsItembuttons()
    
  def itemToDrop(self):
    """ Drops a picked item in front of the player.
    """  
    self.__player.drop(self.__selectedItem)
    self.itemUnselected()
    if self.__selectedItem:
      if self.__isoviewRoom:  
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.removeSprite(self.__selectedImage)        
        self.__selectedItem = None
    self.dropActionsItembuttons()

  def initExchange(self,event):
    """ Starts the exchange project after receiving an exchange event.
    event: event info.
    """  
    itemList = event.getParams()["list"]
    if len(itemList):
      step = 2
    else:
      step = 1
    self.exchangeWindow = exchangewindow.ExchangeWindow(self, step, itemList)
    self.exchangeWindow.draw()
    self.addSprite(self.exchangeWindow.window)
    self.widgetContainer.add_widget(self.exchangeWindow.window)
    self.activeWindow = True
    
  def itemToExchange(self):
    """ Attempts to exchange an item with another player.
    """  
    self.exchangeWindow.addItemOut(self.__selectedItem)
    self.__player.setUnselectedItem()

  def cancelExchange(self,event):
    """ Cancels the exchange process after receiving a cancel exchange event.
    event: event info.
    """  
    self.widgetContainer.remove_widget(self.exchangeWindow.window)
    self.removeSprite(self.exchangeWindow.window)
    self.exchangeWindow = None
    self.activeWindow = False

  def addListExchange(self, event):
    """ Adds an item to the exchange list after receiving an event.
    event: event info.
    """  
    itemList = event.getParams()["list"]
    self.exchangeWindow.addInList(itemList) 

  def itemToClimb(self):
    """ Climbs over an item.
    """
    self.__player.climb(self.__selectedItem)
    self.itemUnselected()
    if self.__selectedItem:
      if self.__isoviewRoom:  
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.removeSprite(self.__selectedImage)        
        self.__selectedItem = None
    self.dropActionsItembuttons()
    
  def itemToGiveCard(self):
    """ Gives a contact card to another player.
    """  
    self.__selectedItem.checkContact(self.__player)
    self.itemUnselected()
    self.dropActionsItembuttons()
    
  def newContactDialog(self, event):
    """ Shows the new contact confirmation dialog after receiving an event.
    event: event info.
    """  
    if self.activeContactDialog:
      return  
    newContact = event.getParams()["contact"]
    self.confirmDialog = ocempgui.widgets.Box(300, 120)
    self.confirmDialog.set_position = [0, 0]
    
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/contactWindow.png")
    imgBackground = GG.utils.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0,0
    self.confirmDialog.add_child(imgBackground)
     
    cad = "Intercambiar tarjetas con " + newContact.username 
    questionLabel = GG.utils.OcempLabel(cad, 200, GG.utils.STYLES["dialogFont"])
    questionLabel.topleft = 22, 20 
    self.confirmDialog.add_child(questionLabel)
     
    okButton = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/editor/ok_button.png"))
    okButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.giveContactCard, event.getParams()['contact'])
    okButton.topleft = [20, 55]
    cancelButton = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/editor/cancel_button.png"))
    cancelButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.dropContactDialog)
    cancelButton.topleft = [170, 55]
    self.confirmDialog.add_child(okButton)
    self.confirmDialog.add_child(cancelButton)
    self.confirmDialog.zOrder = 20000
    self.addSprite(self.confirmDialog)
    self.widgetContainer.add_widget(self.confirmDialog)
    self.dropActionsItembuttons()
    self.activeContactDialog = event.getParams()['contact']
    
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
    self.activeContactDialog = None
    self.itemUnselected()
    self.dropActionsItembuttons()
    
  def newContactAdded(self, event):
    """ Updates the contacts window after receiving a contact added event.
    event: event info.
    """  
    self.privateChatWindow.updateContactList()
    
  def privateChatReceived(self, event):
    """ Triggers after receiving a new private chat message event.
    event: event info.
    """  
    chat = event.getParams()['chat']
    player = event.getParams()['player']
    if self.privateChatWindow.hide == True:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/4.png")
      self.__privateChatButton.picture = ocempgui.draw.Image.load_image(imgPath)
      self.hud.remove_child(self.__privateChatButton)
      self.hud.add_child(self.__privateChatButton)
    self.privateChatWindow.incomingChatMessage(chat, player)
      
  def removeContactRemote(self, event):
    """ Triggers after receiving a remove contact event from another player.
    event: event info.
    """  
    contact = event.getParams()['contact']
    self.privateChatWindow.removeContactRemote(contact)      

  def unsubscribeAllEvents(self):
    self.findIVItem(self.__player).unsubscribeAllEvents()
    isoview.IsoView.unsubscribeAllEvents(self) 
      
