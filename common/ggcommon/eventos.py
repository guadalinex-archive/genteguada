
class Event:

  """
  Clase padre de los eventos, todos los eventos definidos en el juego
  tienen que heredar de esta clase
  """

  def __init__(self):
    """
    Constructor de la clase
    """
    self.name = "Evento Padre"
    self.listeners = []
    
  def register(self,listener):
    self.listeners.append(listener)

  def emit(self):
    pass
  
  
class MovePlayerEvent(Event):
  
  def emit(self, idplayer, x, y):
    for listener in self.listeners:
      listener.movePlayer(idplayer, x, y)
