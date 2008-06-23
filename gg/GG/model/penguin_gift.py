# -*- coding: iso-8859-15 -*-

import GG.model.gift
import GG.isoview.isoview_item

class GGPenguinGift(GG.model.room_item.GGRoomItem):
  """ GGPenguinGift class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, position, anchor, label):
    """ Class builder.
    sprite: sprite used to paint the npc.
    position: penguin position.
    anchor: image anchor on screen.
    label: penguin's label
    """
    GG.model.room_item.GGRoomItem.__init__(self, sprite, position, anchor)
    self.label = label
    self.__msg1 = "Debes ser muy habil para haber llegado hasta aquí. Toma esto como premio a tu esfuerzo."
    self.__msg2 = "¿Has vuelto? Ya no me quedan más cosas que darte" 
        
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talk"]
  
  def checkSimilarity(self, item):
    if GG.model.room_item.GGRoomItem.checkSimilarity(self, item):
      if item.label == self.label:
        return True
    return False   
  
  def checkCondition(self, condition, player):
    """ Checks a condition for a given player.
    condition: condition to check.
    player: given player.
    """
    return True

  def createGift(self):
    return GG.model.gift.GGGift(GG.utils.KEY_SPRITE, "regalo", self.anchor, self.getPosition())
  
  def clickedBy(self, clicker):
    """ Triggers an event when the npc receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
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
        
    