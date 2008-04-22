import dMVC.model

class GGModel(dMVC.model.Model):
  """ Model class.
  Defines a generic model, its attributes and behaviour.
  """
  
  def __init__(self):
    """ Class constructor.
    """
    dMVC.model.Model.__init__(self)
    
  def defaultView(self):
    raise "Metodo no definido en los hijos"
  