import pygame
import utils
import isoview

class IsoViewHud(isoview.IsoView):
  """ Clase IsoViewHud.
  Define a la vista del interfaz de usuario.
  """
  
  def __init__(self, name, screen):
    """ Constructor de la clase.
    name: nombre de la vista.
    screen: controlador de pantalla.
    """
    isoview.IsoView.__init__(self, name)
    self.screen = screen
    
  def paint(self):
    """ Reliza llamadas para pintar el interfaz de usuario.
    """
    self.paintHud()
    self.paintChat()
    pygame.display.update()

  def paintHud(self):
    """ Pinta en pantalla el interfaz de usuario.
    """
    #screen = pygame.display.set_mode(utils.SCREEN_SZ)
    pygame.draw.rect(self.screen, utils.HUD_COLOR_BORDER1,
              (utils.HUD_OR[0], utils.HUD_OR[1], utils.HUD_SZ[0] - 1, utils.HUD_SZ[1] - 1))
    pygame.draw.rect(self.screen, utils.HUD_COLOR_BORDER2,
              (utils.HUD_OR[0] + 2, utils.HUD_OR[1] + 2, utils.HUD_SZ[0] - 5, utils.HUD_SZ[1] - 5))
    pygame.draw.rect(self.screen, utils.HUD_COLOR_BORDER3,
              (utils.HUD_OR[0] +10, utils.HUD_OR[1] +10, utils.HUD_SZ[0] -21, utils.HUD_SZ[1] -21))
    pygame.draw.rect(self.screen, utils.HUD_COLOR_BASE,
              (utils.HUD_OR[0] + 12, utils.HUD_OR[1] + 12, utils.HUD_SZ[0] - 25, utils.HUD_SZ[1] - 25))

  def paintChat(self):
    """ Pinta un recuadro de chat en el interfaz de usuario.
    """
    pygame.draw.rect(self.screen, utils.CHAT_COLOR_BG,
              (utils.CHAT_OR[0], utils.CHAT_OR[1], utils.CHAT_SZ[0] - 1, utils.CHAT_SZ[1] - 1))
    