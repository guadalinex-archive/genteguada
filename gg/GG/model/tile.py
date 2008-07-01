import room
import GG.model.ggmodel

class Tile(GG.model.ggmodel.GGModel):

  def __init__(self, position, spriteName, anchor, room):
    GG.model.ggmodel.GGModel.__init__(self)
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

  def getRoom(self):
    return self.__room

  def stackItem(self, item):
    self.__items.append(item)
    
  def unstackItem(self):
    aux = self.__items.pop()
    aux = None
    
    
  def getTopItem(self):
    if len(self.__items) == 0:
      return None
    return self.__items[len(self.__items)-1]  
  
  def getItems(self):
    return self.__items  
    
  def getItemsAndDestroy(self):
    items = self.__items
    self.__items = []
    return items

  def getItemsFrom(self, item):
    items = []
    k = 0
    for it in self.__items:
      if it == item:
        items.append(it)
        k = 1
      elif k:  
        items.append(it)
    return items

  def getItemsAndDestroyFrom(self, item):
    items = []
    k = 0
    for it in self.__items:
      if not k:
        if it == item:
          items.append(it)
          self.__items.remove(it)  
          k = 1
      else:
        items.append(it)
        self.__items.remove(it)
    return items

  def stepOn(self):
    x = len(self.__items)-1
    while x >= 0:
      if self.__items[x].stepOn():
        x -= 1
      else:
        return False
    return True  