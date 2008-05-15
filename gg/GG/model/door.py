import GG.model.item
import GG.isoview.isoview_item
import dMVC.model

class GGDoor(GG.model.item.GGItem):
  """ Door class.
  Defines a door object behaviour.
  """
 
  def __init__(self, sprite, entryPosition, exitPosition, position, offset, destinationRoom):
    """ Class builder.
    sprite: sprite used to paint the door.
    entryPosition: door entrance position.
    exitPosition: door exit position on the new room.
    position: door position.
    offset: image offset on screen.
    destinationRoom: room the door will teleport players to.
    """
    GG.model.item.GGItem.__init__(self, sprite, position, offset)
    self.__entryPosition = entryPosition
    self.__exitPosition = exitPosition
    self.__destinationRoom = destinationRoom
    
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
  
  # self.__destinationRoom
  
  def getDestinationRoom(self):
    """ Returns the room that the door connects to.
    """
    return self.__destinationRoom
  
  def setDestinationRoom(self, destinationRoom):
    """ Sets a new room connected to the door.
    """
    if not self.__destinationRoom == destinationRoom:
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
    k = 0
    if clicker.getPosition() == self.__entryPosition:
      for item in clicker.getInventory():
        if item.label == "llave dorada":
          k = 1
      if k:
        clicker.changeRoom(self.__destinationRoom, self.__exitPosition)
          
