
import dMVC.remoteclient
import pygame
import GG.utils
import GG.model.ggsystem
import time
import pygame.locals
import sys
import GG.isoview.login
import os


class GenteGuada:

  def __init__(self):
    self.screen = None
    self.system = None
    self.player = None
    self.isoHud = None
    self.session = None
    self.client = None
    GenteGuada.instance = self

  @staticmethod
  def getInstance():
    return GenteGuada.instance

  def input(self, events):
    for event in events:
      if event.type == pygame.locals.QUIT:
        self.finish()
      if event.type == pygame.locals.KEYDOWN:
        if event.key == pygame.locals.K_ESCAPE:
          self.finish()
        elif event.key == pygame.locals.K_RETURN: 
          self.isoHud.chatMessageEntered()
      if event.type == pygame.locals.MOUSEBUTTONDOWN:
        cordX, cordY = pygame.mouse.get_pos()
        if 0 <= cordY <= GG.utils.HUD_OR[1]:
          dest = self.isoHud.getIsoviewRoom().findTile([cordX, cordY])
          if not dest == [-1, -1]:
            self.isoHud.getIsoviewRoom().getModel().clickedByPlayer(self.player, [dest[0], 0, dest[1]])
    self.isoHud.widgetContainer.distribute_events(*events)

  def finish(self):
    #print dMVC.utils.statClient.strClient()
    #print dMVC.utils.statEventTriggered.strEvent()
    pygame.mixer.music.stop()
    sys.exit(0)
  
  def start(self, params):
    pygame.init()
    #self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ, pygame.HWSURFACE|pygame.FULLSCREEN,0)
    self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ)
    pygame.display.set_caption(GG.utils.VERSION)
    self.__getSystem(params.ip) 
    winLogin = GG.isoview.login.Login(self.screen, self)
    self.session = winLogin.draw()
    #self.session = winLogin.draw(params.user, params.password)
    self.initGame()

  def __getSystem(self, ipAddress):
    if ipAddress:
      try:
        self.client = dMVC.remoteclient.RClient(ipAddress)
      except Exception, excep:
        print excep, "No hay conexion con el servidor"
        self.finish()
      self.system = self.client.getRootModel()
    else:
      self.system = GG.model.ggsystem.GGSystem()

  def initGame(self):
    if self.client:
      self.client.registerSession(self.session)
    self.player = self.session.getPlayer()
    self.isoHud = self.session.defaultView(self.screen)
    self.isoHud.draw()
    while True:
      time.sleep(GG.utils.ANIM_DELAY)
      self.input(pygame.event.get())
      self.isoHud.updateFrame()

  def getDataPath(self, img):
    return os.path.join(GG.utils.DATA_PATH, img)
