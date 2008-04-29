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
    #self.getModel().subscribeEvent('heading', self.headingChanged)
    #self.getModel().subscribeEvent('state', self.stateChanged)
    #self.getModel().subscribeEvent('destination', self.destinationChanged)
    #self.getModel().subscribeEvent('addInventory', self.inventoryAdded)
    #self.getModel().subscribeEvent('removeInventory', self.inventoryRemoved)
    
 
