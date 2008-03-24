from isoview import *

class IsoViewItem(IsoView):
  """ Clase IsoViewItem.
  Clase en la que se definen metodos genericos para todos los items.
  """
  
  def draw(self, screen):
    """ Realiza llamadas para pintar en pantalla todos los items observados.
    screen: controlador de pantalla.
    """
    for ind in range(self.modelList.__len__()):
      self.drawSingle(ind, screen)
  
  def drawSingle(self, caller, screen):
    """ Obtiene los datos de un item y realiza llamadas para pintarlo.
    ind: identificador del item a pintar.
    screen: controlador de pantalla.
    """
    pos = self.modelList[caller].getPosition()
    varPos = [pos[0], pos[1], pos[2]]
    sprite = self.modelList[caller].getSprite()
    #self.paintObject(sprite, varPos, caller, screen)
  
  def paintModel(self, sprite, cord3d, caller, screen):
    """ Pinta un modelo concreto en pantalla.
    sprite: grafico del modelo.
    cord3d: coordenada 3d donde se encuentra el modelo.
    caller: identificador del modelo a pintar.
    screen: controlador de pantalla.
    """
    ob = os.path.join(DATA_PATH, sprite)
    obSurface = pygame.image.load(ob)
    screen.blit(obSurface, self.p3dToP2d(cord3d))
    pygame.display.update()
 
  def notify(self, caller, event):
    """ Al recibir una notificacion, inicia el pintado de un item.
    caller: identificador del item a pintar.
    event: notificacion recibida
    """
    self.paintModel(OBJ_BOOK_SPRITE1, [3, 0, 2])

  def getType(self):
    """ Devuelve un valor indicando que esta es una clase tipo IsoViewItem.
    """
    return 2
