# -*- coding: utf-8 -*-

import time
import room_item
import dMVC.model
import GG.utils
import chat_message
import ggsystem

class GGTeleport(room_item.GGRoomItem):
  """ GGTeleport class.
  Defines a teleporter object behaviour.
  """
 
  def __init__(self, sprite, exitPosition, destinationRoom, label):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    """
    room_item.GGRoomItem.__init__(self, sprite, label)
    self.__exitPosition = exitPosition
    self.__destinationRoom = destinationRoom
    self.points = 10
    
  def objectToPersist(self):
    dict = room_item.GGRoomItem.objectToPersist(self)
    dict["exitPosition"] = self.__exitPosition
    dict["destinationRoom"] = self.__destinationRoom
    return dict

  def load(self, dict):
    room_item.GGRoomItem.load(self, dict)
    self.__exitPosition = dict["exitPosition"] 
    self.__destinationRoom = dict["destinationRoom"] 
    self.points = 10

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGTeleport(self.spriteName, self.__exitPosition, self.__destinationRoom, self.getName())
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["open"]    
      
  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    adminDict = room_item.GGRoomItem.getAdminActions(self)
    adminDict["Etiqueta"] = [self.getName()]
    if self.__destinationRoom:
      adminDict["Habitacion destino"] = [self.__destinationRoom]
    else:
      adminDict["Habitacion destino"] = [""]
    adminDict["Posicion salida"] = self.__exitPosition
    return adminDict    

  def applyChanges(self, fields, player, room):
    keys = fields.keys()
    if "Etiqueta" in keys:
      oldLabel = self.getName()
      newLabel = fields["Etiqueta"]
      if self.setName(newLabel):
        ggsystem.GGSystem.getInstance().labelChange(oldLabel, newLabel)
    if "Habitacion destino" in keys:
      destRoom = ggsystem.GGSystem.getInstance().getRoom(fields["Habitacion destino"])
      if not destRoom:
        player.newChatMessage('Valor "Habitacion destino" incorrecto', 1)
        return None  
      else:
        self.setDestinationRoom(fields["Habitacion destino"]) 
    if "Posicion salida" in keys:
      try: 
        posX = int(fields["Posicion salida"][0])
        posY = int(fields["Posicion salida"][1])    
      except ValueError:
        player.newChatMessage('Valor "Posicion salida" incorrecto', 1)
        return None
      roomSize = ggsystem.GGSystem.getInstance().getRoom(self.getDestinationRoom()).size
      if 0 < posX < roomSize[0] and  0 < posY < roomSize[1]: 
        self.setExitPosition([posX, posY])
      else:
        player.newChatMessage('Valor "Posicion salida" incorrecto', 1)
        return None
    return room_item.GGRoomItem.applyChanges(self, fields, player, room)

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
  def defaultView(self, screen, room, parent, position=None, imagePath=None, image=None):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    position: item position.
    image: item default image.
    """
    import GG.isoview.isoview_item
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent, position, imagePath, image)
  
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

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    self.transportTo(clicker)

  def transportTo(self, clicker):
    """ Teleports a player to another location.
    clicker: player to be teleported.
    """  
    destinationRoom = ggsystem.GGSystem.getInstance().getRoom(self.__destinationRoom)
    if not destinationRoom:
      clicker.newChatMessage("La habitacion de destino no existe", 1)
      return
    if destinationRoom.isFull():
      clicker.newChatMessage("La habitacion esta completa. Volvere a intentarlo mas tarde", 1)
      return
    if not destinationRoom.getEnabled() and not clicker.getAccessMode():
      clicker.newChatMessage("La habitacion esta bloqueada. Volvere a intentarlo mas tarde", 1)
      return
    clicker.addPoints(self.points, self.getName())
    itemList = clicker.getTile().getItemsFrom(clicker)
    finalPosition = destinationRoom.getNearestEmptyCell(self.__exitPosition)
    for item in itemList:
      item.changeRoom(destinationRoom, finalPosition)
    clicker.setUnselectedItem()  
      
  def labelChange(self, oldLabel, newLabel):
    """ Changes the destination room label if necessary.
    oldLabel: old label.
    newLabel: new label.
    """  
    if self.__destinationRoom == oldLabel:
      self.__destinationRoom = newLabel      


class GGDoorWithKey(GGTeleport):
  """ GGDoorWithKey class.
  Defines a locked door object behaviour.
  """

  def __init__(self, sprite, exitPosition, destinationRoom, label, key):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    key: door's key
    """
    GGTeleport.__init__(self, sprite, exitPosition, destinationRoom, label)
    self.__key = key

  def objectToPersist(self):
    dict = GGTeleport.objectToPersist(self)
    dict["key"] = self.__key
    return dict

  def load(self, dict):
    GGTeleport.load(self, dict)
    self.__key = dict["key"]

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGDoorWithKey(self.spriteName, self.getExitPosition(), self.getDestinationRoom(), self.getName(), self.__key)

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    if not clicker.hasItemLabeledInInventory(self.__key):
      clicker.newChatMessage('Necesitas ' + self.__key + ' para poder pasar', 2)  
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
    dict["Key"] = [self.__key]
    return dict
    
# ===============================================================

class GGDoorPressedTiles(GGTeleport):
  """ GGDoorPressedTiles class.
  Defines a door with pressed tiles behaviour.
  """

  def __init__(self, sprite, exitPosition, destinationRoom, label, pressedTiles):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    pressedTiles: tiles that need to be pressed to open the door.
    """
    GGTeleport.__init__(self, sprite, exitPosition, destinationRoom, label)
    self.__pressedTiles = pressedTiles
    #tile1 = self.getRoom().getTile(pressedTiles[0])
    #tile1.setImage(GG.utils.PRESSED_TILE,True)
    #tile2 = self.getRoom().getTile(pressedTiles[1])
    #tile2.setImage(GG.utils.PRESSED_TILE,True)

  def objectToPersist(self):
    dict = GGTeleport.objectToPersist(self)
    dict["pressedTiles"] = self.__pressedTiles
    return dict

  def load(self, dict):
    GGTeleport.load(self, dict)
    self.__pressedTiles = dict["pressedTiles"]

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGDoorPressedTiles(self.spriteName, self.getExitPosition(), self.getDestinationRoom(), self.getName(), self.__pressedTiles)

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

  def __init__(self, sprite, exitPosition, destinationRoom, label, pointsGiver):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    pointsGiver: item who gave points to the player.
    """
    GGTeleport.__init__(self, sprite, exitPosition, destinationRoom, label)
    self.pointsGiver = pointsGiver 

  def objectToPersist(self):
    dict = GGTeleport.objectToPersist(self)
    dict["pointsGiver"] = self.pointsGiver
    return dict

  def load(self, dict):
    GGTeleport.load(self, dict)
    self.pointsGiver = dict["pointsGiver"]

  def getPointsGiver(self):
    return self.pointsGiver

  def setPointsGiver(self, pointsGiver):
    self.pointsGiver = pointsGiver    

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGDoorOpenedByPoints(self.spriteName, self.getExitPosition(), self.getDestinationRoom(), self.getName(), self.pointsGiver)

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    if not clicker.checkPointGiver(self.pointsGiver):
      self.newChatMessage('No has respondido correctamente a la pregunta de  ' + self.pointsGiver + ' ,no puedo dejarte pasar')
      return False
    self.transportTo(clicker)


class GGDoorOpenedByForo(GGTeleport):
  """ GGDoorOpenedByPoints class.
  Defines a door object opened if the clicker received points from another item.
  """

  def __init__(self, sprite, exitPosition, destinationRoom, label, numEntradasForo):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    exitPosition: teleporter exit position on the new room.
    destinationRoom: room the teleporter will carry players to.
    label: teleporter label.
    """
    GGTeleport.__init__(self, sprite, exitPosition, destinationRoom, label)
    self.numEntradasForo = numEntradasForo 

  def objectToPersist(self):
    dict = GGTeleport.objectToPersist(self)
    dict["numEntradasForo"] = self.numEntradasForo
    return dict

  def load(self, dict):
    GGTeleport.load(self, dict)
    self.numEntradasForo = dict["numEntradasForo"]

  def getNumEntradasForo(self):
    return self.numEntradasForo

  def setNumEntradasForo(self, numEntradasForo):
    self.numEntradasForo = numEntradasForo    

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGDoorOpenedByForo(self.spriteName, self.getExitPosition(), self.getDestinationRoom(), self.getName(), self.numEntradasForo)

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    if not clicker.checkEntradasForo(self.numEntradasForo):
      self.newChatMessage('Si no has participado en el foro ' + str(self.numEntradasForo) + ' o mas veces no puedo dejarte pasar')
      return False
    self.transportTo(clicker)

