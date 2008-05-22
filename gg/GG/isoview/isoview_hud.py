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
    self.__player.subscribeEvent('selectedItem', self.itemSelected)
    self.__player.subscribeEvent('unselectedItem', self.itemUnselected)
    self.itemSelected = None

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
    self.paintActionsButtons()
    
  def updateFrame(self):
    """ Updates all sprites for a new frame.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.updateFrame()
    #self.paintUpperPannel()
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
           
  # Paint methods
    
  def paintBackground(self):
    """ Paints the HUD background on screen.
    """
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER1,
              (GG.utils.HUD_OR[0], GG.utils.HUD_OR[1], GG.utils.HUD_SZ[0] - 1, GG.utils.HUD_SZ[1] - 1))

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
    self.windowInventory = ocempgui.widgets.ScrolledWindow(GG.utils.INV_SZ[0], GG.utils.INV_SZ[1])
    self.windowInventory.border = 1
    self.windowInventory.topleft = GG.utils.INV_OR[0], GG.utils.INV_OR[1]
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

  def paintUpperPannel(self):
    #pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER1,
    #          (GG.utils.UPPERPANNEL_OR[0], GG.utils.UPPERPANNEL_OR[1], GG.utils.UPPERPANNEL_SZ[0] - 1, GG.utils.UPPERPANNEL_SZ[1] - 1))
    pass
    
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
    

  def itemSelected(self,event):
    self.itemSelected = event.getParams()['item'] 
    self.__isoviewRoom.itemSelected(self.itemSelected)
    self.botomInventario = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, "guardar.png"))
    self.botomInventario.border = 0
    self.botomInventario.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.guardarInventario)
    self.botonera.add_child(self.botomInventario)

  def guardarInventario(self):
    self.__player.addInventory(self.itemSelected)
    self.itemSelected.getRoom().removeItem(self.itemSelected)
    #print "al inventario"

    
  def itemUnselected(self,event):
    if self.itemSelected:
      self.__isoviewRoom.itemUnselected(self.itemSelected)
      self.itemSelected = None
      self.botonera.remove_child(self.botomInventario)

  def paintActionsButtons(self):
    ACTIONS = [
                {"image":"vestidor.png", "action": self.mostrarVestidor},
                {"image":"derecha.png", "action": self.rotarDerecha},
                {"image":"izquierda.png", "action": self.rotarIzquierda},
                {"image":"herramientas.png", "action": self.mostrarHerramientas},
                {"image":"sonido.png", "action": self.mostrarBarraSonido},
                {"image":"ayuda.png", "action": self.mostrarAyuda},
              ]

    self.botonera = ocempgui.widgets.HFrame()
    self.botonera.topleft = [0,GG.utils.HUD_OR[1] - 80]
    self.widgetContainer.add_widget(self.botonera)
    for buttonData in ACTIONS:
      buttom = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, buttonData['image']))
      buttom.border = 0
      buttom.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, buttonData['action'])
      self.botonera.add_child(buttom)

  def mostrarVestidor(self):
    print "vestidor"

  def rotarDerecha(self):
    print "rotar derecha"

  def rotarIzquierda(self):
    print "rotar izquierda"

  def mostrarHerramientas(self):
    print "mostrar herramienta"

  def mostrarBarraSonido(self):
    print "mostrar la barra de sonido"

  def mostrarAyuda(self):
    print "mostrar ayuda"


