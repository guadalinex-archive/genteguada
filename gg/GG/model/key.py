import item
import GG.isoview.isoview_item

class GGKey(item.GGItem):
  """ Key class.
  Defines a key object behaviour.
  """
 
  def __init__(self, sprite, position, offset, spriteInventory, label):
    """ Class builder.
    sprite: sprite used to paint the key.
    position: key position.
    offset: image offset on screen.
    spriteName: sprite used to paint the key on the screen game zone.
    label: key's label
    """
    item.GGItem.__init__(self, sprite, position, offset)
    self.spriteInventory = spriteInventory
    self.label = label
    
  def variablesToSerialize(self):
    parentVars = item.GGItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']
  
  def clickedBy(self, clicker):
    """ Triggers an event when the key receives a click by a player.
    clicker: player who clicks.
    """
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.addInventory(self)
      self.getRoom().removeItem(self)