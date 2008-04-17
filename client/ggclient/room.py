import math
import operator
import utils
import ggmodel

class Room(ggmodel.GGModel):
  """ Room class.
  Defines atributes and methods for a single room.
  """

  def __init__(self, name, id, sprite, spriteFull):
    """ Class constructor.
    name: room label.
    id: identifier.
    sprite: sprite used to paint the room tiles on screen.
    """
    ggmodel.GGModel.__init__(self, name, id, sprite, [0, 0])
    self.__players = []
    self.__blocked = []
    self.__spriteFull = spriteFull
    for i in range(0, utils.SCENE_SZ[0]):
      self.__blocked.append([])
      for j in range(0, utils.SCENE_SZ[1]):
        self.__blocked[i].append(0)
    
  def getPlayerState(self, player):
    """ Returns the player state.
    player: player to check.
    """
    return self.__players[player].getState()
 
  def getBlocked(self, pos):
    """ Checks if a tile is blocked.
    pos: tile position.
    """
    return self.__blocked[pos[0]][pos[2]]
  
  def getSpriteFull(self):
    """ Returns the background image name.
    spriteFull: image name.
    """
    return self.__spriteFull

  def setBlockedTile(self, pos):
    """ Sets a tile as blocked.
    pos: tile position.
    """
    self.__blocked[pos[0]][pos[2]] = 1

  def setUnblockedTile(self, pos):
    """ Sets a tile as unblocked or passable.
    pos: tile position.
    """
    self.__blocked[pos[0]][pos[2]] = 0
    
  def setSpriteFull(self, spriteFull):
    """ Sets a new sprite to be used as background image.
    spriteFull: sprite name.
    """
    self.__spriteFull = spriteFull

  def getNextDirection(self, caller, pos1, pos2):
    """ Returns the direction that the player must follow, according to a rute between 2 points.
    caller: player
    pos1: starting point.
    pos2: ending point.
    """

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
        #if self.__blocked[first[2][0]][first[2][2]] == 0:
          if not self.__players[caller].hasBeenVisited(first[2]):
            return first[0]
    return "standing_down"

  def clickedByPlayer(self, player, target):
    """ Indica que un jugador ha hecho click en una posicion.
    player: jugador.
    target: objetivo del click.
    """
    #if self.__blocked[target[0]][target[2]] == 0:
    for ind in range(self.__players.__len__()):
      if self.__players[ind].getId() == player:
        clickerLabel = self.__players[ind].getName()
          
    if self.getBlocked(target) == 0:
      for ind in range(self.__players.__len__()):
        if self.__players[ind].getId() == player:
          direction = self.getNextDirection(self.__players[ind].getId(), self.__players[ind].getPosition(), target)
          self.__players[ind].setDestination(direction, target)
          self.triggerEvent('click on tile', pl=self.__players[ind].getName(), room=self.getId(), tg=target)
    else:
      for ind2 in range(self.__players.__len__()):
        if self.__players[ind2].getPosition() == target:
          self.__players[ind2].clickedByPlayer(player, clickerLabel, self.getName())
      
  def insertFloor(self, floor):
    """ Sets a new room floor.
    floor: room floor.
    """
    self.__floor = floor

  def insertPlayer(self, player):
    """ Inserts a new player on the room.
    player: new player.
    """
    self.__players.append(player)
    self.setBlockedTile(player.getPosition())

  def isCloser(self, ori, pos, dest):
    """ Checks if "pos2" is closer to "dest" than "ori"
    ori: starting point.
    pos: point to check.
    dest: ending point.
    """
    dist1 = math.sqrt(pow((dest[0] - ori[0]), 2) + pow((dest[2] - ori[2]), 2))
    dist2 = math.sqrt(pow((dest[0] - pos[0]), 2) + pow((dest[2] - pos[2]), 2))
    if dist1 > dist2:
      return 1
    else:
      return 0
    
  def p2pDistance(self, point1, point2):
    """ Returns the distance between two points.
    point1 = starting point.
    point2 = ending point.
    """
    if point1 == point2: return 0
    return '%.3f' % math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[2] - point1[2]), 2))

  def tick(self):
    """ Updates positions and states for all players.
    """
    for player in self.__players:
      direction = self.getNextDirection(player.getId(), player.getPosition(), player.getDestination())
      if direction <> "standing_down":
        pos = player.getPosition()
        self.setUnblockedTile(pos)
        if direction == "walking_up": self.__blocked[pos[0]][pos[2] - 1] = 1
        if direction == "walking_down": self.__blocked[pos[0]][pos[2] + 1] = 1
        if direction == "walking_left": self.__blocked[pos[0] - 1][pos[2]] = 1
        if direction == "walking_right": self.__blocked[pos[0] + 1][pos[2]] = 1
        if direction == "walking_topleft": self.__blocked[pos[0] - 1][pos[2] - 1] = 1
        if direction == "walking_bottomright": self.__blocked[pos[0] + 1][pos[2] + 1] = 1
        if direction == "walking_bottomleft": self.__blocked[pos[0] - 1][pos[2] + 1] = 1
        if direction == "walking_topright": self.__blocked[pos[0] + 1][pos[2] - 1] = 1
        player.tick(direction)