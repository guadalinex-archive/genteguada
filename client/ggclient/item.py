from model import *

class Item(Model):
  """ Clase Item.
  Define el comportamiento de un item generico.
  """
  
  def __init__(self, name, id, sprite, size, position):
    """ Constructor de la clase.
    name: etiqueta del item.
    id: identificador.
    sprite: grafico usado para representar el item.
    size: tamano del item.
    position: posicion en la que se encuentra el item.
    """
    Model.__init__(self, name, id, sprite, size)
    self.position = position
    
  def getPosition(self):
    """ Devuelve la posicion en la que se encuentra el item.
    """
    return self.position

  def setPosition(self, position):
    """ Asigna una posicion al item.
    position: posicion del objeto a asignar.
    """
    self.position = position