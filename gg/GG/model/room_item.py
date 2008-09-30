# -*- coding: utf-8 -*-

import GG.utils
import inventory_item
import dMVC.model
import ggsystem

class GGRoomItem(inventory_item.GGInventoryItem):
  """GGRoomItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, anchor, topAnchor, label=None):
    """ Class constructor.
    spriteName: image name.
    anchor: image offset on screen.
    topAnchor: image top offset on screen.
    """
    inventory_item.GGInventoryItem.__init__(self, spriteName, label)
    self.anchor = anchor
    self.topAnchor = [topAnchor[0] , GG.utils.TILE_SZ[1] + anchor[1] + topAnchor[1]]
    self.__room = None
    self.__tile = None
    self.points = 0

  def objectToPersist(self):
    dict = inventory_item.GGInventoryItem.objectToPersist(self)
    dict["anchor"] = self.anchor
    dict["topAnchor"] = self.topAnchor
    if self.__tile:
      dict["position"] = self.__tile.getPosition()
    else:
      dict["position"] = [-1,-1]
    if self.__room:
      dict["room"] = self.__room.label
    else:
      dict["room"] = None
    return dict

  def load(self, dict): 
    inventory_item.GGInventoryItem.load(self, dict)
    self.anchor = dict["anchor"]
    self.topAnchor = dict["topAnchor"]
    if "room" in dict.keys():
      myRoom = ggsystem.GGSystem.getInstance().getRoom(dict["room"])
    else:
      myRoom = None
    self.__room = myRoom
    self.__tile = None
    self.points = 0

  def getItemBuildPackage(self):    
    """ Returns info used to build the item.
    """  
    infoPackage = {}
    infoPackage["position"] = self.getPosition() 
    infoPackage["imagepath"] = self.getImagePath()
    return infoPackage

  def copyObject(self):
    """ Creates and returns a copy of this item.
    """  
    copy = GGRoomItem(self.spriteName ,self.anchor, self.topAnchor)
    return copy
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.inventory_item.GGInventoryItem.variablesToSerialize(self)
    return parentVars + ['anchor', 'topAnchor', 'points']

  def getOptions(self):
    """ Returns the item's available options.
    """
    return []

  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    dic = {"Position": self.__tile.position}
    return dic  
        
  def getImageLabel(self):
    """ Returns the item image sprite name.
    """  
    return self.spriteName

  def setPoints(self, points):
    """ Sets a new points value for this item.
    points: new points value.
    """  
    self.points = points
      
  # self.__tile

  def getItemsOnMyTile(self):
    return self.__tile.getItems()
  
  def getTile(self):
    """ Returns the tile that this item is located in.
    """  
    return self.__tile
  
  def setTile(self, tile):
    """ Sets a new tile for this item.
    tile: new item's tile.
    """  
    self.__tile = tile
    
  def getPosition(self):
    """ Returns the item position.
    """
    return self.__tile.position
  
  def setPosition(self, pos, jump=None):
    """ Sets a new position for the item.
    pos: new position.
    jump: enables the player to jump to the new position.
    """
    listItems = self.getRoom().getTile(pos).getItems()
    oldListItems = self.getRoom().getTile(self.getPosition()).getItems()
    if pos == self.__tile.position:
      return
    old = self.__tile.position
    self.__room.moveItem(self.__tile.position, pos, self)
    if not jump:
      self.triggerEvent('position', position=pos, oldPosition=old, itemList=listItems, oldItemList=oldListItems)
    else:
      self.triggerEvent('jumpOver', position=pos, oldPosition=old, itemList=listItems, oldItemList=oldListItems)

  def setStartPosition(self, pos):
    """ Sets a new start position for the item.
    pos: new position.
    """
    if self.__tile.position == pos:
      return
    self.__room.moveItem(self.__tile.position, pos, self)
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
    if room:
      roomLabel = room.getName()
    else:
      roomLabel = None
    self.triggerEvent('room', room=room, roomLabel = roomLabel)

  def changeRoom(self, room, pos):
    """ Changes the item's room.
    room: new room.
    pos: starting position on the new room.
    """
    oldRoom = self.getRoom()
    if oldRoom:
      oldRoom.removeItem(self)
    room.addItemFromVoid(self, pos)
    self.triggerEvent('roomChanged', oldRoom=oldRoom)
    
  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent, position=None, imagePath=None, image=None):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    room: item's room.
    parent: isoview hud handler.
    position: item position.
    image: default item image.
    """
    import GG.isoview.isoview_item
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent, position, imagePath, image)
  
  def inventoryOnly(self):
    """ checks if this is an inventory only item.
    """  
    return False
  
  def clickedBy(self, clicker):
    """ Triggers an event when the item receives a click by a player.
    clicker: player who clicks.
    """
    clickerPos = clicker.getPosition()
    selfPos = self.getPosition()
    if clickerPos != selfPos:
      clicker.setHeading(GG.utils.getNextDirection(clickerPos, selfPos))
      if not GG.utils.checkNeighbour(clickerPos, self.__tile.position):
        direction = self.__room.getNextDirection(self.__tile.position, clickerPos)
        destination = GG.utils.getFrontPosition(self.__tile.position, direction[0], self.__room.size)
        if destination != clickerPos and destination != [-1, -1]:
          clicker.setDestination(destination)
      if clicker.getAccessMode():
        clicker.setSelectedItem(self)
    
  def tick(self, now):
    """ Call for an update on item. Do NOT delete.
    Not used at the moment.
    """
    pass
  
  def abandonRoom(self):
    """ Tells a room to remove this item from it.
    """
    self.__room.removeItem(self)
    
  def isStackable(self):
    """ Checks if this is an stackable item or not.
    """  
    return False

  def stepOn(self):
    """ Checks if other items can be placed on top of this one.
    """  
    return False

  def labelChange(self, oldLabel, newLabel):
    """ DO NOT delete.
    """  
    pass  

  def isTopItem(self):
    """ Checks if this is the top item on the tile.
    """  
    if self.__tile.getTopItem() == self:
      return True
    else:
      return False    
