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
    self.__spriteInventory = spriteInventory
    self.__pickable = pickable
    self.__label = label
    
  # self.__spriteInventory
  
  def getSpriteInventory(self):
    """ Returns the inventory zone sprite.
    """
    return self.__spriteInventory

  def setSpriteInventory(self, spriteInventory):
    """ Sets the inventory zone sprite with a new value.
    spriteInventory: new spriteInventory value.
    """
    if self.__spriteInventory <> spriteInventory:
      self.__spriteInventory = spriteInventory
      self.triggerEvent('spriteInventory', spriteInventory=spriteInventory)
      return True
    return False
  
  # self.__pickable
  
  def getPickable(self):
    """ Returns the pickable flag.
    """
    return self.__pickable

  def setPickable(self, pickable):
    """ Sets the pickable flag with a new value.
    pickable: new flag value.
    """
    if self.__pickable <> pickable:
      self.__pickable = pickable
      self.triggerEvent('state', state=state)
      return True
    return False

  # self.__label
  
  def getLabel(self):
    """ Returns the book's label.
    """
    return self.__label

  def setLabel(self, label):
    """ Sets a new content for the book's label.
    label: new label content.
    """
    if self.__label <> label:
      self.__label = label
      self.triggerEvent('label', label=label)
      return True
    return False

  def clickedBy(self, clicker):
    """ Triggers an event when the penguin receives a click by a player.
    clicker: player who clicks.
    """
    if self.__pickable and GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      self.getRoom().removeItem(self)
      clicker.addInventory(self)
      self.triggerEvent('chat', actor=clicker, receiver=self, msg="Obtienes Pinguino Misterioso")
  