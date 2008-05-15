import GG.model.item
import GG.model.pickable_item
import GG.isoview.isoview_item

class GGPenguin(GG.model.item.GGItem):
  """ Penguin class.
  Defines a penguin object behaviour.
  """
 
  def __init__(self, sprite, position, offset, spriteInventory, label):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    position: penguin position.
    offset: image offset on screen.
    spriteName: sprite used to paint the penguin on the screen game zone.
    label: penguin's label
    """
    GG.model.item.GGItem.__init__(self, sprite, position, offset)
    self.spriteInventory = spriteInventory
    self.label = label
    
  def variablesToSerialize(self):
    parentVars = GG.model.item.GGItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']
  
  def clickedBy(self, clicker):
    """ Triggers an event when the penguin receives a click by a player.
    clicker: player who clicks.
    """
    #if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
    #  clicker.addInventory(GG.model.key.GGKey(GG.utils.KEY_SPRITE, [0, 0, 0], [20, -40], GG.utils.KEY_SPRITE, "llave dorada"))

    k = 0
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      for item in clicker.getInventory():
        if item.label == "llave dorada":
          k = 1
      if not k:
        clicker.addInventory(GG.model.pickable_item.GGPickableItem(GG.utils.KEY_SPRITE, [0, 0, 0], [20, -40], GG.utils.KEY_SPRITE, "llave dorada"))
      