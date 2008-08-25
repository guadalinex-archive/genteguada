# -*- coding: utf-8 -*-

import isoview

class PositionedView(isoview.IsoView):
  """ PositionedView class.
  Defines a positioned view object.
  """
  
  def __init__(self, model, screen):
    """ Class constructor.
    model: view model.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)

  def getScreenPosition(self):
    raise "Error: getScreenPosition"

  def setScreenPosition(self, pos):
    raise "Error: setScreenPosition"
