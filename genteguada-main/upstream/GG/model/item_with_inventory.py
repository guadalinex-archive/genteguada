import room_item
import ggmodel

class GGItemWithInventory(room_item.GGRoomItem):
  """ GGItemWithInventory class.
  Defines an item with inventory.
  """
 
  def __init__(self, spritePath):
    """ Class builder.
    spriteList: sprite list used to paint the player.
    position: player position.
    """
    room_item.GGRoomItem.__init__(self, spritePath)
    self.__inventory = []

  def objectToPersist(self):
    dict = room_item.GGRoomItem.objectToPersist(self)
    itemsToPersist = []
    for item in self.__inventory:
      itemsToPersist.append(item.objectToPersist())
    dict["inventory"] = itemsToPersist
    return dict

  def load(self, dict):
    room_item.GGRoomItem.load(self, dict)
    self.__inventory = []
    for itemDict in dict["inventory"]:
      item = ggmodel.GGModel.read(itemDict["id"], "player", itemDict)
      item.setPlayer(self)
      self.__inventory.append(item)

  # self.__inventory
  
  def getInventory(self):
    """ Returns the item's inventory.
    """  
    dictInventory = {}
    i = 0
    for invItem in self.__inventory:
      dictInventory[i] = {"name":invItem.getName(), "object":invItem}
      i+=1
    return dictInventory  
  
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
    """ Checks if there is an item on the inventory.
    label: item inventory.
    """  
    for item in self.__inventory:
      if item.label == label:
        return True  
    return False    
    
  def addToInventory(self, item, position = None):
    """ Adds a new item to inventory from room.
    item: new item.
    """  
    self.__inventory.append(item)
    item.setPlayer(self)
    if not position:
      position = item.getPosition()
    self.triggerEvent('addToInventory', item=item, position = position, itemName = item.getName())
    self.save("player")
    
  def removeFromInventory(self, item):
    """ Removes an item from the player's inventory.
    item: item to be removed.
    """
    if item in self.__inventory:
      self.__inventory.remove(item)
      self.triggerEvent('removeFromInventory', item=item)
      self.save("player")
      return True
    return False
  
  def addToRoomFromInventory(self, item, dropLocation):
    """ Removes an item from the inventory and drops it in front of the player.
    item: item to drop.
    dropLocation: item's drop location.
    """
    itemOnPosition = self.getRoom().getItemOnPosition(dropLocation)
    if dropLocation == [-1, -1]: 
      return False
    if itemOnPosition != None:
      if not itemOnPosition.isStackable():
        return False
    if not self.getRoom().addItemFromInventory(item, dropLocation):
      return False
    self.__inventory.remove(item)
    item.setPlayer(None)
    self.save("player")
    self.newChatMessage(item.getName() + " depositado en el suelo", 1)
    
  def tick(self, now):
    """ Call for an update on item.
    now: ellapsedTime.
    """
    for item in self.__inventory:
      item.tick(now)

  def getItemFromInventory(self, label):
    """ Gets an item from the inventory.
    label: item's label.
    """  
    for item in self.__inventory:
      if item.label == label:
        return item 
    return None
