# -*- coding: iso-8859-15 -*-

import GG.model.room_item
import GG.model.golden_key
#import GG.model.pickable_item
import GG.isoview.isoview_item

class GGPenguinRoom5Shirt(GG.model.room_item.GGRoomItem):
  """ GGPenguinRoom5 class.
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
    self.__msg = "Vaya, veo que me traes un regalo. Toma, déjame cambiártelo por esta nueva camiseta."
        
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talkAndGet"]
        
  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteName

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

  def clickedBy(self, clicker):
    """ Triggers an event when the npc receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
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
      
