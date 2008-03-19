from utils import *

class Model:
  """ Clase Model.
  Define un subject, un objeto, de forma generica.
  """
  
  def __init__(self, name, id, sprite, size):
    """ Constructor de la clse.
    name: etiqueta de la clase.
    id: identificador de la clase.
    sprite: grafico usado para representarla.
    size: tamano del subject.
    """
    self.name = name
    self.sprite = sprite
    self.size = size
    self.id = id
    self.views = []
    
  def register(self, view):
    """ Registra una vista como visor de este subject.
    view: vista a registrar.
    """
    self.views.append(view)
    
  def unregister(self, view):
    """ Elimina de la lista de registrados una vista de este subject.
    vista: vista a eliminar.
    """
    self.views.remove(view)
    
  def getName(self):
    """ Devuelve la etiqueta de la clase.
    """
    return self.name

  def getSprite(self):
    """ Devuelve el grafico usado para representar la clase.
    """
    return self.sprite
  
  def getSize(self):
    """ Devuelve el tamano del objeto.
    """
    return self.size
