import ggmodel
import GG.isoview.isoview_item
import dMVC.model

class GGItem(ggmodel.GGModel):
  """GGItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, size, position, offset):
    """ Class constructor.
    sprite: image name.
    size: image size.
    position: position on screen for the item.
    offset: offset for that position.
    """
    ggmodel.GGModel.__init__(self)
    self.spriteName = spriteName
    self.size = size
    self.offset   = offset
    self.__position = position
    self.__room = None

  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['spriteName', 'size', 'offset']
  
  # self.__position
  
  def getPosition(self):
    """ Returns the item position.
    """
    return self.__position

  def setPosition(self, pos):
    """ Sets a new position for the item.
    """
    if self.__position <> pos:
      self.__position = pos
      self.triggerEvent('position', position=pos)

  # self.__room
    
  def getRoom(self):
    """ Returns the room where the player is.
    """
    return self.__room
  
  def clearRoom(self):
    """ Sets the item's room as none.    
    """
    if self.__room == None:
      raise "Error en limpieza de room"
    self.__setRoom(None)
    
  def setRoom(self, room):
    """ Sets a new room for the player.
    room: new room.
    """
    if self.__room != None:
      raise "Error: el item ya tiene un room"
    if room == None:
      raise "Error: habitacion = None"
    self.__setRoom(room)
      
  def __setRoom(self, room):
    """ Private method. Sets the item's room with a new value and triggers an event.
    room: new room.
    """
    self.__room = room
    self.triggerEvent('room', room=room)
  
  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    """
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)
  
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    self.__room.addMessageChat(str(self)+" recibe click")
    
  def tick(self):
    """ Call for an update on item position.
    Not used at the moment.
    """
    pass
  
  def abandonRoom(self):
    """ Tells a room to remove this item from it.
    """
    self.__room.removeItem(self)
