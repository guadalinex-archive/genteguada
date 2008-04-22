import ggmodel

class GGItem(ggmodel.GGModel):
  
  def __init__(self, sprite, size, position, offset):
    ggmodel.GGModel.__init__(self)
    self.__sprite = sprite
    self.__size = size
    self.__position = position
    self.__offset = offset
    
  def getSprite(self):
    return self.__sprite
    
  def getPosition(self):
    return self.__position
 
  def getOffset(self):
    return self.__offset
  
  def setPosition(self, pos):
    self.__position = pos
    
  