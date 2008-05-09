import GG.utils

class Animation:
    
  def __init__(self, time, img, destination):
    self.__time = time
    self.__step = 0
    self.__img = img
    # Tanto "origin" como "destination" son coordenadas 2d
    self.__origin = img.rect.topleft
    self.__destination = destination
    self.__shift = [((self.__origin[0] - self.__destination[0]) /self.__time), 
      ((self.__origin[1] - self.__destination[1]) /self.__time)]
    
  def move(self):
    #print "nos vamos con el ", (self.__step * self.__shift[0])
    ori = self.__img.rect.topleft
    self.__img.rect.topleft = [ori[0] - self.__shift[0], ori[1] - self.__shift[1]]
    self.__step += 1
    if self.__step >= self.__time:
      return False
    return True
  
  def getStep(self):
    return self.__step