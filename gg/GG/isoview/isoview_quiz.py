import ocempgui
import pygame
import random
import GG.utils
import isoview
import animation
import positioned_view

class IsoViewQuiz(positioned_view.PositionedView):
  """ IsoViewQuiz class.
  Defines a chat message view.
  """
  
  def __init__(self, model, screen, isohud):
    """ Class constructor.
    model: chat message model.
    screen: screen handler.
    """
    self.__isohud = isohud
    self.__answers = model.getAnswers()
    
    positioned_view.PositionedView.__init__(self, model, screen)
    self.container = ocempgui.widgets.VFrame()
    
    self.container.add_child(GG.utils.OcempLabel(model.getMessage() ,140))
    for answer in self.__answers:
      self.container.add_child(GG.utils.OcempLabel(answer ,140))
    self.buttonBar = ocempgui.widgets.HFrame()
    
    i = 1
    for answer in self.__answers:
      button = ocempgui.widgets.ImageButton(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/hud/4.png"))
      button.border = 0
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.actionButton, i)
      i += 1
      self.buttonBar.add_child(button)
    self.buttonBar.border = 0
      
    self.container.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.container.add_child(self.buttonBar)
    self.container.topleft = [20, 20]
    self.container.border = 0
    self.__isohud.getIsoviewRoom().addTopSprite(self.container)
    self.__isohud.widgetContainer.add_widget(self.container)
    
  def actionButton(self, option):
    print option
    if option == self.getModel().getRightAnswer():
      self.__isohud.getIsoviewRoom().getModel().triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage("Respuesta correcta: Has ganado 20 puntos", \
                'Andatuz', GG.utils.TEXT_COLOR["black"], [3, 0, 1], 2))
      self.__isohud.getPlayer().addPoints(20, "Penguin Quiz")
    else:   
      self.__isohud.getIsoviewRoom().getModel().triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage("Respuesta incorrecta", \
                'Andatuz', GG.utils.TEXT_COLOR["black"], [3, 0, 1], 2))
    self.__isohud.widgetContainer.remove_widget(self.container)
    self.__isohud.getIsoviewRoom().removeTopSprite(self.container)
    self.container.destroy()
    
  def __del__(self):
    isoview.IsoView.__del__(self)
    
  def getImg(self):
    return self.container
    #return self.__img
  
  def getScreenPosition(self):
    return self.container.topleft
    #return self.__img.rect.topleft

  def setScreenPosition(self, pos):
    self.container.topleft = pos
  