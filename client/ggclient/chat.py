import ggmodel

class Chat(ggmodel.GGModel):
  """ Chat class.
  Defines all attributes and methods to handle the chat class.
  """
    
  def __init__(self):
    """ Class constructor.
    """
    ggmodel.GGModel.__init__(self, "Chat", 0)
    self.__chat = []
    