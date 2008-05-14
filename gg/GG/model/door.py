import item
import GG.isoview.isoview_item
import dMVC.model

class GGDoor(item.GGItem):
  """ Door class.
  Defines a door object behaviour.
  """
 
  def __init__(self, sprite, size, entryPosition, exitPosition, position, offset, heading, destinationRoom):
    """ Class builder.
    sprite: sprite used to paint the door.
    size: door sprite size.
    entryPosition: door entrance position.
    exitPosition: door exit position on the new room.
    position: door position.
    offset: image offset on screen.
    heading: direction the door opens to.
    destinationRoom: room the door will teleport players to.
    """
    item.GGItem.__init__(self, sprite, size, position, offset)
    self.__entryPosition = entryPosition
    self.__exitPosition = exitPosition
    self.__destinationRoom = destinationRoom
    #TODO atributo "mega"-privado
    self.__heading = heading
    
  def getBackground(self):
    return self.__background

  # self.__entryPosition
  
  def getEntryPosition(self):
    """ Returns the door entrance position.
    """
    return self.__entryPosition
  
  def setEntryPosition(self, entryPosition):
    """ Sets a new door entrance position:
    entryPosition: new door entrance position.
    """
    if self.__entryPosition != entryPosition:
      self.__entryPosition = entryPosition
      #self.triggerEvent('entryPositon', entryPosition=entryPosition)
    
  # self.__exitPosition
  
  def getExitPosition(self):
    """ Returns the door exit position.
    """
    return self.__exitPosition
  
  def setExitPosition(self, exitPosition):
    """ Sets a new door exit position:
    entryPosition: new door exit position.
    """
    if self.__exitPosition != exitPosition:
      self.__exitPosition = exitPosition
      #self.triggerEvent('exitPosition', exitPosition=exitPosition)
  
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

  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    """
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)
  
  def clickedBy(self, clicker):
    """ Triggers an event when the door receives a click by a player.
    clicker: player who clicks.
    """
    if clicker.getPosition() == self.__entryPosition:
      clicker.changeRoom(self.__destinationRoom, self.__exitPosition)
    