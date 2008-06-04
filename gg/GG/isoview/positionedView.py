import isoview

class PositionedView(isoview.IsoView):
  """ PositionedView class.
  """
  
  def __init__(self, model, screen):
    """ Class constructor.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)

  def getScreenPosition(self):
    raise "Error: getScreenPosition"

  def setScreenPosition(self, pos):
    raise "Error: setScreenPosition"