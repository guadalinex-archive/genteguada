import ggmodel
import time
import dMVC.model
import GG.isoview.isoview_quiz
  
class ChatQuiz(chat_message.GGChatMessage):
  """ ChatQuiz class.
  Defines a book object behaviour.
  """
     
  def __init__(self, message, sender, color, position, type):
    """ Class constructor.
    message: chat message.
    sender: player who sends the message.
    color: text color.
    position: on-screen chat message starting position.
    """
    chat_message.GGChatMessage.__init__(self, message, sender, color, position, type)
    
  @dMVC.model.localMethod 
  def chatView(self, screen, isohud):
    """ Creates an isometric view object for the chat message.
    screen: screen handler.
    """
    return GG.isoview.isoview_quiz.IsoViewQuiz(self, screen, isohud)
  
  