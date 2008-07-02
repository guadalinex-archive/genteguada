import GG.model.room_item
import GG.isoview.isoview_item
import dMVC.model

class GGDoorRoom5b(GG.model.room_item.GGRoomItem):
  """ GGDoorRoom5b class.
  Defines a teleporter object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    exitPosition: teleporter exit position on the new room.
    position: teleporter position.
    anchor: image anchor on screen.
    destinationRoom: room the teleporter will carry players to.
    """
    GG.model.room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor)
    self.__exitPosition = exitPosition
    self.__destinationRoom = destinationRoom
    self.points = 10
    self.label = label
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']    
      
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["open"]    
      
  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteName
    
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
  
  def clickedBy(self, clicker):
    """ Triggers an event when the teleporter receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    if not clicker.checkPointGiver("Penguin Quiz"):
      self.newChatMessage('Antes de pasar, debes responder al acertijo de Andatuz.')
      return False
    else:
      clicker.addPoints(self.points, self.label)
      clicker.changeRoom(self.__destinationRoom, self.__exitPosition)
    
  def newChatMessage(self, message):
    """ Triggers a new event after receiving a new chat message.
    message: new chat message.
    """
    self.getRoom().triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(message, 'Puerta misteriosa', \
                    GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))

