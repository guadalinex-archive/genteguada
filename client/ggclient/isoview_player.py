import os
import math
import pygame
import utils
import isoview

class IsoViewPlayer(isoview.IsoView):
  """ Clase IsoViewPlayer.
  Define a la vista de un objeto, jugador o no.
  """

  def __init__(self, name, type, screen):
    """ Constructor de la clase.
    name: nombre de la vista.
    type: indica si el objeto es un jugador (0) o un item (1).
    screen: controlador de pantalla.
    """
    self._name = name
    self._type = type
    self._modelList = []
    self._modelDataList = []
    self._spritesList = []
    self._bg = None
    self._screen = screen
    self._allPlayers = pygame.sprite.RenderUpdates()
    
  def getBg(self):
    """ Devuelve el fondo para el repintado y limpia de sprites de jugadores.
    """
    return self._bg
  
  def getScreen(self):
    """ Devuelve el controlador de pantalla.
    """
    return self._screen
    
  def setBg(self, bg):
    """ Asigna un fondo a las animaciones de los jugadores.
    bg: grafico de fondo.
    """
    self._bg = bg
    self._bg.rect.topleft = utils.BG_FULL_OR
    
  def _setScreen(self, screen):
    """ Asigna el controlador de pantalla.
    screen: controlador de pantalla.
    """
    self._screen = screen

  def newAction(self, event):
    """ Ejecuta un evento correspondiente a una nueva accion.
    event: informacion del evento.
      > id = self.id
      > sprite = self.sprite
      > pActual = self.position
      > pDestin = self.destination
      > dir = self.state
    """
    for i in range(0, len(self._modelDataList)):
      if self._modelDataList[i]["id"] == event.params["id"]:
        #self._spritesList[i].rect.topleft = self._p3dToP2d(event.params["pDestin"], self._modelList[i].getSize())
        self._spritesList[i].rect.topleft = self._p3dToP2d(event.params["pDestin"])
        self._modelDataList[i]["pActual"] = event.params["pDestin"]
        self._modelDataList[i]["pDestin"] = event.params["pDestin"]
        self._allPlayers.update()                     
        self._allPlayers.clear(self._screen, self._bg.image)
        pygame.display.update(self._allPlayers.draw(self._screen))

  def addModel(self, model):
    """ Anade un modelo a la lista de elementos controlados por la vista
    model: elemento a anadir
    """
    imgPath = os.path.join(utils.DATA_PATH, model.getSprite())
    img = pygame.sprite.Sprite()
    img.image = pygame.image.load(imgPath)
    img.rect = img.image.get_rect()
    #img.rect.topleft = self._p3dToP2d(model.getPosition())
    img.rect.topleft = self._p3dToP2d(model.getPosition(), model.getSize())
    self._allPlayers.add(img)
    self._spritesList.append(img)
    self._modelList.append(model)
    self._modelDataList.append({"id":model.getId(), "sprite":model.getSprite(), \
      "pActual":model.getPosition(), "pDestin":model.getDestination(), \
      "dir":model.getState(), "step": 0})

  def drawFirst(self, screen):
    """ Realiza llamadas para pintar en pantalla todos los jugadores observados por primera vez.
    screen: controlador de pantalla.
    """
    self._allPlayers.draw(screen)
    pygame.display.update()
    
  def draw(self, screen):
    """ Realiza llamadas para pintar en pantalla todos los jugadores observados.
    screen: controlador de pantalla.
    """
    self._allPlayers.update()                     
    self._allPlayers.clear(screen, self._bg.image)
    pygame.display.update(self._allPlayers.draw(screen))
    
  def drawOne(self, caller):
    """ Pinta un jugador moviendose en una direccion en pantalla.
    caller: jugador a pintar
    screen: controlador de pantalla
    NOTA -> Este metodo se emplea solo para mover al jugador con el teclado.
    NOTA -> Si se elimina el control de teclado, se puede prescindir del metodo.
    """
    pos = self._modelList[caller].getPosition()
    varPos = [pos[0], pos[1], pos[2]]
    event = self._modelList[caller].getState()
    sprite = self._modelList[caller].getSprite()
    self.paintPlayer(sprite, pos, caller, self._screen)

  def paintPlayer(self, sprite, cord3d, caller, screen):
    """ Pinta un jugador en pantalla.
    sprite: grafico del jugador.
    cord3d: coordenadas 3d del jugador.
    caller: jugador a pintar.
    screen: controlador de pantalla.
    """
    pl = os.path.join(utils.DATA_PATH, sprite)
    plSurface = pygame.image.load(pl)
    state = self._modelList[caller].getStateFrame()
    dir = self._modelList[caller].getDir()
    screen.blit(plSurface, self._p3dToP2d(cord3d, state, dir))
    pygame.display.update()
    
  def _p3dToP2d(self, cord3d, size=None):
    """ Convierte un punto con coordenadas 3d virtuales en 2d con cord fisicas.
    cord3d: punto 3d a convertir.
    size: tamano del modelo.
    """
    x2d = (cord3d[0] - cord3d[2]) * utils.COS30R * utils.TILE_SZ[0]
    y2d = ((cord3d[0] + cord3d[2]) * utils.SIN30R) - cord3d[1]
    y2d = (y2d * utils.TILE_SZ[1])
    
    if size:
      print size
      x2d = x2d - (size[0])
      y2d = y2d - (size[1] / 4)
    else:
      x2d = x2d - (utils.CHAR_SZ[0])
      y2d = y2d - (utils.CHAR_SZ[1] / 4)
    
    x2d = math.floor((x2d / math.sqrt(3)) + utils.SCREEN_OR[0])
    y2d = math.floor(y2d + utils.SCREEN_OR[1])
   
    if dir == 1: #arriba
      x2d = x2d + (((utils.TILE_SZ[0] / 2)*state) / 5)
      y2d = y2d - (((utils.TILE_SZ[1] / 2)*state) / 5)
    if dir == 2: #abajo
      x2d = x2d - (((utils.TILE_SZ[0] / 2)*state) / 5)
      y2d = y2d + (((utils.TILE_SZ[1] / 2)*state) / 5)
    if dir == 3: #izquierda
      x2d = x2d - (((utils.TILE_SZ[0] / 2)*state) / 5)  
      y2d = y2d - (((utils.TILE_SZ[1] / 2)*state) / 5)
    if dir == 4: #derecha
      x2d = x2d + (((utils.TILE_SZ[0] / 2)*state) / 5)
      y2d = y2d + (((utils.TILE_SZ[1] / 2)*state) / 5)
    if dir == 5: #arriba-izquierda
      y2d = y2d - (((utils.TILE_SZ[1])*state) / 5)
    if dir == 6: #abajo-derecha
      y2d = y2d + (((utils.TILE_SZ[1])*state) / 5)
    if dir == 7: #abajo-izquierda
      x2d = x2d - (((utils.TILE_SZ[0])*state) / 5)  
    if dir == 8: #arriba-derecha
      x2d = x2d + (((utils.TILE_SZ[0])*state) / 5)
      
    cord2d = [x2d, y2d]
    return cord2d
