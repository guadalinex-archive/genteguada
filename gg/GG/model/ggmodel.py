import dMVC.model

class GGModel(dMVC.model.Model):
  """ Model class.
  Defines a generic model, its attributes and behaviour.
  """
  
  def __init__(self):
    """ Class constructor.
    """
    dMVC.model.Model.__init__(self)
  
  @dMVC.model.localMethod
  def defaultView(self):
    raise Exception("Metodo no definido en los hijos")
  
