
class Animation:
  """ Animation class.
  Defines animation methods and atributes.
  """
    
  def __init__(self, time, img, destination):
    """ Class constructor.
    time: number of frames the animation will last.
    img: sprite used for the animation.
    destination: animation destination.
    """
    self.__time = time
    self.__step = 0
    self.__img = img
    self.__origin = img.rect.topleft
    self.__destination = destination
    self.__shift = [((self.__origin[0] - self.__destination[0]) / self.__time), 
      ((self.__origin[1] - self.__destination[1]) /self.__time)]
    
  def move(self):
    """ Moves the sprite to the next frame position.
    """
    ori = self.__img.rect.topleft
    self.__img.rect.topleft = [ori[0] - self.__shift[0], ori[1] - self.__shift[1]]
    self.__step += 1
    if self.__step >= self.__time:
      return False
    return True
  
  def getStep(self):
    """ Returns the frame step the animations is at.
    """
    return self.__step
  
  def restart(self, time, newDestination):
    """ Restarts the animation and sets a new lenght and destination.
    time: new animation lenght.
    newDestination: new animation destination.
    """
    self.__time = time
    self.__step = 0
    self.__origin = self.__destination
    self.__destination = newDestination
    self.__shift = [((self.__origin[0] - self.__destination[0]) /self.__time), 
      ((self.__origin[1] - self.__destination[1]) /self.__time)]
    self.__img.rect.topleft = self.__origin
    
