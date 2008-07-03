import GG.model.room_item
import GG.utils
import dMVC.model

class GGItemWithInventory(GG.model.room_item.GGRoomItem):
  """ GGItemWithInventory class.
  """
 
  def __init__(self, spritePath, anchor, topAnchor):
    """ Class builder.
    spriteList: sprite list used to paint the player.
    position: player position.
    anchor: image anchor on screen.
    """
    GG.model.room_item.GGRoomItem.__init__(self, spritePath, anchor, topAnchor)
    self.__inventory = []
    
  # self.__inventory
  
  def setInventory(self, inventory):
    """ Sets a new player's inventory.
    inventory: new player's inventory.
    """
    if not self.__inventory == inventory:
      self.__inventory = inventory
      self.triggerEvent('inventory', inventory=inventory)
      return True
    return False
  
  def hasItemLabeledInInventory(self, label):
    for item in self.__inventory:
      if item.label == label:
        return True  
    return False    
      
  def addToInventoryFromRoom(self, item):
    self.__inventory.append(item)
    item.setPlayer(self)
    self.triggerEvent('addToInventory', item=item, position=item.getPosition())
    
  def addToInventoryFromVoid(self, item, position):
    self.__inventory.append(item)
    item.setPlayer(self)
    self.triggerEvent('addToInventory', item=item, position=position)
    
  def removeFromInventory(self, item):
    """ Removes an item from the player's inventory.
    item: item to be removed.
    """
    if item in self.__inventory:
      self.__inventory.remove(item)
      #item.setPlayer(None)
      self.triggerEvent('removeFromInventory', item=item)
      return True
    return False
  
  def addToRoomFromInventory(self, item, dropLocation):
    """ Removes an item from the inventory and drops it in front of the player.
    item: item to drop.
    dropLocation: item's drop location.
    """
    itemOnPosition = self.getRoom().getItemOnPosition(dropLocation)
    if dropLocation == [-1, -1, -1]: 
      return False
    if itemOnPosition != None:
      if not itemOnPosition.isStackable():
        return False
    if not self.getRoom().addItemFromInventory(item, dropLocation):
      return False
    self.__inventory.remove(item)
    item.setPlayer(None)
    self.triggerEvent('chat', actor=item, receiver=self, msg=item.label+" depositado en el suelo")
    
  def checkItemOnInventory(self, item):
    for it in self.__inventory:
      if it.checkSimilarity(item):
        return True
    return False      
 
  def tick(self, now):
    for item in self.__inventory:
      item.tick(now)

  def getItemFromInventory(self, label):
    for item in self.__inventory:
      if item.label == label:
        return item 
    return None

    
  
      
