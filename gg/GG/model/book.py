import item
import GG.utils
import GG.isoview.isoview_item
import dMVC.model

class GGBook(item.GGItem):
  """ Book class.
  Defines a book object behaviour.
  """
 
  def __init__(self, spriteName, size, position, offset, spriteInventory, pickable, label):
    """ Class builder.
    spriteName: sprite used to paint the book on the screen game zone.
    size: book sprite size.
    position: book position.
    offset: image offset on screen.
    spriteInventory: sprite used to paint the book on the screen inventory zone.
    pickable: sets the book as a pickable item by a player.
    label: book's label
    """
    item.GGItem.__init__(self, spriteName, size, position, offset)
    self.spriteInventory = spriteInventory
    self.label = label
    #TODO variable "Mega"-privada
    self.__pickable = pickable
    
  def variablesToSerialize(self):
    #TODO esto es una solucin de emergencia mientras que no se arregle en el dMVC
    parentVars = item.GGItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']
  
  # self.__pickable
  
  def getPickable(self):
    """ Returns the pickable flag.
    """
    return self.__pickable

  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    if self.__pickable and GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.addInventory(self)
      self.getRoom().removeItem(self)
      