

class PrivateContact:
  
  def __init__(self, player):
    self.__player = player
    self.__chat = []
    
  def getPlayer(self):
    return self.__player

  def getChat(self):
    return self.__chat

  def addChatLine(self, line):
    self.__chat.append(line)

  def clearChat(self):
    self.__chat = []