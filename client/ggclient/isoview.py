import math
import utils

class IsoView:
  """ IsoView Superclass.
  It defines atributes and methods for a generic view.
  """
  
  def __init__(self, name):
    """ Class constructor.
    name: view name.
    """  
    self.__name = name
    self.__modelList = []
    self.__type = 0

  def getName(self):
    """ Returns the view label.
    """
    return self.__name
  
  def getModelList(self):
    """ Returns the list of observed models.
    """
    return self.__modelList
  
  def getType(self):
    """ Returns the type of the viewed model, beeing: -1: tile, 0: player, 1: object.
    """
    return self.__type
  
  def setName(self, name):
    """ Sets a new label for the view.
    """
    self.__name = name
    
  def addModel(self, model):
    """ Adds a model to the controlled models list
    model: new model.
    """
    self.__modelList.append(model)
    model.register(self)
  
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