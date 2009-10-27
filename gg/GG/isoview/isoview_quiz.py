# -*- coding: utf-8 -*-

import time
import ocempgui
import GG.utils
import isoview
import positioned_view
import guiobjects
import os

class IsoViewQuiz(positioned_view.PositionedView):
  """ IsoViewQuiz class.
  Defines a quiz message view.
  """
  
  def __init__(self, model, screen, isohud):
    """ Class constructor.
    model: chat message model.
    screen: screen handler.
    isohud: isoview_hud handler.
    """
    self.__isohud = isohud
    infoPackage = model.getInfoPackage()
    self.__answers = infoPackage["answers"]
    self.__position = infoPackage["position"]
    
    positioned_view.PositionedView.__init__(self, model, screen)
    self.container = ocempgui.widgets.Box(585, 258)
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.BACKGROUNDS, "trivialWindow2.png"))
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0, 0
    self.container.add_child(imgBackground)
    
    label = guiobjects.OcempLabel(infoPackage["message"], guiobjects.STYLES["quizLabel"])
    label.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["quizLabel"]))
    label.topleft = 20, 40
    self.container.add_child(label)
    i = 0
    for answer in self.__answers:
      label = guiobjects.OcempLabel(answer, guiobjects.STYLES["quizLabel"])
      label.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["quizLabel"]))
      label.topleft = 80, 85 + i *50
      self.container.add_child(label)
      i = i + 1
    buttonA = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.HUD_PATH,"answerA.png")))
    buttonA.topleft = [22, 70]
    buttonA.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.actionButton, 1)
    buttonB = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.HUD_PATH,"answerB.png")))
    buttonB.topleft = [22, 120]
    buttonB.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.actionButton, 2)
    buttonC = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.HUD_PATH,"answerC.png")))
    buttonC.topleft = [22, 170]
    buttonC.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.actionButton, 3)
    self.container.add_child(buttonA)
    self.container.add_child(buttonB)
    self.container.add_child(buttonC)
    self.container.topleft = [20, 20]
    self.container.border = 0
    self.container.zOrder = 20000
    self.__isohud.addSprite(self.container)
    self.__isohud.widgetContainer.add_widget(self.container)
    self.__isohud.setActiveWindow(True)
    
  def __del__(self):
    """ Class destructor.
    """  
    isoview.IsoView.__del__(self)
    
  def actionButton(self, option):
    """ Processes the quiz answer.
    option: quiz answer.
    """ 
    header = time.strftime("%H:%M", time.localtime(time.time())) + " [Andatuz]: "
    if option == self.getModel().getRightAnswer():
      self.__isohud.newChatMessage(GG.model.chat_message.ChatMessage("!Respuesta correcta!", 'Andatuz', GG.utils.TEXT_COLOR["black"], self.__position, 2), "!Respuesta correcta!", header)
      self.getModel().removeRightAnsweredQuestion()
    else:   
      self.__isohud.newChatMessage(GG.model.chat_message.ChatMessage("Respuesta incorrecta", 'Andatuz', GG.utils.TEXT_COLOR["black"], self.__position, 2), "Respuesta incorrecta", header)
    self.__isohud.widgetContainer.remove_widget(self.container)
    self.__isohud.setActiveWindow(False)
    self.container.destroy()
    
  def updateZOrder(self):
    """ Updates the quiz window zOrder attribute with a new value.
    """    
    self.container.zOrder = 20000  
    
  def getImg(self):
    """ Returns the quiz window.
    """  
    return self.container
    
  def getScreenPosition(self):
    """ Returns the quiz window screen position.
    """  
    return self.container.topleft
    
  def setScreenPosition(self, pos):
    """ Sets a new value for the quiz window screen position.
    pos: new position value. 
    """   
    self.container.topleft = pos
  
