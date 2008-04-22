import math
import operator
import utils
import ggmodel
import isoview_room

class GGRoom(ggmodel.GGModel):
  """ Room class.
  Defines atributes and methods for a single room.
  """

  def __init__(self, spriteFull):
    """ Class constructor.
    name: room label.
    id: identifier.
    sprite: sprite used to paint the room tiles on screen.
    """
    ggmodel.GGModel.__init__(self)
    self.__players = []
    self.__items = []
    self.__spriteFull = spriteFull
    self.__blocked = []

  def getSpriteFull(self):
    return self.__spriteFull
  
  def insertPlayer(self, player):
    self.__players.append(player)
    player.setCurrentRoom(self)
    self.setBlockedTile(player.getPosition())

  def insertItem(self, item):
    self.__items.append(item)
    self.setBlockedTile(item.getPosition())

  def defaultView(self, screen):
    return isoview_room.IsoViewRoom(self, screen)
  
  def getPlayers(self):
    return self.__players
  
  def getItems(self):
    return self.__items

  def getBlocked(self, pos):
    return pos in self.__blocked
  
  def setBlockedTile(self, pos):
    self.__blocked.append(pos)

  def setUnblockedTile(self, pos):
    self.__blocked.remove(pos)

  def clickedByPlayer(self, player, target):
    """ Indica que un jugador ha hecho click en una posicion.
    player: jugador.
    target: objetivo del click.
    """
    clickerLabel = player.getUsername()
    if not self.getBlocked(target):
      direction = self.getNextDirection(player, player.getPosition(), target)
      player.setDestination(direction, target)
      #self.triggerEvent('click on tile', pl=player.getUsername(), room=self, tg=target)
    else:
      for ind2 in range(self.__players.__len__()):
        if self.__players[ind2].getPosition() == target:
          self.__players[ind2].clickedBy(player)
          
    
  def getNextDirection(self, player, pos1, pos2):
    if pos1 == pos2: return "standing_down"

    dir = []
    dir.append([pos1[0], pos1[1], pos1[2] - 1]) #up
    dir.append([pos1[0], pos1[1], pos1[2] + 1]) #down
    dir.append([pos1[0] - 1, pos1[1], pos1[2]]) #left
    dir.append([pos1[0] + 1, pos1[1], pos1[2]]) #right
    dir.append([pos1[0] - 1, pos1[1], pos1[2] - 1]) #topleft
    dir.append([pos1[0] + 1, pos1[1], pos1[2] + 1]) #bottomright
    dir.append([pos1[0] - 1, pos1[1], pos1[2] + 1]) #bottomleft
    dir.append([pos1[0] + 1, pos1[1], pos1[2] - 1]) #topright
    
    for i in range(0, len(dir)):
      if (pos2 == dir[i]) and (0 <= dir[i][0] <= utils.SCENE_SZ[0]) and (0 <= dir[i][2] <= utils.SCENE_SZ[1]):
        if self.getBlocked(dir[i]) == 0:
          return utils.DIR[i+1]
    
    dist = []
    for i in range(0, len(dir)):
      dist.append([utils.DIR[i+1], self.p2pDistance(dir[i], pos2), dir[i]])
    dist = sorted(dist, key=operator.itemgetter(1), reverse=True)
    while len(dist) > 0:
      first = dist.pop()
      if (0 <= first[2][0] <= utils.SCENE_SZ[0]) and (0 <= first[2][2] <= utils.SCENE_SZ[1]):
        if self.getBlocked(first[2]) == 0:
          if not player.hasBeenVisited(first[2]):
            return first[0]
    return "standing_down"  
    
    
  def isCloser(self, ori, pos, dest):
    dist1 = math.sqrt(pow((dest[0] - ori[0]), 2) + pow((dest[2] - ori[2]), 2))
    dist2 = math.sqrt(pow((dest[0] - pos[0]), 2) + pow((dest[2] - pos[2]), 2))
    if dist1 > dist2:
      return 1
    else:
      return 0
    
  def p2pDistance(self, point1, point2):
    if point1 == point2: return 0
    return '%.3f' % math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[2] - point1[2]), 2))
  
    
  def tick(self):
    for player in self.__players:
      direction = self.getNextDirection(player, player.getPosition(), player.getDestination())
      if direction <> "standing_down":
        pos = player.getPosition()
        self.setUnblockedTile(pos)
        if direction == "walking_up": self.setBlockedTile([pos[0], pos[1], pos[2] - 1])
        if direction == "walking_down": self.setBlockedTile([pos[0], pos[1], pos[2] + 1])
        if direction == "walking_left": self.setBlockedTile([pos[0] - 1, pos[1], pos[2]])
        if direction == "walking_right": self.setBlockedTile([pos[0] + 1, pos[1], pos[2]])
        if direction == "walking_topleft": self.setBlockedTile([pos[0] - 1, pos[1], pos[2] - 1])
        if direction == "walking_bottomright": self.setBlockedTile([pos[0] + 1, pos[1], pos[2] + 1])
        if direction == "walking_bottomleft": self.setBlockedTile([pos[0] - 1, pos[1], pos[2] + 1])
        if direction == "walking_topright": self.setBlockedTile([pos[0] + 1, pos[1], pos[2] - 1])
        player.tick(direction)  
    
    
    
    
  """    
  def getPlayerState(self, player):
    return self.__players[player].getState()
 
  
  
  def setUnblockedTile(self, pos):
    self.__blocked[pos[0]][pos[2]] = 0
    self.__blocked.delete([2, 4])
    
  def setSpriteFull(self, spriteFull):
    self.__spriteFull = spriteFull

  

          

      
  def insertFloor(self, floor):
    self.__floor = floor



  
  
  """