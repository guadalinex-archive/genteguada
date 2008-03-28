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
    
  def moveOne(self, dir):
    """ Mueve al jugador una casilla en una direccion.
    dir: direccion del movimiento.    
    """
    if self.stateFrame <> 0:
      pass
    else:
      if dir <> 0:
        self.stateFrame = 0
      if dir == 1 and self.position[2] > 0:
        self.state = "walking_up"
        self.destination = [self.position[0], self.position[1], \
                            self.position[2] - 1]
      if dir == 2 and self.position[2] < (SCENE_SZ[1] - 1):
        self.state = "walking_down"
        self.destination = [self.position[0], self.position[1], \
                            self.position[2] + 1]
      if dir == 3 and self.position[0] > 0:
        self.state = "walking_left"
        self.destination = [self.position[0] - 1, self.position[1], \
                            self.position[2]]
      if dir == 4 and self.position[0] < (SCENE_SZ[0] - 1):
        self.state = "walking_right"
        self.destination = [self.position[0] + 1, self.position[1], \
                            self.position[2]]
        
  def setName(self, name):
    self.name = name
    self.triggerEvent('change name', name=self.name)
        
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
    """ Devuelve la direccion de movimiento del jugador.
    """
    if self.state == "standing_up" or self.state == "standing_down" or \
      self.state == "standing_left" or self.state == "standing_right":
      return 0
    if self.state == "walking_up":
      return 1
    if self.state == "walking_down":
      return 2
    if self.state == "walking_left":
      return 3
    if self.state == "walking_right":
      return 4
    if self.state == "walking_topleft":
      return 5
    if self.state == "walking_bottomright":
      return 6
    if self.state == "walking_bottomleft":
      return 7
    if self.state == "walking_topright":
      return 8

  def getDestination(self):
    return self.destination

  def setDestination(self, state, destination):
    """ Asigna un punto de destino al movimiento del jugador.
    state: direccion del siguiente movimiento.
    destiantion: destino del movimiento.
    """
    if self.stateFrame <> 0:
      pass
    else:
      self.stateFrame = 0
      self.state = state
      self.destination = destination
      self.triggerEvent('destination', destination=self.destination)
      #self.state = self.views[0].getNextDir(self.position, destination)
      #self.state = getNextDirection(self.position, destination)

  def tick(self, state):
    """ Procedimiento que actualiza posiciones de movimientos, e incrementa \
    el estado de las animaciones en las que se encuentren los jugadores.
    state: direccion del siguiente movimiento.
    """
    if self.state == "walking_up" or self.state == "walking_down" or \
    self.state == "walking_left" or self.state == "walking_right" or \
    self.state == "walking_topleft" or self.state == "walking_bottomright" or \
    self.state == "walking_bottomleft" or self.state == "walking_topright":
      if self.stateFrame == (MAX_FRAMES - 1):
        #print self.position, " >> ", self.destination, " >> ", state
        print "==================== Finalizacion de movimiento ===================="""
        pos = self.getPosition()
        if self.state == "walking_up":
          self.position = [pos[0], pos[1], pos[2] - 1]
        if self.state == "walking_down":
          self.position = [pos[0], pos[1], pos[2] + 1]
        if self.state == "walking_left":
          self.position = [pos[0] - 1, pos[1], pos[2]]
        if self.state == "walking_right":
          self.position = [pos[0] + 1, pos[1], pos[2]]  
        if self.state == "walking_topleft":
          self.position = [pos[0] - 1, pos[1], pos[2] - 1]  
        if self.state == "walking_bottomright": 
          self.position = [pos[0] + 1, pos[1], pos[2] + 1]  
        if self.state == "walking_bottomleft":
          self.position = [pos[0] - 1, pos[1], pos[2] + 1]  
        if self.state == "walking_topright":
          self.position = [pos[0] + 1, pos[1], pos[2] - 1]  
        self.stateFrame = 0
        if self.position <> self.destination:
          #self.state = self.views[0].getNextDir(self.position, destination)
          #self.state = getNextDirection(self.position, self.destination)
          print self.stateFrame, " }}} ", self.state, " }}} ", self.position, " }}} ", self.destination
          self.state = state
        else:
          self.state = "standing_down"
      else:
        self.stateFrame += 1
       
#  def notify(self):
#    """ Informa a los observadores del jugador de que se ha producido un \
#    cambio.
#    """
#    self.notify_observers(self.state)
  