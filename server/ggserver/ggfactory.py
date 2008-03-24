
from twisted.internet.protocol import Factory

from ggprotocol import GenteGuadaProtocol

class GenteGuadaFactory(Factory):
  """
  Manejador de una conexion de un cliente con el servidor
  """

  def __init__(self):
    """
    constructor de la clase
    """
    self.protocol = GenteGuadaProtocol
    self.clients = []
