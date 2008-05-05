import os
import pygame
import GG.utils
import isoview
import isoview_inventoryitem

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
    self.__textFont = pygame.font.Font(None, 16)
    self.__textRect = pygame.Rect((GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1], GG.utils.CHAT_SZ[0], GG.utils.CHAT_SZ[1]))
    #self.getModel().subscribeEvent('messagesChat', self.messaggesChatChanged)
    self.getModel().subscribeEvent('addMessageChat', self.messagesChatAdded)
    #self.getModel().subscribeEvent('removeMessageChat', self.messaggesChatRemoved)
    #self.getModel().subscribeEvent('changeActiveRoom', self.activeRoomChanged)
    self.__player.subscribeEvent('room', self.roomChanged)    

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
    for ivInventoryItem in self.__isoviewInventory:
      if ivInventoryItem.getModel().getLabel() == item.getLabel():
        toBeRemoved = ivInventoryItem
    self.__isoviewInventory.remove(toBeRemoved)
    self.paintInventory()
    
  def drawFirst(self):
    """ Draws the room and hud view on screen for the first time.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.drawFirst()
    self.paint()
    
  def draw(self):
    """ Updates the changed zones on the room view and draws the hud.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.draw()
    self.paint()
    
  def roomChanged(self, event):
    """ Triggers after receiving a change room event.
    event: event info.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.unsubscribeAllEvents()
      self.__isoviewRoom = None

    if event.getParams()["room"] != None:
      self.__isoviewRoom = event.getParams()["room"].defaultView(self.getScreen(), self)
      self.__isoviewRoom.drawFirst()
    #else:
    #  self.__isoviewRoom.unsubscribeAllEvents()
    #  self.__isoviewRoom = None
    self.draw()
      
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
          #self.printOnChat(self.__isoviewInventory[itemPos].getLabel())
          self.getModel().getPlayer().clickOnInventoryItem(self.__isoviewInventory[itemPos].getModel())
    self.paintInventory()
    pygame.display.update()
          
  # Paint methods
    
  def paint(self):
    """ Paints all HUD parts on screen.
    """
    self.paintBackground()
    self.paintChat()
    self.paintTextBox()
    self.paintInventory()
    pygame.display.update()

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
    pygame.draw.rect(self.getScreen(), GG.utils.CHAT_COLOR_BG,
              (GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1], GG.utils.CHAT_SZ[0] - 1, GG.utils.CHAT_SZ[1] - 1))
  
  def paintTextBox(self):
    pygame.draw.rect(self.getScreen(), GG.utils.TEXT_BOX_COLOR_BG,
              (GG.utils.TEXT_BOX_OR[0], GG.utils.TEXT_BOX_OR[1], GG.utils.TEXT_BOX_SZ[0] - 1, GG.utils.TEXT_BOX_SZ[1] - 1))
  
  def paintInventory(self):
    """ 
    """
    print "Objetos en inventario: ", len(self.getModel().getPlayer().getInventory())
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
    img.image = pygame.image.load(imgPath)
    img.rect = img.image.get_rect()
    img.rect.topleft = [GG.utils.INV_OR[0] + (GG.utils.INV_ITEM_SZ[0]*(position%GG.utils.INV_ITEM_COUNT[0])),
                        GG.utils.INV_OR[1] + (GG.utils.INV_ITEM_SZ[1]*(position/GG.utils.INV_ITEM_COUNT[0]))]
    self.getScreen().blit(img.image, img.rect)
  
    
  def messagesChatAdded(self, event):
    """ Prints a string on the HUD chat window.
    string: the info that will be printed on screen.
    """
    string = event.getParams()["messageChat"]
    renderedText = GG.utils.renderTextRect(string, self.getTextFont(), self.getTextRect(), GG.utils.CHAT_COLOR_FONT, GG.utils.CHAT_COLOR_BG, 0)
    self.getScreen().blit(renderedText, self.getTextRect().topleft)
    pygame.display.update()
    
  def printFullChat(self, chat):
    """ Prints
    
    200 chars max por linea de texto
        
    """
    pass
