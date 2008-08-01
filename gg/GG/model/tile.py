import ggmodel

class Tile(ggmodel.GGModel):

  def __init__(self, position, spriteName, anchor, room):
    ggmodel.GGModel.__init__(self)
    self.__items = []
    self.__room = room
    self.position = position
    self.spriteName = spriteName
    self.anchor = anchor
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['position', 'spriteName', 'anchor']

  def getDepth(self):
    return len(self.__items)

  def getItemDepth(self, item):
    return self.__items.index(item)

  def hasPlayer(self):
    items = self.__room.getItems()
    for item in items:
      if hasattr(item, "username"):
        return True
    return False

  def getRoom(self):
    return self.__room

  def stackItem(self, item):
    self.__items.append(item)
    
  def unstackItem(self):
    self.__items.pop()
    
  def getTopItem(self):
    if len(self.__items) == 0:
      return None
    return self.__items[len(self.__items)-1]  

  def getBottomItem(self):
    if len(self.__items) == 0:
      return None
    return self.__items[0]  
  
  def getItems(self):
    return self.__items  
    
  def getItemsAndDestroy(self):
    items = self.__items
    self.__items = []
    return items

  def getItemsFrom(self, item):
    items = []
    k = 0
    for itFrom in self.__items:
      if itFrom == item:
        items.append(itFrom)
        k = 1
      elif k == 1:  
        items.append(itFrom)
    return items

  def getItemsAndRemoveFrom(self, item):
    items = []
    k = 0
    for itFrom in self.__items:
      if itFrom == item:
        items.append(itFrom)
        self.__items.remove(itFrom)
        k = 1
      elif k:  
        items.append(itFrom)
        self.__items.remove(itFrom)
    return items

  def stepOn(self):
    xValue = len(self.__items)-1
    while xValue >= 0:
      if self.__items[xValue].stepOn():
        xValue -= 1
      else:
        return False
    return True  
