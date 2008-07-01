import GG.model.room_item
import GG.model.pickable_item
import GG.isoview.isoview_item

class GGGiverNPC(GG.model.room_item.GGRoomItem):
  """ GiverNPC class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, label, condition, item):
    """ Class builder.
    sprite: sprite used to paint the npc.
    position: penguin position.
    anchor: image anchor on screen.
    label: penguin's label
    """
    GG.model.room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor)
    self.label = label
    self.__condition = condition
    self.__item = item
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["talk"]
  
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
    self.lalala()
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    

  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    self.lalala()
    for condition in self.__condition:
      if not self.checkCondition(condition, talker):
        return False
    newItem = self.__item["object"](*self.__item["params"])
    if talker.hasItemLabeledInInventory(newItem.label):
      return False
    talker.addToInventoryFromVoid(newItem, self.getPosition())