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
    #TODO tengo dudas de que pickable se pueda modificar desde fuera, por lo tanto seria una variable "Mega"-privada de la que habiamos hablado
    self.__pickable = pickable
    
  def variablesToSerialize(self):
    #TODO esto es una solucin de emergencia mientras que no se arregle en el dMVC
    parentVars = item.GGItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']
  
  @dMVC.model.localMethod 
  def getSpriteInventory(self):
    #TODO al ser una variable publica habria que eliminar este metodo
    """ Returns name of the sprite used to pain the penguin on the inventory.
    """
    return self.spriteInventory    
  
  @dMVC.model.localMethod 
  def getLabel(self):
    #TODO al ser una variable publica habria que eliminar este metodo
    """ Returns penguin label.
    """
    return self.label    
    
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
      #self.getRoom().addMessageChat(str(self)+" Obtienes")
      self.getRoom().removeItem(self)
      #TODO creo que en el removeItem debe de estar el setRoom(None)
      
      #print self.getRoom()
      #self.clearRoom()
      
      #self.triggerEvent('chat', actor=clicker, receiver=self, msg="Obtienes "+self.label)
  
