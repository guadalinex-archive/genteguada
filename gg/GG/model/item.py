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
    self.offset   = offset
    self.__heading = "down"
    self.__state = "standing"
    self.__position = position
    self.__room = None

  @dMVC.model.localMethod 
  def getOffset(self):
    """ Returns the item screen offset.
    """
    return self.offset
  
  def variablesToSerialize(self):
    return ['spriteName', 'offset']
  
  def getHeading(self):
    """ Returns the direction the player is heading to.
    """
    return self.__heading
  
  def getState(self):
    """ Returns the player's state.
    """
    return self.__state
  
  def getRoom(self):
    """ Returns the room where the player is.
    """
    return self.__room
  
  def getPosition(self):
    """ Returns the item position.
    """
    return self.__position

  def setHeading(self, heading):
    """ Sets a new heading direction for the item.
    """
    if self.__heading <> heading:
      self.__heading = heading
      self.triggerEvent('headingChanged', heading=heading)

  def setState(self, state):
    """ Sets a new state for the item.
    """
    if self.__state <> state:
      self.__state = state
      self.triggerEvent('stateChanged', state=state)

  def setRoom(self, room):
    """ Sets a new room for the player.
    room: new room.
    """
    if self.__room <> room:
      self.__room = room
      self.triggerEvent('roomChanged', room=room)

  def setPosition(self, pos):
    """ Sets a new position for the item.
    """
    if self.__position <> pos:
      self.__position = pos
      self.triggerEvent('positionChanged', position=pos)

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
    self.triggerEvent('chat', actor=clicker, receiver=self, msg="probando click")
    
  def tick(self):
    """ Call for an update on item position.
    Not used at the moment.
    """
    pass