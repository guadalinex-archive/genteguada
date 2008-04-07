from item import *
import ggcommon.eventos

class Player(Item):
  """ Clase Player.
  Define el comportamiento de un item jugador.
  """
 
  def __init__(self, name, id, sprite, size, position):
    """ Constructor de la clase.
    name: etiqueta de la clase.
    id: identificador del jugador.
    sprite: grafico que representa al jugador.
    size: tamano del grafico del jugador.
    position: posicion en la que se encuentra el jugador.
    """
    Item.__init__(self, name, id, sprite, size, position)
    self.state = "standing_down"
    self.stateFrame = 0
    self.destination = position
    self.visited = []
        
  def getPosition(self):
    """ Devuelve la posicion en la que se encuentra el jugador.
    """
    return self.position
 
  def getState(self):
    """ Devuelve la animacion en la que se encuentra el jugador.
    """
    return self.state

  def getStateFrame(self):
    """ Devuelve el estado de la animacion en la que se encuentra el jugador.
    """
    return self.stateFrame

  def getId(self):
    """ Devuelve el identificador del jugador.
    """
    return self.id

  def getDir(self):
    """ Devuelve el codigo de direccion de movimiento del jugador.
    """
    for i in range (1, len(DIR)+1):
      if self.state == DIR[i]:
        return i
    return 0  

  def getDestination(self):
    """ Devuelve el destino del movimiento.
    """
    return self.destination
        
  def setName(self, name):
    self.name = name
    self.triggerEvent('name', name=self.name)
      
  def setPosition(self, position):
    """ Asigna una nueva posicion a un jugador.
    position: posicion del jugador.
    """
    if self.destination == position:
      self.visited = []
    self.visited.append(position)
    pActualAux = self.position
    self.position = position
    self.triggerEvent('position', id=self.id, sprite=self.sprite, \
                        pActual=pActualAux, pDestin=self.position, dir=self.state)
    
  def setDestination(self, state, destination):
    """ Asigna un punto de destino al movimiento del jugador.
    state: direccion del siguiente movimiento.
    destiantion: destino del movimiento.
    """
    self.state = state
    self.destination = destination
    
  def hasBeenVisited(self, pos):
    """ Indica si una celda ha sido visitada en el ultimo movimiento del jugador.
    pos: posicion de la celda a comprobar.
    """
    for i in range(0, len(self.visited)):
      if self.visited[i] == pos:
        return 1
    return 0
    
  def tick(self, direction):
    """ Procedimiento que actualiza posiciones de movimientos, e incrementa \
    el estado de las animaciones en las que se encuentren los jugadores.
    direction: direccion del siguiente movimiento.
    """
    if self.position == self.destination:
      self.state = "standing_down"
      return
    if self.state <> "standing_down":
      pos = self.getPosition()
      self.state = direction
      if self.state == "walking_up":
        next = [pos[0], pos[1], pos[2] - 1]
      if self.state == "walking_down":
        next = [pos[0], pos[1], pos[2] + 1]
      if self.state == "walking_left":
        next = [pos[0] - 1, pos[1], pos[2]]
      if self.state == "walking_right":
        next = [pos[0] + 1, pos[1], pos[2]]
      if self.state == "walking_topleft":
        next = [pos[0] - 1, pos[1], pos[2] - 1]
      if self.state == "walking_bottomright": 
        next = [pos[0] + 1, pos[1], pos[2] + 1]
      if self.state == "walking_bottomleft":
        next = [pos[0] - 1, pos[1], pos[2] + 1]
      if self.state == "walking_topright":
        next = [pos[0] + 1, pos[1], pos[2] - 1]
      self.setPosition(next)
      