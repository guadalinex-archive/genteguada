# -*- coding: utf-8 -*-

import os
import copy
import time
import random
import operator
import GG.utils
import ggmodel
import tile
import chat_message
import dMVC.model
import dMVC.synchronized
import player

class GGRoom(ggmodel.GGModel):
  """ Room class.
  Defines atributes and methods for a single room.
  """

  def __init__(self, spriteFull, label, size, maxUsers, enabled, startRoom):
    """ Class constructor.
    spriteFull: sprite used to paint the room floor on screen.
    label: room label.
    size: room size.
    maxUsers: maximum users number on this room.
    enabled: sets this room as enabled or disabled for common users.
    startRoom: sets this room as a start room or not.
    """
    ggmodel.GGModel.__init__(self)
    self.spriteFull = spriteFull
    self.size = size
    self.label = label
    self.maxUsers = maxUsers
    self.__tiles = []
    for i in range(0, self.size[0]):
      line = []  
      for j in range(0, self.size[1]):
        image = os.path.join(GG.utils.TILE, self.spriteFull[random.randint(0, len(self.spriteFull)-1)])  
        line.append(tile.Tile([i, j], image, self))
      self.__tiles.append(line)  
    self.__items = []
    self.__specialTiles = []
    self.__population = 0
    self.__enabled = enabled
    self.__startRoom = startRoom
    self.save("room")

  def objectToPersist(self):
    dict = ggmodel.GGModel.objectToPersist(self)
    dict["spriteFull"] = self.spriteFull
    dict["label"] = self.label
    dict["size"] = self.size
    dict["maxUsers"] = self.maxUsers
    dict["enabled"] = self.__enabled
    dict["startRoom"] = self.__startRoom
    dict["specialTiles"] = self.__specialTiles
    itemsToPersist = []
    for item in self.__items:
      if not isinstance(item, player.GGPlayer):
        itemsToPersist.append(item.objectToPersist())
    dict["items"] = itemsToPersist
    tilesToPersist = []
    for listTile in self.__tiles:
      for tile in listTile:
        dictTile = {}
        dictTile["position"] = tile.position
        dictTile["spriteName"] = tile.spriteName
        tilesToPersist.append(dictTile)
    dict["tiles"] = tilesToPersist
    return dict

  def load(self, dict):
    ggmodel.GGModel.load(self, dict)
    self.spriteFull = dict["spriteFull"]
    self.label = dict["label"] 
    self.size = dict["size"] 
    self.maxUsers = dict["maxUsers"] 
    self.__enabled = dict["enabled"]
    self.__startRoom = dict["startRoom"]  
    self.__specialTiles = dict["specialTiles"] 
    self.__population = 0
    self.__tiles = []
    self.__items = []
    for i in range(0, self.size[0]):
      line = []  
      for j in range(0, self.size[1]):
        image = os.path.join(GG.utils.TILE, self.spriteFull[random.randint(0, len(self.spriteFull)-1)])  
        line.append(tile.Tile([i, j], image, self))
      self.__tiles.append(line)  
    for dataTile in dict["tiles"]:
      self.__tiles[dataTile["position"][0]][dataTile["position"][1]].setImage(dataTile["spriteName"],True)
    for itemDict in dict["items"]:
      item = ggmodel.GGModel.read(itemDict["id"], "room", itemDict)
      pos = itemDict["position"]
      self.__tiles[pos[0]][pos[1]].stackItem(item)
      item.setTile(self.__tiles[pos[0]][pos[1]])
      item.setStartPosition(item.getTile().position)
      self.__items.append(item)
      item.setRoom(self)

  def getRoomBuildPackage(self):
    """ Returns all info used to create the room's view.
    """  
    infoPackage = {}
    infoPackage["tiles"] = self.getTiles()
    infoPackage["specialtiles"] = self.getSpecialTiles()
    infoPackage["positionitems"] = self.getPositionItems()
    populatedtiles = []
    for x in range(len(self.__tiles)):
      for y in range(len(self.__tiles[x])):
        if self.__tiles[x][y].getDepth() > 1:
          populatedtiles.append([[x, y], self.__tiles[x][y].getItems()])
    infoPackage["populatedtiles"] = populatedtiles 
    return infoPackage
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['spriteFull', 'size']

  @dMVC.synchronized.synchronized(lockName='accessLabel')
  def getName(self):
    """ Returns the room label.
    """  
    return self.label
  
  @dMVC.synchronized.synchronized(lockName='accessLabel')
  def setName(self, name):
    """ Sets a new room label.
    name: room label.
    """  
    self.label = name    

  @dMVC.synchronized.synchronized(lockName='accessMaxUser')
  def getMaxUsers(self):
    """ Returns the room label.
    """  
    return self.maxUsers
  
  @dMVC.synchronized.synchronized(lockName='accessMaxUser')
  def setMaxUsers(self, maxUser):
    """ Sets a new room label.
    name: room label.
    """  
    self.maxUsers = maxUser    

  @dMVC.synchronized.synchronized(lockName='accessPopulation')
  def getPopulation(self):
    """ Returns the current population of this room.
    """  
    return self.__population

  @dMVC.synchronized.synchronized(lockName='accessPopulation')
  def __incPopulation(self):
    """ Returns the current population of this room.
    """  
    self.__population += 1

  @dMVC.synchronized.synchronized(lockName='accessPopulation')
  def __decPopulation(self):
    """ Returns the current population of this room.
    """  
    self.__population -= 1

  @dMVC.synchronized.synchronized(lockName='accessEnabled')
  def getEnabled(self):
    """ Returns the room's state.
    """  
    return self.__enabled

  @dMVC.synchronized.synchronized(lockName='accessEnabled')
  def setEnabled(self, enabled):
    """ Sets this room as enabled/disabled.
    enabled: new enabled value.
    """  
    self.__enabled = enabled    

  @dMVC.synchronized.synchronized(lockName='accessStartRoom')
  def getStartRoom(self):
    """ Returns the startRoom flag.
    """  
    return self.__startRoom

  @dMVC.synchronized.synchronized(lockName='accessStartRoom')
  def setStartRoom(self, value):
    """ Sets a new startRoom flag value.
    value: new value.
    """  
    self.__startRoom = value    

  @dMVC.synchronized.synchronized(lockName='accessPopulation')
  def isFull(self):
    """ Checks if this room is already full or not.
    """  
    if self.__population >= self.getMaxUsers():
      return True
    else:
      return False    

  def getTile(self, pos):
    """ Returns an specific tile.
    pos: tile position.
    """  
    return self.__tiles[pos[0]][pos[1]]  

  def getTiles(self):
    """ Returns the tile mesh.
    """  
    return self.__tiles

  def moveItem(self, pos1, pos2, item):
    """ Moves an item from one position to another.
    pos1: starting position.
    pos2: ending position.
    item: item to be moved.
    """  
    self.__tiles[pos1[0]][pos1[1]].unstackItem()
    self.__tiles[pos2[0]][pos2[1]].stackItem(item)
    item.setTile(self.__tiles[pos2[0]][pos2[1]])
    
  def getItems(self):
    """ Return the items shown on the room.
    """
    return self.__items

  def setItems(self, items):
    """ Sets a new items list on the room.
    items: item list.
    """
    if not self.__items == items:
      self.__items = items
      for item in self.__items:
        if isinstance(item, player.GGPlayer):
          self.__incPopulation()
        self.__tiles[item.getPosition()[0]][item.getPosition()[1]].stackItem(item)
      self.triggerEvent('items', items=items)
      self.save("room")
      return True
    return False

  def getPositionItems(self):
    """ Returns the room items data.
    """  
    items = []
    for item in self.__items:
      dictItem = {"obj": item, "position": item.getPosition(), "imagePath": item.getImagePath(), "image":item.getSpriteName()}
      items.append(dictItem)
    return items

  def addItemFromVoid(self, item, pos):
    """ Adds a new item to the room from nowhere.
    item: new item.
    pos: item's position.
    """  
    if not item in self.__items:
      self.__tiles[pos[0]][pos[1]].stackItem(item)
      item.setTile(self.__tiles[pos[0]][pos[1]])
      item.setStartPosition(item.getTile().position)
      self.__items.append(item)
      item.setRoom(self)
      self.triggerEvent('addItemFromVoid', item=item, itemList = self.__tiles[pos[0]][pos[1]].getItems())
      if isinstance(item, player.GGPlayer):
        self.__incPopulation()
      else:
        self.save("room")
      return True
    return False
  
  def addItemFromInventory(self, item, pos):
    """ Adds a new item to the room from player's inventory.
    item: new item.
    pos: item's position.
    """  
    if not item in self.__items:
      if not self.__tiles[pos[0]][pos[1]].stepOn():
        return
      self.__tiles[pos[0]][pos[1]].stackItem(item)
      item.setTile(self.__tiles[pos[0]][pos[1]])
      item.setStartPosition(item.getTile().position)
      self.__items.append(item)
      item.setRoom(self)
      item.setPlayer(None)
      self.triggerEvent('addItemFromInventory', item=item, room=self, itemList = self.__tiles[pos[0]][pos[1]].getItems())
      self.save("room")
      return True
    return False
    
  def removeItem(self, item):
    """ Removes an item from the room.
    item: item to be removed.
    """
    if item in self.__items:
      pos = item.getPosition()
      self.__tiles[pos[0]][pos[1]].unstackItem()
      self.__items.remove(item)
      item.clearRoom()
      self.triggerEvent('removeItem', item=item)
      if isinstance(item, player.GGPlayer):
        self.__decPopulation()
      else:
        self.save("room")

  def exitPlayer(self, item):
    """ Exits a player from the game.
    item: player.
    """
    self.__decPopulation()
    pos = item.getPosition()
    itemList = self.__tiles[pos[0]][pos[1]].getItemsAndRemoveFrom(item)
    itemList.remove(item)
    for upItem in itemList:
      self.__tiles[pos[0]][pos[1]].stackItem(upItem)  
    self.triggerEvent('updateScreenPos', position=pos)
    self.__items.remove(item)
    item.clearRoom()
    item.setState(GG.utils.STATE[1])
    self.triggerEvent('removeItem', item=item)
    
  def getSpecialTiles(self):
    """ Return the special tiles list.
    """  
    return self.__specialTiles

  def setSpecialTile(self, position, imageName):
    """ Changes a tile's image.
    position: tile position.
    imageName: image file name.
    """  
    k = 0
    for checkedTile in self.__specialTiles:
      if checkedTile[0] == position:
        k = 1
        checkedTile[1] = imageName
    if k == 0:
      self.__specialTiles.append([position, imageName])
    self.getTile(position).setImage(imageName)
    self.save("room")
      
  @dMVC.model.localMethod
  def defaultView(self, screen, hud):
    """ Creates a view object associated with this room.
    screen: screen handler.
    hud: isoview hud object.
    """
    import GG.isoview.isoview_room
    return GG.isoview.isoview_room.IsoViewRoom(self, screen, hud)

  def getBlocked(self, pos):
    """ Checks if a tile is blocked or not.
    pos: tile position.
    """
    if (0 <= pos[0] < self.size[0]) and (0 <= pos[1] < self.size[1]):
      if self.__tiles[pos[0]][pos[1]].getDepth() != 0:
        return True
      else:
        return False
    else:
      return True
    
  def clickedByPlayer(self, clickerPlayer, target, item):
    """ Applies a player's click over an item.
    clickerPlayer: active player.
    target: position the active player clicked on.
    item: item that the player clicked on.
    """
    if item:
      if not item == clickerPlayer.getSelected():
        clickerPlayer.setUnselectedItem()
        item.clickedBy(clickerPlayer)
    else:
      clickerPlayer.setUnselectedItem()
      if clickerPlayer.getPosition() != target:
        bottom = self.getTile(target).getBottomItem()
        if bottom:
          bottom.clickedBy(clickerPlayer)
        else:
          if not self.getNextDirection(clickerPlayer.getPosition(), target)[0]:
            clickerPlayer.newChatMessage("No puedo llegar hasta ese lugar.", 2)
            return
          clickerPlayer.setDestination(target)
  
  def clickedTileByAdmin(self, player, target):
    """ Applies an admin's click over an item.
    player: admin.
    target: position the admin clicked on.
    """
    player.setUnselectedItem()
    player.setSelectedItemWithoutHighlight(self.__tiles[target[0]][target[1]])
  
  def __getPossibleDirection(self, pos):
    """ Gets all possible headings for an item, based on room size and blocked tiles.
    pos: item position.
    """  
    result = {}
    if not self.getBlocked([pos[0], pos[1] - 1]):
      result["up"] = [pos[0], pos[1] - 1]
    if not self.getBlocked([pos[0] - 1, pos[1] - 1]):
      result["topleft"] = [pos[0] - 1, pos[1] - 1]
    if not self.getBlocked([pos[0] + 1, pos[1] - 1]):
      result["topright"] = [pos[0] + 1, pos[1] - 1]
    if not self.getBlocked([pos[0], pos[1] + 1]):
      result["down"] = [pos[0], pos[1] + 1]
    if not self.getBlocked([pos[0] - 1, pos[1] + 1]):
      result["bottomleft"] = [pos[0] - 1, pos[1] + 1]
    if not self.getBlocked([pos[0] + 1, pos[1] + 1]):
      result["bottomright"] = [pos[0] + 1, pos[1] + 1]
    if not self.getBlocked([pos[0] - 1 , pos[1]]):
      result["left"] = [pos[0] - 1 , pos[1]]
    if not self.getBlocked([pos[0] + 1, pos[1]]):
      result["right"] = [pos[0] + 1 , pos[1]]
    return result

  def getNextDirection(self, pos1, pos2, player=None):
    """ Gets the direction of a player's movement between 2 points.
    pos1: starting point.
    pos2: ending point.
    player: moving player.
    """
    startingDistance = GG.utils.p2pDistance(pos1, pos2)
    listDirection = self.__getPossibleDirection(pos1)
    dist = []
    for key in listDirection.keys():
      if listDirection[key] == pos2:
        return key, listDirection[key] 
      dist.append([key, GG.utils.p2pDistance(listDirection[key], pos2), listDirection[key]])
    dist = sorted(dist, key=operator.itemgetter(1), reverse=False)
    for dataDist in dist:
      if player:
        if not player.hasBeenVisited(dataDist[2]):
          if dataDist[1] < startingDistance:
            return dataDist[0], dataDist[2]
      else:
        if dataDist[1] < startingDistance:
          return dataDist[0], dataDist[2]
    return None, None  

  def tick(self, now):
    """ Calls for an update on all player movements.
    now: current timestamp.
    """
    for item in self.__items:
      item.tick(now)

  def getPlayers(self):
    """ Returns the players list.
    """
    result = []
    for item in self.__items:
      if isinstance(item, player.GGPlayer):
        result.append(item)
    return result

  def newChatMessage(self, message, player, msgType):
    """ Triggers a new event after receiving a new chat message.
    message: new chat message.
    player: message emitter.
    msgType: message type.
    """
    header = time.strftime("%H:%M", time.localtime(time.time())) + " [" + player.username + "]: "
    self.triggerEvent('chatAdded', message=chat_message.ChatMessage(message, player.username, GG.utils.TEXT_COLOR["black"], player.getPosition(), msgType), text=message, header=header)    
    
  def getEmptyCell(self):
    """ Returns a list with the room's empty cells.
    """  
    listCell = []
    for corx in range(self.size[0]):
      for corz in range(self.size[1]):
        if not self.__tiles[corx][corz].getDepth():
          listCell.append([corx, corz])
    return listCell        

  def getNearestEmptyCell(self, pos):
    """ Returns the nearest empty cell to a position.
    pos: start position.
    """
    if not (pos[0] > self.size[0] or pos[1] > self.size[1]) and not self.getBlocked(pos):
      return pos
    emptyCell = self.getEmptyCell()
    if len(emptyCell) == 0:
      return None
    dist = None 
    point = None
    for emptyPos in emptyCell:
      newDist = GG.utils.p2pDistance(emptyPos, pos)
      if dist is None or dist > newDist:
        dist = newDist
        point = emptyPos
    return point
      
  def getItemOnPosition(self, pos):
    """ Returns the top item on a room's position.
    pos: room's position.
    """  
    return self.__tiles[pos[0]][pos[1]].getTopItem()
    
  def getSelecter(self, selectee):
    """ Returns selected item's selecter.
    selectee: selected item.
    """  
    selec = None
    for item in self.__items:
      if isinstance(item, player.GGPlayer):
        selec = item.getSelected()
        if selec == selectee:
          return item  

  def editRoom(self, maxUsers, newLabel, enabled, startRoom, newTile):
    """ Sets the room attributes with new values.
    maxUsers: new maxUsers value.
    newLabel: new room label.
    enabled: sets the room as enabled or disabled.
    startRoom: sets the room as starter room or not.
    newTile: sets a new tile design for the room floor.
    """  
    self.setMaxUsers(maxUsers)
    self.setName(newLabel)
    self.__enabled = self.setEnabled(enabled)
    self.__startRoom = self.setStartRoom(startRoom)
    if len(newTile):
      tilesList = []
      for x in range(len(self.__tiles)):
        subList = []
        for y in range(len(self.__tiles[x])):
          singleTile = newTile[random.randint(0, len(newTile)-1)]
          imgName = os.path.join(GG.utils.TILE, singleTile)
          self.__tiles[x][y].setImage(imgName, True)
          subList.append(singleTile)  
        tilesList.append(subList)  
      self.triggerEvent('floorChanged', newTile=tilesList)
    self.save("room")
        
  def labelChange(self, oldLabel, newLabel):
    """ Propagates a room label change all over its items.
    oldLabel: old room label.
    newLabel: new room label.
    """  
    for singleItem in self.__items:
      singleItem.labelChange(oldLabel, newLabel)
      self.save("room")
    
  def moveStack(self, newPos, item):
    """ Moves an item and any other item above him to a new position.
    newPos: new position.
    item: selected item.
    """  
    pos = item.getPosition()
    itemsList = self.__tiles[pos[0]][pos[1]].getItemsFrom(item)  
    for singleItem in itemsList:
      singleItem.setPosition(newPos)
      self.moveItem(singleItem.getPosition(), newPos, singleItem)  
      self.save("room")
    
  def tileImageChange(self, tilePos, image):
    """ Calls for an update on a tile image.
    tilePos: tile position.
    image: new tile image.
    """  
    self.save("room")
    self.triggerEvent("tileImageChange", pos=tilePos, image=image)

  def unselectedItemOtherPlayers(self, item, player = None):
    otherPlayers = self.getPlayers()
    for otherPlayer in otherPlayers:
      if not otherPlayer.username == player.username: 
        if otherPlayer.getSelected() == item:
          otherPlayer.setUnselectedItem()

