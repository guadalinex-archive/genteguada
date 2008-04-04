import os
import pygame
from isoview_item import *

class IsoViewPlayer(IsoViewItem):
  """ Clase IsoViewPlayer.
  Define a la vista de un item de tipo jugador.
  """

  def __init__(self, name, screen):
    """ Constructor de la clase.
    name: nombre de la vista.
    """  
    self.name = name
    self.modelList = []
    self.modelDataList = []
    self.spritesList = []
    self.bg = None
    self.screen = screen
    self.allPlayers = pygame.sprite.RenderUpdates()

  def newAction(self, event):
    """ Ejecuta un evento correspondiente a una nueva accion.
    event: informacion del evento.
      > id = self.id
      > sprite = self.sprite
      > pActual = self.position
      > pDestin = self.destination
      > dir = self.state
    """
    for i in range(0, len(self.modelDataList)):
      if self.modelDataList[i]["id"] == event.params["id"]:
        self.spritesList[i].rect.topleft = self.p3dToP2d(event.params["pDestin"])
        self.modelDataList[i]["pActual"] = event.params["pDestin"]
        self.modelDataList[i]["pDestin"] = event.params["pDestin"]
        self.allPlayers.update()                     
        self.allPlayers.clear(self.screen, self.bg.image)
        pygame.display.update(self.allPlayers.draw(self.screen))

  def setBg(self, bg):
    """ Asigna un fondo a las animaciones de los jugadores.
    bg: grafico de fondo.
    """
    self.bg = bg
    self.bg.rect.topleft = BG_FULL_OR

  def addModel(self, model):
    """ Anade un modelo a la lista de elementos controlados por la vista
    model: elemento a anadir
    """
    imgPath = os.path.join(DATA_PATH, model.getSprite())
    img = pygame.sprite.Sprite()
    img.image = pygame.image.load(imgPath)
    img.rect = img.image.get_rect()
    img.rect.topleft = self.p3dToP2d(model.getPosition())
    self.allPlayers.add(img)
    self.spritesList.append(img)
    self.modelList.append(model)
    self.modelDataList.append({"id":model.getId(), "sprite":model.getSprite(), \
      "pActual":model.getPosition(), "pDestin":model.getDestination(), \
      "dir":model.getState(), "step": 0})

  def drawFirst(self, screen):
    """ Realiza llamadas para pintar en pantalla todos los jugadores observados por primera vez.
    screen: controlador de pantalla.
    """
    self.allPlayers.draw(screen)
    pygame.display.update()
    
  def draw(self, screen):
    """ Realiza llamadas para pintar en pantalla todos los jugadores observados.
    screen: controlador de pantalla.
    """
    self.allPlayers.update()                     
    self.allPlayers.clear(screen, self.bg.image)
    pygame.display.update(self.allPlayers.draw(screen))
    
  def drawOne(self, caller):
    """ Pinta un jugador moviendose en una direccion en pantalla.
    caller: jugador a pintar
    screen: controlador de pantalla
    NOTA -> Este metodo se emplea solo para mover al jugador con el teclado.
    NOTA -> Si se elimina el control de teclado, se puede prescindir del metodo.
    """
    pos = self.modelList[caller].getPosition()
    varPos = [pos[0], pos[1], pos[2]]
    event = self.modelList[caller].getState()
    sprite = self.modelList[caller].getSprite()
    self.paintPlayer(sprite, pos, caller, self.screen)

  def paintPlayer(self, sprite, cord3d, caller, screen):
    """ Pinta un jugador en pantalla.
    sprite: grafico del jugador.
    cord3d: coordenadas 3d del jugador.
    caller: jugador a pintar.
    screen: controlador de pantalla.
    """
    pl = os.path.join(DATA_PATH, sprite)
    plSurface = pygame.image.load(pl)
    state = self.modelList[caller].getStateFrame()
    dir = self.modelList[caller].getDir()
    screen.blit(plSurface, self.p3dToP2d(cord3d, state, dir))
    pygame.display.update()
    
  def p3dToP2d(self, cord3d):
    """ Convierte un punto con coordenadas 3d virtuales en 2d con cord fisicas.
    cord3d: punto 3d a convertir.
    """
    x2d = (cord3d[0] - cord3d[2]) * COS30R * TILE_SZ[0]
    y2d = ((cord3d[0] + cord3d[2]) * SIN30R) - cord3d[1]
    y2d = (y2d * TILE_SZ[1])
    
    x2d = x2d - (CHAR_SZ[0])
    y2d = y2d - (CHAR_SZ[1] / 4)
    
    x2d = math.floor((x2d / math.sqrt(3)) + SCREEN_OR[0])
    y2d = math.floor(y2d + SCREEN_OR[1])
   
    if dir == 1: #arriba
      x2d = x2d + (((TILE_SZ[0] / 2)*state) / 5)
      y2d = y2d - (((TILE_SZ[1] / 2)*state) / 5)
    if dir == 2: #abajo
      x2d = x2d - (((TILE_SZ[0] / 2)*state) / 5)
      y2d = y2d + (((TILE_SZ[1] / 2)*state) / 5)
    if dir == 3: #izquierda
      x2d = x2d - (((TILE_SZ[0] / 2)*state) / 5)  
      y2d = y2d - (((TILE_SZ[1] / 2)*state) / 5)
    if dir == 4: #derecha
      x2d = x2d + (((TILE_SZ[0] / 2)*state) / 5)
      y2d = y2d + (((TILE_SZ[1] / 2)*state) / 5)
    if dir == 5: #arriba-izquierda
      y2d = y2d - (((TILE_SZ[1])*state) / 5)
    if dir == 6: #abajo-derecha
      y2d = y2d + (((TILE_SZ[1])*state) / 5)
    if dir == 7: #abajo-izquierda
      x2d = x2d - (((TILE_SZ[0])*state) / 5)  
    if dir == 8: #arriba-derecha
      x2d = x2d + (((TILE_SZ[0])*state) / 5)
      
    cord2d = [x2d, y2d]
    return cord2d

  def getType(self):
    """ Devuelve un valor indicando que esta es una clase tipo IsoViewPlayer.
    """
    return 1
