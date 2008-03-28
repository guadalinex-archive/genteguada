import operator
from model import *

class Room(Model):
  """ Clase Room.
  Define atributos y metodos de una habitacion.
  """

  def __init__(self, name, id, sprite):
    """ Constructor de la clase.
    name: etiqueta de la habitacion.
    id: identificador.
    sprite: grafico asignado a las baldosas de la habitacion.
    """
    Model.__init__(self, name, id, sprite, [0, 0])
    self.players = []
    self.items = []
    self.blocked = []
    for i in range(0, SCENE_SZ[0]):
      self.blocked.append([])
      for j in range(0, SCENE_SZ[1]):
        self.blocked[i].append(0)
        
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

  def getPlayerState(self, player):
    """ Devuelve el estado en el que se encuentra un jugador.
    player: jugador a consultar.
    """
    return self.players[player].getState()
 
  def setPlayerDestination(self, player, destination):
    """ Indiva el destino del movimiento de un jugador.
    player: jugador.
    destination: destino del movimiento.
    """
    for ind in range(self.players.__len__()):
      if self.players[ind].getId() == player:
        #self.players[ind].setDestination(destination)
        self.players[ind].setDestination(self.getNextDirection(self.players[ind].getPosition(), destination), destination)

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

  def getBlocked(self, pos):
    """ Indica si una celda esta libre o bloqueada.
    pos: posicion de la celda.
    """
    return self.blocked[pos[0]][pos[2]]
    
  def getNextDirection(self, pos1, pos2):
    """ Obtiene la siguiente posicion en el trayecto entre 2 puntos.
    pos1: posicion de inicio.
    pos2: posicion de destino.
    """
    
    directions = []
    directions.append([pos1[0], pos1[1], pos1[2] - 1]) #up
    directions.append([pos1[0], pos1[1], pos1[2] + 1]) #down
    directions.append([pos1[0] - 1, pos1[1], pos1[2]]) #left
    directions.append([pos1[0] + 1, pos1[1], pos1[2]]) #right
    directions.append([pos1[0] - 1, pos1[1], pos1[2] - 1]) #topleft
    directions.append([pos1[0] + 1, pos1[1], pos1[2] + 1]) #bottomright
    directions.append([pos1[0] - 1, pos1[1], pos1[2] + 1]) #bottomleft
    directions.append([pos1[0] + 1, pos1[1], pos1[2] - 1]) #topright
    
    if pos1 == pos2: return "standing_down"
    
    if pos2 == directions[0]:
       print pos1, " to ", pos2, " direction *** 1"
       return "walking_up"
    if pos2 == directions[1]:
       print pos1, " to ", pos2, " direction *** 2"
       return "walking_down"
    if pos2 == directions[2]:
       print pos1, " to ", pos2, " direction *** 3"
       return "walking_left"
    if pos2 == directions[3]:
       print pos1, " to ", pos2, " direction *** 4"
       return "walking_right"

    if pos2 == directions[4]:
       print pos1, " to ", pos2, " direction *** 5"
       return "walking_topleft"
    if pos2 == directions[5]:
       print pos1, " to ", pos2, " direction *** 6"
       return "walking_bottomright"
    if pos2 == directions[6]:
       print pos1, " to ", pos2, " direction *** 7"
       return "walking_bottomleft"
    if pos2 == directions[7]:
       print pos1, " to ", pos2, " direction *** 8"
       return "walking_topright"
            
    dict = [("walking_up", self.p2pDistance(directions[0], pos2), directions[0]), \
      ("walking_down", self.p2pDistance(directions[1], pos2), directions[1]), \
    ("walking_left", self.p2pDistance(directions[2], pos2), directions[2]), \
    ("walking_right", self.p2pDistance(directions[3], pos2), directions[3]), \
    ("walking_topleft", self.p2pDistance(directions[4], pos2), directions[4]), \
    ("walking_bottomright", self.p2pDistance(directions[5], pos2), directions[5]), \
    ("walking_bottomleft", self.p2pDistance(directions[6], pos2), directions[6]), \
    ("walking_topright", self.p2pDistance(directions[7], pos2), directions[7])]
        
    distances = sorted(dict, key=operator.itemgetter(1), reverse=True)
    
    while distances.__len__() > 0:
      first = distances.pop()
      if 0 < first[2][0] < SCENE_SZ[0]:
        if 0 < first[2][2] < SCENE_SZ[1]:
          if self.blocked[first[2][0]][first[2][2]] == 0:
            print pos1, " >> ", pos2, " >>", first[0]
            return first[0]
    return "standing down"

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
      player.tick(self.getNextDirection(player.getPosition(), player.getDestination()))  