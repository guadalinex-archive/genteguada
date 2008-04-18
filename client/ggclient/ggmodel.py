import ggcommon.eventos
import dMVC.model

class GGModel(dMVC.model.Model):
  """ Model class.
  Defines a generic model, its attributes and behaviour.
  """
  
  def __init__(self, name, id, sprite=None, size=None):
    """ Class constructor.
    name: class label.
    id: class identifier.
    sprite: image name.
    size: model size.
    """
    dMVC.model.Model.__init__(self)
    self.__name = name
    if sprite: self.__sprite = sprite
    if size:  self.__size = size
    self.__id = id
    self.__events = []
    self.__view = None
    
  def getName(self):
    """ Returns the class label.
    """
    return self.__name

  def getSprite(self):
    """ Returns the sprite name.
    """
    return self.__sprite
  
  def getSize(self):
    """ Returns the model size.
    """
    return self.__size

  def getId(self):
    """ Returns the model id.
    """    
    return self.__id

  def testSetName(self, name):
    """ _setName public version. To be used ONLY on tests.
    """
    self._setName(name)

  def setName(self, name):
    """ Sets a new label for the model.
    name: model label.
    """
    self.__name = name

  def setSprite(self, sprite):
    """ Sets a new sprite for the model.
    sprite: sprite name.
    """
    self.__sprite = sprite

  def setSize(self, size):
    """ Modifies the model size.
    size: model size.
    """
    self.__size = size

  def setId(self, id):
    """ Modifies a model id.
    id: model id.
    """
    self.__id = id

  def subscribeEvent(self, eventType, method):
    """ Subscribes the model to an event type.
    eventType: event to subscribe for.
    method: method to rise.
    """
    self.__events.append([eventType, method])
    
  def triggerEvent(self, eventType, **params):
    """ Triggers an event.
    eventType: event type.
    params: event data.
    """
    for type,method in self.__events:
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
      result = [self.__events[x] for x in range(len(self.__events)) \
                if self.__events[x][0] <> eventType and self.__events[x][1] <> method]
      self.__events = result  
    else:
      #elimina todas las suscripciones a un evento
      result = [self.__events[x] for x in range(len(self.__events)) \
                if self.__events[x][1] <> method]
      self.__events = result

  def register(self, view):
    """ Registers a view as an observer of this object.
    view: view to be registered.
    """
    self.__view = view
    
  def unregister(self, view):
    """ Registers a view as an observer of this object.
    view: view to be registered.
    """ 
    self.__views.remove(view)