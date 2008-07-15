import ggmodel

class PrivateContact(ggmodel.GGModel):
  
  def __init__(self, player):
    ggmodel.GGModel.__init__(self)
    self.__player = player
    self.__chat = []
    
  def getPlayer(self):
    return self.__player

  def getChat(self):
    return self.__chat

  def addChatLine(self, player, line):
    self.__chat.append([player, line])

  def clearChat(self):
    self.__chat = []
