
import dMVC.remoteclient
import pygame
import GG.utils
import GG.model.ggsystem
import time
from pygame.locals import *
import sys

class GenteGuada:

  def input(self,events):
    for event in events:
      if event.type == QUIT:
        self.finish()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          self.finish()
        elif event.key == 13:
          self.isoHud.chatMessageEntered()
      if event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        if y > GG.utils.GAMEZONE_SZ[1]:
          self.isoHud.clickedByPlayer(self.player, [x, y])
        else:  
          dest = self.isoHud.getIsoviewRoom().findTile([x,y])
          if not dest == [-1, -1]:
            self.isoHud.getIsoviewRoom().getModel().clickedByPlayer(self.player, [dest[0], 0, dest[1]])
  
    self.isoHud.widgetContainer.distribute_events(*events)

  def finish(self):
    #print dMVC.utils.statClient.strClient()
    #print dMVC.utils.statEventTriggered.strEvent()
    sys.exit(0)

  def start(self,params):
    pygame.init()
    #self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ,pygame.HWSURFACE|pygame.FULLSCREEN,0)
    self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ)
    pygame.display.set_caption(GG.utils.VERSION)

    if params.ip:
      try:
        client = dMVC.remoteclient.RClient(params.ip)
      except:
        print "No hay conexion con el servidor"
        self.finish()
      self.sy = client.getRootModel()
    else:
      self.sy = GG.model.ggsystem.GGSystem()

    # Declaraciones solo para pruebas
    #self.tree = GG.model.item.GGItem(GG.utils.OAK_SPRITE, [267, 200], [6, 0, 6], [95, 195])
    #self.girl = GG.model.player.GGPlayer(GG.utils.NINA_SPRITE, GG.utils.NINA_SPRITES, GG.utils.NINO_SZ, [2, 0, 2], [2*GG.utils.CHAR_SZ[0]-75, GG.utils.CHAR_SZ[1]-20], "pepe2", "12345")
                    
    login = self.sy.login(params.user, params.password)
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
  
