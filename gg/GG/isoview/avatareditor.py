import os
import sys
import time
import ocempgui.widgets
import GG.utils
import pygame
import pygame.locals



class AvatarEditor:

  def __init__(self):
    print "Iniciando Avatar Editor"
    #Iniciar las ventanas pygame
    pygame.init()
    #self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ,pygame.HWSURFACE|pygame.FULLSCREEN,0)
    self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ)
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
    background = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
    self.screen.fill(GG.utils.GUADALINEX_BLUE, background)
    
    #imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.DUMMY)
    #dummyImage = pygame.sprite.Sprite()
    #dummyImage.image = pygame.image.load(imgPath).convert_alpha()
    #dummyImage.rect = dummyImage.image.get_rect()
    #dummyImage.rect.topleft = [50,50]
    
    customizeZone = pygame.Rect(0, 0, 386, 765)
    self.screen.fill((110,171,234), customizeZone)
    
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.DUMMY)
    dummyImage = pygame.image.load(imgPath)
    self.screen.blit(dummyImage, (528,114))
    pygame.display.flip()
    

        
    pygame.display.update()

  def input(self,events):
    for event in events:
      if event.type == pygame.locals.QUIT:
	sys.exit(0)
    self.renderer.distribute_events(*events)


if __name__=="__main__":
  AvatarEditor()
