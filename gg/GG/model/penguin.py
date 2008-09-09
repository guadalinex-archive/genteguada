# -*- coding: utf-8 -*-

import os
import random
import room_item
import chat_message
import GG.utils
import generated_inventory_item

class GGPenguin(room_item.GGRoomItem):
  """ GGPenguin class.
  Defines a penguin object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    anchor: image anchor on screen.
    topAnchor: image top anchor on screen.
    label: penguin's label.
    """
    room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor)
    self.label = label

  def copyObject(self):
    return GGPenguin(self.spriteName, self.anchor, self.topAnchor, self.label)
        
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talk", "jumpOver"]

  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    dic = {"Position": self.getPosition(), "Label": [self.label]}
    return dic    
      
  def getName(self):
    """ Returns the item's label.
    """  
    return self.label
  
  def getImageLabel(self):
    """ Returns the item's image filename.
    """  
    return self.spriteName

  def setLabel(self, newLabel):
    """ Sets a new label for the item.
    """  
    self.label = newLabel  

  def clickedBy(self, clicker):
    """ Triggers an event when the penguin receives a click by a player.
    clicker: player who clicks.
    """
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    

# ===============================================================

class GGPenguinTalker(GGPenguin):
  """ GGPenguinTalker class.
  Defines a talker penguin object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label, message):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    anchor: image anchor on screen.
    topAnchor: image top anchor on screen.
    label: penguin's label.
    message: penguin's message.
    """
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__msg = message

  def copyObject(self):
    return GGPenguinTalker(self.spriteName, self.anchor, self.topAnchor, self.label, self.__msg)
    
  def getMessage(self):
    """ Returns the penguin's message.
    """  
    return self.__msg

  def setMessage(self, msg):
    """ Sets a new penguin message.
    """  
    self.__msg = msg    

  def getAdminActions(self):
    """ Returns the possible admin actions on this item.
    """  
    dic = {"Position": self.getTile().position, "Message": [self.__msg], "Label": [self.label]}
    return dic  
  
  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    talker.triggerEvent('chatAdded', message=chat_message.ChatMessage(self.__msg, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))

# ===============================================================

class GGPenguinTrade(GGPenguin):
  """ GGPenguinTrade class.
  Defines a trade penguin behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label, message, gift):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    anchor: image anchor on screen.
    topAnchor: image top anchor on screen.
    label: penguin's label
    message: penguin's message.
    gift: item the penguin will ask the player for.
    """
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__msg = message
    self.__giftLabel = gift

  def copyObject(self):
    return GGPenguinTrade(self.spriteName, self.anchor, self.topAnchor, self.label, self.__msg, self.__giftLabel)

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talkAndGet", "jumpOver"]

  def getAdminActions(self):
    """ Returns the possible admin actions on this item.
    """  
    dic = {"Position": self.getTile().position, "Message": [self.__msg], "GiftLabel": [self.__giftLabel], "Label": [self.label]}
    return dic  

  def getMessage(self):
    """ Returns the message.
    """  
    return self.__msg

  def setMessage(self, msg):
    """ Sets a new message.
    msg: new message.
    """  
    self.__msg = msg    

  def getGiftLabel(self):
    """ Returns the gift's label.
    """  
    return self.__giftLabel

  def setGiftLabel(self, giftLabel):
    """ Sets a new gift's label.
    """  
    self.__giftLabel = giftLabel    

  def talkAndGet(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    giftItem = talker.getItemFromInventory(self.__giftLabel)
    if giftItem:
      talker.triggerEvent('chatAdded', message=chat_message.ChatMessage(self.__msg, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
      talker.removeFromInventory(giftItem)
      return generated_inventory_item.GGGeneratedInventoryItem("furniture/shirt.png", "Camiseta GenteGuada", self.anchor, self.getPosition())
    else:
      talker.triggerEvent('chatAdded', message=chat_message.ChatMessage("Si me trajeras un regalo, podr�a darte algo a cambio...", \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
      return None

# ===============================================================
     
class GGPenguinQuiz(GGPenguin):
  """ GGPenguinQuiz class.
  Defines a quiz penguin object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label, filePath):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    anchor: image anchor on screen.
    topAnchor: image top anchor on screen.
    label: penguin's label.
    filePath: folder where quiz questions are.
    """
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__filePath = filePath
    self.__fileList = os.listdir(filePath)
    rmList = []
    for item in self.__fileList:
      if item.find(".") > -1 or item.find("~") > -1:
        rmList.append(item)  
    for item in rmList:
      self.__fileList.remove(item)    
    self.__availableQuestions = {}

  def copyObject(self):
    return GGPenguinQuiz(self.spriteName, self.anchor, self.topAnchor, self.label, self.__filePath)
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talk", "jumpOver"]
  
  def getFileList(self):
    """ Returns the questions list.
    """  
    return self.__fileList  
  
  def removeRightQuestionForPlayer(self, question, player):
    """ Removes a correctly answered question from the question list for a given player.
    question: question to be removed.
    player: given player.
    """  
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
    question = random.randint(0, len(self.__availableQuestions[name])-1)
    talker.triggerEvent('quizAdded', message=chat_message.ChatQuiz(self, self.__availableQuestions[name][question], talker, 'Andatuz',  
                                        GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))   
        
