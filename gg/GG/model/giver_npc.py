import GG.model.item
import GG.model.pickable_item
import GG.isoview.isoview_item

class GGGiverNPC(GG.model.item.GGItem):
  """ GiverNPC class.
  Defines a giver npc object behaviour.
  """
 
  def __init__(self, sprite, position, offset, label, condition, item):
    """ Class builder.
    sprite: sprite used to paint the npc.
    position: penguin position.
    offset: image offset on screen.
    label: penguin's label
    """
    GG.model.item.GGItem.__init__(self, sprite, position, offset)
    self.label = label
    self.__condition = condition
    self.__item = item
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.item.GGItem.variablesToSerialize(self)
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
    GG.model.item.GGItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    

  def talkedBy(self, talker):
    """ Method executed after being talked by a player.
    talker: player.
    """
    for condition in self.__condition:
      if not self.checkCondition(condition, talker):
        return False
    newItem = self.__item["object"](*self.__item["params"])
    if talker.hasItemLabeledInInventory(newItem.label) and isinstance(item, self.__item["object"]):
      return False
    talker.addInventory(newItem)