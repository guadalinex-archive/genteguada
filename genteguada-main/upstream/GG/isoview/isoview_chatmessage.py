 # -*- coding: utf-8 -*- 

import os
import ocempgui
import GG.utils
import isoview
import positioned_view
import guiobjects

# ======================= CONSTANTS ===========================
CHAT_PATH = os.path.join(GG.utils.INTERFACE_PATH,"chat")

BALLOON_OPACITY = 210
# Message types --> 0: general; 1: private; 2: npcs; 3: system)
CHAT_TYPE = {0: "White", 1: "Red", 2: "Green", 3: "Blue"}
# Chat balloon pieces.
CORNER_TOPLEFT = {0: "corner_topleft_white.png", 1: "corner_topleft_red.png", 2: "corner_topleft_green.png", 3: "corner_topleft_blue.png"}
CORNER_TOPRIGHT = {0: "corner_topright_white.png", 1: "corner_topright_red.png", 2: "corner_topright_green.png", 3: "corner_topright_blue.png"}
CORNER_BOTTOMLEFT = {0: "corner_bottomleft_white.png", 1: "corner_bottomleft_red.png", 2: "corner_bottomleft_green.png", 3: "corner_bottomleft_blue.png"}
CORNER_BOTTOMRIGHT = {0: "corner_bottomright_white.png", 1: "corner_bottomright_red.png", 2: "corner_bottomright_green.png", 3: "corner_bottomright_blue.png"}
BORDER_TOP = {0: "border_top_white.png", 1: "border_top_red.png", 2: "border_top_green.png", 3: "border_top_blue.png"}
BORDER_LEFT = {0: "border_left_white.png", 1: "border_left_red.png", 2: "border_left_green.png", 3: "border_left_blue.png"}
BORDER_RIGHT = {0: "border_right_white.png", 1: "border_right_red.png", 2: "border_right_green.png", 3: "border_right_blue.png"}
BORDER_BOTTOM = {0: "border_bottom_white.png", 1: "border_bottom_red.png", 2: "border_bottom_green.png", 3: "border_bottom_blue.png"}
TAIL = {0: "tail_white.png", 1: "tail_red.png", 2: "tail_green.png", 3: "tail_blue.png"}
# ==============================================================

class IsoViewChatMessage(positioned_view.PositionedView):
  """ IsoViewChatMessage class.
  Defines a chat message view.
  """
  
  def __init__(self, model, screen, isohud, message, header):
    """ Class constructor.
    model: chat message model.
    screen: screen handler.
    isohud: isometric hud handler.
    """
    self.__isohud = isohud
    self.__message = message
    self.__header = header
    self.position = model.position
    positioned_view.PositionedView.__init__(self, model, screen)
    self.style = self.getStyleMessageChat()
    self.label = guiobjects.OcempLabelNotTransparent(message, 140)
    self.label.set_style(ocempgui.widgets.WidgetStyle(self.style["balloon"]))
    self.label.padding = 5
    self.label.set_minimum_size(150, 50)
    self.balloon = self.drawBalloon(message)
    if model.type != 3:
      pos = GG.utils.p3dToP2d(self.position, [0, 0])
      if (pos[0] + 10 + self.balloon.size[0]) > GG.utils.SCREEN_SZ[0]:
        xCord = GG.utils.SCREEN_SZ[0] - self.balloon.size[0]
      else:
        xCord = pos[0] + 10
      if (pos[1] - 30 - (self.label.height)) > 0:
        yCord = pos[1] - 30 - (self.balloon.height)  
      else:  
        yCord = 0
      self.balloon.topleft = [xCord, yCord]
    else:      
      self.balloon.topleft = [GG.utils.SCREEN_SZ[0]/2 - (self.balloon.size[0]/2), GG.utils.SCREEN_SZ[1]/3]
    self.balloon.zOrder = 20000
    self.__isohud.addSprite(self.balloon)
    if model.type != 3:
      imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(CHAT_PATH, TAIL[model.type]))  
      self.tail = guiobjects.OcempImageMapTransparent(imgPath)
      self.tail.topleft = [self.balloon.topleft[0] + 30, self.balloon.topleft[1] + self.balloon.size[1] - 5]
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
    styles["balloon"] = guiobjects.STYLES["chatBalloon" + CHAT_TYPE[self.getModel().type]]
    styles["entry"] = guiobjects.STYLES["chatEntry" + CHAT_TYPE[self.getModel().type]]
    return styles
  
  def drawBalloon(self, message):
    """ Draws a balloon containing a given message.
    message: message to be included on the balloon. 
    """  
    label = guiobjects.OcempLabelNotTransparent(message, 140)
    label.set_style(ocempgui.widgets.WidgetStyle(self.style["balloon"]))
    label.padding = 5
    label.set_minimum_size(100, 30)
    label.opacity = 200
    
    width = label.width
    height = label.height
    num = width/10 + 1
    num2 = height/10 + 1
    label.set_minimum_size((num)*10, (num2)*10)
    label.set_maximum_size((num)*10, (num2)*10)
    balloon = ocempgui.widgets.VFrame()
    balloon.border = 0
    balloon.padding = 0
    balloon.set_spacing(0)
    balloon.set_minimum_size((num+1)*10, (num2+1)*10)
    
    modelType = self.getModel().type
    topRow = ocempgui.widgets.HFrame()
    bottomRow = ocempgui.widgets.HFrame()  

    topRow.add_child(guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(CHAT_PATH, CORNER_TOPLEFT[modelType]))))
    bottomRow.add_child(guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(CHAT_PATH, CORNER_BOTTOMLEFT[modelType]))))
    for i in range(0, num):
      topRow.add_child(guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(CHAT_PATH, BORDER_TOP[modelType]))))
      bottomRow.add_child(guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(CHAT_PATH, BORDER_BOTTOM[modelType]))))
    topRow.add_child(guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(CHAT_PATH, CORNER_TOPRIGHT[modelType]))))
    bottomRow.add_child(guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(CHAT_PATH, CORNER_BOTTOMRIGHT[modelType]))))
    topRow.border = 0  
    topRow.padding = 0
    topRow.set_minimum_size((num+2)*10, 10)
    topRow.set_spacing(10)
    topRow.set_align(ocempgui.widgets.Constants.ALIGN_TOP)
    bottomRow.border = 0  
    bottomRow.padding = 0
    bottomRow.set_minimum_size((num+2)*10, 10)
    bottomRow.set_spacing(10)
    bottomRow.set_align(ocempgui.widgets.Constants.ALIGN_TOP)
        
    # *****
    
    middleRow = ocempgui.widgets.HFrame()
    midVerticalColumn1 = ocempgui.widgets.VFrame()
    midVerticalColumn2 = ocempgui.widgets.VFrame()
    for i in range(0, num2):
      midVerticalColumn1.add_child(guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(CHAT_PATH, BORDER_LEFT[modelType]))))
      midVerticalColumn2.add_child(guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(CHAT_PATH, BORDER_RIGHT[modelType]))))
    midVerticalColumn1.border = 0  
    midVerticalColumn1.padding = 0
    midVerticalColumn1.set_minimum_size(10, (num2)*10)
    midVerticalColumn1.set_spacing(10)
    midVerticalColumn1.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    midVerticalColumn2.border = 0  
    midVerticalColumn2.padding = 0
    midVerticalColumn2.set_minimum_size(10, (num2)*10)
    midVerticalColumn2.set_spacing(10)
    midVerticalColumn2.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    label.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    middleRow.border = 0  
    middleRow.padding = 0
    middleRow.add_child(midVerticalColumn1)
    middleRow.add_child(label)
    middleRow.add_child(midVerticalColumn2)
    middleRow.set_minimum_size((num+1)*10, (num2)*10)
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
    #string = self.getModel().getHour()+" [" + self.getModel().getSender() + "]: "
    label = guiobjects.OcempLabelNotTransparent(self.__header, 200)
    label.set_style(ocempgui.widgets.WidgetStyle(self.style["entry"]))
    hframe.add_child(label)
    label = guiobjects.OcempLabelNotTransparent(self.__message, 200)
    label.set_style(ocempgui.widgets.WidgetStyle(self.style["entry"]))
    hframe.add_child(label)
    return hframe
  
