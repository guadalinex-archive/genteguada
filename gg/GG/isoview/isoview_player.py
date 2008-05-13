import os
import math
import pygame
import isoview_item
import GG.utils

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
    self.getModel().subscribeEvent('heading', self.headingChanged)
    #self.getModel().subscribeEvent('state', self.stateChanged)
    #self.getModel().subscribeEvent('destination', self.destinationChanged)
    self.getModel().subscribeEvent('addInventory', self.inventoryAdded)
    self.getModel().subscribeEvent('removeInventory', self.inventoryRemoved)

  def headingChanged(self, event):
    """ Changes the player's sprite heading.
    """
    #self.setImg(GG.utils.NINO_SPRITES[event.getParams()["heading"]])
    self.setImg(self.getModel().spriteList[event.getParams()["heading"]])
    
  def inventoryAdded(self, event):
    """ Triggers after receiving an inventory added event.
    event: event info.
    """
    self.getParent().addInventoryItem(event.getParams()["item"])
    
  def inventoryRemoved(self, event):
    """ Triggers after receivint an inventory removed event.
    event: event info.
    """
    self.getParent().removeInventoryItem(event.getParams()["item"])
  