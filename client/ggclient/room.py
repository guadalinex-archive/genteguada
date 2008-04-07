import operator
from model import *

class Room(Model):
  """ Clase Room.
  Define atributos y metodos de una habitacion.
  """

  def __init__(self, name, id, sprite, spriteFull):
    """ Constructor de la clase.
    name: etiqueta de la habitacion.
    id: identificador.
    sprite: grafico asignado a las baldosas de la habitacion.
    """
    Model.__init__(self, name, id, sprite, [0, 0])
    self.players = []
    self.items = []
    self.blocked = []
    self.spriteFull = spriteFull
    for i in range(0, SCENE_SZ[0]):
      self.blocked.append([])
      for j in range(0, SCENE_SZ[1]):
        self.blocked[i].append(0)
    
  def getPlayerState(self, player):
    """ Devuelve el estado en el que se encuentra un jugador.
    player: jugador a consultar.
    """
    return self.players[player].getState()
 
  def getBlocked(self, pos):
    """ Indica si una celda esta libre o bloqueada.
    pos: posicion de la celda.
    """
    return self.blocked[pos[0]][pos[2]]
  
  def getSpriteFull(self):
    """ Devuelve el nombre del grafico de la habitacion completa.
    spriteFull: grafico a devolver.
    """
    return self.spriteFull

  def getNextDirection(self, caller, pos1, pos2):
    """ Obtiene la siguiente posicion en el trayecto de un jugador entre 2 puntos.
    caller: jugador
    pos1: posicion de inicio.
    pos2: posicion de destino.
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
      if (pos2 == dir[i]) and (0 <= dir[i][0] <= SCENE_SZ[0]) and (0 <= dir[i][2] <= SCENE_SZ[1]):
        if self.blocked[dir[i][0]][dir[i][2]] == 0:
          return DIR[i+1]
    
    dist = []
    for i in range(0, len(dir)):
      dist.append([DIR[i+1], self.p2pDistance(dir[i], pos2), dir[i]])
    dist = sorted(dist, key=operator.itemgetter(1), reverse=True)
    while len(dist) > 0:
      first = dist.pop()
      if (1 <= first[2][0] <= SCENE_SZ[0]) and (0 <= first[2][2] <= SCENE_SZ[1]):
        if self.blocked[first[2][0]][first[2][2]] == 0:
          if not self.players[caller].hasBeenVisited(first[2]):
            return first[0]
    return "standing_down"

  def setPlayerDestination(self, player, destination):
    """ Indiva el destino del movimiento de un jugador.
    player: jugador.
    destination: destino del movimiento.
    """
    if self.blocked[destination[0]][destination[2]] == 0:
      for ind in range(self.players.__len__()):
        if self.players[ind].getId() == player:
          direction = self.getNextDirection(self.players[ind].getId(), self.players[ind].getPosition(), destination)
          self.players[ind].setDestination(direction, destination)

  def setBlockedTile(self, pos):
    """ Pone una celda de la habitacion como bloqueada al paso.
    pos: posicion de la celda.
    """
    self.blocked[pos[0]][pos[2]] = 1

  def setUnblockedTile(self, pos):
    """ Pone una celda de la habitacion como vacia, permitiendo el paso.
    pos: posicion de la celda.
    """
    self.blocked[pos[0]][pos[2]] = 0


  def insertFloor(self, floor):
    """ Asigna el suelo de la habitacion.
    floor: suelo de la habitacion.
    """
    self.floor = floor

  def insertPlayer(self, player):
    """ Asigna un jugador a la habitacion.
    player: jugador a asignar.
    """
    self.players.append(player)

  def insertItem(self, item):
    """ Asigna un item no jugador a la habitacion.
    player: objeto a asignar.
    """
    self.items.append(item)

  def isCloser(self, ori, pos, dest):
    """ Indica si la posicion "pos2" esta mas cerca de "dest" que "ori". \
    Todas las coordenadas son puntos 3d.
    ori: punto de origen.
    pos: punto a comprobar.
    dest: punto de destino.
    """
    dist1 = math.sqrt(pow((dest[0] - ori[0]), 2) + pow((dest[2] - ori[2]), 2))
    dist2 = math.sqrt(pow((dest[0] - pos[0]), 2) + pow((dest[2] - pos[2]), 2))
    if dist1 > dist2:
      return 1
    else:
      return 0
    
  def p2pDistance(self, point1, point2):
    """ Obtiene la distancia entre dos puntos.
    point1 = punto inicial.
    point2 = punto final.
    """
    if point1 == point2: return 0
    return '%.3f' % math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[2] - point1[2]), 2))

  def notify(self):
    """ Indica a las vistas asignadas que se ha producido un cambio.
    """
    self.notify_views(id)
    for player in self.players:
      player.notify()  
  
  def tick(self):
    """ Realiza las llamadas para actualizar posiciones y estados para todos \
    los jugadores asignados.
    """
    for player in self.players:
      direction = self.getNextDirection(player.getId(), player.getPosition(), player.getDestination())
      if direction <> "standing_down":
        pos = player.getPosition()
        self.blocked[pos[0]][pos[2]] = 0
        if direction == "walking_up": self.blocked[pos[0]][pos[2] - 1] = 1
        if direction == "walking_down": self.blocked[pos[0]][pos[2] + 1] = 1
        if direction == "walking_left": self.blocked[pos[0] - 1][pos[2]] = 1
        if direction == "walking_right": self.blocked[pos[0] + 1][pos[2]] = 1
        if direction == "walking_topleft": self.blocked[pos[0] - 1][pos[2] - 1] = 1
        if direction == "walking_bottomright": self.blocked[pos[0] + 1][pos[2] + 1] = 1
        if direction == "walking_bottomleft": self.blocked[pos[0] - 1][pos[2] + 1] = 1
        if direction == "walking_topright": self.blocked[pos[0] + 1][pos[2] - 1] = 1
        player.tick(direction)