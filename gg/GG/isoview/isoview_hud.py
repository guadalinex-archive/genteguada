import os
import pygame
import GG.utils
import isoview
import isoview_inventoryitem

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
    self.__isoviewinventory = []
    self.__textFont = pygame.font.Font(None, 22)
    self.__textRect = pygame.Rect((GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1], GG.utils.CHAT_SZ[0], GG.utils.CHAT_SZ[1]))
    
  def addInventoryItem(self, item):
    """
    """
    invItem = isoview_inventoryitem.IsoViewInventoryItem(item.getSpriteInventory(), item.getLabel())
    self.__isoviewinventory.append(invItem)
    n = 0
    for inventoryitem in self.__isoviewinventory:
      self.paintItemOnInventory(inventoryitem.getSpriteName(), n)
      n += 1
    
  def pruebaChat(self, events):
    """ Procedimiento de prueba para el chat del Hud.
    """
    self.printOnChat(events.getParams()["msg"])
  
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
    self.paintInventory()
    #self.paintItemOnInventory(GG.utils.PENGUIN_SPRITE, 0)
    pygame.display.update()

  def paintHud(self):
    """ Paints the HUD on screen.
    """
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER1,
              (GG.utils.HUD_OR[0], GG.utils.HUD_OR[1], GG.utils.HUD_SZ[0] - 1, GG.utils.HUD_SZ[1] - 1))
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER2,
              (GG.utils.HUD_OR[0] + 2, GG.utils.HUD_OR[1] + 2, GG.utils.HUD_SZ[0] - 5, GG.utils.HUD_SZ[1] - 5))
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BORDER3,
              (GG.utils.HUD_OR[0] + 10, GG.utils.HUD_OR[1] + 10, GG.utils.HUD_SZ[0] - 21, GG.utils.HUD_SZ[1] - 21))
    pygame.draw.rect(self.getScreen(), GG.utils.HUD_COLOR_BASE,
              (GG.utils.HUD_OR[0] + 12, GG.utils.HUD_OR[1] + 12, GG.utils.HUD_SZ[0] - 25, GG.utils.HUD_SZ[1] - 25))

  def paintChat(self):
    """ Paints the chat window on screen.
    """
    pygame.draw.rect(self.getScreen(), GG.utils.CHAT_COLOR_BG,
              (GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1], GG.utils.CHAT_SZ[0] - 1, GG.utils.CHAT_SZ[1] - 1))
    
  def paintItemOnInventory(self, spriteName, position):
    """ Paints an item on the hud inventory.
    spriteName: sprite name.
    position: position in the inventory that the item will be painted into.
    """
    if position >= GG.utils.INV_ITEM_COUNT[0]*GG.utils.INV_ITEM_COUNT[1]:
      return
    imgPath = os.path.join(GG.utils.DATA_PATH, spriteName)
    img = pygame.sprite.Sprite()
    img.image = pygame.image.load(imgPath)
    img.rect = img.image.get_rect()
    img.rect.topleft = [GG.utils.INV_OR[0] + (GG.utils.INV_ITEM_SZ[0]*(position%GG.utils.INV_ITEM_COUNT[0])),
                        GG.utils.INV_OR[1] + (GG.utils.INV_ITEM_SZ[1]*(position/GG.utils.INV_ITEM_COUNT[0]))]
    self.getScreen().blit(img.image, img.rect)
  
  def paintInventory(self):
    """ 
    """
    pygame.draw.rect(self.getScreen(), GG.utils.INV_COLOR_BG,
              (GG.utils.INV_OR[0], GG.utils.INV_OR[1], GG.utils.INV_SZ[0] - 1, GG.utils.INV_SZ[1] - 1))
    pass
  
  def printOnChat(self, string):
    """ Prints a string on the HUD chat window.
    string: the info that will be printed on screen.
    """
    renderedText = GG.utils.renderTextRect(string, self.getTextFont(), self.getTextRect(), GG.utils.CHAT_COLOR_FONT, GG.utils.CHAT_COLOR_BG, 0)
    self.getScreen().blit(renderedText, self.getTextRect().topleft)
    pygame.display.update()
    
