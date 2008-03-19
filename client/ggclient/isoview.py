from utils import *

class IsoView:
  """ Clase IsoView.
  Clase principal que define atributos y metodos de una vista generica.
  """
  
  def __init__(self, name):
    """ Constructor de la clase.
    name: nombre de la vista.
    """  
    self.name = name
    self.modelList = []

  def addModel(self, model):
    """ Anade un modelo a la lista de elementos controlados por la vista
    model: elemento a anadir
    """
    self.modelList.append(model)
    model.register(self)

  def notify(self, caller):
     pass
  
  def p3dToP2d(self, cord3d):
    """ Convierte un punto con coordenadas 3d virtuales en 2d con cord fisicas
    cord3d: punto 3d a convertir
    """
    x2d = (cord3d[0] - cord3d[2]) * COS30R * TILE_SZ[0]
    y2d = ((cord3d[0] + cord3d[2]) * SIN30R) - cord3d[1]
    y2d = (y2d * TILE_SZ[1])
   
    if self.getType() == 0: # tile
      x2d = x2d - (TILE_SZ[0])
    if self.getType() == 1: # player
      x2d = x2d - (CHAR_SZ[0])
      y2d = y2d - (CHAR_SZ[1] / 4)
    if self.getType() == 2: # object
      x2d = x2d - 55
      y2d = y2d + 8
    
    cord2d = [math.floor((x2d/math.sqrt(3)) + SCREEN_OR[0]), \
              math.floor(y2d + SCREEN_OR[1])]
    return cord2d
