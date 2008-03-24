
from twisted.internet import reactor

from ggfactory import GenteGuadaFactory

class Server:
  """
  Servidor del juego genteguada
  """

  def start(self):
    """
    metodo que arranca pone el servidor en escucha y al recibir una conexion
    la trata en la clase GenteGuadaFactory
    """
    reactor.listenTCP(4321, GenteGuadaFactory())
    reactor.run()    

