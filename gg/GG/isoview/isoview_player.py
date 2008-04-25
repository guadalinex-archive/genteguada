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
    isoview_item.IsoViewItem.__init__(self, model, screen, parent)
    self.__ivroom = room
    self.getModel().subscribeEvent('position', room.startMovementEventFired)
    
  def newAction(self, event):
    """ Runs an event associated with a new action.
    event: even info.
    """
    self.getImg().rect.topleft = self.p3dToP2d(event.getParams()["pDestin"], event.getParams()["player"].getOffset())
    
