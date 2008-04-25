import os
import math
import pygame
import isoview_item

class IsoViewPlayer(isoview_item.IsoViewItem):
  """ IsoViewPlayer class.
  Defines a player view.
  """
  
  def __init__(self, model, screen, room, parent):
    """ Class constructor.
    model: observed object.
    screen: screen handler.
    room: the room where the player is.
    parent: isoview_hud handler.
    """
    isoview_item.IsoViewItem.__init__(self, model, screen, room, parent)
    self.getModel().subscribeEvent('position', self.changedPosition)
    
  def changedPosition(self, event):
    """ Updates the item position and draws the room after receiving a position change event.
    event: even info.
    """
    self.getImg().rect.topleft = self.p3dToP2d(event.getParams()["position"], self.getModel().getOffset())
    self.getIVRoom().draw()
    
 
