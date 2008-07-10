import ggmodel
import time
import dMVC.model
import GG.model.chat_message
import GG.isoview.isoview_quiz
  
class ChatQuiz(GG.model.chat_message.ChatMessage):
  """ ChatQuiz class.
  """
     
  #def __init__(self, message, answers, sender, color, position, type, rightAnswer):
  def __init__(self, parent, fileName, question, player, sender, color, position, type):
    """ Class constructor.
    message: chat message.
    sender: player who sends the message.
    color: text color.
    position: on-screen chat message starting position.
    """
    self.loadQuestion(question)
    GG.model.chat_message.ChatMessage.__init__(self, self.__msgQuestion, sender, color, position, type)
    self.__parent = parent
    self.question = question
    self.player = player
    
  def loadQuestion(self, question):
    #filePath = GG.genteguada.GenteGuada.getInstance().getDataPath(fileName)
    filePath = "gg/GG/data/questions/" + question
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
    return GG.isoview.isoview_quiz.IsoViewQuiz(self, screen, isohud)
  
  