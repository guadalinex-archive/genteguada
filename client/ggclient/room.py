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
    self.name = name
    self.id = id
    self.sprite = sprite
    self.views = []
    self.players = []
    self.items = []

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
        self.players[ind].setDestination(destination)

  def notify(self):
    """ Indica a las vistas asignadas de que se ha producido un cambio.
    """
    self.notify_views(id)
    for player in self.players:
      player.notify()  
  
  def tick(self):
    """ Realiza las llamadas para actualizar posiciones y estados para todos \
    los jugadores asignados.
    """
    for player in self.players:
      player.tick()  