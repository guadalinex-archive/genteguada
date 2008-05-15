import item
import GG.model.key
import GG.isoview.isoview_item
import dMVC.model

class GGPenguin(item.GGItem):
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
    item.GGItem.__init__(self, sprite, position, offset)
    self.spriteInventory = spriteInventory
    self.label = label
    
  def variablesToSerialize(self):
    #TODO esto es una solucin de emergencia mientras que no se arregle en el dMVC
    parentVars = item.GGItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']
  
  @dMVC.model.localMethod 
  def getLabel(self):
    #TODO al ser una variable publica habria que eliminar este metodo
    """ Returns penguin label.
    """
    return self.label    
  
  def clickedBy(self, clicker):
    """ Triggers an event when the penguin receives a click by a player.
    clicker: player who clicks.
    """
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.addInventory(GG.model.key.GGKey(GG.utils.KEY_SPRITE, [0, 0, 0], [20, -40], GG.utils.KEY_SPRITE, "llave dorada"))
