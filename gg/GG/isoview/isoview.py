

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

  def unsubscribeAllEvents(self):
    """ Unsubscribe this view's model from all events.
    """
    pass
    #print self.getModel()
    #self.getModel().unsubscribeEventObserver(self)
