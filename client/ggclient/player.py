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
    self.position = position
    self.triggerEvent('position', id=self.id, sprite=self.sprite, \
                        pActual=self.position, pDestin=self.destination, \
                        dir=self.state)

  def setDestination(self, state, destination):
    """ Asigna un punto de destino al movimiento del jugador.
    state: direccion del siguiente movimiento.
    destiantion: destino del movimiento.
    """
    self.state = state
    self.destination = destination
    self.triggerEvent('destination', id=self.id, sprite=self.sprite, \
                        pActual=self.position, pDestin=self.destination, \
                        dir=self.state)

  def tick(self, state):
    """ Procedimiento que actualiza posiciones de movimientos, e incrementa \
    el estado de las animaciones en las que se encuentren los jugadores.
    state: direccion del siguiente movimiento.
    """
    if self.state == "walking_up" or self.state == "walking_down" or \
    self.state == "walking_left" or self.state == "walking_right" or \
    self.state == "walking_topleft" or self.state == "walking_bottomright" or \
    self.state == "walking_bottomleft" or self.state == "walking_topright":
      pos = self.getPosition()
      if self.state == "walking_up":
        self.setPosition([pos[0], pos[1], pos[2] - 1])
      if self.state == "walking_down":
        self.setPosition([pos[0], pos[1], pos[2] + 1])
      if self.state == "walking_left":
        self.setPosition([pos[0] - 1, pos[1], pos[2]])
      if self.state == "walking_right":
        self.setPosition([pos[0] + 1, pos[1], pos[2]]) 
      if self.state == "walking_topleft":
        self.setPosition([pos[0] - 1, pos[1], pos[2] - 1])
      if self.state == "walking_bottomright": 
        self.setPosition([pos[0] + 1, pos[1], pos[2] + 1]) 
      if self.state == "walking_bottomleft":
        self.setPosition([pos[0] - 1, pos[1], pos[2] + 1]) 
      if self.state == "walking_topright":
        self.setPosition([pos[0] + 1, pos[1], pos[2] - 1]) 
      if self.position <> self.destination:
        self.state = state
      else:
        self.state = "standing_down"
  