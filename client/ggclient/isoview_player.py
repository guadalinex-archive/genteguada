import os
import math
import pygame
import utils
import isoview_item

class IsoViewPlayer(isoview_item.IsoViewItem):
  
  def __init__(self, model, screen):
    """ Class constructor.
    screen: screen handler.
    """
    isoview_item.IsoViewItem.__init__(self, model, screen)
    self.__modelData = ({"sprite":model.getSprite(), \
      "pActual":model.getPosition(), "pDestin":model.getDestination(), \
      "dir":model.getHeading(), "step": 0})

  def newAction(self, event):
    """ Runs an event associated with a new action.
    event: even info.
    """
    #self.triggerEvent('position', player=self, pActual=pActualAux, pDestin=self.__position, dir=self.__heading)
    self.getImg().rect.topleft = self.p3dToP2d(event.params["pDestin"], event.params["player"].getOffset())
    self.__modelData["pActual"] = event.params["pDestin"]
    self.__modelData["pDestin"] = event.params["pDestin"]
    
