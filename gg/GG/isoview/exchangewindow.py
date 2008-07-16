import ocempgui.widgets
import GG.utils

class ExchangeWindow:

  def __init__(self, isohud, step, listIn):
    self.window = ocempgui.widgets.DialogWindow("Ventana de intercambio")
    self.window.topleft = 200, 200

    self.container = ocempgui.widgets.Box(585,258)
    self.window.zOrder = 10000
    
    self.window.child = self.container

    self.__listIn = listIn
    self.__listOut = []
    self.__step = step
    self.__isohud = isohud

  def draw(self):
    self.__paintBackground()
    self.__paintOutBox()
    self.__paintInBox()
    self.__paintLabel()
    self.__paintButtons()
    if len(self.__listIn):
      self.__paintListItems()

  def __paintBackground(self):
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/exchangeWindow.png")
    imgBackground = GG.utils.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0,0
    self.container.add_child(imgBackground)

  def __paintOutBox(self):
    self.__outBox = ocempgui.widgets.ScrolledWindow(190, 163)
    self.__outBox.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["inventoryArea"]))
    self.__outBox.border = 1
    self.__outBox.topleft = 20, 80
    self.__outBoxChild = ocempgui.widgets.VFrame()
    self.__outBoxChild.border = 0
    self.__outBoxChild.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.__outBox.child = self.__outBoxChild
    self.__hFrameOutBox = None
    self.container.add_child(self.__outBox)

  def __paintInBox(self):
    self.__inBox = ocempgui.widgets.ScrolledWindow(190, 163)
    self.__inBox.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["inventoryArea"]))
    self.__inBox.border = 1
    self.__inBox.topleft = 370, 80
    self.__inBoxChild = ocempgui.widgets.VFrame()
    self.__inBoxChild.border = 0
    self.__inBoxChild.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.__inBox.child = self.__inBoxChild
    self.__hFrameInBox = None
    self.container.add_child(self.__inBox)

  def __paintLabel(self):
    self.__labelExchange = GG.utils.LabelTransparent("Selecciona los objetos del inventario que quieres intercambiar.",GG.utils.STYLES["dialogFont"])
    self.__labelExchange.topleft = 20,20
    self.container.add_child(self.__labelExchange)
    
    self.__labelExchange = GG.utils.LabelTransparent("Bandeja de salida",GG.utils.STYLES["dialogFont"])
    self.__labelExchange.topleft = 20,60
    self.container.add_child(self.__labelExchange)
    
    self.__labelExchange = GG.utils.LabelTransparent("Bandeja de entrada",GG.utils.STYLES["dialogFont"])
    self.__labelExchange.topleft = 370,60
    self.container.add_child(self.__labelExchange)

  def __paintButtons(self):
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/editor/ok_button.png")
    buttonOK = GG.utils.OcempImageButtonTransparent(filePath)
    buttonOK.topleft = 240,100
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.okExchange)
    self.container.add_child(buttonOK)
     
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/editor/cancel_button.png")
    buttonCancel = GG.utils.OcempImageButtonTransparent(filePath)
    buttonCancel.topleft = 240, 180
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.koExchange)
    self.container.add_child(buttonCancel)

  def okExchange(self):
    if self.__step == 1:
      if len(self.__listOut) == 0:
        self.__labelExchange.set_text("Deberia de seleccionar algun elemento del inventario")
      else:
        self.__isohud.getPlayer().acceptExchangeTo(self.__step, self.__listOut)
        self.__labelExchange.set_text("Espere a que el otro usuario nos envie el intercambio")
        self.__step = 3

    elif self.__step == 2:
      self.__isohud.getPlayer().acceptExchangeTo(self.__step, self.__listOut)
      self.__labelExchange.set_text("Espere a que el otro usuario acepte el intercambio")
      self.__step = 4

    elif self.__step == 3 or self.__step == 4:
      return

    elif self.__step == 5:
      self.__isohud.getPlayer().finishExchange(self.__listIn, self.__listOut)

  def koExchange(self):
    self.__isohud.getPlayer().cancelExchangeTo(self.__step)

  def __paintListItems(self):
    i = 0
    for item in self.__listIn:
      self.__hFrameInBox = self.__paintItemOnList(self.__hFrameInBox, self.__inBoxChild, item, i)
      i+=1

  def addItemOut(self, item):
    self.__listOut.append(item)
    self.__hFrameOutBox = self.__paintItemOnList(self.__hFrameOutBox, self.__outBoxChild, item, len(self.__listIn) - 1)

  def addInList(self, list):
    self.__listIn = list
    self.__paintListItems()
    self.__labelExchange.set_text("Acepte para finalizar el intercambio !!!")
    self.__step = 5

  def __paintItemOnList(self, hframe, boxChild, item, position):
    img = ocempgui.widgets.ImageButton(GG.genteguada.GenteGuada.getInstance().getDataPath(item.spriteInventory))
    img.border = 0
    if position % GG.utils.INV_ITEM_COUNT[0] == 0 or hframe is None:
      hframe =  ocempgui.widgets.HFrame()
      hframe.border = 0
      hframe.add_child(img)
      boxChild.add_child(hframe)
    else:
      hframe.add_child(img)
    return hframe
