# -*- coding: iso-8859-15 -*-
import os
import random
import GG.model.room_item
import GG.model.chat_message

class GGPenguin(GG.model.room_item.GGRoomItem):
  """ GGPenguin class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label):
    """ Class builder.
    sprite: sprite used to paint the npc.
    position: penguin position.
    anchor: image anchor on screen.
    label: penguin's label
    """
    GG.model.room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor)
    self.label = label
        
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
  
  def checkSimilarity(self, item):
    if GG.model.room_item.GGRoomItem.checkSimilarity(self, item):
      if item.label == self.label:
        return True
    return False   
  
  def clickedBy(self, clicker):
    """ Triggers an event when the npc receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    

#================================================================================

class GGPenguinTalker(GGPenguin):
  """ GGPenguinTalker class.
  Defines a penguin talker object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label, message):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    position: penguin position.
    anchor: image anchor on screen.
    label: penguin's label
    """
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__msg = message

  def getMessage(self):
    return self.__msg

  def setMessage(self, msg):
    self.__msg = msg    

  def checkSimilarity(self, item):
    if GGPenguin.checkSimilarity(self, item):
      if item.__msg == self.__msg:
        return True
    return False   

  def getAdminActions(self):
    dic = {"Position": [self.getTile().position[0], self.getTile().position[2]], "Message": [self.__msg]}
    return dic  
  
  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    talker.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(self.__msg, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 3))

#================================================================================

class GGPenguinTrade(GGPenguin):
  """ GGPenguinTrade class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label, message, gift):
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__msg = message
    self.__giftLabel = gift

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talkAndGet"]

  def getAdminActions(self):
    dic = {"Position": [self.getTile().position[0], self.getTile().position[2]], "Message": [self.__msg], \
           "GiftLabel": [self.__giftLabel]}
    return dic  
  
  def checkSimilarity(self, item):
    if GGPenguin.checkSimilarity(self, item):
      if item.__msg == self.__msg:
        if item.__giftLabel == self.__giftLabel:  
          return True
    return False   

  def getMessage(self):
    return self.__msg

  def setMessage(self, msg):
    self.__msg = msg    

  def getGiftLabel(self):
    return self.__giftLabel

  def setGiftLabel(self, giftLabel):
    self.__giftLabel = giftLabel    

  def talkAndGet(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    giftItem = talker.getItemFromInventory(self.__giftLabel)
    if giftItem:
      talker.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(self.__msg, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
      talker.removeFromInventory(giftItem)
      return GG.model.generated_inventory_item.GGGeneratedInventoryItem("furniture/shirt.png", "Camiseta GenteGuada", self.anchor, self.getPosition())
    else:
      talker.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage("Si me trajeras un regalo, podría darte algo a cambio...", \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
      return None

#================================================================================
     
class GGPenguinQuiz(GGPenguin):
  """ GGPenguinQuiz class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label, filePath):
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__fileList = os.listdir(filePath)
    rmList = []
    for item in self.__fileList:
      if item.find(".") > -1 or item.find("~") > -1:
        rmList.append(item)  
    for item in rmList:
      self.__fileList.remove(item)    
    self.__availableQuestions = {}
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talk"]
      
  def getRightAnswer(self):
    return sefl.__rightAnswer
  
  def checkSimilarity(self, item):
    if GGPenguin.checkSimilarity(self, item):
      if item.__fileList == self.__fileList:
        return True
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
    talker.triggerEvent('quizAdded', message=GG.model.chat_message.ChatQuiz(self, fileName, self.__availableQuestions[name][question], talker, 'Andatuz',  
                                        GG.utils.TEXT_COLOR["black"], self.getPosition(), 3))   
        
#================================================================================
