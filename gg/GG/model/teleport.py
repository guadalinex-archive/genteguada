# -*- coding: utf-8 -*-

import time
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
    topAnchor: image top offset on screen.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    """
    room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor, label)
    self.__exitPosition = exitPosition
    self.__destinationRoom = destinationRoom
    self.points = 10
    
  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGTeleport(self.spriteName, self.anchor, self.topAnchor, self.__exitPosition, self.__destinationRoom, self.getName())
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["open", "jumpOver"]    
      
  def getAdminActions(self):
    """ Returns the possible admin actions.
    """  
    if self.__destinationRoom:  
      dic = {"Position": self.getTile().position, "DestinationRoom": [self.__destinationRoom.label], \
           "ExitPosition": self.__exitPosition, "Label": [self.getName()]}
    else:
      dic = {"Position": self.getTile().position, "DestinationRoom": [""], \
           "ExitPosition": self.__exitPosition, "Label": [self.getName()]}    
    return dic  
      
  def getImageLabel(self):
    """ Returns the teleporter's image file name.
    """  
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
  def defaultView(self, screen, room, parent, position=None, image=None):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    position: item position.
    image: item default image.
    """
    import GG.isoview.isoview_item
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent, position, image)
  
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
    header = time.strftime("%H:%M", time.localtime(time.time())) + " [" + self.getName() + "]: "
    self.getRoom().triggerEvent('chatAdded', message=chat_message.ChatMessage(message, self.getName(), GG.utils.TEXT_COLOR["black"], self.getPosition(), 2), text=message, header=header)

  def transportTo(self, clicker):
    """ Teleports a player to another location.
    clicker: player to be teleported.
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
    clicker.addPoints(self.points, self.getName())
    itemList = clicker.getTile().getItemsFrom(clicker)
    finalPosition = self.__destinationRoom.getNearestEmptyCell(self.__exitPosition)
    for item in itemList:
      item.changeRoom(self.__destinationRoom, finalPosition)
    clicker.setUnselectedItem()  
      
  def labelChange(self, oldLabel, newLabel):
    """ Changes the destination room label if necessary.
    oldLabel: old label.
    newLabel: new label.
    """  
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
    topAnchor: image top offset on screen.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    """
    GGTeleport.__init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label)

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGDoor(self.spriteName, self.anchor, self.topAnchor, self.getExitPosition(), self.getDestinationRoom(), self.getName())

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
    topAnchor: image top offset on screen.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    key: door's key
    """
    GGTeleport.__init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label)
    self.__key = key

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGDoorWithKey(self.spriteName, self.anchor, self.topAnchor, self.getExitPosition(), self.getDestinationRoom(), self.getName(), self.__key)

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
    """ Changes the destination room label if necessary.
    oldLabel: old label.
    newLabel: new label.
    """  
    GGTeleport.labelChange(self, oldLabel, newLabel)
    if self.__key == oldLabel:
      self.__key = newLabel    
      
      
  def getAdminActions(self):
    """ Returns the possible admin actions.
    """  
    dict = GGTeleport.getAdminActions(self)
    dict["Key": [self.__key]]
    return dict
    
# ===============================================================

class GGDoorPressedTiles(GGTeleport):
  """ GGDoorPressedTiles class.
  Defines a door with pressed tiles behaviour.
  """

  def __init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label, pressedTiles):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    anchor: image offset on screen.
    topAnchor: image top offset on screen.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    pressedTiles: tiles that need to be pressed to open the door.
    """
    GGTeleport.__init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label)
    self.__pressedTiles = pressedTiles

  def getAdminActions(self):
    """ Returns the possible admin actions.
    """  
    dict = GGTeleport.getAdminActions(self)
    index = 1
    for tile in self.__pressedTiles:
      if tile: 
        dict["PressedTile" + str(index)] = tile
      index += 1
    return dict

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGDoorPressedTiles(self.spriteName, self.anchor, self.topAnchor, self.getExitPosition(), self.getDestinationRoom(), self.getName(), self.__pressedTiles)

  def setPressedTile1(self, pos):
    """ Sets the first monitored tile.
    pos: monitored tile position.
    """  
    self.__pressedTiles[0] = pos  
  
  def setPressedTile2(self, pos):
    """ Sets the second monitored tile.
    pos: monitored tile position.
    """  
    self.__pressedTiles[1] = pos  

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    if self.getDestinationRoom().isFull():
      clicker.newChatMessage("La habitacion esta completa. Volvere a intentarlo mas tarde", 1)
      clicker.setUnselectedItem()
      return
    if not GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      return False
    for tile in self.__pressedTiles:
      if tile:  
        if not self.getRoom().getBlocked(tile):
          clicker.newChatMessage('El resorte no esta activado.', 2)  
          clicker.setUnselectedItem()
          return False
    self.transportTo(clicker)

# ===============================================================

class GGDoorOpenedByPoints(GGTeleport):
  """ GGDoorOpenedByPoints class.
  Defines a door object opened if the clicker received points from another item.
  """

  def __init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label, pointsGiver):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    anchor: image offset on screen.
    topAnchor: image top offset on screen.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    pointsGiver: item who gave points to the player.
    """
    GGTeleport.__init__(self, sprite, anchor, topAnchor, exitPosition, destinationRoom, label)
    self.pointsGiver = pointsGiver 

  def getAdminActions(self):
    """ Returns the possible admin actions.
    """  
    dict = GGTeleport.getAdminActions(self)
    dict["PointsGiver"] = [self.pointsGiver]
    return dict

  def getPointsGiver(self):
    return self.pointsGiver

  def setPointsGiver(self, pointsGiver):
    self.pointsGiver = pointsGiver    

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGDoorOpenedByPoints(self.spriteName, self.anchor, self.topAnchor, self.getExitPosition(), self.getDestinationRoom(), self.getName(), self.pointsGiver)

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    if self.getDestinationRoom().isFull():
      clicker.newChatMessage("La habitacion esta completa. Volvere a intentarlo mas tarde", 1)
      return
    if not clicker.checkPointGiver(self.pointsGiver):
      self.newChatMessage('Si no has obtenido puntos de ' + self.pointsGiver + 'no puedo dejarte pasar')
      return False
    self.transportTo(clicker)

