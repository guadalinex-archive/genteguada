import os
import pygame
import GG.utils
import isoview
import isoview_inventoryitem
import ocempgui.widgets

class IsoViewHud(isoview.IsoView):
  """ IsoViewHud class.
  Defines the HUD.
  """
  
  def __init__(self, model, screen):
    """ Class constructor.
    model: ggsession model.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__isoviewInventory = []
    self.__player = self.getModel().getPlayer()
    self.__isoviewRoom = self.__player.getRoom().defaultView(self.getScreen(), self)
    self.__textFont = pygame.font.Font(None, 24)
    self.__textRect = pygame.Rect((GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1], GG.utils.CHAT_SZ[0], GG.utils.CHAT_SZ[1]))
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(screen)
    model.subscribeEvent('chatAdded', self.chatAdded)
    self.__player.subscribeEvent('room', self.roomChanged)
    #self.getModel().subscribeEvent('messagesChat', self.messaggesChatChanged)
    self.getModel().subscribeEvent('addMessageChat', self.messagesChatAdded)
    #self.getModel().subscribeEvent('removeMessageChat', self.messaggesChatRemoved)
    #self.getModel().subscribeEvent('changeActiveRoom', self.activeRoomChanged)

  def getTextFont(self):
    """ Returns the font used to print text on chat.
    """
    return self.__textFont
  
  def getTextRect(self):
    """ Returns the rectangle used to print text on chat.
    """
    return self.__textRect
  
  def addInventoryItem(self, item):
    """ Adds a new isoview inventory item.
    item: new isoview inventory item.
    """
    invItem = isoview_inventoryitem.IsoViewInventoryItem(item, self.getScreen())
    self.__isoviewInventory.append(invItem)
    self.paintInventory()
    
  def removeInventoryItem(self, item):
    """ Removes an item from the inventory item list.
    item: item to be removed.
    """
    toBeRemoved = None
    for ivInventoryItem in self.__isoviewInventory:
      if ivInventoryItem.getModel().label == item.label:
        toBeRemoved = ivInventoryItem
    if toBeRemoved:    
      self.__isoviewInventory.remove(toBeRemoved)
    self.paintInventory()
    
  def draw(self):
    """ Updates the changed zones on the room view and draws the hud.
    """
    self.paintBackground()
    self.paintChat()
    self.paintTextBox()
    self.paintInventory()

  def updateFrame(self):
    """ Updates all sprites for a new frame.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.updateFrame()
    pygame.display.update()

  def roomChanged(self, event):
    """ Triggers after receiving a change room event.
    event: event info.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.unsubscribeAllEvents()
      self.__isoviewRoom = None
      self.getScreen().fill([0,0,0])
      
      #auxScreen = pygame.display.set_mode(GG.utils.GAMEZONE_SZ)
      #auxScreen.fill([0,0,0])
      #auxScreen = pygame.display.set_mode(GG.utils.SCREEN_SZ)
      #rect = Pygame.Rect((0,0),(1024,568))
      #self.getScreen().fill([0,0,0], rect)
      #pygame.draw.rect(self.getScreen(),[0,0,0],rect)
      self.draw()
    if not event.getParams()["room"] is None:
      self.__isoviewRoom = event.getParams()["room"].defaultView(self.getScreen(), self)
      
  def getIsoviewRoom(self):
    """ Returns the isometric view room.
    """
    return self.__isoviewRoom
    
  def pruebaChat(self, events):
    """ Procedimiento de prueba para el chat del Hud.
    """
    self.printOnChat(events.getParams()["msg"])
    
  def clickedByPlayer(self, player, target):
    """ Indicates that a player has made click the isoview hud object.
    player: player who clicks.
    target: clicked point.
    """
    if not len(self.__isoviewInventory):
      return
    if GG.utils.INV_OR[0] < target[0] < (GG.utils.INV_OR[0] + GG.utils.INV_SZ[0]):
      if GG.utils.INV_OR[1] < target[1] < (GG.utils.INV_OR[1] + GG.utils.INV_SZ[1]):
        # click on the inventory
        auxTarget = [target[0] - GG.utils.INV_OR[0], target[1] - GG.utils.INV_OR[1]]
        i = j = k = itemPos = 0
        while j < GG.utils.INV_ITEM_COUNT[1] and not k:
          while i < GG.utils.INV_ITEM_COUNT[0] and not k:
            if GG.utils.INV_ITEM_SZ[0]*i < auxTarget[0] < (GG.utils.INV_ITEM_SZ[0]*i + GG.utils.INV_ITEM_SZ[0]-1):
              if GG.utils.INV_ITEM_SZ[1]*j < auxTarget[1] < (GG.utils.INV_ITEM_SZ[1]*j + GG.utils.INV_ITEM_SZ[1]-1):
                k = 1
                itemPos = j*GG.utils.INV_ITEM_COUNT[0] + i
            i += 1
          j += 1
        # click on an inventory item, itemPos
        if k:
          self.getModel().getPlayer().clickOnInventoryItem(self.__isoviewInventory[itemPos].getModel())
    self.paintInventory()
    pygame.display.update()
          
  # Paint methods
    
  def paintBackground(self):
    """ Paints the HUD background on screen.
    """
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER1,
              (GG.utils.HUD_OR[0], GG.utils.HUD_OR[1], GG.utils.HUD_SZ[0] - 1, GG.utils.HUD_SZ[1] - 1))
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER2,
              (GG.utils.HUD_OR[0] + 2, GG.utils.HUD_OR[1] + 2, GG.utils.HUD_SZ[0] - 5, GG.utils.HUD_SZ[1] - 5))
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER3,
              (GG.utils.HUD_OR[0] + 10, GG.utils.HUD_OR[1] + 10, GG.utils.HUD_SZ[0] - 21, GG.utils.HUD_SZ[1] - 21))
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BASE,
              (GG.utils.HUD_OR[0] + 12, GG.utils.HUD_OR[1] + 12, GG.utils.HUD_SZ[0] - 25, GG.utils.HUD_SZ[1] - 25))

  def paintChat(self):
    """ Paints the chat window on screen.
    """
    self.textArea = ocempgui.widgets.ScrolledList(GG.utils.CHAT_SZ[0], GG.utils.CHAT_SZ[1])
    self.textArea.set_scrolling(1)
    self.textArea.border = 1
    self.textArea.topleft = GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1]
    self.widgetContainer.add_widget(self.textArea)
 
  
  def paintTextBox(self):
    """ Paints the editable text box on screen.
    """
    self.textField = ocempgui.widgets.Entry()
    self.textField.border = 1
    self.textField.topleft = GG.utils.TEXT_BOX_OR[0], GG.utils.TEXT_BOX_OR[1]
    self.textField.set_minimum_size(GG.utils.TEXT_BOX_SZ[0], GG.utils.TEXT_BOX_SZ[1])
    self.widgetContainer.add_widget(self.textField)

       
  def paintInventory(self):
    """ Paints the inventory box and its items on it.    
    """
    pygame.draw.rect(self.getScreen(), GG.utils.INV_COLOR_BG,
              (GG.utils.INV_OR[0], GG.utils.INV_OR[1], GG.utils.INV_SZ[0] - 1, GG.utils.INV_SZ[1] - 1))
    n = 0
    for inventoryitem in self.__isoviewInventory:
      self.paintItemOnInventory(inventoryitem.getSpriteName(), n)
      n += 1
    
  def paintItemOnInventory(self, spriteName, position):
    """ Paints an item on the hud inventory.
    spriteName: sprite name.
    position: position in the inventory that the item will be painted into.
    """
    if position >= GG.utils.INV_ITEM_COUNT[0]*GG.utils.INV_ITEM_COUNT[1]:
      return 
    imgPath = os.path.join(GG.utils.DATA_PATH, spriteName)
    img = pygame.sprite.Sprite()
    img.image = pygame.image.load(imgPath).convert()
    img.rect = img.image.get_rect()
    img.rect.topleft = [GG.utils.INV_OR[0] + (GG.utils.INV_ITEM_SZ[0]*(position%GG.utils.INV_ITEM_COUNT[0])),
                        GG.utils.INV_OR[1] + (GG.utils.INV_ITEM_SZ[1]*(position/GG.utils.INV_ITEM_COUNT[0]))]
    self.getScreen().blit(img.image, img.rect)
  
  def printLineOnChat(self, string):
    """ Prints a string on the HUD chat window.
    string: the info that will be printed on screen.
    """
    self.textArea.items.append(ocempgui.widgets.components.TextListItem(string))
    self.textArea.vscrollbar.increase()
        
  def messagesChatAdded(self, event):
    """ Prints a string on the HUD chat window.
    string: the info that will be printed on screen.
    """
    string = event.getParams()["messageChat"]
    renderedText = GG.utils.renderTextRect(string, self.getTextFont(), self.getTextRect(), GG.utils.CHAT_COLOR_FONT, GG.utils.CHAT_COLOR_BG, 0)
    self.getScreen().blit(renderedText, self.getTextRect().topleft)
    pygame.display.update()
    
  def chatMessageEntered(self):
    """ Prints a new message on chat window.
    """
    self.getModel().getPlayer().newChatMessage(self.textField.text)
    self.textField.text = ""

  def chatAdded(self, event):
    """ Triggers after receiving a new chat message event.
    event: event info.
    """
    messageChat = event.getParams()['message']
    cad = messageChat.getHour()+" [" + messageChat.getSender() + "]: " + messageChat.getMessage()
    self.printLineOnChat(cad)
