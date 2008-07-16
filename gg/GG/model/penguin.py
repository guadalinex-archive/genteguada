# -*- coding: iso-8859-15 -*-
import GG.model.room_item
import GG.isoview.isoview_item
import random
import GG.model.giver_npc
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
    #self.__msg = "¡Bienvenido a GenteGuada! Soy Andatuz, y te guiaré a lo largo de este tutorial para conocer GenteGuada. Puedes explorar por este jardín para aprender a moverte. Cuando estés listo, ve a la puerta y ábrela."
        
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

  """
  def talkedBy(self, talker):
    talker.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(self.__msg, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 3))
  """              
    
#================================================================================

class GGPenguinLobby(GGPenguin):
  """ GGPenguinLobby class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label):
    """ Class builder.
    sprite: sprite used to paint the npc.
    position: penguin position.
    anchor: image anchor on screen.
    label: penguin's label
    """
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__msg = "¡Bienvenido a GenteGuada! Soy Andatuz, y te guiaré a lo largo de este tutorial para conocer GenteGuada. Puedes explorar por este jardín para aprender a moverte. Cuando estés listo, ve a la puerta y ábrela."

  def checkSimilarity(self, item):
    if GGPenguin.checkSimilarity(self, item):
      if item.__msg == self.__msg:
        return True
    return False   

  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    talker.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(self.__msg, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 3))

#================================================================================

class GGPenguinRoom3(GGPenguin):
  """ GGPenguinRoom3 class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label):
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__msg = "Para abrir el portón de madera deberás depositar algo pesado sobre ese resorte. Quizá puedas hallar cajas en el almacén, pero la puerta está cerrada. Me pregunto dónde estará la llave que abre la puerta..."
        
  def checkSimilarity(self, item):
    if GGPenguin.checkSimilarity(self, item):
      if item.__msg == self.__msg:
        return True
    return False   

  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    talker.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(self.__msg, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
    
#================================================================================

class GGPenguinRoom5(GG.model.room_item.GGRoomItem):
  """ GGPenguinRoom5 class.
  Defines a giver npc object behaviour.
  """
  
  def __init__(self, sprite, anchor, topAnchor, label):
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__msg = "¡Enhorabuena! Has conseguido cruzar las 5 salas y completar el tutorial de GenteGuada. Ahora estás listo para entrar de lleno en el verdadero juego. Cruza el portal para comenzar."
        
  def checkSimilarity(self, item):
    if GGPenguin.checkSimilarity(self, item):
      if item.__msg == self.__msg:
        return True
    return False   
  
  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    self.getRoom().triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(self.__msg, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))

#================================================================================

class GGPenguinRoom5Shirt(GGPenguin):
  """ GGPenguinRoom5 class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label):
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__msg = "Vaya, veo que me traes un regalo. Toma, déjame cambiártelo por esta nueva camiseta."

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talkAndGet"]

  def checkSimilarity(self, item):
    if GGPenguin.checkSimilarity(self, item):
      if item.__msg == self.__msg:
        return True
    return False   
  
  def talkAndGet(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    giftItem = talker.getItemFromInventory("Regalo")
    if giftItem:
      print "tenemos regalo"
      talker.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(self.__msg, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
      talker.removeFromInventory(giftItem)
      return GG.model.gift_inventory.GGGiftInventory("furniture/shirt.png", "Camiseta GenteGuada", self.anchor, self.getPosition())
    else:
      talker.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage("Si me trajeras un regalo, podría darte algo a cambio...", \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
      return None

#================================================================================
        
class GGPenguinGift(GGPenguin):
  """ GGPenguinGift class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, topAnchor, anchor, label):
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__msg1 = "Debes ser muy habil para haber llegado hasta aquí. Toma esto como premio a tu esfuerzo."
    self.__msg2 = "¿Has vuelto? Ya no me quedan más cosas que darte" 

  def checkSimilarity(self, item):
    if GGPenguin.checkSimilarity(self, item):
      if item.__msg1 == self.__msg1 and item.__msg2 == self.__msg2:
        return True
    return False   

  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    gift = self.createGift()
    if not talker.hasItemLabeledInInventory(gift.label):
      talker.addToInventoryFromVoid(gift, self.getPosition())
      self.getRoom().triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(self.__msg1, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 3))
    else:
      self.getRoom().triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(self.__msg2, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 3))
              
#================================================================================
     
class GGPenguinQuiz(GGPenguin):
  """ GGPenguinQuiz class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label, fileList):
    GGPenguin.__init__(self, sprite, anchor, topAnchor, label)
    self.__fileList = fileList
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
