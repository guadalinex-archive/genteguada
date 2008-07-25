# -*- coding: iso-8859-15 -*-

import random
import operator
import GG.utils
import GG.model.ggmodel
import GG.model.tile
import GG.model.inventory_item
import GG.model.chat_message
import dMVC.model
import GG.model.player

class GGRoom(GG.model.ggmodel.GGModel):
  """ Room class.
  Defines atributes and methods for a single room.
  """

  def __init__(self, spriteFull, label, size, maxUsers):
    """ Class constructor.
    spriteFull: sprite used to paint the room floor on screen.
    label: room label.
    """
    GG.model.ggmodel.GGModel.__init__(self)
    self.spriteFull = spriteFull
    self.size = size
    self.label = label
    self.maxUsers = maxUsers
    self.__tiles = []
    for i in range(0, self.size[0]):
      line = []  
      for j in range(0, self.size[1]):
        image = "tiles/" + self.spriteFull[random.randint(0,len(self.spriteFull)-1)]  
        line.append(GG.model.tile.Tile([i, 0, j], image, [0, 0], self))
      self.__tiles.append(line)  
    self.__items = []
    self.__specialTiles = []
    self.__population = 0
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['spriteFull', 'size', 'label', 'maxUsers']

  def getPopulation(self):
    return self.__population

  def isFull(self):
    if self.__population >= self.maxUsers:
      return True
    else:
      return False    

  def getTile(self, pos):
    return self.__tiles[pos[0]][pos[2]]  

  def getTiles(self):
    return self.__tiles

  def getItemTile(self, item):
    if item in self.__items:
      pos = item.getPosition()
      return self.__tiles[pos[0]][pos[2]]
    return None                        
  
  def moveItem(self, pos1, pos2, item):
    self.__tiles[pos1[0]][pos1[2]].unstackItem()
    self.__tiles[pos2[0]][pos2[2]].stackItem(item)
    item.setTile(self.__tiles[pos2[0]][pos2[2]])
    
  # self.__items

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
        if isinstance(item, GG.model.player.GGPlayer):
          self.__population += 1    
        self.__tiles[item.getPosition()[0]][item.getPosition()[2]].stackItem(item)
      self.triggerEvent('items', items=items)
      return True
    return False

  def addItemFromVoid(self, item, pos):
    if not item in self.__items:
      if isinstance(item, GG.model.player.GGPlayer):
        self.__population += 1    
      self.__tiles[pos[0]][pos[2]].stackItem(item)
      item.setTile(self.__tiles[pos[0]][pos[2]])
      item.setStartPosition(item.getTile().position)
      self.__items.append(item)
      item.setRoom(self)
      self.triggerEvent('addItemFromVoid', item=item)
      return True
    return False
  
  def addItemFromInventory(self, item, pos):
    if not item in self.__items:
      if not self.__tiles[pos[0]][pos[2]].stepOn():
        return
      self.__tiles[pos[0]][pos[2]].stackItem(item)
      item.setTile(self.__tiles[pos[0]][pos[2]])
      item.setStartPosition(item.getTile().position)
      self.__items.append(item)
      item.setRoom(self)
      item.setPlayer(None)
      self.triggerEvent('addItemFromInventory', item=item, room=self)
      return True
    return False
    
  def removeItem(self, item):
    """ Removes an item from the room.
    item: player.
    """
    if item in self.__items:
      if isinstance(item, GG.model.player.GGPlayer):
        self.__population -= 1
      pos = item.getPosition()
      self.__tiles[pos[0]][pos[2]].unstackItem()
      self.__items.remove(item)
      item.clearRoom()
      self.triggerEvent('removeItem', item=item)
      return
    raise Exception("Error: item no eliminado")

  def exitPlayer(self, item):
    """ Removes an item from the room.
    item: player.
    """
    self.removeItem(item)
    """
    self.__population -= 1
    pos = item.getPosition()
    self.__tiles[pos[0]][pos[2]].unstackItem()
    self.__items.remove(item)
    item.clearRoom()
    self.triggerEvent('removeItem', item=item)
    """
    
  def getSpecialTiles(self):
    return self.__specialTiles

  def setSpecialTile(self, position, imageName):
    k = 0
    for tile in self.__specialTiles:
      if tile[0] == position:
        k = 1
        tile[1] = imagename
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
    if self.__tiles[pos[0]][pos[2]].getDepth() != 0:
      return True
    return False
    
  def clickedByPlayer(self, player, target, item):
    """ Indicates players inside that a player has made click on another one.
    player: active player.
    target: position the active player clicked on.
    """
    print "--->>> ", player, target, item
    player.setUnselectedItem()
    print "--->>> A"
    if item != None:
      print "--->>> B"  
      item.clickedBy(player)
    else:
      print "--->>> C"  
      if player.getPosition() != target:
        print "--->>> D"  
        bottom = self.getTile(target).getBottomItem()
        if bottom:
          print "--->>> E"  
          bottom.clickedBy(player)
        else:
          print "--->>> F"  
          if not GG.utils.checkNeighbour(target, player.getPosition()) and self.getNextDirectionForAnItem(target, player.getPosition()) == "none":
            print "--->>> G"  
            player.newChatMessage("No puedo llegar hasta ese lugar.", 2)
            return
          player.setDestination(target)
          
  def getNextDirection(self, player, pos1, pos2):
    """ Gets the direction of a player's movement between 2 points.
    player:
    pos1: starting point.
    pos2: ending point.
    """
    startingDistance = GG.utils.p2pDistance(pos1, pos2)
    
    direction = []
    direction.append([pos1[0], pos1[1], pos1[2] - 1]) #up
    direction.append([pos1[0], pos1[1], pos1[2] + 1]) #down
    direction.append([pos1[0] - 1, pos1[1], pos1[2]]) #left
    direction.append([pos1[0] + 1, pos1[1], pos1[2]]) #right
    direction.append([pos1[0] - 1, pos1[1], pos1[2] - 1]) #topleft
    direction.append([pos1[0] + 1, pos1[1], pos1[2] + 1]) #bottomright
    direction.append([pos1[0] - 1, pos1[1], pos1[2] + 1]) #bottomleft
    direction.append([pos1[0] + 1, pos1[1], pos1[2] - 1]) #topright
    
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
      if (0 <= first[2][0] < self.size[0]) and (0 <= first[2][2] < GG.utils.SCENE_SZ[1]):
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
    direction.append([pos1[0], pos1[1], pos1[2] - 1]) #up
    direction.append([pos1[0], pos1[1], pos1[2] + 1]) #down
    direction.append([pos1[0] - 1, pos1[1], pos1[2]]) #left
    direction.append([pos1[0] + 1, pos1[1], pos1[2]]) #right
    direction.append([pos1[0] - 1, pos1[1], pos1[2] - 1]) #topleft
    direction.append([pos1[0] + 1, pos1[1], pos1[2] + 1]) #bottomright
    direction.append([pos1[0] - 1, pos1[1], pos1[2] + 1]) #bottomleft
    direction.append([pos1[0] + 1, pos1[1], pos1[2] - 1]) #topright
    
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
      if (0 <= first[2][0] < self.size[0]) and (0 <= first[2][2] < GG.utils.SCENE_SZ[1]):
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
      if isinstance(item, GG.model.player.GGPlayer):
        result.append(item)
    return result

  def newChatMessage(self, message, player, type):
    """ Triggers a new avent after receiving a new chat message.
    """
    self.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(message, player.username, \
                    GG.utils.TEXT_COLOR["black"], player.getPosition(), type))    
    
  def getEmptyCell(self):
    listCell = []
    for corx in range(self.size[0]):
      for corz in range(self.size[1]):
        if not self.__tiles[corx][corz].getDepth():
          listCell.append([corx, 0, corz])
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
    return self.__tiles[pos[0]][pos[2]].getTopItem()
    
  def setUnselectedtFor(self, item):
    for player in self.__items:
      if isinstance(player, GG.model.player.GGPlayer):
        if player.getSelected() == item:
          player.setUnselectedItem()  
