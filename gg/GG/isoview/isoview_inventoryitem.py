import isoview

class IsoViewInventoryItem(isoview.IsoView):
    
  def __init__(self, model, screen):
    """
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__spriteName = model.spriteInventory
    self.__label = model.label
    self.__count = 0

  def getSpriteName(self):
    """
    """
    return self.__spriteName

  def getLabel(self):
    """
    """
    return self.__label
  
  def getCount(self):
    """
    """
    return self.__count
  
  def increaseCount(self):
    """
    """
    self.__count += 1
    
  def decreaseCount(self):
    """
    """
    self.__count -= 1