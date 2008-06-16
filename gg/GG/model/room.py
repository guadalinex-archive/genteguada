import operator
import GG.utils
import GG.model.ggmodel
import GG.model.inventory_item
import GG.model.chat_message
#import GG.model.inventory_only_item
import GG.isoview.isoview_room
import dMVC.model
import GG.model.player

class GGRoom(GG.model.ggmodel.GGModel):
  """ Room class.
  Defines atributes and methods for a single room.
  """

  def __init__(self, spriteFull, label, size):
    """ Class constructor.
    spriteFull: sprite used to paint the room floor on screen.
    label: room label.
    """
    GG.model.ggmodel.GGModel.__init__(self)
    self.spriteFull = spriteFull
    self.size = size
    self.__items = []
    self.__specialTiles = []
    self.label = label # Variable para realizar pruebas, sera eliminada
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['spriteFull', 'size']

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
      self.triggerEvent('items', items=items)
      return True
    return False

  def addItemFromVoid(self, item, pos):
    """
    if isinstance(item, GG.model.inventory_only_item.GGInventoryOnlyItem):
      del item
      return True
    """  
    if not item in self.__items:
      item.setStartPosition(None)
      item.setStartPosition(self.getNearestEmptyCell(pos))
      self.__items.append(item)
      item.setRoom(self)
      self.triggerEvent('addItemFromVoid', item=item)
      return True
    return False
  
  def addItemFromInventory(self, item, pos):
    """
    if isinstance(item, GG.model.inventory_only_item.GGInventoryOnlyItem):
      del item
      return True
    """  
    if not item in self.__items:
      item.setStartPosition(None)
      item.setStartPosition(self.getNearestEmptyCell(pos))
      self.__items.append(item)
      #if item.getRoom() == self:
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
      item.clearRoom()
      self.__items.remove(item)
      self.triggerEvent('removeItem', item=item)
      return
    raise Exception("Error: item no eliminado")

  def setSpecialTile(self, position, imageName):
    k = 0
    for tile in self.__specialTiles:
      if tile[0] == position:
        k = 1
        tile[1] = imagename
        print "1"
        self.triggerEvent('setSpecialTile', position=position, imageName=imageName)
    if k == 0:
      print "2"  
      self.__specialTiles.append([position, imageName])
      print "2A"  
      self.triggerEvent('setSpecialTile', position=position, imageName=imageName)
      print "2B"  
      
  @dMVC.model.localMethod
  def defaultView(self, screen, hud):
    """ Creates a view object associated with this room.
    screen: screen handler.
    hud: isoview hud object.
    """
    return GG.isoview.isoview_room.IsoViewRoom(self, screen, hud)

  def getBlocked(self, pos):
    """ Checks if a tile is blocked or not.
    pos: tile position.
    """
    for item in self.__items:
      if item.getPosition() == pos:
        return True
    return False  
  
  def clickedByPlayer(self, player, target):
    """ Indicates players inside that a player has made click on another one.
    player: active player.
    target: position the active player clicked on.
    """
    #print target, player.getPosition(), player.getDestination()
    player.setUnselectedItem()
    if not self.getBlocked(target) and player.getPosition != target:
      #direction = self.getNextDirection(player, player.getPosition(), target)
      player.setDestination(target)
    else:
      for item in self.__items:
        if item.getPosition() == target:
          item.clickedBy(player)
          
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
      for cory in range(self.size[1]):
        point = [corx,0,cory]
        if not self.getBlocked(point):
          listCell.append(point)
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
      newDist = GG.utils.distPoints([emptyPos[0], emptyPos[2]], [pos[0], pos[2]])
      if dist is None or dist > newDist:
        dist = newDist
        point = emptyPos
    return point
      
      
    """
    retVar = None
    if pos[2] > 0:
      auxPos = [pos[0], pos[1], pos[2] - 1]
      res = self.getNearestEmptyCell(auxPos)
      if res != None:
        retVar = res
    elif pos[2] < (GG.utils.SCENE_SZ[1] - 1):
      auxPos = [pos[0], pos[1], pos[2] + 1]
      res = self.getNearestEmptyCell(auxPos)
      if res != None:
        retVar = res

    elif pos[0] > 0:
      auxPos = [pos[0] - 1, pos[1], pos[2]]
      res = self.getNearestEmptyCell(auxPos)
      if res != None:
        retVar = res
    elif pos[0] < (GG.utils.SCENE_SZ[0] - 1):
      auxPos = [pos[0] + 1, pos[1], pos[2]]
      res = self.getNearestEmptyCell(auxPos)
      if res != None:
        retVar = res

    elif (pos[0] > 0) and (pos[2] > 0):
      auxPos = [pos[0] - 1, pos[1], pos[2] - 1]
      res = self.getNearestEmptyCell(auxPos)
      if res != None:
        retVar = res
    elif (pos[2] < (GG.utils.SCENE_SZ[1] - 1)) and (pos[0] < (GG.utils.SCENE_SZ[0] - 1)):
      auxPos = [pos[0] + 1, pos[1], pos[2] + 1]
      res = self.getNearestEmptyCell(auxPos)
      if res != None:
        retVar = res
    elif (pos[0] > 0) and (pos[0] < (GG.utils.SCENE_SZ[0] - 1)):
      auxPos = [pos[0] - 1, pos[1], pos[2] + 1]
      res = self.getNearestEmptyCell(auxPos)
      if res != None:
        retVar = res
    elif (pos[0] < (GG.utils.SCENE_SZ[0] - 1)) and (pos[2] > 0):
      auxPos = [pos[0] + 1, pos[1], pos[2] - 1]
      res = self.getNearestEmptyCell(auxPos)
      if res != None:
        retVar = res
    else:
      retVar = False
    
    return retVar
    """
