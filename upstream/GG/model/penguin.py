# -*- coding: utf-8 -*-

import os
import time
import random
import room_item
import chat_message
import GG.utils
import generated_inventory_item
import ggsystem

class GGPenguin(room_item.GGRoomItem):
  """ GGPenguin class.
  Defines a penguin object behaviour.
  """
 
  def __init__(self, sprite, label):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    label: penguin's label.
    """
    room_item.GGRoomItem.__init__(self, sprite, label)

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGPenguin(self.spriteName, self.getName())
        
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talk", "jumpOver"]

  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    adminDict = room_item.GGRoomItem.getAdminActions(self)
    adminDict["Etiqueta"] = [self.getName()]
    return adminDict    

  def applyChanges(self, fields, player, room):
    keys = fields.keys()
    if "Etiqueta" in keys:
      oldLabel = self.getName()
      newLabel = fields["Etiqueta"]
      if self.setName(newLabel):
        ggsystem.GGSystem.getInstance().labelChange(oldLabel, newLabel)
    return room_item.GGRoomItem.applyChanges(self, fields, player, room)
      
  def clickedBy(self, clicker):
    """ Triggers an event when the penguin receives a click by a player.
    clicker: player who clicks.
    """
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    
  
  def newChatMessage(self, talker, chatMessage, text):
    """ Sends a new chat message.
    talker: message emitter.
    chatMessage: message object.
    text: message text.
    """  
    header = time.strftime("%H:%M", time.localtime(time.time())) + " [" + self.label + "]: "
    talker.triggerEvent('chatAdded', message=chatMessage, text=text, header=header)


class GGPenguinTalker(GGPenguin):
  """ GGPenguinTalker class.
  Defines a talker penguin object behaviour.
  """
 
  def __init__(self, sprite, label, message):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    label: penguin's label.
    message: penguin's message.
    """
    GGPenguin.__init__(self, sprite, label)
    self.__msg = message

  def objectToPersist(self):
    dict = GGPenguin.objectToPersist(self)
    dict["msg"] = self.__msg
    return dict

  def load(self, dict):
    GGPenguin.load(self, dict)
    self.__msg = dict["msg"]

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGPenguinTalker(self.spriteName, self.getName(), self.__msg)
    
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
    adminDict = GGPenguin.getAdminActions(self)
    adminDict["Mensaje"] = [self.__msg]
    return adminDict  

  def applyChanges(self, fields, player, room):
    keys = fields.keys()
    if "Mensaje" in keys:
      self.setMessage(fields["Mensaje"])
    return GGPenguin.applyChanges(self, fields, player, room)

  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    self.newChatMessage(talker, chat_message.ChatMessage(self.__msg, 'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2), self.__msg)
    talker.setUnselectedItem()
    


class GGPenguinTrade(GGPenguin):
  """ GGPenguinTrade class.
  Defines a trade penguin behaviour.
  """
 
  def __init__(self, sprite, label, message, gift):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    label: penguin's label
    message: penguin's message.
    gift: item the penguin will ask the player for.
    """
    GGPenguin.__init__(self, sprite, label)
    self.__msg = message
    self.__giftLabel = gift

  def objectToPersist(self):
    dict = GGPenguin.objectToPersist(self)
    dict["msg"] = self.__msg
    dict["giftLabel"] = self.__giftLabel
    return dict

  def load(self, dict):
    GGPenguin.load(self, dict)
    self.__msg = dict["msg"]
    self.__giftLabel = dict["giftLabel"]

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGPenguinTrade(self.spriteName, self.getName(), self.__msg, self.__giftLabel)

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talkAndGet", "jumpOver"]

  def getAdminActions(self):
    """ Returns the possible admin actions on this item.
    """  
    adminDict = GGPenguin.getAdminActions(self)
    adminDict["Mensaje"] = [self.__msg]
    adminDict["Regalo"] = [self.__giftLabel]
    return adminDict  

  def applyChanges(self, fields, player, room):
    keys = fields.keys()
    if "Mensaje" in keys:
      self.setMessage(fields["Mensaje"])
    if "Regalo" in keys:
      self.setGiftLabel(fields["Regalo"])
    return GGPenguin.applyChanges(self, fields, player, room)

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
      self.newChatMessage(talker, chat_message.ChatMessage(self.__msg, 'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2), self.__msg)
      talker.removeFromInventory(giftItem)
      item = generated_inventory_item.GGGeneratedInventoryItem(os.path.join(GG.utils.FURNITURE_PATH, "shirt.png"), "Camiseta GenteGuada", self.getPosition()) 
      talker.addToInventory(item, talker.getPosition())
      return True 
    else:
      chatMessage = "Si me trajeras un regalo, podría darte algo a cambio..." 
      self.newChatMessage(talker, chat_message.ChatMessage(chatMessage, 'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2), chatMessage)
    talker.setUnselectedItem()
    return None

class GGNewPenguinTrade(GGPenguinTrade):

  def __init__(self, sprite, label, message, gift, labelGift, spriteGift):
    GGPenguinTrade.__init__(self, sprite, label, message, gift)
    self.__labelGift = labelGift
    self.__spriteGift = spriteGift

  def objectToPersist(self):
    dict = GGPenguinTrade.objectToPersist(self)
    dict["labelGift"] = self.__labelGift
    dict["spriteGift"] = self.__spriteGift
    return dict

  def load(self, dict):
    GGPenguinTrade.load(self, dict)
    self.__labelGift = dict["labelGift"]
    self.__spriteGift = dict["spriteGift"]

  def talkAndGet(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    giftItem = talker.getItemFromInventory(self.getGiftLabel())
    if giftItem:
      self.newChatMessage(talker, chat_message.ChatMessage(self.getMessage(), 'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2), self.getMessage())
      talker.removeFromInventory(giftItem)
      item = generated_inventory_item.GGGeneratedInventoryItem(self.__spriteGift, self.__labelGift, self.getPosition()) 
      talker.addToInventory(item, talker.getPosition())
      return True 
    else:
      chatMessage = "Si me trajeras un regalo, podría darte algo a cambio..." 
      self.newChatMessage(talker, chat_message.ChatMessage(chatMessage, 'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2), chatMessage)
    talker.setUnselectedItem()
    return None

     
class GGPenguinQuiz(GGPenguin):
  """ GGPenguinQuiz class.
  Defines a quiz penguin object behaviour.
  """
 
  def __init__(self, sprite, label, filePath):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    label: penguin's label.
    filePath: folder where quiz questions are.
    """
    GGPenguin.__init__(self, sprite, label)
    self.__filePath = filePath
    self.__fileList = os.listdir(filePath)
    rmList = []
    for item in self.__fileList:
      if item.find(".") > -1 or item.find("~") > -1:
        rmList.append(item)  
    for item in rmList:
      self.__fileList.remove(item)    
    self.__availableQuestions = {}

  def objectToPersist(self):
    dict = GGPenguin.objectToPersist(self)
    dict["filePath"] = self.__filePath
    return dict

  def load(self, dict):
    GGPenguin.load(self, dict)
    self.__filePath = dict["filePath"]
    self.__fileList = os.listdir(self.__filePath)
    rmList = []
    for item in self.__fileList:
      if item.find(".") > -1 or item.find("~") > -1:
        rmList.append(item)  
    for item in rmList:
      self.__fileList.remove(item)    
    self.__availableQuestions = {}

  def copyObject(self):
    """ Copies and returns this item.
    """      
    return GGPenguinQuiz(self.spriteName, self.getName(), self.__filePath)
  
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
      player.addPointsSinGiver(20)
    else: 
      player.addPoints(10, self.label)
      
  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    name = talker.getName()
    if not name in self.__availableQuestions.keys():
      self.__availableQuestions[name] = self.__fileList  
    if len(self.__availableQuestions[name]) == 0:
      talker.newChatMessage("Ya no tengo preguntas que hacerte", 2)
      talker.setUnselectedItem()
      return  
    question = random.randint(0, len(self.__availableQuestions[name])-1)
    talker.triggerEvent('quizAdded', message=chat_message.ChatQuiz(self, self.__filePath,self.__availableQuestions[name][question], talker, 'Andatuz',  
                                        GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))   
    talker.setUnselectedItem()
 
