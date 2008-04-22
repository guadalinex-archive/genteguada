import math
import utils

class IsoView:
  """ IsoView Superclass.
  It defines atributes and methods for a generic view.
  """
  
  def __init__(self, model, screen):
    """ Class constructor.
    name: view name.
    """  
    self.__model = model
    self.__screen = screen
    
  def getModel(self):
    """ Returns the list of observed models.
    """
    return self.__model
  
  def getScreen(self):
    """ Returns the screen handler.
    """
    return self.__screen
  
  def p3dToP2d(self, cord3d, offset):
    """ Returns the physical 2d coordinates of a 3d virtual point.
    cord3d: 3d virtual point.
    offset: point's offset on screen.
    """
    x2d = (cord3d[0] - cord3d[2]) * utils.COS30R * utils.TILE_SZ[0]
    y2d = ((cord3d[0] + cord3d[2]) * utils.SIN30R) - cord3d[1]
    y2d = (y2d * utils.TILE_SZ[1])

    x2d = x2d - (offset[0])
    y2d = y2d - (offset[1])
    
    x2d = math.floor((x2d / math.sqrt(3)) + utils.SCREEN_OR[0])
    y2d = math.floor(y2d + utils.SCREEN_OR[1])
    
    cord2d = [x2d, y2d]
    return cord2d