import GG.utils

class Animation:
    
  def __init__(self, time, origin, destination):
    self.__time = time
    self.__step = 0
    self.__origin = origin
    self.__destination = destination
    
  def move(self):
    pass