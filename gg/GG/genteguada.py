
import dMVC.remoteclient
import pygame
import GG.utils
import GG.model.ggsystem
import time
import pygame.locals
import sys

class GenteGuada:

  def __init__(self):
    self.screen = None
    self.system = None
    self.player = None
    self.isoHud = None
    self.session = None
  
  def input(self, events):
    for event in events:
      if event.type == pygame.locals.QUIT:
        self.finish()
      if event.type == pygame.locals.KEYDOWN:
        if event.key == pygame.locals.K_ESCAPE:
          self.finish()
        elif event.key == 13: #TODO: cambiar 13 por tecla de intro
          self.isoHud.chatMessageEntered()
      if event.type == pygame.locals.MOUSEBUTTONDOWN:
        cordX, cordY = pygame.mouse.get_pos()
        if cordY > GG.utils.GAMEZONE_SZ[1]:
          self.isoHud.clickedByPlayer([cordX, cordY])
        else:  
          dest = self.isoHud.getIsoviewRoom().findTile([cordX, cordY])
          if not dest == [-1, -1]:
            self.isoHud.getIsoviewRoom().getModel().clickedByPlayer(self.player, [dest[0], 0, dest[1]])
      self.isoHud.widgetContainer.distribute_events(event)

  def finish(self):
    #print dMVC.utils.statClient.strClient()
    #print dMVC.utils.statEventTriggered.strEvent()
    sys.exit(0)

  def start(self, params):
    pygame.init()
    #self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ,pygame.HWSURFACE|pygame.FULLSCREEN,0)
    self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ)
    pygame.display.set_caption(GG.utils.VERSION)

    if params.ip:
      try:
        client = dMVC.remoteclient.RClient(params.ip)
      except Exception, excep:
        print excep, "No hay conexion con el servidor"
        self.finish()
      self.system = client.getRootModel()
    else:
      self.system = GG.model.ggsystem.GGSystem()

    login = self.system.login(params.user, params.password)
    if not login[0]:
      print login[1]
      self.finish()
    self.session = login[1] 
    self.player = self.session.getPlayer()
    self.isoHud = self.session.defaultView(self.screen)
    self.isoHud.draw()
    while True:
      time.sleep(GG.utils.ANIM_DELAY)
      self.input(pygame.event.get())
      self.isoHud.updateFrame()
  
