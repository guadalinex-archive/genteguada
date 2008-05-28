import os
import pygame
import GG.utils
import isoview
import isoview_inventoryitem
import ocempgui.widgets
import ocempgui.draw
import copy
import random

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
    self.__player.subscribeEvent('selectedItem', self.itemSelected)
    self.__player.subscribeEvent('unselectedItem', self.itemUnselected)
    self.__selectedItem = None
    self.buttonActions = {
        "inventory":{"image":"guardar.png", "action": self.itemToInventory,"button":None},
        "clone":{"image":"guardar.png", "action": self.itemToClone,"button":None},
        "push":{"image":"empujar.png", "action": self.itemToPush,"button":None},
        "up":{"image":"levantar.png", "action": self.itemToUp,"button":None},
        "talk":{"image":"sonido.png", "action": self.itemToTalk,"button":None},
        "exchange":{"image":"empujar.png", "action": self.exchangeItemPlayer,"button":None},
        "open":{"image":"sonido.png", "action": self.itemToOpen,"button":None}
    }
  
  def inventoryAdded(self, event):
    """ Adds a new isoview inventory item.
    item: new isoview inventory item.
    """
    item = event.getParams()["item"]
    invItem = isoview_inventoryitem.IsoViewInventoryItem(item, self.getScreen(), self)
    self.__isoviewInventory.append(invItem)
    self.paintItemOnInventory(invItem, len(self.__isoviewInventory) - 1)
    
  def inventoryRemoved(self, event):
    """ Removes an item from the inventory item list.
    item: item to be removed.
    """
    item = event.getParams()["item"]
    toBeRemoved = None
    for ivInventoryItem in self.__isoviewInventory:
      if ivInventoryItem.getModel() == item:
        toBeRemoved = ivInventoryItem
    if toBeRemoved:    
      GG.utils.playSound(GG.utils.SOUND_DROPITEM)
      self.__isoviewInventory.remove(toBeRemoved)
    self.paintItemsInventory()
    
  def draw(self):
    """ Updates the changed zones on the room view and draws the hud.
    """
    self.paintBackground()
    self.paintInventory()
    self.paintChat()
    self.paintTextBox()
    self.paintActionButtons()
    self.createItemActionButtons()

  def updateFrame(self):
    """ Updates all sprites for a new frame.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.updateFrame()
    pygame.display.update()

    #self.widgetContainer.update()
    #self.widgetContainer.set_screen(self.getScreen())
    #self.widgetContainer.set_screen(self.getScreen())

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
           
  # Paint methods
    
  def paintBackground(self):
    """ Paints the HUD background on screen.
    """
    img = pygame.sprite.Sprite()
    img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.INTERFACE_LOWER)).convert_alpha()
    img.rect = img.image.get_rect()
    img.rect.topleft = GG.utils.HUD_OR
    self.getScreen().blit(img.image, GG.utils.HUD_OR)
    pygame.display.update()
    # pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER1, (GG.utils.HUD_OR[0], GG.utils.HUD_OR[1], GG.utils.HUD_SZ[0] - 1, GG.utils.HUD_SZ[1] - 1))

  def paintChat(self):
    """ Paints the chat window on screen.
    """
    self.textArea = ocempgui.widgets.ScrolledWindow(GG.utils.CHAT_SZ[0], GG.utils.CHAT_SZ[1])
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
    self.windowInventory = ocempgui.widgets.ScrolledWindow(GG.utils.INV_SZ[0], GG.utils.INV_SZ[1] - 10)
    self.windowInventory.border = 1
    self.windowInventory.topleft = GG.utils.INV_OR[0], GG.utils.INV_OR[1] - 20
    self.widgetContainer.add_widget(self.windowInventory)
    self.paintItemsInventory()

  def paintItemsInventory(self):
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
    self.__player.clickOnInventoryItem(invIsoItem.getModel())

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
  
  def printLineOnChat(self, string):
    """ Prints a string on the HUD chat window.
    string: the info that will be printed on screen.
    """
    hframe = ocempgui.widgets.HFrame()
    hframe.border = 0
    
    imgPath = os.path.join(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.IMAGE_CHAT_MESSAGE))
    image = ocempgui.widgets.ImageLabel(imgPath)
    image.buttom = 0
    hframe.add_child(image)
    
    label = ocempgui.widgets.Label(string)
    label.set_style(ocempgui.widgets.WidgetStyle(self.getStyleMessageChat()))
    hframe.add_child(label)
    
    self.__layoutTextArea.add_child(hframe)
    self.textArea.vscrollbar.value = self.textArea.vscrollbar.maximum

  def getStyleMessageChat(self):
    #TODO entiendo que el color del chat depende de cada usuario 
    listStyle = ["chatEntryBlack","chatEntryRed","chatEntryGreen","chatEntryBlue"]
    return GG.utils.STYLES[listStyle[random.randint(0,len(listStyle)-1)]]

    
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

  def itemSelected(self,event):
    self.__selectedItem = event.getParams()['item'] 
    self.__isoviewRoom.itemSelected(self.__selectedItem)
    options = self.__selectedItem.getOptions()
    self.buttonBarActions = ocempgui.widgets.HFrame()
    if len(options) == 1:
      offset = 0
    else:
      offset = 3 + len(options) 
    #self.buttonBarActions.topleft = [GG.utils.SCREEN_SZ[0] - (GG.utils.ACTION_BUTTON_SZ[0]*len(options) - offset), \
    #                                 GG.utils.HUD_OR[1] - GG.utils.ACTION_BUTTON_SZ[1]]
    self.buttonBarActions.topleft = 0,0
    for action in options:
      self.buttonBarActions.add_child(self.buttonActions[action]["button"])
    self.widgetContainer.add_widget(self.buttonBarActions)
    #import time
    #time.sleep(2)
    #self.dropActionsItembuttons()

  
  def itemUnselected(self,event=None):
    if self.__selectedItem:
      self.__isoviewRoom.itemUnselected(self.__selectedItem)
      self.dropActionsItembuttons()

  #Defincion de la buttonBar y sus acciones permanentes

  def paintActionButtons(self):
    ACTIONS = [
                {"image":"vestidor.png", "action": self.showDresser},
                {"image":"derecha.png", "action": self.turnRight},
                {"image":"izquierda.png", "action": self.turnLeft},
                {"image":"herramientas.png", "action": self.showTools},
                {"image":"sonido.png", "action": self.showSoundControl},
                {"image":"ayuda.png", "action": self.showHelp},
              ]

    self.buttonBar = ocempgui.widgets.HFrame()
    self.buttonBar.topleft = [0,GG.utils.HUD_OR[1] - 80]
    self.widgetContainer.add_widget(self.buttonBar)
    for buttonData in ACTIONS:
      button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, buttonData['image']))
      button.border = 0
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, buttonData['action'])
      self.buttonBar.add_child(button)

  def showDresser(self):
    print "show dresser room"

  def turnRight(self):
    print "turn right"

  def turnLeft(self):
    print "turn left"

  def showTools(self):
    print "show tools"

  def showSoundControl(self):
    print "show sound control"

  def showHelp(self):
    print "show help"
    #TODO solo funciona en linux con las X, para e
    pygame.display.toggle_fullscreen()


  #definicion de las acciones y botones en funcion del item seleccionado
  
  def createItemActionButtons(self):
    for key in self.buttonActions.keys():
      button = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, self.buttonActions[key]['image']))
      button.border = 0
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.buttonActions[key]['action'])
      self.buttonActions[key]['button'] = button

  def dropActionsItembuttons(self):
    self.__selectedItem = None
    children = copy.copy(self.buttonBarActions.children)
    for child in children:
      self.buttonBarActions.remove_child(child)
    self.widgetContainer.remove_widget(self.buttonBarActions)

  def itemToInventory(self):
    self.__player.addInventory(self.__selectedItem)
    self.__selectedItem.getRoom().removeItem(self.__selectedItem)
    self.dropActionsItembuttons()
 
  def itemToClone(self):
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
    #print "talk"
    self.__player.talkTo(self.__selectedItem)
    self.itemUnselected()

  def exchangeItemPlayer(self):
    #print "intercambio"
    self.showExchangeWindow()

  def showExchangeWindow(self):
    window = ocempgui.widgets.VFrame()
    window.set_minimum_size(GG.utils.INV_SZ[0], GG.utils.INV_SZ[1])
    window.topleft = GG.utils.SCREEN_SZ[0] - 200, GG.utils.HUD_OR[1] - 200
    window.border = 1
    #self.buttonBarActions.topleft = [GG.utils.SCREEN_SZ[0] - (GG.utils.ACTION_BUTTON_SZ[0]*len(options) - offset), \
    #                                 GG.utils.HUD_OR[1] - GG.utils.ACTION_BUTTON_SZ[1]]
    self.widgetContainer.add_widget(window)

  def itemToOpen(self):
    #print "open"
    self.__player.open(self.__selectedItem)
    self.itemUnselected()
