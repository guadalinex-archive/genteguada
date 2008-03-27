
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
    
  