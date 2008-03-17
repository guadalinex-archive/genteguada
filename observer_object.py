import pygame
from observer_item import *

#******************************************************************************
# CLASE OBS_OBJECT (subclase de OBS_ITEM)
# Observador de un objeto

class ObserverObject(ObserverItem):

  def notify(self, caller, event):
    self.paintObject(OBJ_BOOK_SPRITE1, [3, 0, 2])

  def paintObject(self, sprite, cord3d):
    pl = os.path.join("data", sprite)
    plSurface = pygame.image.load(pl)
    screen.blit(plSurface, self.p3dToP2d(cord3d))
    pygame.display.update()

  def getType(self):
    return 2
