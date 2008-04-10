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
    self._name = name
    self._sprite = sprite
    self._size = size
    self._id = id
    self._events = []
    self._views = []
    
  def getName(self):
    """ Devuelve la etiqueta de la clase.
    """
    return self._name

  def getSprite(self):
    """ Devuelve el grafico usado para representar la clase.
    """
    return self._sprite
  
  def getSize(self):
    """ Devuelve el tamano del objeto.
    """
    return self._size

  def subscribeEvent(self, eventType, method):
    """ Indica la accion a realizar ante un evento.
    eventType: tipo de evento.
    method: metodo que se lanzara.
    """
    self._events.append([eventType, method])
    
  def triggerEvent(self, eventType, **params):
    """ Activa un evento.
    eventType: tipo de evento.
    params: datos sobre el evento.
    """
    for type,method in self._events:
      if type == eventType:
        event = ggcommon.eventos.Event(self, eventType, params)
        method(event)
    
  def unsubscribeEventObserver(self, observer, eventType=None):
    pass

  def unsubscribeEventMethod(self, method, eventType=None):
    pass
  

  def deleteEvent(self, eventType=None):
    """ Elimina un evento de la lista de escuchas.
    """
    if eventType:
      result = [self._events[x] for x in range(len(self._events)) if not self._events[x][0] == eventType]
      self._events = result
    else:
      self._events = []
        
  def register(self, view):
    """ Registra una vista como visor de este subject.
    view: vista a registrar.
    """
    self._views.append(view)
    
  def unregister(self, view):
    """ Elimina de la lista de registrados una vista de este subject.
    vista: vista a eliminar.
    """
    self._views.remove(view)
  
