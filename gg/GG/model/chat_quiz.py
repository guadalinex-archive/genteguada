import ggmodel
import time
import dMVC.model
import GG.model.chat_message
import GG.isoview.isoview_quiz
  
class ChatQuiz(GG.model.chat_message.ChatMessage):
  """ ChatQuiz class.
  """
     
  def __init__(self, message, answers, sender, color, position, type, rightAnswer):
    """ Class constructor.
    message: chat message.
    sender: player who sends the message.
    color: text color.
    position: on-screen chat message starting position.
    """
    GG.model.chat_message.ChatMessage.__init__(self, message, sender, color, position, type)
    self.__answers = answers
    self.__rightAnswer = rightAnswer
    
  def getAnswers(self):
    return self.__answers

  def getRightAnswer(self):
    return self.__rightAnswer
    
  @dMVC.model.localMethod 
  def chatView(self, screen, isohud):
    """ Creates an isometric view object for the chat message.
    screen: screen handler.
    """
    return GG.isoview.isoview_quiz.IsoViewQuiz(self, screen, isohud)
  
  