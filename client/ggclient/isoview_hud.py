import pygame
import utils
import isoview

class IsoViewHud(isoview.IsoView):
  """ IsoViewHud class.
  Defines the HUD.
  """
  
  def __init__(self, name, screen):
    """ Class constructor.
    name: HUD label.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, name)
    self.screen = screen
    
  def paint(self):
    """ Paints all HUD parts on screen.
    """
    self.paintHud()
    self.paintChat()
    pygame.display.update()

  def paintHud(self):
    """ Paints the HUD on screen.
    """
    pygame.draw.rect(self.screen, utils.HUD_COLOR_BORDER1,
              (utils.HUD_OR[0], utils.HUD_OR[1], utils.HUD_SZ[0] - 1, utils.HUD_SZ[1] - 1))
    pygame.draw.rect(self.screen, utils.HUD_COLOR_BORDER2,
              (utils.HUD_OR[0] + 2, utils.HUD_OR[1] + 2, utils.HUD_SZ[0] - 5, utils.HUD_SZ[1] - 5))
    pygame.draw.rect(self.screen, utils.HUD_COLOR_BORDER3,
              (utils.HUD_OR[0] +10, utils.HUD_OR[1] +10, utils.HUD_SZ[0] -21, utils.HUD_SZ[1] -21))
    pygame.draw.rect(self.screen, utils.HUD_COLOR_BASE,
              (utils.HUD_OR[0] + 12, utils.HUD_OR[1] + 12, utils.HUD_SZ[0] - 25, utils.HUD_SZ[1] - 25))

  def paintChat(self):
    """ Paints the chat window on screen.
    """
    pygame.draw.rect(self.screen, utils.CHAT_COLOR_BG,
              (utils.CHAT_OR[0], utils.CHAT_OR[1], utils.CHAT_SZ[0] - 1, utils.CHAT_SZ[1] - 1))
    