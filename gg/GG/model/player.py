import GG.model.room_item
#import GG.model.temp_pickable_item
import GG.model.chat_message
import GG.isoview.isoview_player
import GG.utils
import time
import dMVC.model

class GGPlayer(GG.model.room_item.GGRoomItem):
  """ Player class.
  Defines a player object behaviour.
  """
 
  def __init__(self, spritePath, position, anchor, username, password):
    """ Class builder.
    spriteList: sprite list used to paint the player.
    position: player position.
    anchor: image anchor on screen.
    username: user name.
    password: user password.
    """
    #print username, password
    filename = GG.utils.getSpriteName(GG.utils.STATE[1], GG.utils.HEADING[2], 0)
    GG.model.room_item.GGRoomItem.__init__(self, filename, position, anchor)
    self.username = username
    self.imagePath = spritePath
    self.__password = password # Not used outside this class
    self.__visited = [] # Not used outside this class
    self.__heading = GG.utils.HEADING[2]
    self.__state = GG.utils.STATE[1]
    self.__destination = position
    self.__inventory = []
    self.__visited = []
    self.__selected = None
    self.__pointGivers = []
    self.__points = 0
    self.__playedTime = 0
    self.__startPlayedTime = 0
    self.startSessionTiming()    
    self.__avatarConfiguration = self.__dictAvatarConfiguration()

  def startSessionTiming(self):
    #print "**********************************"  
    tmp = time.localtime(time.time())
    self.__startPlayedTime = tmp
    
  def updateSessionTiming(self):
    tmp = time.localtime(time.time())
    #print self.__startPlayedTime
    v1 = (self.__startPlayedTime[4]*60 + self.__startPlayedTime[5])
    v2 = (tmp[4]*60 + tmp[5])
    playedTime = v2 - v1
    self.__startPlayedTime = tmp  
    self.__playedTime += playedTime
    self.triggerEvent('exp', exp=self.__playedTime)
  
  def __dictAvatarConfiguration(self):
    dict = {}
    dict["gender"] = "boy"
    dict["headSize"] = "S"
    dict["mask"] = None
    dict["hairStyle"] = "1"
    dict["hairColor"] = "1"
    dict["skin"] = "1"
    dict["bodySize"] = "S"
    dict["typeShirt"] = "short"
    dict["shirt"] = "3"
    dict["typeTrousers"] = "short"
    dict["trousers"] = "5"
    dict["typeSkirt"] = "short"
    dict["skirt"] = "3"
    dict["shoes"] = "9"
    return dict

  def getAvatarConfiguration(self):
    return self.__avatarConfiguration

  def setAvatarConfiguration(self, avatarConfiguration):
    self.__avatarConfiguration = avatarConfiguration
    self.triggerEvent('avatarConfiguration', avatarConfiguration=avatarConfiguration)
        
  def getPoints(self):
    return self.__points

  def addPoints(self, points, giverLabel):
    if (giverLabel in self.__pointGivers) or (points == 0):
      return
    self.__points += points
    self.__pointGivers.append(giverLabel)
    self.triggerEvent('points', points=self.__points)
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['username']
  
    # self.__heading

  def getHeading(self):
    """ Returns the direction the player is heading to.
    """
    return self.__heading
  
  def setHeading(self, heading):
    """ Sets a new heading direction for the item.
    """
    if self.__heading != heading:
      self.__heading = heading
      self.triggerEvent('heading', heading=heading)

  # self.__state
  
  def getState(self):
    """ Returns the player's state.
    """
    return self.__state
  
  def setState(self, state):
    """ Sets a new state for the item.
    state: new state
    """
    if not self.__state == state:
      self.__state = state
      self.triggerEvent('state', state=state)
      
  def setCarrying(self):
    #print "--> print setCarrying"
    if self.__state == GG.utils.STATE[1]:
      self.__state == GG.utils.STATE[3]   
      self.triggerEvent('state', state=self.__state)
    if self.__state == GG.utils.STATE[2]:
      self.__state == GG.utils.STATE[4]   
      self.triggerEvent('state', state=self.__state)

  def setNotCarrying(self):
    #print "--> print setNotCarrying"
    if self.__state == GG.utils.STATE[3]:
      self.__state == GG.utils.STATE[1]   
      self.triggerEvent('state', state=self.__state)
    if self.__state == GG.utils.STATE[4]:
      self.__state == GG.utils.STATE[2]   
      self.triggerEvent('state', state=self.__state)

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
  
  def setInventory(self, inventory):
    """ Sets a new player's inventory.
    inventory: new player's inventory.
    """
    if not self.__inventory == inventory:
      self.__inventory = inventory
      self.triggerEvent('inventory', inventory=inventory)
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
  
  
  def addToInventoryFromRoom(self, item):
    self.addPoints(item.points, item.label)
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
  
  def addToRoomFromInventory(self, item):
    """ Removes an item from the inventory and drops it in front of the player.
    item: item to drop.
    """
    #self.lala()
    dropLocation = GG.utils.getFrontPosition(self.getPosition(), self.__heading)
    itemOnPosition = self.getRoom().getItemOnPosition(dropLocation)
    if dropLocation == [-1, -1, -1]: 
      return False
    if itemOnPosition != None:
      if not itemOnPosition.isStackable():
        return False
    self.__inventory.remove(item)
    item.setPlayer(None)
    self.getRoom().addItemFromInventory(item, dropLocation)
    self.triggerEvent('chat', actor=item, receiver=self, msg=item.label+" depositado en el suelo")
    
  def checkItemOnInventory(self, item):
    for it in self.__inventory:
      if it.checkSimilarity(item):
        return True
    return False      

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
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    #if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
    #  clicker.setSelectedItem(self)
    self.newChatMessage(clicker.username + ' ha pinchado en mi', 0)

  def getOptions(self):
    """ Returns the available item options.
    """
    return ["talk","exchange"]
      
  def tick(self, now):
    """ Calls for an update on player's position an movement direction.
    """
    for item in self.__inventory:
      item.tick(now)
    if self.getPosition() == self.__destination:
      self.setState(GG.utils.STATE[1])
      return
    direction = self.getRoom().getNextDirection(self, self.getPosition(), self.getDestination())
    if direction == GG.utils.HEADING[0]:
      self.setDestination(self.getPosition())
      return
    pos = self.getPosition()
    self.setState(GG.utils.STATE[2])
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
    room.addItemFromVoid(self, pos)
    self.updateSessionTiming()
    self.triggerEvent('roomChanged', oldRoom=oldRoom)
    
  def newChatMessage(self, message, type):
    """ Triggers a new event after receiving a new chat message.
    message: new chat message.
    """
    self.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(message, self.username, \
                    GG.utils.TEXT_COLOR["black"], self.getPosition(), type))

  def setSelectedItem(self, item):
    """ Sets an item as selected.
    """
    if self.__selected != item:
      self.__selected = item
      self.triggerEvent('selectedItem', item=item)
    
  def setUnselectedItem(self):
    """ Sets an item as unselected.
    """
    if self.__selected:
      self.__selected = None
      self.triggerEvent('unselectedItem')
    
  def talkTo(self, item):
    """ Talks to an item.
    item: item to talk to.
    """
    item.talkedBy(self)
    
  def open(self, item):
    """ Opens an item.
    open: item to open.
    """
    item.openedBy(self)
    
  def setStartPosition(self, pos):
    self.__destination = pos
    GG.model.room_item.GGRoomItem.setStartPosition(self, pos)
    
  def hasItemLabeledInInventory(self, label):
    for item in self.__inventory:
      if item.label == label:
        return True  
    return False    
      
  def jump(self):
    self.triggerEvent('jump', position=self.getPosition())
 
