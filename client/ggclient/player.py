import model
import ggcommon.eventos

class Player(model.Model):
  """ Clase Player.
  Define el comportamiento de un objeto, jugador o no.
  """
 
  def __init__(self, name, id, sprite, size, position):
    """ Constructor de la clase.
    name: etiqueta de la clase.
    id: identificador del jugador.
    sprite: grafico que representa al jugador.
    size: tamano del grafico del jugador.
    position: posicion en la que se encuentra el jugador.
    """
    model.Model.__init__(self, name, id, sprite, size)
    self._position = position
    self._state = "standing_down"
    self._stateFrame = 0
    self._destination = position
    self._visited = []
        
  def getPosition(self):
    """ Devuelve la posicion en la que se encuentra el objeto.
    """
    return self._position
 
  def getState(self):
    """ Devuelve la animacion en la que se encuentra el objeto.
    """
    return self._state

  def getStateFrame(self):
    """ Devuelve el estado de la animacion en la que se encuentra el objeto.
    """
    return self._stateFrame

  def getId(self):
    """ Devuelve el identificador del objeto.
    """
    return self._id

  def getDir(self):
    """ Devuelve el codigo de direccion de movimiento del objeto.
    """
    for i in range (1, len(utils.DIR)+1):
      if self._state == utils.DIR[i]:
        return i
    return 0  

  def getDestination(self):
    """ Devuelve el destino del movimiento.
    """
    return self._destination
        
  def setName(self, name):
    self._name = name
    self.triggerEvent('name', name=self.name)
      
  def setPosition(self, position):
    """ Asigna una nueva posicion a un objeto.
    position: posicion del objeto.
    """
    if self._destination == position:
      self._visited = []
    self._visited.append(position)
    pActualAux = self._position
    self._position = position
    self.triggerEvent('position', id=self._id, sprite=self._sprite, \
                        pActual=pActualAux, pDestin=self._position, dir=self._state)
    
  def setDestination(self, state, destination):
    """ Asigna un punto de destino al movimiento del objeto.
    state: direccion del siguiente movimiento.
    destiantion: destino del movimiento.
    """
    self._state = state
    self._destination = destination
    
  def hasBeenVisited(self, pos):
    """ Indica si una celda ha sido visitada en el ultimo movimiento del objeto.
    pos: posicion de la celda a comprobar.
    """
    for i in range(0, len(self._visited)):
      if self._visited[i] == pos:
        return 1
    return 0
    
  def tick(self, direction):
    """ Procedimiento que actualiza posiciones de movimientos, e incrementa \
    el estado de las animaciones en las que se encuentren los objetos.
    direction: direccion del siguiente movimiento.
    """
    if self._position == self._destination:
      self._state = "standing_down"
      return
    if self._state <> "standing_down":
      pos = self.getPosition()
      self._state = direction
      if self._state == "walking_up":
        next = [pos[0], pos[1], pos[2] - 1]
      if self._state == "walking_down":
        next = [pos[0], pos[1], pos[2] + 1]
      if self._state == "walking_left":
        next = [pos[0] - 1, pos[1], pos[2]]
      if self._state == "walking_right":
        next = [pos[0] + 1, pos[1], pos[2]]
      if self._state == "walking_topleft":
        next = [pos[0] - 1, pos[1], pos[2] - 1]
      if self._state == "walking_bottomright": 
        next = [pos[0] + 1, pos[1], pos[2] + 1]
      if self._state == "walking_bottomleft":
        next = [pos[0] - 1, pos[1], pos[2] + 1]
      if self._state == "walking_topright":
        next = [pos[0] + 1, pos[1], pos[2] - 1]
      self.setPosition(next)
      