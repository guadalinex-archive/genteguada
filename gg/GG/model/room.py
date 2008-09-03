# -*- coding: utf-8 -*-

import os
import random
import operator
import GG.utils
import ggmodel
import tile
import chat_message
import dMVC.model
import player

class GGRoom(ggmodel.GGModel):
  """ Room class.
  Defines atributes and methods for a single room.
  """

  def __init__(self, spriteFull, label, size, maxUsers):
    """ Class constructor.
    spriteFull: sprite used to paint the room floor on screen.
    label: room label.
    size: room size.
    maxUsers: maximum users number on this room.
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
        image = os.path.join("tiles/", self.spriteFull[random.randint(0, len(self.spriteFull)-1)])  
        line.append(tile.Tile([i, j], image, [0, 0], self))
      self.__tiles.append(line)  
    self.__items = []
    self.__specialTiles = []
    self.__population = 0
    self.__enabled = True
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['spriteFull', 'size', 'label', 'maxUsers']

  def getPopulation(self):
    """ Returns the current population of this room.
    """  
    return self.__population

  def getEnabled(self):
    """ Returns the room's state.
    """  
    return self.__enabled

  def setEnabled(self, enabled):
    """ Sets this room as enabled/disabled.
    enabled: new enabled value.
    """  
    self.__enabled = enabled    

  def isFull(self):
    """ Checks if this room is already full or not.
    """  
    if self.__population >= self.maxUsers:
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

  def getItemTile(self, item):
    """ Returns the tile where a given item is.
    item: given item.
    """  
    if item in self.__items:
      pos = item.getPosition()
      return self.__tiles[pos[0]][pos[1]]
    return None                        
  
  def moveItem(self, pos1, pos2, item):
    """ Moves an item from one position to another.
    pos1: starting position.
    pos2: ending position.
    item: item to be moved.
    """  
    self.__tiles[pos1[0]][pos1[1]].unstackItem()
    self.__tiles[pos2[0]][pos2[1]].stackItem(item)
    item.setTile(self.__tiles[pos2[0]][pos2[1]])
    
  # self.__items

  def getItems(self):
    """ Return the items shown on the room.
    """
    return self.__items

  def getPositionItems(self):
    items = []
    for item in self.__items:
      dictItem = {"obj": item, "position": item.getPosition(), "image": item.getImagePath()}
      items.append(dictItem)
    return items

  def setItems(self, items):
    """ Sets a new items list on the room.
    items: item list.
    """
    if not self.__items == items:
      self.__items = items
      for item in self.__items:
        if isinstance(item, player.GGPlayer):
          self.__population += 1    
        self.__tiles[item.getPosition()[0]][item.getPosition()[1]].stackItem(item)
      self.triggerEvent('items', items=items)
      return True
    return False

  def addItemFromVoid(self, item, pos):
    """ Adds a new item to the room from nowhere.
    item: new item.
    pos: item's position.
    """  
    if not item in self.__items:
      if isinstance(item, player.GGPlayer):
        self.__population += 1    
      self.__tiles[pos[0]][pos[1]].stackItem(item)
      item.setTile(self.__tiles[pos[0]][pos[1]])
      item.setStartPosition(item.getTile().position)
      self.__items.append(item)
      item.setRoom(self)
      self.triggerEvent('addItemFromVoid', item=item)
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
      self.triggerEvent('addItemFromInventory', item=item, room=self)
      return True
    return False
    
  def removeItem(self, item):
    """ Removes an item from the room.
    item: item to be removed.
    """
    if item in self.__items:
      if isinstance(item, player.GGPlayer):
        self.__population -= 1
      pos = item.getPosition()
      self.__tiles[pos[0]][pos[1]].unstackItem()
      self.__items.remove(item)
      item.clearRoom()
      self.triggerEvent('removeItem', item=item)
      return
    raise Exception("Error: item no eliminado")

  def exitPlayer(self, item):
    """ Exits a player from the game.
    item: player.
    """
    self.__population -= 1
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
    #self.removeItem(item)    
    
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
        #self.triggerEvent('setSpecialTile', position=position, imageName=imageName)
    if k == 0:
      self.__specialTiles.append([position, imageName])
      #self.triggerEvent('setSpecialTile', position=position, imageName=imageName)
      
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
    if self.__tiles[pos[0]][pos[1]].getDepth() != 0:
      return True
    return False
    
  def clickedByPlayer(self, clickerPlayer, target, item):
    """ Applies a player's click over an item.
    clickerPlayer: active player.
    target: position the active player clicked on.
    item: item that the player clicked on.
    """
    clickerPlayer.setUnselectedItem()
    if item != None:
      item.clickedBy(clickerPlayer)
    else:
      if clickerPlayer.getPosition() != target:
        bottom = self.getTile(target).getBottomItem()
        if bottom:
          bottom.clickedBy(clickerPlayer)
        else:
          if not GG.utils.checkNeighbour(target, clickerPlayer.getPosition()) and self.getNextDirectionForAnItem(target, clickerPlayer.getPosition()) == "none":
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
          
  def getNextDirection(self, player, pos1, pos2):
    """ Gets the direction of a player's movement between 2 points.
    player: moving player.
    pos1: starting point.
    pos2: ending point.
    """
    startingDistance = GG.utils.p2pDistance(pos1, pos2)
    
    direction = []
    direction.append([pos1[0], pos1[1] - 1]) #up
    direction.append([pos1[0], pos1[1] + 1]) #down
    direction.append([pos1[0] - 1, pos1[1]]) #left
    direction.append([pos1[0] + 1, pos1[1]]) #right
    direction.append([pos1[0] - 1, pos1[1] - 1]) #topleft
    direction.append([pos1[0] + 1, pos1[1] + 1]) #bottomright
    direction.append([pos1[0] - 1, pos1[1] + 1]) #bottomleft
    direction.append([pos1[0] + 1, pos1[1] - 1]) #topright
    for i in range(0, len(direction)):
      if (pos2 == direction[i]) and (0 <= direction[i][0] <= self.size[0]) and (0 <= direction[i][2] <= self.size[1]):
        if self.getBlocked(direction[i]) == 0:
          return GG.utils.HEADING[i+1]
    dist = []
    for i in range(0, len(direction)):
      dist.append([GG.utils.HEADING[i+1], GG.utils.p2pDistance(direction[i], pos2), direction[i]])
    dist = sorted(dist, key=operator.itemgetter(1), reverse=True)
    while len(dist) > 0:
      first = dist.pop()
      if (0 <= first[2][0] < self.size[0]) and (0 <= first[2][1] < self.size[1]):
        if self.getBlocked(first[2]) == 0:
          if not player.hasBeenVisited(first[2]):
            if first[1] < startingDistance:
              return first[0]
    return "none"  
    
  def getNextDirectionForAnItem(self, pos1, pos2):
    """ Gets the direction of an item's movement between 2 points.
    pos1: starting point.
    pos2: ending point.
    """
    startingDistance = GG.utils.p2pDistance(pos1, pos2)
    
    direction = []
    direction.append([pos1[0], pos1[1] - 1]) #up
    direction.append([pos1[0], pos1[1] + 1]) #down
    direction.append([pos1[0] - 1, pos1[1]]) #left
    direction.append([pos1[0] + 1, pos1[1]]) #right
    direction.append([pos1[0] - 1, pos1[1] - 1]) #topleft
    direction.append([pos1[0] + 1, pos1[1] + 1]) #bottomright
    direction.append([pos1[0] - 1, pos1[1] + 1]) #bottomleft
    direction.append([pos1[0] + 1, pos1[1] - 1]) #topright
    for i in range(0, len(direction)):
      if (pos2 == direction[i]) and (0 <= direction[i][0] <= self.size[0]) and (0 <= direction[i][2] <= self.size[1]):
        if self.getBlocked(direction[i]) == 0:
          return GG.utils.HEADING[i+1]
    dist = []
    for i in range(0, len(direction)):
      dist.append([GG.utils.HEADING[i+1], GG.utils.p2pDistance(direction[i], pos2), direction[i]])
    dist = sorted(dist, key=operator.itemgetter(1), reverse=True)
    while len(dist) > 0:
      first = dist.pop()
      if (0 <= first[2][0] < self.size[0]) and (0 <= first[2][1] < self.size[1]):
        if self.getBlocked(first[2]) == 0:
          if first[1] < startingDistance:
            return first[0]
    return "none"    
    
  def tick(self, now):
    """ Calls for an update on all player movements.
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
    self.triggerEvent('chatAdded', message=chat_message.ChatMessage(message, player.username, \
                    GG.utils.TEXT_COLOR["black"], player.getPosition(), msgType))    
    
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
    if not self.getBlocked(pos):
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
    
  def setUnselectedFor(self, item):
    """ Sets an item as unselected.
    item: unselected item.  
    """  
    for itemPlayer in self.__items:
      if isinstance(itemPlayer, player.GGPlayer):
        if itemPlayer.getSelected() == item:
          itemPlayer.setUnselectedItem()  

  def getSelecter(self, selectee):
    """ Returns the selecter of a selectee.
    selectee: selected item.
    """  
    selec = None
    for item in self.__items:
      if isinstance(item, player.GGPlayer):
        selec = item.getSelected()
        if selec == selectee:
          return item  

  def editRoom(self, maxUsers, newLabel, enabled, newTile):
    self.maxUsers = maxUsers
    self.label = newLabel
    self.__enabled = enabled
    if not newTile:
      return
    for x in range(len(self.__tiles)):
      for y in range(len(self.__tiles[x])):
        self.__tiles[x][y].setImage(os.path.join("tiles/", newTile), True)
    self.triggerEvent('floorChanged', newTile=newTile)    
        
  def labelChange(self, oldLabel, newLabel):
    for singleItem in self.__items:
      singleItem.labelChange(oldLabel, newLabel)