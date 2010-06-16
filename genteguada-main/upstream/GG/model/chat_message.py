# -*- coding: utf-8 -*-

import os
import ggmodel
import time
import dMVC.model
import codecs

class ChatMessage(ggmodel.GGModel):
  """ ChatMessage class.
  Defines a chat message behaviour.
  """
     
  def __init__(self, message, sender, color, position, chatType):
    """ Class constructor.
    message: chat message.
    sender: player who sends the message.
    color: text color.
    position: on-screen chat message starting position.
    chatType: message type.
    """
    ggmodel.GGModel.__init__(self)
    self.__message = message
    self.__sender = sender
    self.__hour = time.time()
    self.__color = color
    self.position = position
    self.type = chatType
    
  def variablesToSerialize(self):
    """ Sets some class attributes as public access.
    """  
    return ['type', 'position']
    
  def getName(self):
    """ Returns the chat message.
    """
    return self.__message  
    
  def getMessage(self):
    """ Returns the chat message.
    """
    return self.__message

  def getSender(self):
    """ Returns the sender message label.
    """
    return self.__sender

  def getHour(self):
    """ Returns the hour that the message was sended at.
    """
    return time.strftime("%H:%M", time.localtime(self.__hour))

  def getColor(self):
    """ Returns the message color.
    """
    return self.__color

  def getPosition(self):
    """ On-screen chat message starting position.
    """
    return self.position

  def getType(self):
    """ Returns the chat message type.
    """  
    return self.type

  @dMVC.model.localMethod 
  def chatView(self, screen, isohud, message, header):
    """ Creates an isometric view object for the chat message.
    screen: screen handler.
    isohud: isohud handler.
    message: message text.
    header: chat message header.
    """
    import GG.isoview.isoview_chatmessage
    return GG.isoview.isoview_chatmessage.IsoViewChatMessage(self, screen, isohud, message, header)

# ===============================================================

class ChatQuiz(ChatMessage):
  """ ChatQuiz class.
  Defines a quiz message.
  """
     
  def __init__(self, parent, filePath, question, player, sender, color, position, chatType):
    """ Class constructor.
    parent: isohud handler.
    question: quiz question.
    player: asked player.
    sender: player who sends the message.
    color: text color.
    position: on-screen chat message starting position.
    chatType: message type.
    """
    self.__parent = parent
    self.question = question
    self.filePath = os.path.join(filePath,question)
    self.player = player
    self.__msgQuestion = ""
    self.__msgAnswers = []
    self.__rightAnswer = 0
    self.loadQuestion()
    ChatMessage.__init__(self, self.__msgQuestion, sender, color, position, chatType)
    
  def loadQuestion(self):
    """ Loads a quiz question from a file.
    """  
    quizFile = codecs.open(self.filePath, "r", "utf-8" )
    self.__msgQuestion = quizFile.readline()[:-1]
    self.__msgAnswers = []
    self.__msgAnswers.append(quizFile.readline()[:-1])
    self.__msgAnswers.append(quizFile.readline()[:-1])
    self.__msgAnswers.append(quizFile.readline()[:-1])
    answer = quizFile.readline()
    if answer.find("A") > -1:  
      self.__rightAnswer = 1
    elif answer.find("B") > -1:  
      self.__rightAnswer = 2
    else:  
      self.__rightAnswer = 3
    quizFile.close()
 
  def getInfoPackage(self):
    infoPackage = {}
    infoPackage["answers"] = self.getAnswers()
    infoPackage["position"] = self.getPosition()
    infoPackage["message"] = self.getMessage()
    return infoPackage

  def removeRightAnsweredQuestion(self):  
    """ Removes a question from the questions list.
    """
    self.__parent.removeRightQuestionForPlayer(self.question, self.player)  
    
  def getAnswers(self):
    """ Returns the quiz answers.
    """  
    return self.__msgAnswers

  def getRightAnswer(self):
    """ Returns the quiz right answer.
    """  
    return self.__rightAnswer
    
  @dMVC.model.localMethod 
  def chatView(self, screen, isohud):
    """ Creates an isometric view object for the chat message.
    screen: screen handler.
    isohud: isohud handler.
    """
    import GG.isoview.isoview_quiz
    return GG.isoview.isoview_quiz.IsoViewQuiz(self, screen, isohud)

    
