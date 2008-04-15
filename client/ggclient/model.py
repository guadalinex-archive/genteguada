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
    """ Devuelve las dimensiones del objeto.
    """
    return self._size

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
    """ Devuelve las dimensiones del objeto.
    """
    return self._size

  def getId(self):
    """ Devuelve el identificador del objeto.
    """    
    return self._id

  def testSetName(self, name):
    """ Version publica del metodo _setName. Usar SOLO para realizar test.
    """
    self._setName(name)

  def _setName(self, name):
    """ Asigna una nueva etiqueta para el objeto.
    name: etiqueta del objeto.
    """
    self._name = name

  def _setSprite(self, sprite):
    """ Asigna un nuevo sprite para representar al objeto.
    sprite: nombre del fichero del grafico.
    """
    self._sprite = sprite

  def _setSize(self, size):
    """ Modifica las dimensiones del objeto y les asigna un nuevo valor.
    size: dimensiones del objeto.
    """
    self._size = size

  def _setId(self, id):
    """ Modifica el identificador de un objeto y le asigna un nuevo valor.
    id: identificador del objeto.
    """
    self._id = id

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
    if eventType <> None:
      #elimina una suscripcion hecha por un observador a un evento
      #p.uno.im_self.__class__
      pass
    else:
      #elimina todas las suscripciones hechas por un jugador
      pass    

  def unsubscribeEventMethod(self, method, eventType=None):
    if eventType:
      #elimina una suscripcion a un metodo para un evento concreto
      result = [self._events[x] for x in range(len(self._events)) \
                if self._events[x][0] <> eventType and self._events[x][1] <> method]
      self._events = result  
    else:
      #elimina todas las suscripciones a un evento
      result = [self._events[x] for x in range(len(self._events)) \
                if self._events[x][1] <> method]
      self._events = result

  """
  def deleteEvent(self, eventType=None):
    if eventType:
      result = [self._events[x] for x in range(len(self._events)) if not self._events[x][0] == eventType]
      self._events = result
    else:
      self._events = []
  """

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
