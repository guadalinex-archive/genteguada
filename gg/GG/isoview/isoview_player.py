import os
import math
import pygame
import isoview_item

class IsoViewPlayer(isoview_item.IsoViewItem):
  
  def __init__(self, model, screen, room, parent):
    """ Class constructor.
    screen: screen handler.
    """
    isoview_item.IsoViewItem.__init__(self, model, screen, parent)
    self.__ivroom = room
    #self.__modelData["pDestin"] = model.getDestination()
    #self.__modelData["dir"]:model.getHeading(), "step": 0})
    self.getModel().subscribeEvent('position', room.startMovementEventFired)
    
  def newAction(self, event):
    """ Runs an event associated with a new action.
    event: even info.
    """
    #print event
    #pass
    #self.triggerEvent('position', player=self, pActual=pActualAux, pDestin=self.__position, dir=self.__heading)
    self.getImg().rect.topleft = self.p3dToP2d(event.getParams()["pDestin"], event.getParams()["player"].getOffset())
    #self.__modelData["pActual"] = event.getParams()["pDestin"]
    #self.__modelData["pDestin"] = event.getParams()["pDestin"]
    
