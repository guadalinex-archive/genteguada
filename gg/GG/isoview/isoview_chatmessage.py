import pygame
import GG.utils
import animation
import positioned_view

class IsoViewChatMessage(positioned_view.PositionedView):
  """ IsoViewChatMessage class.
  Defines a chat message view.
  """
  
  def __init__(self, model, screen):
    """ Class constructor.
    model: chat message model.
    screen: screen handler.
    """
    positioned_view.PositionedView.__init__(self, model, screen)
    