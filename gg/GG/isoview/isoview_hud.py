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
  
  def getTextFont(self):
    """ Returns the font used to print text on chat.
    """
    return self.__textFont
  
  def getTextRect(self):
    """ Returns the rectangle used to print text on chat.
    """
    return self.__textRect
  
  def addInventoryItem(self, item):
    """
    """
    invItem = isoview_inventoryitem.IsoViewInventoryItem(item, self.getScreen())
    self.__isoviewinventory.append(invItem)
    self.paintInventory()
    
  def removeInventoryItem(self, item):
    """
    """
    for ivInventoryItem in self.__isoviewinventory:
      if ivInventoryItem.getModel().getLabel() == item.getLabel():
        toBeRemoved = ivInventoryItem
    self.__isoviewinventory.remove(toBeRemoved)
    self.paintInventory()
    
  def pruebaChat(self, events):
    """ Procedimiento de prueba para el chat del Hud.
    """
    self.printOnChat(events.getParams()["msg"])
    
  def clickedByPlayer(self, player, target):
    """ Indicates that a player has made click the isoview hud object.
    player: player who clicks.
    target: clicked point.
    """
    if not len(self.__isoviewinventory):
      return
    if GG.utils.INV_OR[0] < target[0] < (GG.utils.INV_OR[0] + GG.utils.INV_SZ[0]):
      if GG.utils.INV_OR[1] < target[1] < (GG.utils.INV_OR[1] + GG.utils.INV_SZ[1]):
        # click on the inventory
        auxTarget = [target[0] - GG.utils.INV_OR[0], target[1] - GG.utils.INV_OR[1]]
        i = j = k = itemPos = 0
        while j < GG.utils.INV_ITEM_COUNT[1] and not k:
          while i < GG.utils.INV_ITEM_COUNT[0] and not k:
            if GG.utils.INV_ITEM_SZ[0]*i < auxTarget[0] < (GG.utils.INV_ITEM_SZ[0]*i + GG.utils.INV_ITEM_SZ[0]-1):
              if GG.utils.INV_ITEM_SZ[1]*j < auxTarget[1] < (GG.utils.INV_ITEM_SZ[1]*j + GG.utils.INV_ITEM_SZ[1]-1):
                k = 1
                itemPos = j*GG.utils.INV_ITEM_COUNT[0] + i
            i += 1
          j += 1
        # click on an inventory item, itemPos
        if k:
          self.printOnChat(self.__isoviewinventory[itemPos].getLabel())
          self.getModel().getPlayer().clickOnInventoryItem(self.__isoviewinventory[itemPos].getModel())
        #  self.removeInventoryItem(self.__isoviewinventory[itemPos])
          
  # Paint methods
    
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
    n = 0
    for inventoryitem in self.__isoviewinventory:
      self.paintItemOnInventory(inventoryitem.getSpriteName(), n)
      n += 1
    
  def printOnChat(self, string):
    """ Prints a string on the HUD chat window.
    string: the info that will be printed on screen.
    """
    renderedText = GG.utils.renderTextRect(string, self.getTextFont(), self.getTextRect(), GG.utils.CHAT_COLOR_FONT, GG.utils.CHAT_COLOR_BG, 0)
    self.getScreen().blit(renderedText, self.getTextRect().topleft)
    pygame.display.update()
    
