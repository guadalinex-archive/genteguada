import ggmodel
import GG.isoview.isoview_item
import dMVC.model

class GGItem(ggmodel.GGModel):
  """GGItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteImg, size, position, offset):
    """ Class constructor.
    sprite: image name.
    size: image size.
    position: position on screen for the item.
    offset: offset for that position.
    """
    ggmodel.GGModel.__init__(self)
    self.spriteImg   = spriteImg
    self.__position = position
    self.__offset   = offset
    self.__currentRoom = None

  def getCurrentRoom(self):
    """ Returns the room where the player is.
    """
    return self.__currentRoom
  
  def setCurrentRoom(self, room):
    """ Sets a new room for the player.
    room: new room.
    """
    self.__currentRoom = room
    
  def variablesToSerialize(self):
    return ['spriteImg']
  
  def getPosition(self):
    """ Returns the item position.
    """
    return self.__position

  def setPosition(self, pos):
    """ Sets a new position for the item.
    """
    self.__position = pos 

  def getOffset(self):
    """ Returns the item screen offset.
    """
    return self.__offset
  
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