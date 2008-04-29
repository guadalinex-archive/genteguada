import item
import GG.isoview.isoview_item
import dMVC.model

class GGDoor(item.GGItem):
  """ Door class.
  Defines a door object behaviour.
  """
 
  def __init__(self, sprite, size, position, offset, heading, destinationRoom):
    """ Class builder.
    sprite: sprite used to paint the door.
    size: door sprite size.
    position: door position.
    offset: image offset on screen.
    heading: direction the door opens to.
    destinationRoom: room the door will teleport players to.
    """
    item.GGItem.__init__(self, sprite, size, position, offset)
    self.__heading = heading
    self.__destinationRoom = destinationRoom  
  
  def clickedBy(self, clicker):
    """ Triggers an event when the door receives a click by a player.
    clicker: player who clicks.
    """
    # comprueba que el jugador este .
    pPos = clicker.getPosition()
    dPos = self.getPosition()
    #if self.__heading == "up":   
    self.triggerEvent('teleport', clicker=clicker, destinationRoom=self.__destinationRoom)
    #   procesa cambios en el modelo.
