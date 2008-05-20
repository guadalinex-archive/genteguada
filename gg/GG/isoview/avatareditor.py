import pygame
import time
import ocempgui.widgets
import sys
import pygame.locals

class AvatarEditor:

  def __init__(self):
    print "Iniciando Avatar Editor"
    #Iniciar las ventanas pygame
    pygame.init()
    #self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ,pygame.HWSURFACE|pygame.FULLSCREEN,0)
    self.screen = pygame.display.set_mode([1024,768])
    pygame.display.set_caption("DEMO AVATAR GENERATOR")
    self.renderer = ocempgui.widgets.Renderer()
    self.renderer.set_screen(self.screen)
    self.paintScreen()
    #Creamos el Renderer
    while True:
      time.sleep(0.4)
      self.input(pygame.event.get())

  def paintScreen(self):
    print "Pinta la pantalla"
    print self.screen.get_width()
    print self.screen.get_height()
    rect = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
    self.screen.fill((34, 133, 234), rect)
    
    image = pygame.Image
    
    
    pygame.display.update()

  def input(self,events):
    for event in events:
      if event.type == pygame.locals.QUIT:
	sys.exit(0)
    self.renderer.distribute_events(*events)


if __name__=="__main__":
  AvatarEditor()
