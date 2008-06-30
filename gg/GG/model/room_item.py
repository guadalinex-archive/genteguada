import ggmodel
import GG.utils
import inventory_item
import GG.isoview.isoview_item
import dMVC.model

class GGRoomItem(inventory_item.GGInventoryItem):
  """GGRoomItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, position, anchor):
    """ Class constructor.
    sprite: image name.
    position: position on screen for the item.
    anchor: anchor for that position.
    """
    inventory_item.GGInventoryItem.__init__(self, spriteName)
    self.anchor = anchor
    self.topAnchor = GG.utils.TILE_SZ[1] + anchor[1]
    self.__position = position
    self.__room = None
    self.points = 0
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.inventory_item.GGInventoryItem.variablesToSerialize(self)
    return parentVars + ['anchor', 'topAnchor', 'points']

  def setPoints(self, points):
    self.points = points
  
  # self.__position
  
  def getPosition(self):
    """ Returns the item position.
    """
    #print "KUKUYUKU", self
    return self.__position

  def setPosition(self, pos):
    """ Sets a new position for the item.
    pos: new position.
    """
    self.__room.moveItem(self.__position, pos, self)
    if not self.__position == pos:
      old = self.__position
      self.__position = pos
      self.triggerEvent('position', position=pos, oldPosition=old)

  def setStartPosition(self, pos):
    """ Sets a new start position for the item.
    pos: new position.
    """
    if self.__position != pos:
      self.__position = pos
      if pos != None:
        self.triggerEvent('startPosition', position=pos)

  # self.__room
    
  def getRoom(self):
    """ Returns the room where the player is.
    """
    return self.__room
  
  def clearRoom(self):
    """ Sets the item's room as none.    
    """
    if self.__room == None:
      raise Exception("Error en limpieza de room")
    self.__setRoom(None)
    
  def setRoom(self, room):
    """ Sets a new room for the player.
    room: new room.
    """
    if self.__room != None:
      raise Exception("Error: el item ya tiene un room")
    if room == None:
      raise Exception("Error: habitacion = None")
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
  
  def checkSimilarity(self, item):
    if inventory_item.GGInventoryItem.checkSimilarity(self, item):
      if item.anchor == self.anchor:
        if item.getPosition() == self.getPosition():  
          return True
    return False   
  
  def inventoryOnly(self):
    return False
  
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    clicker.setHeading(GG.utils.getNextDirection(clicker.getPosition(), self.__position))
    
  def tick(self, now):
    """ Call for an update on item.
    Not used at the moment.
    """
    pass
  
  def abandonRoom(self):
    """ Tells a room to remove this item from it.
    """
    self.__room.removeItem(self)
    
  def isStackable(self):
    return False

  def stepOn(self):
    return False
