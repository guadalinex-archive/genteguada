import math
import operator
import utils
import model

class Room(model.Model):
  """ Clase Room.
  Define atributos y metodos de una habitacion.
  """

  def __init__(self, name, id, sprite, spriteFull):
    """ Constructor de la clase.
    name: etiqueta de la habitacion.
    id: identificador.
    sprite: grafico asignado a las baldosas de la habitacion.
    """
    model.Model.__init__(self, name, id, sprite, [0, 0])
    self._players = []
    self._blocked = []
    self._spriteFull = spriteFull
    for i in range(0, utils.SCENE_SZ[0]):
      self._blocked.append([])
      for j in range(0, utils.SCENE_SZ[1]):
        self._blocked[i].append(0)
    
  def getPlayerState(self, player):
    """ Devuelve el estado en el que se encuentra un jugador.
    player: jugador a consultar.
    """
    return self._players[player].getState()
 
  def getBlocked(self, pos):
    """ Indica si una celda esta libre o bloqueada.
    pos: posicion de la celda.
    """
    return self._blocked[pos[0]][pos[2]]
  
  def getSpriteFull(self):
    """ Devuelve el nombre del grafico de la habitacion completa.
    spriteFull: grafico a devolver.
    """
    return self._spriteFull

  def setBlockedTile(self, pos):
    """ Pone una celda de la habitacion como bloqueada al paso.
    pos: posicion de la celda.
    """
    self._blocked[pos[0]][pos[2]] = 1

  def setUnblockedTile(self, pos):
    """ Pone una celda de la habitacion como vacia, permitiendo el paso.
    pos: posicion de la celda.
    """
    self._blocked[pos[0]][pos[2]] = 0
    
  def _setSpriteFull(self, spriteFull):
    """ Asigna un sprite para mostrar en el fondo.
    spriteFull: nombre del sprite.
    """
    self._spriteFull = spriteFull

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
      if (pos2 == dir[i]) and (0 <= dir[i][0] <= utils.SCENE_SZ[0]) and (0 <= dir[i][2] <= utils.SCENE_SZ[1]):
        if self._blocked[dir[i][0]][dir[i][2]] == 0:
          return utils.DIR[i+1]
    
    dist = []
    for i in range(0, len(dir)):
      dist.append([utils.DIR[i+1], self.p2pDistance(dir[i], pos2), dir[i]])
    dist = sorted(dist, key=operator.itemgetter(1), reverse=True)
    while len(dist) > 0:
      first = dist.pop()
      if (1 <= first[2][0] <= utils.SCENE_SZ[0]) and (0 <= first[2][2] <= utils.SCENE_SZ[1]):
        if self._blocked[first[2][0]][first[2][2]] == 0:
          if not self._players[caller].hasBeenVisited(first[2]):
            return first[0]
    return "standing_down"

  def clickedByPlayer(self, player, target):
    """ Indica que un jugador ha hecho click en una posicion.
    player: jugador.
    target: objetivo del click.
    """
    #if self._blocked[target[0]][target[2]] == 0:
    for ind in range(self._players.__len__()):
      if self._players[ind].getId() == player:
        clickerLabel = self._players[ind].getName()
          
    if self.getBlocked(target) == 0:
      for ind in range(self._players.__len__()):
        if self._players[ind].getId() == player:
          direction = self.getNextDirection(self._players[ind].getId(), self._players[ind].getPosition(), target)
          self._players[ind].setDestination(direction, target)
          self.triggerEvent('click on tile', pl=self._players[ind].getName(), room=self._id, tg=target)
    else:
      for ind2 in range(self._players.__len__()):
        posAux = self._players[ind2].getPosition()
        posAux2 = [posAux[0], posAux[1], posAux[2]]
        if posAux2 == target:
          self._players[ind2].clickedByPlayer(player, clickerLabel, self.getName())
      
  def insertFloor(self, floor):
    """ Asigna el suelo de la habitacion.
    floor: suelo de la habitacion.
    """
    self._floor = floor

  def insertPlayer(self, player):
    """ Asigna un jugador a la habitacion.
    player: jugador a asignar.
    """
    self._players.append(player)
    self.setBlockedTile(player.getPosition())

  def insertItem(self, item):
    """ Asigna un item no jugador a la habitacion.
    player: objeto a asignar.
    """
    self._items.append(item)

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
    self._notify_views(id)
    for player in self._players:
      player.notify()  
  
  def tick(self):
    """ Realiza las llamadas para actualizar posiciones y estados para todos \
    los jugadores asignados.
    """
    for player in self._players:
      direction = self.getNextDirection(player.getId(), player.getPosition(), player.getDestination())
      if direction <> "standing_down":
        pos = player.getPosition()
        self._blocked[pos[0]][pos[2]] = 0
        if direction == "walking_up": self._blocked[pos[0]][pos[2] - 1] = 1
        if direction == "walking_down": self._blocked[pos[0]][pos[2] + 1] = 1
        if direction == "walking_left": self._blocked[pos[0] - 1][pos[2]] = 1
        if direction == "walking_right": self._blocked[pos[0] + 1][pos[2]] = 1
        if direction == "walking_topleft": self._blocked[pos[0] - 1][pos[2] - 1] = 1
        if direction == "walking_bottomright": self._blocked[pos[0] + 1][pos[2] + 1] = 1
        if direction == "walking_bottomleft": self._blocked[pos[0] - 1][pos[2] + 1] = 1
        if direction == "walking_topright": self._blocked[pos[0] + 1][pos[2] - 1] = 1
        player.tick(direction)