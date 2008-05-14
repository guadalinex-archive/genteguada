import os
import pygame
import isoview_item
import GG.utils

class IsoViewGhostItem(isoview_item.IsoViewItem):
  """ IsoViewGhostItem class.
  Defines a ghost item view.
  """
  
  def __init__(self, model, screen, room, parent):
    """ Class constructor.
    model: observed object.
    screen: screen handler.
    room: the room where the ghost item is.
    parent: isoview_hud handler.
    """
    isoview_item.IsoViewItem.__init__(self, model, screen, room, parent)
    imgPath = os.path.join(GG.utils.DATA_PATH, model.spriteName)
    img = pygame.sprite.Sprite()
    img.image = pygame.image.load(imgPath).convert_alpha()
    img.rect = img.image.get_rect()
    img.rect.topleft = model.getScreenPosition()
    self.setSprite(img)
    