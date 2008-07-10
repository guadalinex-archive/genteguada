# -*- coding: iso-8859-15 -*-

import GG.model.room_item
import GG.model.golden_key
#import GG.model.pickable_item
import GG.isoview.isoview_item
import GG.model.chat_quiz
import random
import GG.utils

class GGPenguinQuiz(GG.model.room_item.GGRoomItem):
  """ GGPenguinQuiz class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label, fileList):
    """ Class builder.
    sprite: sprite used to paint the npc.
    position: penguin position.
    anchor: image anchor on screen.
    label: penguin's label
    """
    GG.model.room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor)
    self.label = label
    self.__fileList = fileList
    self.__availableQuestions = {}
    #self.loadQuestion()
    
  """      
  def loadQuestion(self):
    question = random.randint(0,len(self.__fileList)-1)   
    fileName = "questions/" + self.__fileList[question]  
    #filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(fileName)
    filePath = "gg/GG/data/questions/q1"
    f = open(filePath)
    self.__msgQuestion = f.readline()
    self.__msgAnswers = []
    self.__msgAnswers.append(f.readline())
    self.__msgAnswers.append(f.readline())
    self.__msgAnswers.append(f.readline())
    answer = f.readline()
    if answer == "A":  self.__rightAnswer = 1
    elif answer == "B":  self.__rightAnswer = 2
    elif answer == "C":  self.__rightAnswer = 2
    f.close()
  """

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

  def removeRightQuestionForPlayer(self, question, player):
    name = player.getName()
    self.__availableQuestions[name].remove(question)
    if len(self.__availableQuestions[name]) == 0:
      player.addPoints(0, "Penguin Quiz")
      
  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    name = talker.getName()
    if not name in self.__availableQuestions.keys():
      self.__availableQuestions[name] = self.__fileList  
    if len(self.__availableQuestions[name]) == 0:
      talker.newChatMessage("Ya no tengo preguntas que hacerte", 2)
      return  
    question = random.randint(0,len(self.__availableQuestions[name])-1)
    fileName = "questions/" + self.__availableQuestions[name][question]
    print "==============================="
    print self.__availableQuestions[name][question]
    print fileName
    print "==============================="
    talker.triggerEvent('quizAdded', message=GG.model.chat_quiz.ChatQuiz(self, fileName, self.__availableQuestions[name][question], talker, 'Andatuz',  
                                        GG.utils.TEXT_COLOR["black"], self.getPosition(), 3))
