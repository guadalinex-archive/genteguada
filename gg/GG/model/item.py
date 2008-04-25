import ggmodel
import GG.isoview.isoview_item
import dMVC.model

class GGItem(ggmodel.GGModel):
  """GGItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, sprite, size, position, offset):
    """ Class constructor.
    sprite: image name.
    size: image size.
    position: position on screen for the item.
    offset: offset for that position.
    """
    ggmodel.GGModel.__init__(self)
    self.__sprite   = sprite
    self.__size     = size # TODO: REMOVE!!!!
    self.__position = position
    self.__offset   = offset
    
  def getPosition(self):
    """ Returns the item position.
    """
    return self.__position

  def setPosition(self, pos):
    """ Sets a new position for the item.
    """
    self.__position = pos 

  def getSprite(self):
    """ Returns the sprite name used to paint the item on screen.
    """
    return self.__sprite
    
  def getOffset(self):
    """ Returns the item screen offset.
    """
    return self.__offset
  
  @dMVC.model.localMethod 
  def defaultView(self, screen, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    """
    return GG.isoview.isoview_item.IsoViewItem(self, screen, parent)
  
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    self.triggerEvent('chat', actor=clicker, receiver=self, msg="probando click")