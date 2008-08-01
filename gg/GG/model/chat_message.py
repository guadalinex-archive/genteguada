import ggmodel
import time
import GG.utils
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
    """
    ggmodel.GGModel.__init__(self)
    self.__message = message
    self.__sender = sender
    self.__hour = time.time()
    self.__color = color
    self.__position = position
    self.type = chatType
    self.imagePath = ""
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['imagePath', 'type']
    
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
    return self.__position

  def getType(self):
    return self.type

  @dMVC.model.localMethod 
  def chatView(self, screen, isohud):
    """ Creates an isometric view object for the chat message.
    screen: screen handler.
    """
    import GG.isoview.isoview_chatmessage
    return GG.isoview.isoview_chatmessage.IsoViewChatMessage(self, screen, isohud)

#================================================================================

class ChatQuiz(ChatMessage):
  """ ChatQuiz class.
  """
     
  def __init__(self, parent, question, player, sender, color, position, chatType):
    self.__parent = parent
    self.question = question
    self.player = player
    self.__msgQuestion = ""
    self.__msgAnswers = []
    self.__rightAnswer = 0
    self.loadQuestion()
    ChatMessage.__init__(self, self.__msgQuestion, sender, color, position, chatType)
    
  def loadQuestion(self):
    filePath = "gg/GG/data/questions/" + self.question
    quizFile = codecs.open(filePath, "r", "utf-8" )
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
  
  def removeRightAnsweredQuestion(self):  
    self.__parent.removeRightQuestionForPlayer(self.question, self.player)  
    
  def getAnswers(self):
    return self.__msgAnswers

  def getRightAnswer(self):
    return self.__rightAnswer
    
  @dMVC.model.localMethod 
  def chatView(self, screen, isohud):
    """ Creates an isometric view object for the chat message.
    screen: screen handler.
    """
    import GG.isoview.isoview_quiz
    return GG.isoview.isoview_quiz.IsoViewQuiz(self, screen, isohud)

#================================================================================
    
