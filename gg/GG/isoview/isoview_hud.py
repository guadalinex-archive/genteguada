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
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(screen)
    self.textArea = None
    self.__textField = None
    model.subscribeEvent('chatAdded', self.chatAdded)
    self.__player.subscribeEvent('room', self.roomChanged)
    self.__player.subscribeEvent('addInventory', self.inventoryAdded)
    self.__player.subscribeEvent('removeInventory', self.inventoryRemoved)

  def inventoryAdded(self, event):
    """ Adds a new isoview inventory item.
    item: new isoview inventory item.
    """
    item = event.getParams()["item"]
    invItem = isoview_inventoryitem.IsoViewInventoryItem(item, self.getScreen())
    self.__isoviewInventory.append(invItem)
    #self.paintInventory()
    self.paintItemOnInventory(invItem.getSpriteName(), len(self.__isoviewInventory) - 1)
    
  def inventoryRemoved(self, event):
    """ Removes an item from the inventory item list.
    item: item to be removed.
    """
    item = event.getParams()["item"]
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
      GG.utils.playSound(GG.utils.SOUND_OPENDOOR)
      self.__isoviewRoom = None
      rect = pygame.Rect(0, 0, GG.utils.GAMEZONE_SZ[0], GG.utils.GAMEZONE_SZ[1])
      self.getScreen().fill((0, 0, 0), rect)
    if not event.getParams()["room"] is None:
      self.__isoviewRoom = event.getParams()["room"].defaultView(self.getScreen(), self)
      
  def getIsoviewRoom(self):
    """ Returns the isometric view room.
    """
    return self.__isoviewRoom
    
  def clickedByPlayer(self, target):
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
          GG.utils.playSound(GG.utils.SOUND_DROPITEM)
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
    self.__textField = ocempgui.widgets.Entry()
    self.__textField.border = 1
    self.__textField.topleft = GG.utils.TEXT_BOX_OR[0], GG.utils.TEXT_BOX_OR[1]
    self.__textField.set_minimum_size(GG.utils.TEXT_BOX_SZ[0], GG.utils.TEXT_BOX_SZ[1])
    self.widgetContainer.add_widget(self.__textField)

  def paintInventory(self):
    """ Paints the inventory box and its items on it.    
    """
    windowInventory = ocempgui.widgets.ScrolledWindow(GG.utils.INV_SZ[0], GG.utils.INV_SZ[1])
    windowInventory.border = 1
    windowInventory.topleft = GG.utils.INV_OR[0], GG.utils.INV_OR[1]
    self.__frameInventory = ocempgui.widgets.VFrame()
    self.__frameInventory.border = 0
    self.__frameInventory.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    #self.__frameInventory.topleft = GG.utils.INV_OR[0], GG.utils.INV_OR[1]
    windowInventory.child = self.__frameInventory
    self.widgetContainer.add_widget(windowInventory)
    #pygame.draw.rect(self.getScreen(), GG.utils.INV_COLOR_BG,
    #          (GG.utils.INV_OR[0], GG.utils.INV_OR[1], GG.utils.INV_SZ[0] - 1, GG.utils.INV_SZ[1] - 1))
    position = 0
    for inventoryitem in self.__isoviewInventory:
      self.paintItemOnInventory(inventoryitem.getSpriteName(), position)
      position += 1

  def prueba(self,event,img):
    print "aunque sea"
    print img
    
  def paintItemOnInventory(self, spriteName, position):
    """ Paints an item on the hud inventory.
    spriteName: sprite name.
    position: position in the inventory that the item will be painted into.
    """
    #if position >= GG.utils.INV_ITEM_COUNT[0]*GG.utils.INV_ITEM_COUNT[1]:
    #  return 

    imgInventory = ocempgui.widgets.ImageMap(os.path.join(GG.utils.DATA_PATH, spriteName))
    #imgInventory = ocempgui.widgets.ImageLabel(os.path.join(GG.utils.DATA_PATH, spriteName))
    imgInventory.connect_signal (ocempgui.widgets.Constants.SIG_MOUSEDOWN, self.prueba, imgInventory)

    #imgInventory.border = 0
    #imgInventory.topleft = GG.utils.INV_OR[0] + (GG.utils.INV_ITEM_SZ[0]*(position%GG.utils.INV_ITEM_COUNT[0])), GG.utils.INV_OR[1] + (GG.utils.INV_ITEM_SZ[1]*(position/GG.utils.INV_ITEM_COUNT[0]))
    """
    self.hframe =  ocempgui.widgets.HFrame()
    self.hframe.border = 1
    self.hframe.add_child(imgInventory)
    self.__frameInventory.add_child(self.hframe)
    """
    if position % 4 == 0:
      self.hframe =  ocempgui.widgets.HFrame()
      self.hframe.border = 0
      self.hframe.add_child(imgInventory)
      self.__frameInventory.add_child(self.hframe)
    else:
      self.hframe.add_child(imgInventory)
    
    """
    #metiendo la imagen en el inventory
    self.__frameInventory.add_child(imgInventory)
    """

    """
    #Pintando Sprites
    imgPath = os.path.join(GG.utils.DATA_PATH, spriteName)
    img = pygame.sprite.Sprite()
    img.image = pygame.image.load(imgPath).convert()
    img.rect = img.image.get_rect()
    img.rect.topleft = [GG.utils.INV_OR[0] + (GG.utils.INV_ITEM_SZ[0]*(position%GG.utils.INV_ITEM_COUNT[0])),
                        GG.utils.INV_OR[1] + (GG.utils.INV_ITEM_SZ[1]*(position/GG.utils.INV_ITEM_COUNT[0]))]
    self.getScreen().blit(img.image, img.rect)
    """
  
  def printLineOnChat(self, string):
    """ Prints a string on the HUD chat window.
    string: the info that will be printed on screen.
    """
    self.textArea.items.append(ocempgui.widgets.components.TextListItem(string))
    self.textArea.vscrollbar.increase()
    
  def chatMessageEntered(self):
    """ Prints a new message on chat window.
    """
    self.__player.getRoom().newChatMessage(self.__textField.text, self.__player)
    self.__textField.text = ""

  def chatAdded(self, event):
    """ Triggers after receiving a new chat message event.
    event: event info.
    """
    messageChat = event.getParams()['message']
    cad = messageChat.getHour()+" [" + messageChat.getSender() + "]: " + messageChat.getMessage()
    self.printLineOnChat(cad)
    
    
