# -*- coding: iso-8859-15 -*-

import GG.model.room_item
import GG.model.golden_key
#import GG.model.pickable_item
import GG.isoview.isoview_item
import GG.model.chat_quiz

class GGPenguinQuiz(GG.model.room_item.GGRoomItem):
  """ GGPenguinQuiz class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label):
    """ Class builder.
    sprite: sprite used to paint the npc.
    position: penguin position.
    anchor: image anchor on screen.
    label: penguin's label
    """
    GG.model.room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor)
    self.label = label
    self.loadQuestion()
        
  def loadQuestion(self):        
    #self.__msgIntro = "Enhorabuena por conseguir llegar hasta aquí. Para finalizar el tutoria, deberás probar tu inteligencia con una sencilla pregunta."
    self.__msgQuestion = "¿De qué color era el caballo blanco de santiago?"
    self.__msgAnswers = []
    self.__msgAnswers.append("Verde")
    self.__msgAnswers.append("Amarillo con topos azules")
    self.__msgAnswers.append("Catorce")
    self.__msgAnswers.append("Blanco")
    self.__rightAnswer = 4
        
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talk"]
      
  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteName
  
  def getRightAnswer(self):
    return sefl.__rightAnswer
  
  def checkSimilarity(self, item):
    if GG.model.room_item.GGRoomItem.checkSimilarity(self, item):
      if item.label == self.label:
        return True
    return False   
  
  def createKey(self):
    return GG.model.golden_key.GGGoldenKey(GG.utils.KEY_SPRITE, "llave dorada", self.getPosition())
  
  def clickedBy(self, clicker):
    """ Triggers an event when the npc receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    

  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    self.getRoom().triggerEvent('quizAdded', message=GG.model.chat_quiz.ChatQuiz(self.__msgQuestion, self.__msgAnswers, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 3, self.__rightAnswer))
    