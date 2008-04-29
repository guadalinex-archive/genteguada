import item
import GG.isoview.isoview_item
import dMVC.model

class GGPenguin(item.GGItem):
  """ Penguin class.
  Defines a penguin object behaviour.
  """
 
  def __init__(self, sprite, size, position, offset, destinationRoom):
    """ Class builder.
    sprite: sprite used to paint the penguin.
    size: penguin sprite size.
    position: penguin position.
    offset: image offset on screen.
    destinationRoom: room the penguin will teleport players to.
    """
    item.GGItem.__init__(self, sprite, size, position, offset)
    self.__destinationRoom = destinationRoom  
  
  # self.__destinationRoom
  
  def getDestinationRoom(self):
    """ Returns the room that the door connects to.
    """
    return self.__destinationRoom
  
  def setDestinationRoom(self, destinationRoom):
    """ Sets a new room connected to the door.
    """
    if self.__destinationRoom <> destinationRoom:
      self.__destinationRoom = destinationRoom
      self.triggerEvent('destinationRoom', destinationRoom=destinationRoom)
  
  def clickedBy(self, clicker):
    """ Triggers an event when the penguin receives a click by a player.
    clicker: player who clicks.
    """
    # comprueba que en el inventario del jugador aparezca la llave.
    self.triggerEvent('teleport', clicker=clicker, destinationRoom=self.__destinationRoom)
    #   procesa cambios en el modelo.
