import pygame
import GG.utils
import isoview

class IsoViewHud(isoview.IsoView):
  """ IsoViewHud class.
  Defines the HUD.
  """
  
  def __init__(self, model, screen):
    """ Class constructor.
    model: ggsession model.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__textFont = pygame.font.Font(None, 22)
    self.__textRect = pygame.Rect((GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1], GG.utils.CHAT_SZ[0], GG.utils.CHAT_SZ[1]))
    
  def pruebaChat(self, events):
    """ Procedimiento de prueba para el chat del Hud.
    """
    #string = events.getParams()["actor"].getUsername() + " clicked on " + events.getParams()["receiver"].getUsername()
    string = events.getParams()["actor"].getUsername() + " clicked on "
    self.printOnChat(string)
  
  def getTextFont(self):
    """ Returns the font used to print text on chat.
    """
    return self.__textFont
  
  def getTextRect(self):
    """ Returns the rectangle used to print text on chat.
    """
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
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER1,
              (GG.utils.HUD_OR[0], GG.utils.HUD_OR[1], GG.utils.HUD_SZ[0] - 1, GG.utils.HUD_SZ[1] - 1))
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER2,
              (GG.utils.HUD_OR[0] + 2, GG.utils.HUD_OR[1] + 2, GG.utils.HUD_SZ[0] - 5, GG.utils.HUD_SZ[1] - 5))
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER3,
              (GG.utils.HUD_OR[0] +10, GG.utils.HUD_OR[1] +10, GG.utils.HUD_SZ[0] -21, GG.utils.HUD_SZ[1] -21))
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BASE,
              (GG.utils.HUD_OR[0] + 12, GG.utils.HUD_OR[1] + 12, GG.utils.HUD_SZ[0] - 25, GG.utils.HUD_SZ[1] - 25))

  def paintChat(self):
    """ Paints the chat window on screen.
    """
    pygame.draw.rect(self.getScreen(), GG.utils.CHAT_COLOR_BG,
              (GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1], GG.utils.CHAT_SZ[0] - 1, GG.utils.CHAT_SZ[1] - 1))
    
  def printOnChat(self, string):
    """ Prints a string on the HUD chat window.
    string: the info that will be printed on screen.
    """
    renderedText = GG.utils.renderTextRect(string, self.getTextFont(), self.getTextRect(), GG.utils.CHAT_COLOR_FONT, GG.utils.CHAT_COLOR_BG, 0)
    self.getScreen().blit(renderedText, self.getTextRect().topleft)
    pygame.display.update()
    
