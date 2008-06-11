import room_item
import GG.utils
import time
import GG.isoview.isoview_item

class GGMP3Lobby(room_item.GGRoomItem):
  """ GGMP3Lobby class.
  Defines a temporary pickable item behaviour.
  """
    
  def __init__(self, spriteName, position, offset, spriteInventory, label, time, startRoom):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    offset: image offset on screen.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
    time: item's life time.
    startRoom: item's starting room.
    """
    room_item.GGRoomItem.__init__(self, spriteName, position, offset)
    self.spriteInventory = spriteInventory
    self.label = label
    self.__time = time*1000
    self.__startRoom = startRoom
    self.__startTime = 0
  
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']
  
  def getStartRoom(self):
    """ Returns the item's starting room.
    """
    return self.__startRoom

  def setStartRoom(self, room):
    """ Sets a new item's starting room.
    room: new starting room.
    """
    self.__startRoom = room
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["inventory"]
  
  def tick(self, now):
    """ Call for an update on item.
    """
    if self.getPlayer() == None:
      return
    if self.__startTime == 0:
      self.__startTime = now    
    if (now - self.__startTime) > self.__time: 
      self.getPlayer().removeInventory(self)
      self.__startRoom.addItemFromInventory(self, self.getPosition())
      self.setPlayer(None)
      self.__startTime = 0
    
  def timeLeft(self):
    """ Returns the item's time left.
    """
    if self.__time > self.__elapsedTime:
      return True
    else:
      return False
    
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    
  