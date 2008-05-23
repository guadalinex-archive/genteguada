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
    parentVars = GG.model.item.GGItem.variablesToSerialize(self)
    return parentVars + ['label']
  
  def getOptions(self):
    return ["talk"]
  
  def checkCondition(self, condition, player):
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
    for condition in self.__condition:
      if not self.checkCondition(condition, talker):
        return False
    newItem = self.__item["object"](*self.__item["params"])
    for item in talker.getInventory():
      if isinstance(item, self.__item["object"]) and item.label == newItem.label:
        return False
    talker.addInventory(newItem)