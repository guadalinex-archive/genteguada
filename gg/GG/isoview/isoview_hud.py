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

from pygame.locals import * # faster name resolution


class IsoViewHud(isoview.IsoView):
  """ IsoViewHud class.
  Defines the HUD.
  """
  
  def __init__(self, model, screen, parent):
    """ Class constructor.
    model: ggsession model.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__isoviewInventory = []
    self.__player = self.getModel().getPlayer()
    self.__isoviewRoom = self.__player.getRoom().defaultView(self.getScreen(), self)
    #self.widgetContainer = ocempgui.widgets.Renderer()
    #self.widgetContainer.set_screen(screen)
    self.textArea = None
    self.__textField = None
    self.windowInventory = None
    
    self.__fullScreen = False
    
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.INTERFACE_LOWER)).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    #self.__img.rect.topleft = GG.utils.HUD_OR

    self.__toolBarBackground = pygame.sprite.Sprite()
    self.__toolBarBackground.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/interface_upper.png")).convert_alpha()
    #self.__toolBarBackground.rect = self.__img.image.get_rect()
    #self.__toolBarBackground.rect.topleft = GG.utils.HUD_OR[0],GG.utils.HUD_OR[1] - 400

    self.__optionsBarBackground = pygame.sprite.Sprite()
    self.__optionsBarBackground.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/actionsNotification.png")).convert_alpha()
    #self.__optionsBarBackground.rect = self.__img.image.get_rect()
    #self.__toolBarBackground.rect.topleft = GG.utils.HUD_OR[0],GG.utils.HUD_OR[1] - 400


    model.subscribeEvent('chatAdded', self.chatAdded)
    model.subscribeEvent('quizAdded', self.quizAdded)
    self.__player.subscribeEvent('room', self.roomChanged)
    #elf.__player.subscribeEvent('addInventory', self.inventoryAdded)
    self.__player.subscribeEvent('liftItem', self.liftItem)
    self.__player.subscribeEvent('addToInventory', self.addItemToInventory)
    self.__player.subscribeEvent('removeFromInventory', self.inventoryRemoved)
    self.__player.subscribeEvent('selectedItem', self.itemSelected)
    self.__player.subscribeEvent('unselectedItem', self.itemUnselected)
    self.__player.subscribeEvent('points', self.pointsAdded)
    self.__player.subscribeEvent('exp', self.expAdded)
    
    self.__selectedItem = None
    self.buttonActions = {
        "inventory":{"image":"interface/hud/movein.png", "action": self.itemToInventory},
        "copy":{"image":"interface/hud/movein.png", "action": self.itemCopyToInventory},
        "removeInventory":{"image":"interface/hud/moveout.png", "action": self.itemOutInventory},
        "lift":{"image":"interface/hud/rotateright.png", "action": self.itemToLift},
        "clone":{"image":"interface/hud/movein.png", "action": self.itemToClone},
        "push":{"image":"interface/hud/push.png", "action": self.itemToPush},
        "up":{"image":"interface/hud/lift.png", "action": self.itemToUp},
        "talk":{"image":"interface/hud/chat.png", "action": self.itemToTalk},
        "exchange":{"image":"interface/hud/empujar.png", "action": self.exchangeItemPlayer},
        "open":{"image":"interface/hud/open.png", "action": self.itemToOpen},
        "url":{"image":"interface/hud/rotateright.png", "action": self.itemToUrl}
    }
    self.winWardrobe = None
    self.wardrobe = None
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
        cordX, cordY = pygame.mouse.get_pos()
        if 0 <= cordY <= GG.utils.HUD_OR[1]:
          dest = self.getIsoviewRoom().findTile([cordX, cordY])
          if not dest == [-1, -1, -1]:
            self.__isoviewRoom.getModel().clickedByPlayer(self.__player, dest)
    self.widgetContainer.distribute_events(*events)

  def getPlayer(self):
    return self.__player
  
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
    self.__isoviewInventory.remove(ivInventItem)
    self.paintItemsInventory()
      
  def liftItem(self, event):
    item = event.getParams()["item"]  
    ivItem = self.__isoviewRoom.findIVItem(item)  
    if ivItem != None:
      self.__isoviewRoom.updateScreenPositionsOn(item.getPosition())  
      
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
    if ivItem != None:
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            GG.utils.p3dToP2d(posOrigin, item.anchor), pos, True)
      #positionAnim.setOnStop(self.__isoviewRoom.removeSprite, ivItem.getImg())
      positionAnim.setOnStop(item.getRoom().removeItem, item)
    else:
      ivItem = item.defaultView(self.getScreen(), self.__isoviewRoom, self)
      self.__isoviewRoom.addIsoViewItem(ivItem)  
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            GG.utils.p3dToP2d(posOrigin, [0, 0]), pos, True)
      positionAnim.setOnStop(self.__isoviewRoom.removeSprite, ivItem.getImg())
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
      GG.utils.playSound(GG.utils.SOUND_DROPITEM)
      
  def draw(self):
    """ Updates the changed zones on the room view and draws the hud.
    """
    #self.paintBackground()
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.getScreen())
    self.paintInventory()
    self.paintChat()
    self.paintTextBox()
    self.paintActionButtons()
    self.paintUserActions()

  def updateFrame(self, ellapsedTime):
    """ Updates all sprites for a new frame.
    """
    #hay que dibujar la habitacion DESPUES del hud, para que las animaciones de los items 
    #se vean sobre el HUD y no debajo como ahora.

    self.paintBackground()
    self.buttonBar.update()
    self.textArea.update()
    self.__textField.update()
    self.windowInventory.update()

    if self.__isoviewRoom:
      self.__isoviewRoom.updateFrame(ellapsedTime)
    #for item in self.__isoviewInventory:
    #  item.updateFrame(ellapsedTime)
    pygame.display.update()

  def roomChanged(self, event):
    """ Triggers after receiving a change room event.
    event: event info.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.stopAnimations()
      self.__isoviewRoom.unsubscribeAllEvents()
      GG.utils.playSound(GG.utils.SOUND_OPENDOOR)
      self.__isoviewRoom = None
      rect = pygame.Rect(0, 0, GG.utils.GAMEZONE_SZ[0], GG.utils.GAMEZONE_SZ[1])
      self.getScreen().fill((0, 0, 0), rect)
      self.buttonBar.update()
    if not event.getParams()["room"] is None:
      self.__isoviewRoom = event.getParams()["room"].defaultView(self.getScreen(), self)
      #self.__isoviewRoom.addSprite(self.__pointsLabel)
      #self.__isoviewRoom.addSprite(self.__expLabel)
      
  def getIsoviewRoom(self):
    """ Returns the isometric view room.
    """
    return self.__isoviewRoom
           
  # Paint methods
    
  def paintBackground(self):
    """ Paints the HUD background on screen.
    """
    self.getScreen().blit(self.__img.image, GG.utils.HUD_OR)
    self.getScreen().blit(self.__toolBarBackground.image, [GG.utils.HUD_OR[0],GG.utils.HUD_OR[1] - 63])
    self.getScreen().blit(self.__optionsBarBackground.image, [GG.utils.SCREEN_SZ[0] - 260,0])
    #pygame.display.update()

  def paintChat(self):
    """ Paints the chat window on screen.
    """
    self.textArea = ocempgui.widgets.ScrolledWindow(GG.utils.CHAT_SZ[0], GG.utils.CHAT_SZ[1])
    self.textArea.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["chatArea"]))
    self.textArea.set_scrolling(1)
    self.textArea.border = 1
    self.textArea.topleft = GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1]
    self.__layoutTextArea= ocempgui.widgets.VFrame()
    self.__layoutTextArea.border = 0
    self.__layoutTextArea.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.textArea.child = self.__layoutTextArea
    self.widgetContainer.add_widget(self.textArea)
  
  def paintTextBox(self):
    """ Paints the editable text box on screen.
    """
    self.__textField = ocempgui.widgets.Entry()
    self.__textField.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["textFieldChat"]))
    self.__textField.border = 1
    self.__textField.topleft = GG.utils.TEXT_BOX_OR[0], GG.utils.TEXT_BOX_OR[1]
    self.__textField.set_minimum_size(GG.utils.TEXT_BOX_SZ[0], GG.utils.TEXT_BOX_SZ[1])
    self.widgetContainer.add_widget(self.__textField)

  def paintInventory(self):
    """ Paints the inventory box and its items on it.    
    """
    self.windowInventory = ocempgui.widgets.ScrolledWindow(GG.utils.INV_SZ[0], GG.utils.INV_SZ[1])
    self.windowInventory.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["inventoryArea"]))
    self.windowInventory.border = 1
    self.windowInventory.topleft = GG.utils.INV_OR[0], GG.utils.INV_OR[1] - 15
    self.widgetContainer.add_widget(self.windowInventory)
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
      self.__player.removeFromInventory(self.__selectedItem)  
      #self.__isoviewInventory.remove(invIsoItem)
      self.paintItemsInventory()
    else:   
      self.__player.addToRoomFromInventory(self.__selectedItem)
    self.__player.setUnselectedItem()
    """
      self.itemUnselected()
      
      if self.__selectedItem:
        if self.__isoviewRoom:  
          self.__isoviewRoom.itemUnselected(self.__selectedItem)
          self.__selectedItem = None
      self.dropActionsItembuttons()
    """

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
    secAnim.setOnStop(self.__isoviewRoom.removeTopSprite, ivMessageChat.getImg())
    ivMessageChat.setAnimation(secAnim)
    self.__isoviewRoom.addIsoViewChatItem(ivMessageChat)

  def quizAdded(self, event):
    """ Triggers after receiving a new quiz event.
    event: event info.
    """
    print "quizzzzzzzzzzzzzzz"
    messageChat = event.getParams()['message']
    ivMessageChat = messageChat.chatView(self.getScreen(), self)
    self.__isoviewRoom.addIsoViewChatItem(ivMessageChat)
        
  def itemSelected(self,event):
    """ Triggers after receiving an item selected event.
    event: event info.
    """
    self.__selectedItem = event.getParams()['item'] 
    self.__isoviewRoom.itemSelected(self.__selectedItem)
    options = self.__selectedItem.getOptions()
    
    self.buttonBarActions = ocempgui.widgets.VFrame()
    self.buttonBarActions.topleft = [GG.utils.SCREEN_SZ[0] - 260,0]
    self.buttonBarActions.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["buttonBar"]))
    self.buttonBarActions.border = 0
    self.buttonBarActions.align = ocempgui.widgets.Constants.ALIGN_RIGHT

    informationBar = ocempgui.widgets.HFrame()
    informationBar.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["buttonBar"]))
    informationBar.border = 0

    if self.__selectedItem.spriteInventory:
      img = self.__selectedItem.spriteInventory
    else:
      img = self.__selectedItem.spriteName
    from PIL import Image
    import os
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(img)
    img = Image.open(filePath)
    size = 20,20
    img.thumbnail(size,Image.ANTIALIAS)
    img.save(os.path.join(GG.utils.LOCAL_DATA_PATH,"imgToolbar.png"))
    imgPath = os.path.join(GG.utils.LOCAL_DATA_PATH,"imgToolbar.png")
    img = GG.utils.OcempImageButtonTransparent(imgPath)
    informationBar.add_child(img)
    
    
    itemLabel = GG.utils.OcempLabel(self.__selectedItem.label,290)
    itemLabel.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    informationBar.add_child(itemLabel)

    self.buttonBarActions.add_child(informationBar)

    optionsBar = ocempgui.widgets.HFrame()
    optionsBar.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["buttonBar"]))
    optionsBar.border = 0
    for action in options:
      button = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(self.buttonActions[action]['image']))
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.buttonActions[action]['action'])
      optionsBar.add_child(button)

    self.buttonBarActions.add_child(optionsBar)
    self.buttonBarActions.set_minimum_size(260,self.buttonBarActions.height)
    self.__isoviewRoom.addSprite(self.buttonBarActions)
    self.widgetContainer.add_widget(self.buttonBarActions)
  
  def itemUnselected(self,event=None):
    if self.__selectedItem:
      if self.__isoviewRoom:
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
    self.dropActionsItembuttons()

  def pointsAdded(self, event):
    self.__pointsLabel.set_text("Puntos: " + str(event.getParams()["points"]))
    
  def expAdded(self, event):
    self.__expLabel.set_text("Exp: " + str(event.getParams()["exp"]))
  
  #Defincion de la buttonBar y sus acciones permanentes

  def paintActionButtons(self):
    """ Paints the general action buttons.
    """
    """
    ACTIONS = [
                {"image":"interface/hud/dresser.png", "action": self.showDresser},
                {"image":"interface/hud/rotateright.png", "action": self.turnRight},
                {"image":"interface/hud/rotateleft.png", "action": self.turnLeft},
                {"image":"interface/hud/tools.png", "action": self.showTools},
                {"image":"interface/hud/sound.png", "action": self.showSoundControl},
                #{"image":"interface/hud/help.png", "action": self.showHelp},
                {"image":"interface/hud/fullscreen.png", "action": self.showFullScreen},
              ]
    """
    ACTIONS = [
                {"image":"interface/hud/fullscreen.png", "action": self.showFullScreen},
                {"image":"interface/hud/sound.png", "action": self.showSoundControl},
                {"image":"interface/hud/help.png", "action": self.showHelp},
                {"image":"interface/hud/exit.png", "action": self.finishGame},
              ]
    
    self.buttonBar = ocempgui.widgets.HFrame()
    self.buttonBar.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["buttonBar"]))
    self.buttonBar.border = 0
    self.buttonBar.topleft = [0,GG.utils.HUD_OR[1] - 65]
    self.widgetContainer.add_widget(self.buttonBar)
    for buttonData in ACTIONS:
      #button = ocempgui.widgets.ImageButton(GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image']))
      button = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image']))
      #button.border = 0
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, buttonData['action'])
      self.buttonBar.add_child(button)
  
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
    print configuration

  def turnRight(self):
    print "turn right"
    self.__player.turnRight()
    
  def turnLeft(self):
    print "turn left"
    self.__player.turnLeft()
    
  def showTools(self):
    self.__player.setCarrying()
    print "show tools"

  def showSoundControl(self):
    self.__player.setNotCarrying()
    print "show sound control"
    
  def showHelp(self):
    """ Show help menu. (At the moment, It doesn't. It just toggles the full screen mode)
    """
    print "show help"

  def finishGame(self):
    GG.genteguada.GenteGuada.getInstance().finish()
    
  def showFullScreen(self):
    """ Show help menu. (At the moment, It doesn't. It just toggles the full screen mode)
    """
    print "show full screen"
    #TODO solo funciona en linux con las X, para e
    self.__fullScreen = not self.__fullScreen
    pygame.display.toggle_fullscreen()

  def paintUserActions(self):
    
    self.userBar = ocempgui.widgets.VFrame()
    self.userBar.topleft = [GG.utils.SCREEN_SZ[0] - 400 ,GG.utils.HUD_OR[1] - 90]
    self.userBar.border = 0
    self.userBar.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["buttonBar"]))
    self.userBar.align = ocempgui.widgets.Constants.ALIGN_LEFT
    
    labelUserName = GG.utils.OcempLabel(self.__player.username, 280)
    labelUserName.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    self.userBar.add_child(labelUserName)

    pointsBar = ocempgui.widgets.VFrame()
    pointsBar.border = 0
    pointsBar.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["buttonBar"]))
    pointsBar.align = ocempgui.widgets.Constants.ALIGN_RIGHT
    self.__pointsLabel = GG.utils.OcempLabel("Puntos: 0",140)
    self.__pointsLabel.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    pointsBar.add_child(self.__pointsLabel)
    self.__expLabel = GG.utils.OcempLabel("Exp: 0",140)
    self.__expLabel.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["points"]))
    pointsBar.add_child(self.__expLabel)
    #self.userBar.add_child(pointsBar)

    actionsBar = ocempgui.widgets.HFrame()
    actionsBar.border = 0
    actionsBar.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["buttonBar"]))
    ACTIONS = [
                {"image":"interface/hud/dresser.png", "action": self.showDresser},
                {"image":"interface/hud/jump.png", "action": self.jump},
                {"image":"interface/hud/rotateright.png", "action": self.turnRight},
                {"image":"interface/hud/rotateleft.png", "action": self.turnLeft},
              ]
    for buttonData in ACTIONS:
      button = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image']))
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, buttonData['action'])
      actionsBar.add_child(button)
    actionsBar.add_child(pointsBar)
    self.userBar.add_child(actionsBar)

    self.__isoviewRoom.addSprite(self.userBar)

    self.widgetContainer.add_widget(self.userBar)

  def jump(self):
    self.__player.jump()

  #definicion de las acciones y botones en funcion del item seleccionado
  
  def dropActionsItembuttons(self):
    """ Removes the action buttons from the screen.
    """
    if self.__selectedItem == None:
      return
    self.__selectedItem = None
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
    #self.__isoviewRoom.setItemOnTile(None, self.__selectedItem.getPosition())
    #self.__selectedItem.getRoom().removeItem(self.__selectedItem)
    self.dropActionsItembuttons()
 
  def itemCopyToInventory(self):
    """ Brings an item from the room to the player's inventory.
    """
    if self.__selectedItem == None:
      return
    item = self.__selectedItem.getCopyFor(self.__player)
    if item != None:
      self.__player.addToInventoryFromVoid(item, self.__selectedItem.getPosition())
    self.itemUnselected()
    self.dropActionsItembuttons()
 
  def itemToClone(self):
    """ Clones an item from the room and inserts it on the player's inventory
    """
    clone = self.__selectedItem.getClone()
    self.__player.addInventory(clone)
    self.itemUnselected()

  def itemToPush(self):
    print "push"
    self.itemUnselected()

  def itemToUp(self):
    print "lift"
    self.itemUnselected()

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
    self.showExchangeWindow()

  def showExchangeWindow(self):
    """ Shows the exchange items window.
    """
    window = ocempgui.widgets.VFrame()
    window.set_minimum_size(GG.utils.INV_SZ[0], GG.utils.INV_SZ[1])
    window.topleft = GG.utils.SCREEN_SZ[0] - 200, GG.utils.HUD_OR[1] - 200
    window.border = 1
    #self.buttonBarActions.topleft = [GG.utils.SCREEN_SZ[0] - (GG.utils.ACTION_BUTTON_SZ[0]*len(options) - anchor), \
    #                                 GG.utils.HUD_OR[1] - GG.utils.ACTION_BUTTON_SZ[1]]
    self.widgetContainer.add_widget(window)

  def itemToOpen(self):
    """ Attempts to open a teleporter item.
    """
    print "open"
    self.__player.open(self.__selectedItem)
    self.itemUnselected()

  def itemToUrl(self):
    """ Attempts to open a teleporter item.
    """
    print "url"
    import webbrowser
    if self.__fullScreen:
      self.showHelp()
    webbrowser.open(self.__selectedItem.url)
    self.itemUnselected()


  def itemToLift(self):
    print "lift"
    self.__player.lift(self.__selectedItem)
    self.itemUnselected()
    if self.__selectedItem:
      if self.__isoviewRoom:  
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
        self.__selectedItem = None
    self.dropActionsItembuttons()
    
