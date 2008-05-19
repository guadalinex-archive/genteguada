import GG.model.item
import GG.isoview.isoview_item
import dMVC.model

class GGTeleporter(GG.model.item.GGItem):
  """ Teleporter class.
  Defines a teleporter object behaviour.
  """
 
  def __init__(self, sprite, entryPosition, exitPosition, position, offset, destinationRoom, condition):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    entryPosition: teleporter entrance position.
    exitPosition: teleporter exit position on the new room.
    position: teleporter position.
    offset: image offset on screen.
    destinationRoom: room the teleporter will carry players to.
    """
    GG.model.item.GGItem.__init__(self, sprite, position, offset)
    self.__entryPosition = entryPosition
    self.__exitPosition = exitPosition
    self.__destinationRoom = destinationRoom
    self.__condition = condition
    
  # self.__entryPosition
  
  def getEntryPosition(self):
    """ Returns the teleporter entrance position.
    """
    return self.__entryPosition
  
  def setEntryPosition(self, entryPosition):
    """ Sets a new teleporter entrance position:
    entryPosition: new teleporter entrance position.
    """
    if self.__entryPosition != entryPosition:
      self.__entryPosition = entryPosition
      #self.triggerEvent('entryPositon', entryPosition=entryPosition)
    
  # self.__exitPosition
  
  def getExitPosition(self):
    """ Returns the teleporter exit position.
    """
    return self.__exitPosition
  
  def setExitPosition(self, exitPosition):
    """ Sets a new teleporter exit position:
    entryPosition: new teleporter exit position.
    """
    if self.__exitPosition != exitPosition:
      self.__exitPosition = exitPosition
      #self.triggerEvent('exitPosition', exitPosition=exitPosition)
  
  # self.__destinationRoom
  
  def getDestinationRoom(self):
    """ Returns the room that the teleporter connects to.
    """
    return self.__destinationRoom
  
  def setDestinationRoom(self, destinationRoom):
    """ Sets a new room connected to the teleporter.
    """
    if not self.__destinationRoom == destinationRoom:
      self.__destinationRoom = destinationRoom
      self.triggerEvent('destinationRoom', destinationRoom=destinationRoom)

  # self.__condition
  
  def setCondition(self, condition):
    """ Sets a new condition for teleporter activation.
    condition: new condition list.
    """
    self.__condition = condition
    
  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    """
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)
  
  def checkCondition(self, condition, player):
    for item in player.getInventory():
      if item.label == condition:
        return True
    return False    
      
  def clickedBy(self, clicker):
    """ Triggers an event when the teleporter receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.item.GGItem.clickedBy(self, clicker)
    if clicker.getPosition() == self.__entryPosition:
      for condition in self.__condition:
        if not self.checkCondition(condition, clicker):
          return False
      clicker.changeRoom(self.__destinationRoom, self.__exitPosition)
    else:
      return False    