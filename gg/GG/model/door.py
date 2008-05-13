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
    #TODO atributo "mega"-privado, no creo que se puede cambiar desde el cliente
    self.__destinationRoom = destinationRoom  

  # self.__heading

  def getHeading(self):
    """ Returns the direction the door is heading to.
    """
    return self.__heading
  
  def setHeading(self, heading):
    """ Sets a new heading direction for the item.
    """
    if self.__heading <> heading:
      self.__heading = heading
      self.triggerEvent('heading', heading=heading)

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
    """ Triggers an event when the door receives a click by a player.
    clicker: player who clicks.
    """
    pPos = clicker.getPosition()
    dPos = self.getPosition()
    if self.__heading == "up" and pPos == [dPos[0], dPos[1], dPos[2] - 1]:
      clicker.changeRoom(self.__destinationRoom)
    elif self.__heading == "down" and pPos == [dPos[0], dPos[1], dPos[2] + 1]:
      clicker.changeRoom(self.__destinationRoom)
    elif self.__heading == "left" and pPos == [dPos[0] - 1, dPos[1], dPos[2]]:
      clicker.changeRoom(self.__destinationRoom)
    elif self.__heading == "right" and pPos == [dPos[0] + 1, dPos[1], dPos[2]]:
      clicker.changeRoom(self.__destinationRoom)
