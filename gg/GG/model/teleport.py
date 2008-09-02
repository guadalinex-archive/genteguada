# -*- coding: utf-8 -*-

import room_item
import dMVC.model
import GG.utils
import chat_message

class GGTeleport(room_item.GGRoomItem):
  """ GGTeleport class.
  Defines a teleporter object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    anchor: image offset on screen.
    anchor: image top offset on screen.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    """
    room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor)
    self.__exitPosition = exitPosition
    self.__destinationRoom = destinationRoom
    self.points = 10
    self.label = label

  def copyObject(self):
    return GGTeleport(self.spriteName, self.anchor, self.topAnchor, self.__exitPosition, self.__destinationRoom, self.label)
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']    
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["open"]    
      
  def getAdminActions(self):
    """ Returns the possible admin actions.
    """  
    if self.__destinationRoom:  
      dic = {"Position": self.getTile().position, "DestinationRoom": [self.__destinationRoom.label], \
           "ExitPosition": self.__exitPosition, "Label": [self.label]}
    else:
      dic = {"Position": self.getTile().position, "DestinationRoom": [""], \
           "ExitPosition": self.__exitPosition, "Label": [self.label]}    
    return dic  
      
  def getName(self):
    """ Returns the teleporter's label.
    """  
    return self.label
  
  def getImageLabel(self):
    """ Returns the teleporter's image file name.
    """  
    return self.spriteName

  def setLabel(self, newLabel):
    """ Sets a new label for the item.
    """  
    self.label = newLabel  
  
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
      self.triggerEvent('exitPosition', exitPosition=exitPosition)
  
  # self.__destinationRoom
  
  def getDestinationRoom(self):
    """ Returns the room that the teleporter connects to.
    """
    return self.__destinationRoom
  
  def setDestinationRoom(self, destinationRoom):
    """ Sets a new room connected to the teleporter.
    destinationRoom: teleporter's destination room.
    """
    if not self.__destinationRoom == destinationRoom:
      self.__destinationRoom = destinationRoom
      self.triggerEvent('destinationRoom', destinationRoom=destinationRoom)


  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    """
    import GG.isoview.isoview_item
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)
  
  def clickedBy(self, clicker):
    """ Triggers an event when the teleporter receives a click by a player.
    clicker: player who clicks.
    """
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    

  def newChatMessage(self, message):
    """ Triggers a new event after receiving a new chat message.
    message: new chat message.
    """
    self.getRoom().triggerEvent('chatAdded', message=chat_message.ChatMessage(message, self.label, GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))

  def transportTo(self, clicker):
    """ Teleports a player to another location.
    """  
    if not self.__destinationRoom:
      clicker.newChatMessage("La habitacion de destino no existe", 1)
      return
    if self.__destinationRoom.isFull():
      clicker.newChatMessage("La habitacion esta completa. Volvere a intentarlo mas tarde", 1)
      return
    #if not self.__destinationRoom.getEnabled():
    if not self.__destinationRoom.getEnabled() and not clicker.getAccessMode():
      clicker.newChatMessage("La habitacion esta bloqueada. Volvere a intentarlo mas tarde", 1)
      return
    clicker.addPoints(self.points, self.label)
    itemList = clicker.getTile().getItemsFrom(clicker)
    for item in itemList:
      item.changeRoom(self.__destinationRoom, self.__exitPosition)
      
  def labelChange(self, oldLabel, newLabel):
    if self.__destinationRoom == oldLabel:
      self.__destinationRoom = newLabel      

# ===============================================================

class GGDoor(GGTeleport):
  """ GGDoor class.
  Defines a door object behaviour.
  """
 
  def __init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    anchor: image offset on screen.
    anchor: image top offset on screen.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    """
    GGTeleport.__init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label)

  def copyObject(self):
    return GGDoor(self.spriteName, self.anchor, self.topAnchor, self.getExitPosition(), self.getDestinationRoom(), self.label)

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    self.transportTo(clicker)
        
# ===============================================================

class GGDoorWithKey(GGTeleport):
  """ GGDoorWithKey class.
  Defines a locked door object behaviour.
  """

  def __init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label, key):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    anchor: image offset on screen.
    anchor: image top offset on screen.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    key: door's key
    """
    GGTeleport.__init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label)
    self.__key = key

  def copyObject(self):
    return GGDoorWithKey(self.spriteName, self.anchor, self.topAnchor, self.getExitPosition(), self.getDestinationRoom(), self.label, self.__key)

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    if self.getDestinationRoom().isFull():
      clicker.newChatMessage("La habitacion esta completa. Volvere a intentarlo mas tarde", 1)
      return
    if not GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      return False
    if not clicker.hasItemLabeledInInventory(self.__key):
      clicker.newChatMessage('Necesitas ' + self.__key + 'para poder pasar', 2)  
      return False
    self.transportTo(clicker)
  
  def labelChange(self, oldLabel, newLabel):
    GGTeleport.labelChange(self, oldLabel, newLabel)
    if self.__key == oldLabel:
      self.__key = newLabel    

# ===============================================================

class GGDoorPressedTiles(GGTeleport):
  """ GGDoorPressedTiles class.
  Defines a door with pressed tiles behaviour.
  """

  def __init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label, pressedTiles):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    anchor: image offset on screen.
    anchor: image top offset on screen.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    pressedTiles: tiles that need to be pressed to open the door.
    """
    GGTeleport.__init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label)
    self.__pressedTiles = pressedTiles

  def copyObject(self):
    return GGDoorPressedTiles(self.spriteName, self.anchor, self.topAnchor, self.getExitPosition(), self.getDestinationRoom(), self.label, self.__pressedTiles)

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    if self.getDestinationRoom().isFull():
      clicker.newChatMessage("La habitacion esta completa. Volvere a intentarlo mas tarde", 1)
      return
    if not GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      return False
    for tile in self.__pressedTiles:
      if not self.getRoom().getBlocked(tile):
        clicker.newChatMessage('El resorte no esta activado.', 2)  
        return False
    self.transportTo(clicker)

# ===============================================================

class GGDoorRoom5b(GGTeleport):
  """ GGDoorRoom5b class.
  Defines a door object behaviour.
  """

  def __init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    anchor: image offset on screen.
    anchor: image top offset on screen.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    """
    GGTeleport.__init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label)

  def copyObject(self):
    return GGDoorRoom5b(self.spriteName, self.anchor, self.topAnchor, self.getExitPosition(), self.getDestinationRoom(), self.label)

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    if self.getDestinationRoom().isFull():
      clicker.newChatMessage("La habitacion esta completa. Volvere a intentarlo mas tarde", 1)
      return
    if not clicker.checkPointGiver("Penguin Quiz"):
      self.newChatMessage('Antes de pasar, debes responder al acertijo de Andatuz.')
      return False
    self.transportTo(clicker)

