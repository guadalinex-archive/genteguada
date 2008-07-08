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
import os

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
    self.__img.zOrder = 10000
    #self.__img.rect.topleft = GG.utils.HUD_OR

    model.subscribeEvent('chatAdded', self.chatAdded)
    self.__player.subscribeEvent('quizAdded', self.quizAdded)
    self.__player.subscribeEvent('room', self.roomChanged)
    #elf.__player.subscribeEvent('addInventory', self.inventoryAdded)
    self.__player.subscribeEvent('liftItem', self.liftItem)
    self.__player.subscribeEvent('liftItem', self.dropItem)
    self.__player.subscribeEvent('addToInventory', self.addItemToInventory)
    self.__player.subscribeEvent('removeFromInventory', self.inventoryRemoved)
    self.__player.subscribeEvent('selectedItem', self.itemSelected)
    self.__player.subscribeEvent('unselectedItem', self.itemUnselected)
    self.__player.subscribeEvent('points', self.pointsAdded)
    self.__player.subscribeEvent('exp', self.expAdded)
    self.__player.subscribeEvent('initExchange', self.initExchange)
    self.__player.subscribeEvent('cancelExchange', self.cancelExchange)
    self.__player.subscribeEvent('listExchange', self.addListExchange)
    
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
    
    self.buttonActions = {
        "inventory":{"image":"interface/hud/movein.png", "action": self.itemToInventory, "tooltip":"al inventario"},
        "copy":{"image":"interface/hud/movein.png", "action": self.itemCopyToInventory, "tooltip":"al inventario"},
        "removeInventory":{"image":"interface/hud/moveout.png", "action": self.itemOutInventory, "tooltip":" sacar del inventario"},
        "lift":{"image":"interface/hud/lift.png", "action": self.itemToLift, "tooltip":"levantar"},
        "drop":{"image":"interface/hud/drop.png", "action": self.itemToDrop, "tooltip":" arrastrar"},
        "climb":{"image":"interface/hud/climb.png", "action": self.itemToClimb, "tooltip":"subir"},
        "clone":{"image":"interface/hud/movein.png", "action": self.itemToClone, "tooltip":"al inventario"},
        "push":{"image":"interface/hud/push.png", "action": self.itemToPush, "tooltip":"empujar"},
        "up":{"image":"interface/hud/lift.png", "action": self.itemToUp, "tooltip": "subir"},
        "talk":{"image":"interface/hud/chat.png", "action": self.itemToTalk, "tooltip":"hablar"},
        "talkAndGet":{"image":"interface/hud/chat.png", "action": self.itemToTalkAndGet, "tooltip":"hablar"},
        "privateChat":{"image":"interface/hud/chat.png", "action": self.privateChat, "tooltip":"chat"},
        "exchange":{"image":"interface/hud/exchange.png", "action": self.exchangeItemPlayer, "tooltip":"intercambio"},
        "open":{"image":"interface/hud/open.png", "action": self.itemToOpen, "tooltip":"abrir"},
        "url":{"image":"interface/hud/www.png", "action": self.itemToUrl, "tooltip":"ir a "},
        "toExchange":{"image":"interface/hud/push.png", "action": self.itemToExchange, "tooltip":"al intercambio"}
    }
    self.winWardrobe = None
    self.wardrobe = None
    self.exchangeWindow = None
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
  
  def processEvent(self, events):
    for event in events:
      event_type = event.type
      if event_type == QUIT:
        GG.genteguada.GenteGuada.getInstance().finish()
      elif event_type == KEYDOWN:
        if event.key == K_ESCAPE:
          GG.genteguada.GenteGuada.getInstance().finish()
        elif event.key == K_RETURN: 
          self.chatMessageEntered()
      elif event_type == MOUSEBUTTONDOWN:
        if not self.exchangeWindow:
          cordX, cordY = pygame.mouse.get_pos()
          if 0 <= cordY <= GG.utils.HUD_OR[1]:
            dest, item = self.getIsoviewRoom().findTile([cordX, cordY])
            if not dest == [-1, -1, -1]:
              self.__isoviewRoom.getModel().clickedByPlayer(self.__player, dest, item)
    self.widgetContainer.distribute_events(*events)

  def compareSelectedItem(self, item):
    if self.__selectedItem:  
      return self.__selectedItem.checkSimilarity(item)
    else:
      return False

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
    ivInventItem = self.findIVInventoryItem(item)
    if ivItem:    
      posX = len(self.__isoviewInventory)%GG.utils.INV_ITEM_COUNT[0]
      posY = len(self.__isoviewInventory)/GG.utils.INV_ITEM_COUNT[1]
      pos = [GG.utils.INV_OR[0] + (posX * GG.utils.INV_ITEM_SZ[0]), GG.utils.INV_OR[1] + (posY * GG.utils.INV_ITEM_SZ[1])]
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            #pos, GG.utils.p3dToP2d(item.getPosition(), item.anchor), True)
                            pos, self.__isoviewRoom.getFutureScreenPosition(ivItem, item.getPosition()), True)
      positionAnim.setOnStop(self.__isoviewRoom.updateScreenPositionsOn, item.getPosition())
      ivItem.setAnimation(positionAnim)
      if ivInventItem != None:
        self.__isoviewInventory.remove(ivInventItem)
        self.paintItemsInventory()
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
    imgBackground = GG.utils.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0,0
    self.hud.add_child(imgBackground)

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
            "font" : ocempgui.widgets.WidgetStyle ({ "name" : None,
                                    "size" : 0,
                                    "alias" : False,
                                    "style" : 0 }),
            "shadow" : 0
            })
    self.textArea = ocempgui.widgets.ScrolledWindow(573, 117)
    self.textArea.set_style(myOwnStyle)
    self.textArea.update()
    self.textArea.set_scrolling(1)
   # self.textArea.border = 1
    #self.textArea.topleft = GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1] + 20
    self.textArea.topleft = GG.utils.CHAT_OR[0], 70
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
    self.__textField.topleft = 14, 190
    self.__textField.set_minimum_size(571, 30)
    self.hud.add_child(self.__textField)
    #self.widgetContainer.add_widget(self.__textField)

  def paintInventory(self):
    """ Paints the inventory box and its items on it.    
    """
    self.windowInventory = ocempgui.widgets.ScrolledWindow(190, 163)
    self.windowInventory.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["inventoryArea"]))
    self.windowInventory.border = 1
    self.windowInventory.topleft = 805, 70
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
    self.removeMovementDestination()
    self.__targetTileImage.rect.topleft = GG.utils.p3dToP2d(target, GG.utils.TILE_TARGET_SHIFT)
    self.__targetTileImage.zOrder = (pow(target[0], 2) + pow(target[2], 2))*10 - 1
    self.addSprite(self.__targetTileImage)        
    self.__targetTile = True  
    
  def removeMovementDestination(self):
    #if self.__targetTile:
    #if self.__allSprites.has(self.__targetTileImage):
      #if self.__allSprites.has(self.__targetTileImage):
    try:
      self.removeSprite(self.__targetTileImage)  
    except KeyError:
        # This can happen if a sprite is removed before
        # update() has had a chance to be called.
      pass
    self.__targetTile = False
    
  def itemSelected(self,event):
    """ Triggers after receiving an item selected event.
    event: event info.
    """
    self.__selectedItem = event.getParams()['item']
    if not self.__selectedItem.inventoryOnly():
      if self.__selectedItem.getRoom():
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
    for action in options:
      #button = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(self.buttonActions[action]['image']))
      filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.buttonActions[action]['image'])
      button = GG.utils.OcempImageButtonTransparent2(filePath, self.buttonActions[action]['tooltip'], self.showTooltip, self.removeTooltip)
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.buttonActions[action]['action'])
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
                {"image":"interface/hud/exit.png", "action": self.finishGame, "tooltip":"Finalizar"},
                {"image":"interface/hud/maximize.png", "action": self.showFullScreen, "tooltip":"Maximizar o minimizar pantalla"},
                {"image":"interface/hud/sound.png", "action": self.showSoundControl, "tooltip":"Controles de sonido"},
                #{"image":"interface/hud/rotateright.png", "action": self.turnRight, "tooltip":"rotar derecha"},
                #{"image":"interface/hud/rotateleft.png", "action": self.turnLeft, "tooltip":"rotar izquierda"},
                ]
    else:
      ACTIONS = [
                #{"image":"interface/hud/help.png", "action": self.showHelp, "tooltip":"Ayuda"},
                {"image":"interface/hud/exit.png", "action": self.finishGame, "tooltip":"Finalizar"},
                {"image":"interface/hud/minimize.png", "action": self.showFullScreen, "tooltip":"Maximizar o minimizar pantalla"},
                {"image":"interface/hud/sound.png", "action": self.showSoundControl, "tooltip":"Controles de sonido"},
                #{"image":"interface/hud/rotateright.png", "action": self.turnRight, "tooltip":"rotar derecha"},
                #{"image":"interface/hud/rotateleft.png", "action": self.turnLeft, "tooltip":"rotar izquierda"},
                ]
    
    i = 0
    for buttonData in ACTIONS:
      #button = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image']))
      filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image'])
      button = GG.utils.OcempImageButtonTransparent2(filePath, buttonData['tooltip'], self.showTooltip, self.removeTooltip)
      button.topleft = 16 + i*60 ,10
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, buttonData['action'])
      if buttonData['action'] == self.showFullScreen:
        self.__fullscreenButton = button
      elif  buttonData['action'] == self.showSoundControl:
        self.__soundButton = button
      i+=1
      self.hud.add_child(button)
  
  def showTooltip(self, label):
    self.tooltipWindow = ocempgui.widgets.TooltipWindow (label)
    self.tooltipWindow.depth = 1
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
    GG.genteguada.GenteGuada.getInstance().activeScreen = self.wardrobe

  def closeDresser(self, configuration = None):
    if configuration:
      self.setAvatarConfiguration(configuration)
    GG.genteguada.GenteGuada.getInstance().activeScreen = self
    self.winWardrobe.destroy()
    self.winWardrobe = None

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
    print "show sound control"
    if self.__sound:
      print "Cambiamos el icono a mute"
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.PATH_HUD + "/mute.png")
      self.__soundButton.picture = ocempgui.draw.Image.load_image(imgPath)
    else:
      print "Cambiamos el icono a sonido"
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.PATH_HUD + "/sound.png")
      self.__soundButton.picture = ocempgui.draw.Image.load_image(imgPath)
    self.__soundButton.dirty = True 
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
    print "show full screen"
    #TODO solo funciona en linux con las X, para e
    if self.__fullScreen:
      self.__fullscreenButton.picture = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/minimize.png")
    else:
      self.__fullscreenButton.picture = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/maximize.png")
    self.__fullScreen = not self.__fullScreen
    pygame.display.toggle_fullscreen()

  def paintUserActions(self):
    
    ACTIONS = [
                {"image":"interface/hud/spinright.png", "action": self.turnLeft, "tooltip":"rotar derecha"},
                {"image":"interface/hud/spinleft.png", "action": self.turnRight, "tooltip":"rotar izquierda"},
                {"image":"interface/hud/jump.png", "action": self.jump, "tooltip":"saltar"},
                {"image":"interface/hud/dresser.png", "action": self.showDresser, "tooltip":"Cambiar configuracion avatar"},
              ]
    i = 0
    for buttonData in ACTIONS:
      #button = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image']))
      filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image'])
      button = GG.utils.OcempImageButtonTransparent2(filePath, buttonData['tooltip'], self.showTooltip, self.removeTooltip)
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
    img.topleft = 660,84 
    self.hud.add_child(img)

    labelUserName = GG.utils.OcempLabel(self.__player.username, 280)
    labelUserName.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    labelUserName.topleft = ((182 - labelUserName.width) / 2) + 600, 150
    self.hud.add_child(labelUserName)
    
    self.__pointsLabel = GG.utils.OcempLabel("GuadaPuntos: 0", 280)
    self.__pointsLabel.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    self.__pointsLabel.topleft = 617, 170
    self.hud.add_child(self.__pointsLabel)

    self.__labelOld = GG.utils.OcempLabel("ClockPuntos: 0", 280)
    self.__labelOld.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    self.__labelOld.topleft = 617, 190
    self.hud.add_child(self.__labelOld)

    self.__expLabel = GG.utils.OcempLabel("Experiencia: 0", 280)
    self.__expLabel.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    self.__expLabel.topleft = 617, 210
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
    self.__player.lift(self.__selectedItem)
    self.itemUnselected()
    if self.__selectedItem:
      if self.__isoviewRoom:  
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.__selectedItem = None
        self.removeSprite(self.__selectedImage)        
    
    self.dropActionsItembuttons()
    
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
  
  def itemToExchange(self):
    self.exchangeWindow.addItemOut(self.__selectedItem)
    self.__player.setUnselectedItem()

  def cancelExchange(self,event):
    self.widgetContainer.remove_widget(self.exchangeWindow.window)
    self.removeSprite(self.exchangeWindow.window)
    self.exchangeWindow = None

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
