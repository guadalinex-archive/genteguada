import ggmodel
import time
import dMVC.model

class ChatMessage(ggmodel.GGModel):
  """ ChatMessage class.
  Defines a chat message behaviour.
  """
     
  def __init__(self, message, sender, color, position, type):
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
    self.type = type
    self.imagePath = ""
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['imagePath', 'type']
    
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
     
  def __init__(self, parent, fileName, question, player, sender, color, position, type):
    self.loadQuestion(question)
    ChatMessage.__init__(self, self.__msgQuestion, sender, color, position, type)
    self.__parent = parent
    self.question = question
    self.player = player
    
  def loadQuestion(self, question):
    filePath = "gg/GG/data/questions/" + question
    f = open(filePath)
    self.__msgQuestion = unicode(f.readline(), "utf-8")[:-1]
    print self.__msgQuestion.__class__    
    self.__msgAnswers = []
    self.__msgAnswers.append(unicode(f.readline())[:-1])
    self.__msgAnswers.append(unicode(f.readline())[:-1])
    self.__msgAnswers.append(unicode(f.readline())[:-1])
    answer = f.readline()
    if answer == "A":  self.__rightAnswer = 1
    elif answer == "B":  self.__rightAnswer = 2
    elif answer == "C":  self.__rightAnswer = 2
    f.close()
  
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
    
