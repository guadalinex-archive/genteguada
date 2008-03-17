import pygame
from observer import *

#******************************************************************************
# CLASE OBS_HUD (subclase de OBSERVER)
# Observador de HUD

class ObserverHud(Observer):
  
  def paint(self):
    self.paintHud()

  def paintHud(self):
    screen = pygame.display.set_mode(SCREEN_SZ)
    pygame.draw.rect(screen, HUD_COLOR_BORDER1, (HUD_OR[0], HUD_OR[1], \
                                                 HUD_SZ[0] - 1, HUD_SZ[1] - 1))
    pygame.draw.rect(screen, HUD_COLOR_BORDER2, (HUD_OR[0] + 2,HUD_OR[1] + 2, \
                                                 HUD_SZ[0] - 5, HUD_SZ[1] - 5))
    pygame.draw.rect(screen, HUD_COLOR_BORDER3, (HUD_OR[0] +10, HUD_OR[1] +10, \
                                                 HUD_SZ[0] -21, HUD_SZ[1] -21))
    pygame.draw.rect(screen, HUD_COLOR_BASE, (HUD_OR[0] + 12, HUD_OR[1] + 12, \
                                              HUD_SZ[0] - 25, HUD_SZ[1] - 25))
    pygame.display.update()
