import GG.model.item
import GG.model.temp_pickable_item
import GG.model.chat_message
import GG.isoview.isoview_player
import GG.utils
import dMVC.model

class GGPlayer(GG.model.item.GGItem):
  """ Player class.
  Defines a player object behaviour.
  """
 
  def __init__(self, spritePath, position, offset, username, password):
    """ Class builder.
    spriteList: sprite list used to paint the player.
    position: player position.
    offset: image offset on screen.
    username: user name.
    password: user password.
    """
    GG.model.item.GGItem.__init__(self, "standing_down.png", position, offset)
    self.username = username
    self.__spritePath = spritePath
    self.__password = password # Not used outside this class
    self.__visited = [] # Not used outside this class
    self.__heading = "down"
    self.__state = "standing"
    self.__destination = position
    self.__inventory = []
    self.__visited = []
    self.__selected = None

  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.item.GGItem.variablesToSerialize(self)
    return parentVars + ['username']
  
  def getImagePath(self):
    return self.__spritePath

  # self.__heading

  def getHeading(self):
    """ Returns the direction the player is heading to.
    """
    return self.__heading
  
  def setHeading(self, heading):
    """ Sets a new heading direction for the item.
    """
    self.__heading = heading
    self.triggerEvent('heading', heading=heading)

  # self.__state
  
  def getState(self):
    """ Returns the player's state.
    """
    return self.__state
  
  def setState(self, state):
    """ Sets a new state for the item.
    """
    if not self.__state == state:
      self.__state = state
      self.triggerEvent('state', state=state)

  # self.__destination
  
  def getDestination(self):
    """ Returns the player's movement destination.
    """
    return self.__destination
  
  def setDestination(self, destination):
    """ Sets a new destination for the player movement.
    heading: movement direction.
    destination: movement destination.
    """
    if not self.__destination == destination:
      for vis in self.__visited:
        self.__visited.remove(vis)
      self.__visited = []
      self.__destination = destination
      self.triggerEvent('destination', destination=destination)

  def setStartDestination(self, destination):
    """ Sets a new destination for the player movement without calling for a 'destination' event.
    heading: movement direction.
    destination: movement destination.
    """
    if self.__destination != destination:
      for vis in self.__visited:
        self.__visited.remove(vis)
      self.__visited = []
      self.__destination = destination
      
  # self.__inventory
  
  def getInventory(self):
    """ Return the player's inventory.
    """
    return self.__inventory

  def setInventory(self, inventory):
    """ Sets a new player's inventory.
    inventory: new player's inventory.
    """
    if not self.__inventory == inventory:
      self.__inventory = inventory
      self.triggerEvent('inventory', inventory=inventory)
      return True
    return False

  def addInventory(self, item):
    """ Adds a new item to the player's inventory.
    item: new item.
    """
    self.__inventory.append(item)
    if isinstance(item, GG.model.temp_pickable_item.GGTempPickableItem):
      item.startCount()
    self.triggerEvent('addInventory', item=item)
    
  def removeInventory(self, item):
    """ Removes an item from the player's inventory.
    item: item to be removed.
    """
    if item in self.__inventory:
      self.__inventory.remove(item)
      self.triggerEvent('removeInventory', item=item)
      return True
    return False
  
  @dMVC.model.localMethod
  def defaultView(self, screen, room, parent):
    """ Creates a view object associated with this player.
    screen: screen handler.
    room: room view object.
    parent: hud or session view object.
    """
    return GG.isoview.isoview_player.IsoViewPlayer(self, screen, room, parent)
  
  def clickOnInventoryItem(self, item):
    """ Removes an item from the inventory and drops it in front of the player.
    item: item to drop.
    """
    dropLocation = GG.utils.getFrontPosition(self.getPosition(), self.__heading)
    if dropLocation == [-1, -1, -1] or self.getRoom().getBlocked(dropLocation):
      return False
    item.setPosition(dropLocation)
    self.getRoom().addItem(item, item.getPosition())
    self.removeInventory(item)
    self.triggerEvent('chat', actor=item, receiver=self, msg=item.label+" depositado en el suelo")
    
  def checkUser(self, username, password):
    """ Searchs for an user by his user name and password.
    username: user name.
    password: user password.
    """
    if self.username == username and self.__password == password:
      return 1
    return 0
  
  def hasBeenVisited(self, pos):
    """ Checks if a tile has been visited by the player on the last movement.
    pos: tile position.
    """
    if pos in self.__visited:
      return True
    return False
  
  def clickedBy(self, clicker):
    """ Triggers an event when the player receives a click by another player.
    clicker: player who clicks.
    """
    GG.model.item.GGItem.clickedBy(self, clicker)
    self.newChatMessage(clicker.username + ' ha pinchado en mi')
      
  def tick(self):
    """ Calls for an update on player's position an movement direction.
    """
    for item in self.__inventory:
      item.tick()
      if isinstance(item, GG.model.temp_pickable_item.GGTempPickableItem):
        if not item.timeLeft():
          self.removeInventory(item)
          item.getStartRoom().addItem(item, item.getPosition())
    if self.getPosition() == self.__destination:
      self.setState("standing")
      return
    direction = self.getRoom().getNextDirection(self, self.getPosition(), self.getDestination())
    if direction == "none":
      self.setDestination(self.getPosition())
      return
    pos = self.getPosition()
    self.setState("walking")
    self.setHeading(direction)
    if self.getHeading() == "up":
      next = [pos[0], pos[1], pos[2] - 1]
    if self.getHeading() == "down":
      next = [pos[0], pos[1], pos[2] + 1]
    if self.getHeading() == "left":
      next = [pos[0] - 1, pos[1], pos[2]]
    if self.getHeading() == "right":
      next = [pos[0] + 1, pos[1], pos[2]]
    if self.getHeading() == "topleft":
      next = [pos[0] - 1, pos[1], pos[2] - 1]
    if self.getHeading() == "bottomright": 
      next = [pos[0] + 1, pos[1], pos[2] + 1]
    if self.getHeading() == "bottomleft":
      next = [pos[0] - 1, pos[1], pos[2] + 1]
    if self.getHeading() == "topright":
      next = [pos[0] + 1, pos[1], pos[2] - 1]
    self.__visited.append(pos)
    self.setPosition(next)

  def changeRoom(self, room, pos):
    """ Changes the player's room.
    room: new room.
    pos: starting position on the new room.
    """
    oldRoom = self.getRoom()
    if oldRoom:
      oldRoom.removeItem(self)
    room.addItem(self, pos)
    self.triggerEvent('roomChanged', oldRoom=oldRoom)
    
  def newChatMessage(self, message):
    """ Triggers a new event after receiving a new chat message.
    message: new chat message.
    """
    self.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(message, self.username))

  def setSelectedItem(self, item):
    self.__selected = item
    self.triggerEvent('selectedItem', item=item)
    
  def setUnselectedItem(self):
    self.__selected = None
    self.triggerEvent('unselectedItem')
    
  def talkTo(self, item):
    item.talkedBy(self)
    
