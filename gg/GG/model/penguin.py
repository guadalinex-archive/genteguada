import item
import GG.isoview.isoview_item
import dMVC.model

class GGPenguin(item.GGItem):
  """ Penguin class.
  Defines a penguin object behaviour.
  """
 
  def __init__(self, sprite, size, position, offset, spriteInventory, pickable, label):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    size: penguin sprite size.
    position: penguin position.
    offset: image offset on screen.
    spriteName: sprite used to paint the book on the screen game zone.
    pickable: sets the book as a pickable item by a player.
    label: book's label
    """
    item.GGItem.__init__(self, sprite, size, position, offset)
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
    """ Triggers an event when the penguin receives a click by a player.
    clicker: player who clicks.
    """
    if self.__pickable and GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.addInventory(self)
      #self.getRoom().addMessageChat(str(self)+" Obtienes")
      
      self.getRoom().removeItem(self)
      
      #self.clearRoom()
      #self.triggerEvent('chat', actor=clicker, receiver=self, msg="Obtienes "+self.label)
  
