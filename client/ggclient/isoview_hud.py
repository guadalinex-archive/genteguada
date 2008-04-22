import pygame
import utils
import isoview

class IsoViewHud(isoview.IsoView):
  """ IsoViewHud class.
  Defines the HUD.
  """
  
  def __init__(self, model, screen):
    """ Class constructor.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__textFont = pygame.font.Font(None, 22)
    self.__textRect = pygame.Rect((utils.CHAT_OR[0], utils.CHAT_OR[1], utils.CHAT_SZ[0], utils.CHAT_SZ[1]))
  
  def getTextFont(self):
    return self.__textFont
  
  def getTextRect(self):
    return self.__textRect
    
  def paint(self):
    """ Paints all HUD parts on screen.
    """
    self.paintHud()
    self.paintChat()
    pygame.display.update()

  def paintHud(self):
    """ Paints the HUD on screen.
    """
    pygame.draw.rect(self.getScreen(), utils.HUD_COLOR_BORDER1,
              (utils.HUD_OR[0], utils.HUD_OR[1], utils.HUD_SZ[0] - 1, utils.HUD_SZ[1] - 1))
    pygame.draw.rect(self.getScreen(), utils.HUD_COLOR_BORDER2,
              (utils.HUD_OR[0] + 2, utils.HUD_OR[1] + 2, utils.HUD_SZ[0] - 5, utils.HUD_SZ[1] - 5))
    pygame.draw.rect(self.getScreen(), utils.HUD_COLOR_BORDER3,
              (utils.HUD_OR[0] +10, utils.HUD_OR[1] +10, utils.HUD_SZ[0] -21, utils.HUD_SZ[1] -21))
    pygame.draw.rect(self.getScreen(), utils.HUD_COLOR_BASE,
              (utils.HUD_OR[0] + 12, utils.HUD_OR[1] + 12, utils.HUD_SZ[0] - 25, utils.HUD_SZ[1] - 25))

  def paintChat(self):
    """ Paints the chat window on screen.
    """
    pygame.draw.rect(self.getScreen(), utils.CHAT_COLOR_BG,
              (utils.CHAT_OR[0], utils.CHAT_OR[1], utils.CHAT_SZ[0] - 1, utils.CHAT_SZ[1] - 1))
    
  def printOnChat(self, string):
    """ Prints a string on the HUD chat window.
    string: the info that will be printed on screen.
    """
    renderedText = utils.renderTextRect(string, self.getTextFont(), self.getTextRect(), utils.CHAT_COLOR_FONT, utils.CHAT_COLOR_BG, 0)
    self.getScreen().blit(renderedText, self.getTextRect().topleft)
    pygame.display.update()
    