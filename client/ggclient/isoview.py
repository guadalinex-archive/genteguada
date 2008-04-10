import math
import utils

class IsoView:
  """ Clase IsoView.
  Clase principal que define atributos y metodos de una vista generica.
  """
  
  def __init__(self, name):
    """ Constructor de la clase.
    name: nombre de la vista.
    """  
    self._name = name
    self._modelList = []
    self._type = 0

  def getName(self):
    """ Devuelve la etiqueta del observador.
    """
    return self._name
  
  def getType(self):
    """ Indica el tipo de objeto que observa. -1: baldosa, 0: jugador, 1: objeto.
    """
    return self._type
  
  def setName(self, name):
    """ Asigna una nueva etiqueta al observador.
    """
    self._name = name
    
  def addModel(self, model):
    """ Anade un modelo a la lista de elementos controlados por la vista
    model: elemento a anadir
    """
    self._modelList.append(model)
    model.register(self)

  def notify(self, caller):
     pass
  
  def _p3dToP2d(self, cord3d):
    """ Convierte un punto con coordenadas 3d virtuales en 2d con cord fisicas
    cord3d: punto 3d a convertir
    """
    x2d = (cord3d[0] - cord3d[2]) * utils.COS30R * utils.TILE_SZ[0]
    y2d = ((cord3d[0] + cord3d[2]) * utils.SIN30R) - cord3d[1]
    y2d = (y2d * utils.TILE_SZ[1])

    x2d = x2d - (utils.TILE_SZ[0])
    y2d = y2d + 5
    """
    print self.getType(), dir(self)
   
    if self.getType() == 0: # tile
      x2d = x2d - (utils.TILE_SZ[0])
    if self.getType() == 1: # player
      x2d = x2d - (utils.CHAR_SZ[0])
      y2d = y2d - (utils.CHAR_SZ[1] / 4)
    if self.getType() == 2: # object
      x2d = x2d - 55
      y2d = y2d + 8
    """
    
    cord2d = [math.floor((x2d/math.sqrt(3)) + utils.SCREEN_OR[0]), \
              math.floor(y2d + utils.SCREEN_OR[1])]
    return cord2d
