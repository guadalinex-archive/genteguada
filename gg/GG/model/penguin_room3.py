# -*- coding: iso-8859-15 -*-

import GG.model.room_item
import GG.model.golden_key
#import GG.model.pickable_item
import GG.isoview.isoview_item

class GGPenguinRoom3(GG.model.room_item.GGRoomItem):
  """ GGPenguinRoom3 class.
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
    self.__msg = "Para abrir el portón de madera deberás depositar algo pesado sobre ese resorte. Quizá puedas hallar cajas en el almacén, pero la puerta está cerrada. Me pregunto dónde estará la llave que abre la puerta..."
        
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

  def createKey(self):
    return GG.model.golden_key.GGGoldenKey(GG.utils.KEY_SPRITE, "llave dorada", self.getPosition())
  
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
    self.getRoom().triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(self.__msg, \
                'Andatuz', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
    """
    newKey = self.createKey()
    if talker.checkItemOnInventory(newKey):
      return False
    talker.addToInventoryFromVoid(newKey, self.getPosition())
    """
    