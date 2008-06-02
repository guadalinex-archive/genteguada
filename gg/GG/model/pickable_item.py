import item
import GG.isoview.isoview_item

class GGPickableItem(item.GGItem):
  """ PickableItem class.
  Defines a pickable item behaviour.
  """
 
  def __init__(self, spriteName, position, offset, spriteInventory, label):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    offset: image offset on screen.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
    """
    item.GGItem.__init__(self, spriteName, position, offset)
    self.spriteInventory = spriteInventory
    self.label = label
    
  def variablesToSerialize(self):
    parentVars = item.GGItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["inventory"]
  
  def clickedBy(self, clicker):
    """ Triggers an event when the item receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.item.GGItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
      #clicker.addInventory(self)
      #self.getRoom().removeItem(self)
      
