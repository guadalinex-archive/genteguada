import utils
import isoview

class IsoViewTile(isoview.IsoView):
  """ Clase IsoViewTile.
  Define a la vista de una baldosa de la habitacion.
  """

  def __init__(self, topLeft, bottomRight, sprite, size, blocked):
    """ Constructor de la clase.
    topLeft: coordenada superior izquierda (origen) de la baldosa.
    bottomRight: coordenada inferior derecha de la baldosa.
    size: tamano de la baldosa.
    blocked: indica si se puede pasar a traves de ella.
    """
    self._type = -1
    self._topLeft = topLeft
    self._bottomRight = bottomRight
    self._id = id
    self._sprite = sprite
    self._size = size
    self._views = []
    self._blocked = blocked
    
  def getTopLeft(self):
    """ Devuelve la coordenada superior izquierda.
    """
    return self._topLeft
  
  def getBottomRight(self):
    """ Devuelve la coordenada inferior derecha.
    """
    return self._bottomRight
  
  def getId(self):
    """ Devuelve el identificador de la baldosa.
    """
    return self._id

  def getBlocked(self):
    """ Indica si la baldosa esta bloqueada al paso.
    """
    return self._blocked
  
  def setBlocked(self, blocked):
    """ Pone una baldosa como bloqueada para pasar.
    """
    self._blocked = blocked
  
  def contained(self, pos):
    """ Indica si un punto 2d esta contenido en la baldosa.
    pos: punto a comprobar.
    """
    if self._bottomRight[0] > pos[0] > self._topLeft[0]:
      if self._bottomRight[1] > pos[1] > self._topLeft[1]:
        return 1
    return 0

  def onBlank(self, pos):
    """ Indica si la posicion en la que ha pinchado el usuario en la baldosa \
    corresponde a una zona transparente de la imagen o al cuerpo de la baldosa.
    pos: posicion en la que ha pinchado el usuario.
    """
    iniPos = [pos[0]-self._topLeft[0], pos[1]-self._topLeft[1]]
    if iniPos[0] < (utils.TILE_SZ[0] / 2):
      if iniPos[1] < (utils.TILE_SZ[1] / 2):
        #top left corner
        if (iniPos[0] + (iniPos[1] * 2)) <= (utils.TILE_SZ[0]/2):
          return 1
      else:
        #bottom left corner
        iniPos[1] -= (utils.TILE_SZ[1] / 2)
        iniPos[1] = (utils.TILE_SZ[1] / 2) - iniPos[1]
        if (iniPos[0] + (iniPos[1] * 2)) <= (utils.TILE_SZ[0]/2):
          return 1
    else:
      if iniPos[1] < (utils.TILE_SZ[1] / 2):
        #top right corner
        iniPos[0] -= (utils.TILE_SZ[0] / 2)
        iniPos[0] = (utils.TILE_SZ[0] / 2) - iniPos[0]
        if (iniPos[0] + (iniPos[1] * 2)) <= (utils.TILE_SZ[0]/2):
          return 1
      else:
        #bottom right corner
        iniPos[0] -= (utils.TILE_SZ[0] / 2)
        iniPos[1] -= (utils.TILE_SZ[1] / 2)
        iniPos[0] = (utils.TILE_SZ[0] / 2) - iniPos[0]
        iniPos[1] = (utils.TILE_SZ[1] / 2) - iniPos[1]
        if (iniPos[0] + (iniPos[1] * 2)) <= (utils.TILE_SZ[0]/2):
          return 1
    return 0    
