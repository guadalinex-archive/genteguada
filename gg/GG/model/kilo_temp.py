import room_item
import GG.utils
import time
import GG.isoview.isoview_item

class GGKiloTemp(room_item.GGRoomItem):
  """ GGKiloTemp class.
  Defines a temporary pickable item behaviour.
  """
    
  def __init__(self, spriteName, position, anchor, spriteInventory, label, time):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    anchor: image anchor on screen.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
    time: item's life time.
    startRoom: item's starting room.
    """
    room_item.GGRoomItem.__init__(self, spriteName, position, anchor)
    self.spriteInventory = spriteInventory
    self.label = label
    self.__time = time*1000
    self.__startTime = 0
  
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']
  
  def setPlayer(self, player):
    if player == None:
      self.__startTime = 0
    room_item.GGRoomItem.setPlayer(self, player)
    
  def getStartTime(self):
    return self.__startTime
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["inventory"]
  
  def tick(self, now):
    """ Call for an update on item.
    """
    if self.__startTime == 0:
      self.__startTime = now
      return 
    if (now - self.__startTime) > self.__time:
      if self.getPlayer() != None:
        self.getPlayer().removeFromInventory(self)
      else:
        self.getRoom().removeItem(self)  
        
  def timeLeft(self):
    """ Returns the item's time left.
    """
    if self.__time > self.__elapsedTime:
      return True
    else:
      return False
  
  def checkSimilarity(self, item):
    print "****************** comprobando"  
    if kilo.GGKilo.checkSimilarity(self, item):
      if item.label == self.label:
        if item.getStartTime() == self.__startTime:
          return True
    return False   
    
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    
  def isStackable(self):
    return False


