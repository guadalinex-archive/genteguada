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
    #self.widgetContainer = ocempgui.widgets.Renderer()
    #self.widgetContainer.set_screen(screen)
    self.textArea = None
    self.__textField = None
    self.windowInventory = None
    self.privateChatWindow = None
    
    if fullscreen:
      self.__fullScreen = True
    else:
      self.__fullScreen = False
    self.__sound = True
    
    self.__soundButton = None
    self.__fullscreenButton = None
    
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.INTERFACE_LOWER)).convert_alpha()
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
    self.__player.subscribeEvent('exp', self.expAdded)
    self.__player.subscribeEvent('initExchange', self.initExchange)
    self.__player.subscribeEvent('cancelExchange', self.cancelExchange)
    self.__player.subscribeEvent('listExchange', self.addListExchange)
    self.__player.subscribeEvent('contactDialog', self.newContactDialog)
    self.__player.subscribeEvent('contactAdded', self.newContactAdded)
    self.__player.subscribeEvent("privateChatReceived", self.privateChatReceived)
    
    self.__selectedItem = None
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("tiles/" + GG.utils.TILE_SELECTED)  
    self.__selectedImage = pygame.sprite.Sprite()
    self.__selectedImage.image = pygame.image.load(imgPath).convert_alpha()
    self.__selectedImage.rect = self.__selectedImage.image.get_rect()
    #self.__selectedImage.rect.topleft = GG.utils.p3dToP2d(self.getModel().getPosition(), self.getModel().anchor)
    
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
        "giveCard":{"image":"interface/hud/contact.png", "action": self.itemToGiveCard, "tooltip":"Dar tarjeta de visita (V)"}
    }
    
    self.hotkeys = {K_x: self.finishGame, K_f: self.showFullScreen, K_s: self.showSoundControl, \
                    K_d: self.showDresser, K_j: self.jump, K_r: self.turnRight, K_l: self.turnLeft, \
                    K_p: self.itemToInventory, K_c: self.itemCopyToInventory, K_m: self.itemOutInventory, \
                    K_i: self.itemToLift , K_q: self.itemToDrop , K_b: self.itemToClimb , \
                    K_y: self.itemToClone , K_k: self.itemToPush , K_p: self.itemToUp , \
                    K_t: self.itemToTalk , K_g: self.itemToTalkAndGet , K_h: self.privateChat , \
                    K_e: self.exchangeItemPlayer , K_o: self.itemToOpen , K_w: self.itemToUrl , \
                    K_a: self.itemToExchange, K_v: self.itemToGiveCard}
                          
    self.winWardrobe = None
    self.wardrobe = None
    self.exchangeWindow = None
    self.activeExchageWindow = False
    self.activeQuizWindow = False
    self.activeContactDialog = None
    self.tooltipWindow = None
    """
    self.__pointsLabel = GG.utils.OcempLabel("Puntos: 0",140)
    self.__pointsLabel.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    self.__pointsLabel.topleft = [GG.utils.POINTS_LOCATION[0], GG.utils.POINTS_LOCATION[1] - self.__pointsLabel.height]
    self.__isoviewRoom.addSprite(self.__pointsLabel)
    
    self.__expLabel = GG.utils.OcempLabel("Exp: 0",140)
    self.__expLabel.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    self.__expLabel.topleft = [GG.utils.EXP_LOCATION[0], GG.utils.EXP_LOCATION[1] - self.__expLabel.height]
    self.__isoviewRoom.addSprite(self.__expLabel)
    """
    self.ctrl = 0
  
  def processEvent(self, events):
    for event in events:
      event_type = event.type
      if event_type == QUIT:
        GG.genteguada.GenteGuada.getInstance().finish()
        
      elif event_type == KEYUP:
        if event.key == K_LCTRL or event.key == K_RCTRL:
          self.ctrl = 0
          
      elif event_type == KEYDOWN:
        if self.ctrl:
          #self.ctrl = 0
          if event.key in self.hotkeys.keys():
            if self.hotkeys[event.key] in self.__activeActions:
              self.hotkeys[event.key]()
              # atajos de teclado
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
        #if not self.exchangeWindow:
        if not self.windowOpen():
          cordX, cordY = pygame.mouse.get_pos()
          if 0 <= cordY <= GG.utils.HUD_OR[1]:
            dest, item = self.getIsoviewRoom().findTile([cordX, cordY])
            if not dest == [-1, -1, -1]:
              self.__isoviewRoom.getModel().clickedByPlayer(self.__player, dest, item)
    self.widgetContainer.distribute_events(*events)

  def windowOpen(self):
    if self.activeExchageWindow:
      return True
    if self.activeQuizWindow:
      return True
    if self.privateChatWindow:
      if not self.privateChatWindow.hide:
        return True
    if self.activeContactDialog != None:
      return True
    return False

  def restoreActiveActionButtonsList(self):
    self.__activeActions = []  
    self.__activeActions.append(self.finishGame)
    self.__activeActions.append(self.showFullScreen)
    self.__activeActions.append(self.showSoundControl)
    self.__activeActions.append(self.showDresser)
    self.__activeActions.append(self.jump)
    self.__activeActions.append(self.turnRight)
    self.__activeActions.append(self.turnLeft)
    
  def compareSelectedItem(self, item):
    if self.__selectedItem:  
      return self.__selectedItem.checkSimilarity(item)
    else:
      return False

  def setActiveQuizWindow(self, value):
    self.activeQuizWindow = value
    
  def getActiveQuizWindow(self):
    return self.activeQuizWindow

  def addSprite(self, sprite):
    self.__allSprites.add(sprite)

  def removeSprite(self, sprite):
    self.__allSprites.remove(sprite)

  def getPlayer(self):
    return self.__player
  
  def getSelectedItem(self):
    return self.__selectedItem

  def getSound(self):
    return self.__sound

  def findIVItem(self, item):
    for ivItem in self.__isoviewRoom.getIsoViewItems():
      if ivItem.getModel() == item:
        return ivItem
    return None

  def findIVInventoryItem(self, item):
    for ivItem in self.__isoviewInventory:
      if ivItem.getModel() == item:
        return ivItem
    return None
  
  def inventoryRemoved(self, event):
    item = event.getParams()["item"]  
    ivInventItem = self.findIVInventoryItem(item)
    #print "inventoryRemoved",ivInventItem
    self.__isoviewInventory.remove(ivInventItem)
    self.paintItemsInventory()
      
  def liftItem(self, event):
    item = event.getParams()["item"]  
    pos = event.getParams()["position"]
    ivItem = self.__isoviewRoom.findIVItem(item)  
    if ivItem != None:
      self.__isoviewRoom.updateScreenPositionsOn(pos)  
    
  def dropItem(self, event):
    item = event.getParams()["item"]  
    pos = event.getParams()["position"]
    ivItem = self.__isoviewRoom.findIVItem(item)  
    if ivItem != None:
      self.__isoviewRoom.updateScreenPositionsOn(pos)  
      
  def addItemToInventory(self, event):
    """ Adds a new isoview inventory item.
    """
    item = event.getParams()["item"]
    posOrigin = event.getParams()["position"]
    posX = len(self.__isoviewInventory)%GG.utils.INV_ITEM_COUNT[0]
    posY = len(self.__isoviewInventory)/GG.utils.INV_ITEM_COUNT[1]
    pos = [GG.utils.INV_OR[0] + (posX * GG.utils.INV_ITEM_SZ[0]), GG.utils.INV_OR[1] + (posY * GG.utils.INV_ITEM_SZ[1])]
    ivItem = self.findIVItem(item)
    invItem = isoview_inventoryitem.IsoViewInventoryItem(item, self.getScreen(), self)
    #print "@@@@",ivItem
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
    """ Removes an item from the inventory item list and creates an animation to the room.
    event: event info.
    """
    item = ivItem.getModel()
    itemPos = item.getPosition()
    ivInventItem = self.findIVInventoryItem(item)
    if ivItem:    
      posX = len(self.__isoviewInventory)%GG.utils.INV_ITEM_COUNT[0]
      posY = len(self.__isoviewInventory)/GG.utils.INV_ITEM_COUNT[1]
      pos = [GG.utils.INV_OR[0] + (posX * GG.utils.INV_ITEM_SZ[0]), GG.utils.INV_OR[1] + (posY * GG.utils.INV_ITEM_SZ[1])]
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            #pos, GG.utils.p3dToP2d(item.getPosition(), item.anchor), True)
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
    itemPos = item.getPosition()
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
    self.addSprite(self.hud)
    #print "hud ",self.hud.depth
    self.widgetContainer.add_widget(self.hud)


  def updateFrame(self, ellapsedTime):
    """ Updates all sprites for a new frame.
    """
    #hay que dibujar la habitacion DESPUES del hud, para que las animaciones de los items 
    #se vean sobre el HUD y no debajo como ahora.

    #self.paintBackground()
    #self.buttonBar.update()
    #self.textArea.update()
    #self.__textField.update()
    #self.windowInventory.update()

    if self.__isoviewRoom:
      self.__isoviewRoom.updateFrame(ellapsedTime)
    
    screen = self.getScreen()
    bg_image = self.__bg.image
    self.__allSprites.clear(screen, bg_image)
    self.__allSprites.draw(screen)
    #print self.__img.zOrder, self.hud.zOrder
    
    pygame.display.update()

  def roomChanged(self, event):
    """ Triggers after receiving a change room event.
    event: event info.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.stopAnimations()
      self.__isoviewRoom.unsubscribeAllEvents()
      if self.__sound:
        GG.utils.playSound(GG.utils.SOUND_OPENDOOR)

      list = self.__isoviewRoom.getSpritesDict()
      for img in list.keys():
        self.removeSprite(img)
      list = self.__isoviewRoom.getBottomSpritesDict()
      for img in list.keys():
        self.removeSprite(img)
      
      self.__isoviewRoom = None
      rect = pygame.Rect(0, 0, GG.utils.GAMEZONE_SZ[0], GG.utils.GAMEZONE_SZ[1])
      self.getScreen().fill((0, 0, 0), rect)
      #self.buttonBar.update()
    if not event.getParams()["room"] is None:
      self.__isoviewRoom = event.getParams()["room"].defaultView(self.getScreen(), self)
      
  def getIsoviewRoom(self):
    """ Returns the isometric view room.
    """
    return self.__isoviewRoom
           
  # Paint methods
    
  def paintBackground(self):
    """ Paints the HUD background on screen.
    """
    self.hud = ocempgui.widgets.Box(1024,262)
    self.hud.topleft = GG.utils.HUD_OR[0], GG.utils.HUD_OR[1]- 50

    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/interface_lower.png")
    self.imgBackground = GG.utils.OcempImageMapTransparent(filePath)
    self.imgBackground.topleft = 0,0
    self.hud.add_child(self.imgBackground)
    
    labelChat = GG.utils.OcempLabel("Chat", 280)
    labelChat.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["hudLabel"]))
    labelChat.topleft = 17, 65
    self.hud.add_child(labelChat)
    
    labelProfile = GG.utils.OcempLabel("Mi perfil:", 280)
    labelProfile.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["userName"]))
    labelProfile.topleft = 540, 80
    self.hud.add_child(labelProfile)
    
    labelInventory = GG.utils.OcempLabel("Inventario:", 280)
    labelInventory.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["hudLabel"]))
    labelInventory.topleft = 819, 65
    self.hud.add_child(labelInventory)

    #self.getScreen().blit(self.__img.image, [GG.utils.HUD_OR[0], GG.utils.HUD_OR[1]- 50])
    #self.__img.zOrder = 0
    #self.addSprite(self.__img)
    #pygame.display.update()

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
   # self.textArea.border = 1
    #self.textArea.topleft = GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1] + 20
    self.textArea.topleft = GG.utils.CHAT_OR[0], 90
    self.__layoutTextArea= ocempgui.widgets.VFrame()
    self.__layoutTextArea.border = 0
    self.__layoutTextArea.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.textArea.child = self.__layoutTextArea
    self.hud.add_child(self.textArea)
    #self.widgetContainer.add_widget(self.textArea)
    #self.widgetContainer.update()
    #print self.textArea.create_style()
  
  def paintTextBox(self):
    """ Paints the editable text box on screen.
    """
    self.__textField = ocempgui.widgets.Entry()
    self.__textField.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["textFieldChat"]))
    self.__textField.border = 1
    #self.__textField.topleft = 14, 732
    self.__textField.topleft = 14, 210
    self.__textField.set_minimum_size(490, 20)
    self.hud.add_child(self.__textField)
    #self.widgetContainer.add_widget(self.__textField)

  def paintInventory(self):
    """ Paints the inventory box and its items on it.    
    """
    self.windowInventory = ocempgui.widgets.ScrolledWindow(186, 135)
    self.windowInventory.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["inventoryArea"]))
    self.windowInventory.border = 1
    self.windowInventory.topleft = 819, 90
    self.windowInventory.set_depth(1)
    self.hud.add_child(self.windowInventory)
    #self.widgetContainer.add_widget(self.windowInventory)
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

  def itemInventorySelected(self,invIsoItem):
    """ Selects an item from the player's inventory.
    invIsoItem: selected item.
    """
    #print "item seleccionado"
    item = invIsoItem.getModel()
    self.__player.setSelectedItem(item)

  def itemOutInventory(self):
    if self.__selectedItem.inventoryOnly():
      #self.__player.removeFromInventory(self.__selectedItem) 
      self.__player.newChatMessage("Mejor no. Creo que puede ser util mas adelante.", 2) 
      self.paintItemsInventory()
    else:   
      self.__player.addToRoomFromInventory(self.__selectedItem)
    self.__player.setUnselectedItem()
    
  def paintItemOnInventory(self, invItem, position):
    """ Paints an item on the hud inventory.
    spriteName: sprite name.
    position: position in the inventory that the item will be painted into.
    """
    if position % GG.utils.INV_ITEM_COUNT[0] == 0:
      self.hframe =  ocempgui.widgets.HFrame()
      self.hframe.border = 0
      self.hframe.add_child(invItem.draw(self.widgetContainer))
      self.__frameInventory.add_child(self.hframe)
    else:
      self.hframe.add_child(invItem.draw(self.widgetContainer))
  
  def printChatMessage(self, chatMessage):
    self.__layoutTextArea.add_child(chatMessage.draw())
    self.textArea.vscrollbar.value = self.textArea.vscrollbar.maximum
  
  def getStyleMessageChat(self):
    """ Returns the chat current style.
    """
    #TODO entiendo que el color del chat depende de cada usuario 
    listStyle = ["chatEntryBlack","chatEntryRed","chatEntryGreen","chatEntryBlue"]
    return GG.utils.STYLES[listStyle[random.randint(0,len(listStyle)-1)]]
    
  def chatMessageEntered(self):
    """ Prints a new message on chat window.
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
    #print "quizzzzzzzzzzzzzzz"
    messageChat = event.getParams()['message']
    ivMessageChat = messageChat.chatView(self.getScreen(), self)
    self.__isoviewRoom.addIsoViewChatItem(ivMessageChat)
        
  def setMovementDestination(self, target):
    #print "===>>> Ini"  
    self.removeMovementDestination()
    #print "setMovementDestination"
    self.__targetTileImage.rect.topleft = GG.utils.p3dToP2d(target, GG.utils.TILE_TARGET_SHIFT)
    self.__targetTileImage.zOrder = (pow(target[0], 2) + pow(target[2], 2))*10 - 1
    self.addSprite(self.__targetTileImage)        
    self.__targetTile = True  
    #print "<<<=== Fin"  
    
  def removeMovementDestination(self):
    #print "removeMovementDestination"
    #if self.__targetTile:
    #if self.__allSprites.has(self.__targetTileImage):
      #if self.__allSprites.has(self.__targetTileImage):
    try:
      self.removeSprite(self.__targetTileImage)  
    except KeyError:
        # This can happen if a sprite is removed before
        # update() has had a chance to be called.
      self.__targetTile = not self.__targetTile
      pass
    self.__targetTile = not self.__targetTile
    #self.__targetTile = False
    
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
        self.__selectedImage.zOrder = (pow(selImgPos[0], 2) + pow(selImgPos[2], 2))*10 - 1
        self.addSprite(self.__selectedImage)        
    
    options = self.__selectedItem.getOptions()
    
    self.buttonBarActions = ocempgui.widgets.Box(259,95)
    #self.buttonBarActions.topleft = [GG.utils.SCREEN_SZ[0] - 260,0]
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
    
    itemLabel = GG.utils.OcempLabel(self.__selectedItem.getName(),290)
    
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
    if self.__selectedItem:
      if self.__isoviewRoom:
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.removeSprite(self.__selectedImage)
        self.restoreActiveActionButtonsList()     
    
    self.dropActionsItembuttons()

  def pointsAdded(self, event):
    self.__pointsLabel.set_text("Puntos: " + str(event.getParams()["points"]))
    
  def expAdded(self, event):
    self.__expLabel.set_text("Exp: " + str(event.getParams()["exp"]))
  
  #Defincion de la buttonBar y sus acciones permanentes

  def paintActionButtons(self):
    """ Paints the general action buttons.
    """
    if not self.__fullScreen:
      ACTIONS = [
                #{"image":"interface/hud/help.png", "action": self.showHelp, "tooltip":"Ayuda"},
                {"image":"interface/hud/exit.png", "action": self.finishGame, "tooltip":"Finalizar (X)"},
                {"image":"interface/hud/maximize.png", "action": self.showFullScreen, "tooltip":"Maximizar o minimizar pantalla (F)"},
                {"image":"interface/hud/sound.png", "action": self.showSoundControl, "tooltip":"Controles de sonido (S)"},
                {"image":"interface/hud/chat.png", "action": self.privateChatHandler, "tooltip":"Abre o cierra chat privado"},
                #{"image":"interface/hud/rotateright.png", "action": self.turnRight, "tooltip":"rotar derecha"},
                #{"image":"interface/hud/rotateleft.png", "action": self.turnLeft, "tooltip":"rotar izquierda"},
                ]
    else:
      ACTIONS = [
                #{"image":"interface/hud/help.png", "action": self.showHelp, "tooltip":"Ayuda"},
                {"image":"interface/hud/exit.png", "action": self.finishGame, "tooltip":"Finalizar (X)"},
                {"image":"interface/hud/minimize.png", "action": self.showFullScreen, "tooltip":"Maximizar o minimizar pantalla (F)"},
                {"image":"interface/hud/sound.png", "action": self.showSoundControl, "tooltip":"Controles de sonido (S)"},
                {"image":"interface/hud/chat.png", "action": self.privateChatHandler, "tooltip":"Abre o cierra chat privado"},
                #{"image":"interface/hud/rotateright.png", "action": self.turnRight, "tooltip":"rotar derecha"},
                #{"image":"interface/hud/rotateleft.png", "action": self.turnLeft, "tooltip":"rotar izquierda"},
                ]
    
    i = 0
    for buttonData in ACTIONS:
      #button = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image']))
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
    if not self.privateChatWindow:
      self.showPrivateChat()
    else:
      if self.privateChatWindow.hide:
        self.showPrivateChat()
      else:
        self.hidePrivateChat()
      
  def showPrivateChat(self):
    if not self.privateChatWindow:
      self.privateChatWindow = privatechatwindow.PrivateChatWindow("Chat Privado", self.__player)
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
    self.removeSprite(self.privateChatWindow.window)
    self.widgetContainer.remove_widget(self.privateChatWindow.window)
    self.privateChatWindow.hide = True
  
  def showTooltip(self, label):
    self.tooltipWindow = ocempgui.widgets.TooltipWindow (label)
    x, y = pygame.mouse.get_pos ()
    self.tooltipWindow.topleft = x + 8, y - 5
    self.tooltipWindow.depth = 99 # Make it the topmost widget.
    self.tooltipWindow.zOrder = 30000
    self.addSprite(self.tooltipWindow)
      
  def removeTooltip(self):
    if self.tooltipWindow:
      self.removeSprite(self.tooltipWindow)  
      self.tooltipWindow.destroy ()
      self.tooltipWindow = None
  
  def showDresser(self):
    self.wardrobe = avatareditor.AvatarEditor(self.widgetContainer, self, self.__player.getAvatarConfiguration())
    self.winWardrobe = self.wardrobe.draw()
    self.widgetContainer.add_widget(self.winWardrobe)
    self.addSprite(self.winWardrobe)
    GG.genteguada.GenteGuada.getInstance().activeScreen = self.wardrobe

  def closeDresser(self, configuration = None):
    if configuration:
      self.setAvatarConfiguration(configuration)
    GG.genteguada.GenteGuada.getInstance().activeScreen = self
    self.removeSprite(self.winWardrobe)
    self.winWardrobe.destroy()
    self.winWardrobe = None
    self.hud.remove_child(self.imgBackground)
    self.hud.insert_child(0,self.imgBackground)

  def setAvatarConfiguration(self,configuration):
    GG.genteguada.GenteGuada.getInstance().uploadAvatarConfiguration(configuration, self.__player)
    #print configuration

  def turnRight(self):
    #print "turn right"
    if not self.findIVItem(self.__player).hasAnimation():
      self.__player.turnRight()
    
  def turnLeft(self):
    #print "turn left"
    if not self.findIVItem(self.__player).hasAnimation():
      self.__player.turnLeft()
    
  def showTools(self):
    #print "show tools"
    pass

  def showSoundControl(self):
    
    if self.__sound:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.PATH_HUD + "/mute.png")
      self.__soundButton.picture = ocempgui.draw.Image.load_image(imgPath)
    else:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.PATH_HUD + "/sound.png")
      self.__soundButton.picture = ocempgui.draw.Image.load_image(imgPath)
    
    self.hud.remove_child(self.__soundButton)
    self.hud.add_child(self.__soundButton)
    self.__sound = not self.__sound

    
  def showHelp(self):
    """ Show help menu. (At the moment, It doesn't. It just toggles the full screen mode)
    """
    #print "show help"
    pass

  def finishGame(self):
    GG.genteguada.GenteGuada.getInstance().finish()
    
  def showFullScreen(self):
    """ Show help menu. (At the moment, It doesn't. It just toggles the full screen mode)
    """
    #print "show full screen"
    #TODO solo funciona en linux con las X, para e
    if self.__fullScreen:
      #imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/minimize.png")
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/maximize.png")
      self.__fullscreenButton.picture = ocempgui.draw.Image.load_image(imgPath)
    else:
      #imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/maximize.png")
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/minimize.png")
      self.__fullscreenButton.picture = ocempgui.draw.Image.load_image(imgPath)
    
    self.hud.remove_child(self.__fullscreenButton)
    self.hud.add_child(self.__fullscreenButton)

    self.__fullScreen = not self.__fullScreen
    pygame.display.toggle_fullscreen()

  def paintUserActions(self):
    
    ACTIONS = [
                {"image":"interface/hud/spinright.png", "action": self.turnRight, "tooltip":"Rotar derecha (R)"},
                {"image":"interface/hud/spinleft.png", "action": self.turnLeft, "tooltip":"Rotar izquierda (L)"},
                {"image":"interface/hud/jump.png", "action": self.jump, "tooltip":"Saltar (J)"},
                {"image":"interface/hud/dresser.png", "action": self.showDresser, "tooltip":"Cambiar configuracion avatar (D)"},
              ]
    i = 0
    for buttonData in ACTIONS:
      #button = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image']))
      filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image'])
      button = GG.utils.OcempImageButtonTransparent(filePath, buttonData['tooltip'], self.showTooltip, self.removeTooltip)
      button.topleft = 950 - i * 60 , 10
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, buttonData['action'])
      self.hud.add_child(button)
      i += 1

    from PIL import Image
    import os
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/editor/masko.png")
    img = Image.open(filePath)
    size = 64,64
    img.thumbnail(size,Image.ANTIALIAS)
    img.save(os.path.join(GG.utils.LOCAL_DATA_PATH,"imgMaskUser.png"))
    imgPath = os.path.join(GG.utils.LOCAL_DATA_PATH,"imgMaskUser.png")
    img = GG.utils.OcempImageButtonTransparent(imgPath)
    #img.topleft = 660,84
    img.topleft = 540,110
    self.hud.add_child(img)

    labelUserName = GG.utils.OcempLabel(self.__player.username, 280)
    labelUserName.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["userName"]))
    #labelUserName.topleft = ((182 - labelUserName.width) / 2) + 600, 150
    labelUserName.topleft = 620,80
    self.hud.add_child(labelUserName)
    
    self.__pointsLabel = GG.utils.OcempLabel("GuadaPuntos: 0", 280)
    self.__pointsLabel.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    self.__pointsLabel.topleft = 620, 120
    self.hud.add_child(self.__pointsLabel)

    self.__labelOld = GG.utils.OcempLabel("ClockPuntos: 0", 280)
    self.__labelOld.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    self.__labelOld.topleft = 620, 140
    self.hud.add_child(self.__labelOld)

    self.__expLabel = GG.utils.OcempLabel("Experiencia: 0", 280)
    self.__expLabel.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    self.__expLabel.topleft = 620, 160
    self.hud.add_child(self.__expLabel)

  def jump(self):
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
    #print "################",self.__selectedItem
    if self.__selectedItem == None:
      return
    self.__player.addToInventoryFromRoom(self.__selectedItem)
    self.__player.setUnselectedItem()    

  def itemCopyToInventory(self):
    """ Brings an item from the room to the player's inventory.
    """
    if self.__selectedItem == None:
      return
    item, pos = self.__selectedItem.getCopyFor(self.__player)
    #print "*********************",item
    if item != None:
      #self.__player.addToInventoryFromVoid(item, self.__selectedItem.getPosition())
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
    #print "push"
    self.itemUnselected()

  def itemToUp(self):
    #print "lift"
    self.itemUnselected()

  def privateChat(self):
    self.__player.setUnselectedItem()
    
  def itemToTalk(self):
    """ Talks to an item.
    """
    #print "talk"
    self.__player.talkTo(self.__selectedItem)
    self.itemUnselected()

  def exchangeItemPlayer(self):
    """ Shows the trade window.
    """
    #print "intercambio"
    self.__player.initExchangeTo(self.__selectedItem)
    #self.showExchangeWindow()

  def itemToOpen(self):
    """ Attempts to open a teleporter item.
    """
    #print "open"
    self.__player.open(self.__selectedItem)
    self.itemUnselected()

  def itemToUrl(self):
    """ Attempts to open a teleporter item.
    """
    #print "url"
    import webbrowser
    if self.__fullScreen:
      self.__fullScreen = False
      pygame.display.toggle_fullscreen()
    webbrowser.open(self.__selectedItem.url)
    self.itemUnselected()

  def itemToLift(self):
    #print "lift"
    pass
    """
    self.__player.lift(self.__selectedItem)
    self.itemUnselected()
    if self.__selectedItem:
      if self.__isoviewRoom:  
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.__selectedItem = None
        self.removeSprite(self.__selectedImage)        
    
    self.dropActionsItembuttons()
    """
  def itemToDrop(self):
    #print "drop"
    self.__player.drop(self.__selectedItem)
    self.itemUnselected()
    if self.__selectedItem:
      if self.__isoviewRoom:  
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.removeSprite(self.__selectedImage)        
        self.__selectedItem = None
    self.dropActionsItembuttons()

  def initExchange(self,event):
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
    self.exchangeWindow.addItemOut(self.__selectedItem)
    self.__player.setUnselectedItem()

  def cancelExchange(self,event):
    self.widgetContainer.remove_widget(self.exchangeWindow.window)
    self.removeSprite(self.exchangeWindow.window)
    self.exchangeWindow = None
    self.activeWindow = False

  def addListExchange(self, event):
    itemList = event.getParams()["list"]
    self.exchangeWindow.addInList(itemList) 

  def itemToClimb(self):
    #print "climb"
    self.__player.climb(self.__selectedItem)
    self.itemUnselected()
    if self.__selectedItem:
      if self.__isoviewRoom:  
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.removeSprite(self.__selectedImage)        
        self.__selectedItem = None
    self.dropActionsItembuttons()
    
  def itemToGiveCard(self):
    self.__selectedItem.checkContact(self.__player)
    self.itemUnselected()
    self.dropActionsItembuttons()
    
  def newContactDialog(self, event):
    if self.activeContactDialog:
      return  
    newContact = event.getParams()["contact"]
    self.confirmDialog = ocempgui.widgets.Box(300, 120)
    self.confirmDialog.set_position = [0, 0]
    okButton = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/editor/ok_button.png"))
    #okButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.giveContactCard)
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
    #self.activeContactDialog.addContact(self.__player)
    #self.__player.addContact(self.activeContactDialog)
    contact.addContact(self.__player)
    self.__player.addContact(contact)
    self.dropContactDialog()
      
  def dropContactDialog(self):
    self.widgetContainer.remove_widget(self.confirmDialog)
    self.removeSprite(self.confirmDialog)
    self.activeContactDialog = None
    self.itemUnselected()
    self.dropActionsItembuttons()
    
  def newContactAdded(self, event):
    contact = event.getParams()['contact']
    pass

  def privateChatReceived(self, event):
    chat = event.getParams()['chat']
    player = event.getParams()['player']
    self.privateChatWindow.incomingChatMessage(chat, player)
    
