import threading
import ggcommon.remotemodel
import traceback


class Model: #{{{

  def __init__(self):
    self._id = None
    self._events = []
    self._eventsMutex = threading.Semaphore(1)

  #def hasID(self):
  #  return (self._id != None)

  def setID(self, id):
    self._id = id

  def __str__(self):
    return '<Model ID: ' + str(self._id) +'>'

  def objectToSerialize(self, server):

    if self._id == None:
      server.registerModel(self)

    return ggcommon.remotemodel.RemoteModel(self._id)


  def subscribeEvent(self, eventType, method):
    """ Indica la accion a realizar ante un evento.
    eventType: tipo de evento.
    method: metodo que se lanzara.
    """
    self._eventsMutex.acquire()
    self._events.append([eventType, method])
    self._eventsMutex.release()

    
  def triggerEvent(self, eventType, **params):
    """ Activa un evento.
    eventType: tipo de evento.
    params: datos sobre el evento.
    """
    self._eventsMutex.acquire()
    eventsCopy = self._events
    self._eventsMutex.release()
    for type, method in eventsCopy:
      if type == eventType:
        event = ggcommon.eventos.Event(self, eventType, params)
        try:
          method(event)
        except:
          traceback.print_exc()
          print sys.exc_info()[1]

    
  def unsubscribeEventObserver(self, observer, eventType=None):
    toRemove = []
    self._eventsMutex.acquire()
    for event in self._events:
      if id(event[1].im_self) == id(observer):
        if eventType == None or eventType == event[0]: 
          toRemove.append(event)
    for event in toRemove:
      self._events.remove(event)
    self._eventsMutex.release()

  def unsubscribeEventMethod(self, method, eventType=None):
    self._eventsMutex.acquire()
    pass # actually do it!
    self._eventsMutex.release()


  def __eq__(self, comparand):
      return id(self) == id(comparand)
#}}}
