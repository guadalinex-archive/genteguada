import ggcommon.remotemodel


class Model: #{{{

  def __init__(self):
    self._id = None
    self._events = []

  #def hasID(self):
  #  return (self._id != None)

  def setID(self, id):
    self._id = id

  def __str__(self):
    return '<Model ID: ' + str(self.getID()) +'>'

  def objectToSerialize(self, server):
    if self._id == None:
      server.registerModel(self)
    return ggcommon.remotemodel.RemoteModel(self._id)


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


#}}}
