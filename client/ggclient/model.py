from utils import *
import ggcommon.eventos

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
    
  def onEvent(self, eventType, method):
    self.views.append([eventType, method])
    
  def triggerEvent(self, eventType, **params):
    for type,method in self.views:
      if type == eventType:
        event = ggcommon.eventos.Event(self, eventType, params)
        method(event)
    
  def removeEvent(self, eventType):
    i=0
    for type,method in self.views:
      if type == eventType:
        del(self.views[i])
      i += 1  
        
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
