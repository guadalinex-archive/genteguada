import ocempgui
import pygame
import random
import GG.utils
import isoview
import animation
import positioned_view

class IsoViewChatMessage(positioned_view.PositionedView):
  """ IsoViewChatMessage class.
  Defines a chat message view.
  """
  
  def __init__(self, model, screen, isohud):
    """ Class constructor.
    model: chat message model.
    screen: screen handler.
    isohud: isometric hud handler.
    """
    self.__isohud = isohud
    positioned_view.PositionedView.__init__(self, model, screen)
    self.style = self.getStyleMessageChat()
    self.label = GG.utils.OcempLabelNotTransparent(model.getMessage(),140)
    self.label.set_style(ocempgui.widgets.WidgetStyle(self.style["balloon"]))
    self.label.padding = 5
    self.label.set_minimum_size(150,50)
    self.label.opacity = 200
    
    self.balloon = self.drawBalloon(model.getMessage())
    
    pos = GG.utils.p3dToP2d(model.getPosition(), [0, 0])
    aux = self.balloon.topleft[0] + self.balloon.size[0]
    if (pos[0] + 10 + self.balloon.size[0]) > GG.utils.SCREEN_SZ[0]:
      xCord = GG.utils.SCREEN_SZ[0] - self.balloon.size[0]
    else:
      xCord = pos[0] + 10
    if (pos[1] - 30 - (self.label.height)) > 0:
      yCord = pos[1] - 30 - (self.balloon.height)  
    else:  
      yCord = 0
          
    self.balloon.topleft = [xCord, yCord]    
    self.balloon.zOrder = 20000
    self.__isohud.addSprite(self.balloon)
    
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("interface/chat/" + GG.utils.TAIL[model.type])  
    self.tail = GG.utils.OcempImageMapTransparent(imgPath)
    self.tail.topleft = [self.balloon.topleft[0] + 30, self.balloon.topleft[1] + self.balloon.size[1] - 10]
    self.tail.zOrder = 20002
    self.__isohud.addSprite(self.tail)
    
  def __del__(self):
    """ Class destructor.
    """  
    isoview.IsoView.__del__(self)
    
  def updateZOrder(self):
    """ Updates the zOrder value.
    """    
    self.label.zOrder = 20000  
    
  def getImg(self):
    """ Returns the chat balloon.
    """  
    return self.balloon
  
  def getTail(self):
    """ Returns the balloon tail.
    """  
    return self.tail  
  
  def getScreenPosition(self):
    """ Returns the balloon screen position.
    """
    return self.balloon.topleft
    
  def setScreenPosition(self, pos):
    """ Sets a new balloon screen position.
    """  
    self.balloon.topleft = pos
  
  def getStyleMessageChat(self):
    """ Returns the chat current style.
    """
    styles = {}
    styles["balloon"] = GG.utils.STYLES["chatBalloon" + GG.utils.CHAT_TYPE[self.getModel().type]]
    styles["entry"] = GG.utils.STYLES["chatEntry" + GG.utils.CHAT_TYPE[self.getModel().type]]
    return styles
  
  def drawBalloon(self, message):
    """ Draws a balloon containing a given message.
    message: message to be included on the balloon. 
    """  
    label = GG.utils.OcempLabelNotTransparent(message,140)
    label.set_style(ocempgui.widgets.WidgetStyle(self.style["balloon"]))
    label.padding = 5
    label.set_minimum_size(150,50)
    label.opacity = 200
    
    width = label.width
    height = label.height
    num = width/20 + 1
    num2 = height/20 + 1
    label.set_minimum_size((num)*20, (num2)*20)
    label.set_maximum_size((num)*20, (num2)*20)
    balloon = ocempgui.widgets.VFrame()
    balloon.border = 0
    balloon.padding = 0
    balloon.set_spacing(0)
    balloon.set_minimum_size((num+1)*20, (num2+1)*20)
    
    type = self.getModel().type
    topRow = ocempgui.widgets.HFrame()
    bottomRow = ocempgui.widgets.HFrame()  
    topRow.add_child(GG.utils.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/chat/" + GG.utils.CORNER_TOPLEFT[type])))
    bottomRow.add_child(GG.utils.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/chat/" + GG.utils.CORNER_BOTTOMLEFT[type])))
    for i in range(0, num):
      topRow.add_child(GG.utils.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/chat/" + GG.utils.BORDER_TOP[type])))
      bottomRow.add_child(GG.utils.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/chat/" + GG.utils.BORDER_BOTTOM[type])))
    topRow.add_child(GG.utils.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/chat/" + GG.utils.CORNER_TOPRIGHT[type])))
    bottomRow.add_child(GG.utils.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/chat/" + GG.utils.CORNER_BOTTOMRIGHT[type])))
    topRow.border = 0  
    topRow.padding = 0
    topRow.set_minimum_size((num+2)*20, 20)
    topRow.set_spacing(20)
    topRow.set_align(ocempgui.widgets.Constants.ALIGN_TOP)
    bottomRow.border = 0  
    bottomRow.padding = 0
    bottomRow.set_minimum_size((num+2)*20, 20)
    bottomRow.set_spacing(20)
    bottomRow.set_align(ocempgui.widgets.Constants.ALIGN_TOP)
    
    # *****
    
    middleRow = ocempgui.widgets.HFrame()
    midVerticalColumn1 = ocempgui.widgets.VFrame()
    midVerticalColumn2 = ocempgui.widgets.VFrame()
    for i in range(0, num2):
      midVerticalColumn1.add_child(GG.utils.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/chat/" + GG.utils.BORDER_LEFT[type])))
      midVerticalColumn2.add_child(GG.utils.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/chat/" + GG.utils.BORDER_RIGHT[type])))
    midVerticalColumn1.border = 0  
    midVerticalColumn1.padding = 0
    midVerticalColumn1.set_minimum_size(20, (num2)*20)
    midVerticalColumn1.set_spacing(20)
    midVerticalColumn1.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    midVerticalColumn2.border = 0  
    midVerticalColumn2.padding = 0
    midVerticalColumn2.set_minimum_size(20, (num2)*20)
    midVerticalColumn2.set_spacing(20)
    midVerticalColumn2.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    label.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    middleRow.border = 0  
    middleRow.padding = 0
    middleRow.add_child(midVerticalColumn1)
    middleRow.add_child(label)
    middleRow.add_child(midVerticalColumn2)
    middleRow.set_minimum_size((num+1)*20, (num2)*20)
    middleRow.set_spacing(0)
    middleRow.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    
    # *****
    
    balloon.add_child(topRow)
    balloon.add_child(middleRow)
    balloon.add_child(bottomRow)
    
    return balloon
      
  def draw(self):
    """ Draws a label containing a message.
    """  
    hframe = ocempgui.widgets.HFrame()
    hframe.border = 0
    hframe.set_align(ocempgui.widgets.Constants.ALIGN_TOP) 
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.IMAGE_CHAT_MESSAGE)
    image = ocempgui.widgets.ImageLabel(imgPath)
    image.buttom = 0
    hframe.add_child(image)
    string = self.getModel().getHour()+" [" + self.getModel().getSender() + "]: "
    label = GG.utils.OcempLabelNotTransparent(string,300)
    label.set_style(ocempgui.widgets.WidgetStyle(self.style["entry"]))
    hframe.add_child(label)
    label = GG.utils.OcempLabelNotTransparent(self.getModel().getMessage(),300)
    label.set_style(ocempgui.widgets.WidgetStyle(self.style["entry"]))
    hframe.add_child(label)
    return hframe
  