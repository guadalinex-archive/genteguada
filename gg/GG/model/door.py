import item
import GG.isoview.isoview_ghostitem
import dMVC.model

class GGDoor(item.GGItem):
  """ Door class.
  Defines a door object behaviour.
  """
 
  def __init__(self, sprite, size, entryPosition, screenPosition, offset, heading, destinationRoom, background):
    """ Class builder.
    sprite: sprite used to paint the door.
    size: door sprite size.
    entrancePosition: door entrance position.
    screenPosition: door position on screen
    offset: image offset on screen.
    heading: direction the door opens to.
    destinationRoom: room the door will teleport players to.
    background: indicates if this item is on the background or in the front.
    """
    item.GGItem.__init__(self, sprite, size, [-3,-3,-3], offset)
    self.__entryPosition = entryPosition    
    self.__screenPosition = screenPosition
    self.__destinationRoom = destinationRoom
    #TODO atributo "mega"-privado
    self.__heading = heading
    self.__background = background
    
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
    
  # self.__screenPosition

  def getScreenPosition(self):
    return self.__screenPosition
  
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
    return GG.isoview.isoview_ghostitem.IsoViewGhostItem(self, screen, room, parent)
  
  def isContained(self, point):
    """ Checks if a point is inside the door.
    point: point to check.
    """
    x0 = self.__screenPosition[0] - self.offset[0]
    y0 = self.__screenPosition[1] - self.offset[1]
    x1 = x0 + self.size[0]
    y1 = y0 + self.size[1]
    if x0 <= point[0] <= x1:
      if y0 <= point[1] <= y1:
        return True
    return False
  
  def clickedBy(self, clicker):
    """ Triggers an event when the door receives a click by a player.
    clicker: player who clicks.
    """
    if clicker.getPosition() == self.__entryPosition:
      clicker.changeRoom(self.__destinationRoom)
    