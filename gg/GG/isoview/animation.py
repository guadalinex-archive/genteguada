import GG.utils

class Animation:
  """ Animation class.
  Defines animation methods and atributes.
  """
    
  def __init__(self, time, img, destination):
    """ Class constructor.
    time: animation length in time.
    img: sprite used for the animation.
    destination: animation destination.
    """
    self.__time = time
    self.__img = img
    self.__origin = img.rect.topleft
    self.__destination = destination
    #self.__shift = [((self.__origin[0] - self.__destination[0]) / self.__time), ((self.__origin[1] - self.__destination[1]) /self.__time)]
    
  def step(self, time):
    """ Moves the sprite to the next frame position.
    time: time passed since the animation start.
    """
    ori = self.__img.rect.topleft
    if self.__time < time:
      return False
    shift = [(self.__time - time)*(self.__origin[0] - self.__destination[0])/GG.utils.ANIM_TIME, (self.__time - time)*(self.__origin[1] - self.__destination[1])/GG.utils.ANIM_TIME]
    self.__img.rect.topleft = [ori[0] - shift[0], ori[1] - shift[1]]
    return True
  
  def restart(self, time, newDestination):
    """ Restarts the animation and sets a new lenght and destination.
    time: new animation lenght.
    newDestination: new animation destination.
    """
    self.__time = time
    self.__origin = self.__destination
    self.__destination = newDestination
    #self.__shift = [((self.__origin[0] - self.__destination[0]) /self.__time), ((self.__origin[1] - self.__destination[1]) /self.__time)]
    self.__img.rect.topleft = self.__origin
    
