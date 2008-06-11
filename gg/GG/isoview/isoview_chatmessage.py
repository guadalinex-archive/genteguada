import ocempgui
import pygame
import random
import GG.utils
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
    """
    self.__isohud = isohud
    positioned_view.PositionedView.__init__(self, model, screen)
    self.label = GG.utils.OcempLabel(model.getMessage(),300)
    pos = GG.utils.p3dToP2d(model.getPosition(), [0, 0])
    self.label.topleft = [pos[0] + 40, pos[1] - 30]
    self.__isohud.getIsoviewRoom().addTopSprite(self.label)
    
  def getImg(self):
    return self.label
    #return self.__img
  
  def getScreenPosition(self):
    return self.label.topleft
    #return self.__img.rect.topleft

  def setScreenPosition(self, pos):
    self.label.topleft = pos
  
  def getStyleMessageChat(self):
    """ Returns the chat current style.
    """
    #TODO entiendo que el color del chat depende de cada usuario 
    listStyle = ["chatEntryBlack","chatEntryRed","chatEntryGreen","chatEntryBlue"]
    return GG.utils.STYLES[listStyle[random.randint(0,len(listStyle)-1)]]
  
  def draw(self):
    hframe = ocempgui.widgets.HFrame()
    hframe.border = 0
    hframe.set_align(ocempgui.widgets.Constants.ALIGN_TOP) 
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.IMAGE_CHAT_MESSAGE)
    image = ocempgui.widgets.ImageLabel(imgPath)
    image.buttom = 0
    hframe.add_child(image)
    style = self.getStyleMessageChat()
    string = self.getModel().getHour()+" [" + self.getModel().getSender() + "]: "
    label = GG.utils.OcempLabel(string,300)
    label.set_style(ocempgui.widgets.WidgetStyle(style))
    hframe.add_child(label)
    label = GG.utils.OcempLabel(self.getModel().getMessage(),300)
    label.set_style(ocempgui.widgets.WidgetStyle(style))
    hframe.add_child(label)
    return hframe
