import utils

class Event:

  """
  Clase padre de los eventos, todos los eventos definidos en el juego
  tienen que heredar de esta clase
  """

  def __init__(self, producer, name, params):
    """
    Constructor de la clase
    """
    self.producer = producer
    self.name = name
    self.params = params
    
  
  def objectToSerialize(self, rServer):

    eventToSerialize = Event(utils.objectToSerialize(self.producer, rServer),
                             utils.objectToSerialize(self.name, rServer),
                             utils.objectToSerialize(self.params, rServer))

    return eventToSerialize

  def __repr__(self):
    return "EVENT Name: "+str(self.name)+" Producer: "+str(self.producer)+" Params: "+str(self.params)
