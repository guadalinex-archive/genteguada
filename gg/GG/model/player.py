# -*- coding: iso-8859-15 -*-

import GG.model.item_with_inventory
import GG.model.chat_message
import GG.model.private_contact
import GG.utils
import time
import dMVC.model
import os

class GGPlayer(GG.model.item_with_inventory.GGItemWithInventory):
  """ Player class.
  Defines a player object behaviour.
  """
 
  def __init__(self, spritePath, anchor, topAnchor, username, password, timestamp, admin):
    """ Class builder.
    spriteList: sprite list used to paint the player.
    position: player position.
    anchor: image anchor on screen.
    username: user name.
    password: user password.
    """
    #print username, password
    filename = GG.utils.getSpriteName(GG.utils.STATE[1], GG.utils.HEADING[2], 0, timestamp)
    GG.model.item_with_inventory.GGItemWithInventory.__init__(self, filename, anchor, topAnchor)
    self.username = username
    self.__password = password # Not used outside this class
    self.__visited = [] # Not used outside this class
    self.__heading = GG.utils.HEADING[2]
    self.__state = GG.utils.STATE[1]
    self.__destination = None
    self.__visited = []
    self.__selected = None
    self.__pointGivers = []
    self.__points = 0
    self.__playedTime = 0
    self.__startPlayedTime = 0
    self.startSessionTiming()
    self.__exp = 0    
    self.__expRooms = []
    self.__avatarConfiguration = self.__dictAvatarConfiguration()
    self.__exchangeTo = None
    self.__agenda = []
    self.__timestamp = timestamp
    if not self.__timestamp == "":
      self.imagePath = "avatars/"+self.username+"/"
    else:
      self.imagePath = spritePath
    self.admin = admin  
    self.__accessMode = admin

  def getAccessMode(self):
    return self.__accessMode  

  def setAccessMode(self, mode):
    self.__accessMode = mode

  def getTimestamp(self):
    return self.__timestamp

  def setTimestamp(self, timestamp):
    timestamp = str(timestamp)
    self.__timestamp = timestamp
    self.imgPath = "avatars/"+self.username+"/"
    self.triggerEvent('timestamp', timestamp=timestamp, imgPath = self.imgPath)
      
  def getName(self):
    return self.username
  
  def getImageLabel(self):
    if os.path.isfile(os.path.join(GG.utils.DATA_PATH,"avatars/masks",self.username+".png")):
      return "avatars/masks/"+self.username+".png"
    else:
      return "interface/editor/masko.png"

  def startSessionTiming(self):
    tmp = time.localtime(time.time())
    self.__startPlayedTime = tmp
    
  def updateSessionTiming(self):
    tmp = time.localtime(time.time())
    v1 = (self.__startPlayedTime[4]*60 + self.__startPlayedTime[5])
    v2 = (tmp[4]*60 + tmp[5])
    playedTime = v2 - v1
    self.__startPlayedTime = tmp  
    self.__playedTime += playedTime
    self.triggerEvent('clock', clock=self.__playedTime)
  
  def updateExp(self, room):
    if not room.label in self.__expRooms:
      self.__expRooms.append(room.label)  
      self.__exp += 1
      self.triggerEvent('exp', exp=self.__exp)
  
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

  def setAvatarConfiguration(self, avatarConfiguration, timestamp=None):
    self.__avatarConfiguration = avatarConfiguration
    #self.setTimestamp(timestamp)
    self.triggerEvent('avatarConfiguration', avatarConfiguration=avatarConfiguration, imageLabel = self.getImageLabel())
    for contact in self.__agenda:
      contact.getPlayer().changeMaskContact(self.username, self.getImageLabel())
    
  def changeMaskContact(self, name, imageLabel):
    self.triggerEvent('contactMask', playerName = name, imageLabel = imageLabel)

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["privateChat", "exchange", "giveCard"]
        
  def getPoints(self):
    return self.__points

  def addPoints(self, points, giverLabel):
    if giverLabel in self.__pointGivers:
      return
    self.__points += points
    self.__pointGivers.append(giverLabel)
    if points != 0:
      self.triggerEvent('points', points=self.__points)
    
  def checkPointGiver(self, pointGiver):
    if pointGiver in self.__pointGivers:
      return True
    return False

  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['username', 'admin']
  
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
      self.triggerEvent('heading', heading=heading, state=self.__state)

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
      self.triggerEvent('state', state=state, position=self.getPosition())
      
  def setCarrying(self):
    if self.__state == GG.utils.STATE[1]:
      self.__state = GG.utils.STATE[3]   
      self.triggerEvent('state', state=self.__state)
    if self.__state == GG.utils.STATE[2]:
      self.__state = GG.utils.STATE[4]   
      self.triggerEvent('state', state=self.__state)

  def setNotCarrying(self):
    if self.__state == GG.utils.STATE[3]:
      self.__state = GG.utils.STATE[1]   
      self.triggerEvent('state', state=self.__state)
    if self.__state == GG.utils.STATE[4]:
      self.__state = GG.utils.STATE[2]   
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
      
  @dMVC.model.localMethod
  def defaultView(self, screen, room, parent):
    """ Creates a view object associated with this player.
    screen: screen handler.
    room: room view object.
    parent: hud or session view object.
    """
    import GG.isoview.isoview_player
    return GG.isoview.isoview_player.IsoViewPlayer(self, screen, room, parent)
  
  def addToInventoryFromRoom(self, item):
    tile = item.getTile()
    itemList = tile.getItemsFrom(item)
    itemList.reverse()
    for it in itemList:
      self.addPoints(it.points, it.label)
      GG.model.item_with_inventory.GGItemWithInventory.addToInventoryFromRoom(self, it)
    
  def addToRoomFromInventory(self, item):
    """ Removes an item from the inventory and drops it in front of the player.
    item: item to drop.
    """
    dropLocation = GG.utils.getFrontPosition(self.getPosition(), self.__heading)
    if not self.getRoom().getTile(dropLocation).stepOn() or dropLocation == [-1, -1, -1]:
      self.newChatMessage("No puedo soltarlo ahí", 1)
    else:    
      GG.model.item_with_inventory.GGItemWithInventory.addToRoomFromInventory(self, item, dropLocation)
    
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
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    #self.newChatMessage(clicker.username + ' ha pinchado en mi', 0)

  def tick(self, now):
    """ Calls for an update on player's position an movement direction.
    """
    if self.getRoom() == None:
      return
    GG.model.item_with_inventory.GGItemWithInventory.tick(self, now) 
    if self.getPosition() == self.__destination:
      if self.__state == GG.utils.STATE[2]:
        self.setState(GG.utils.STATE[1])
        return
      if self.__state == GG.utils.STATE[4]:
        self.setState(GG.utils.STATE[3])
        return
      return
  
    ori = self.getPosition()
    end = self.getDestination()
    if GG.utils.checkNeighbour(ori, end):
      direction = GG.utils.getNextDirection(ori, end)
    else:
      direction = self.getRoom().getNextDirection(self, ori, end)
      if direction == GG.utils.HEADING[0]:
        #print self.getPosition(), self.__destination  
        self.newChatMessage("No puedo llegar hasta ese lugar.", 2)
        self.setDestination(self.getPosition())
        return
    
    if direction == GG.utils.HEADING[0]:
      self.setDestination(self.getPosition())
      return
    pos = self.getPosition()
    if self.__state == GG.utils.STATE[1]:
      self.setState(GG.utils.STATE[2])
    elif self.__state == GG.utils.STATE[3]:
        self.setState(GG.utils.STATE[4])
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
    
    items = self.getTile().getItemsFrom(self)
    for item in items:
      item.setPosition(next)

  def changeRoom(self, room, pos):
    """ Changes the player's room.
    room: new room.
    pos: starting position on the new room.
    """
    if room:
      self.updateExp(room)
      self.updateSessionTiming()
    GG.model.room_item.GGRoomItem.changeRoom(self, room, pos)
    
  def newChatMessage(self, message, type):
    """ Triggers a new event after receiving a new chat message.
    message: new chat message.
    """
    self.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(message, self.username, \
                    GG.utils.TEXT_COLOR["black"], self.getPosition(), type))

  def getSelected(self):
    return self.__selected  
  
  def setSelectedItem(self, item):
    """ Sets an item as selected.
    """
    if self.__selected != item:
      self.__selected = item
      self.triggerEvent('selectedItem', item=item, position=self.getPosition(), highlight=1)
  
  def setSelectedItemWithoutHighlight(self, item):
    """ Sets an item as selected, but it doesn't hightlights it.
    """
    if self.__selected != item:
      self.__selected = item
      self.triggerEvent('selectedItem', item=item, position=self.getPosition(), highlight=0)
    
  def setUnselectedItem(self):
    """ Sets an item as unselected.
    """
    if self.__selected:
      self.__selected = None
      self.triggerEvent('unselectedItem')
    
  def setStartPosition(self, pos):
    self.__destination = pos
    GG.model.room_item.GGRoomItem.setStartPosition(self, pos)
    
  def talkTo(self, item):
    """ Talks to an item.
    item: item to talk to.
    """
    item.talkedBy(self)
    
  def talkAndGetFrom(self, item):
    """ Talks to an item.
    item: item to talk to.
    """
    return item.talkAndGet(self)
  
  def open(self, item):
    """ Opens an item.
    item: item to open.
    """
    item.openedBy(self)
    
  def lift(self, item):
    """ Lifts an item.
    item: item to lift.
    """
    if self.__state == GG.utils.STATE[3] or self.__state == GG.utils.STATE[4]:
      self.newChatMessage("Ya tengo algo cogido. ¡No puedo aguantar más peso!", 1)  
      return
    #self.addPoints(99, "Heavy Box") 
    self.setState(GG.utils.STATE[3])
    item.setPosition(self.getPosition())
    self.triggerEvent('liftItem', item=item, position=item.getPosition())
    
  def drop(self, item):
    """ Drops an item.
    item: item to drop.
    """
    if not (self.__state == GG.utils.STATE[3] or self.__state == GG.utils.STATE[4]):
      return
    dropLocation = GG.utils.getFrontPosition(self.getPosition(), self.__heading)
    if self.getRoom().getTile(dropLocation).getDepth():
      self.newChatMessage("No puedo soltarlo encima de eso, podría aplastarlo.", 1)
    else:
      if dropLocation == [-1, -1, -1]:
        self.newChatMessage("No puedo soltarlo ahí.", 1)
        return
      self.setState(GG.utils.STATE[1])
      item.setPosition(dropLocation)
      self.triggerEvent('dropItem', item=item, position=item.getPosition())
  
  def climb(self, itemToClimb):
    tile = itemToClimb.getTile()  
    if tile.getDepth() <= GG.utils.MAX_DEPTH and tile.stepOn():
      self.setDestination(itemToClimb.getPosition())
    else:
      self.newChatMessage("No puedo subirme ahí", 1)

  def jump(self):
    if self.__state == GG.utils.STATE[3] or self.__state == GG.utils.STATE[4]:
      self.newChatMessage("No puedo saltar con tanto peso", 1)
      return
    if not self.__selected:
      self.triggerEvent('jump', position=self.getPosition())
      return
    heading = GG.utils.getNextDirection(self.getPosition(), self.__selected.getPosition())
    dest = GG.utils.getJumpDestination(self.getPosition(), heading, self.getRoom().size)
    if dest == None or self.getRoom().getTile(dest).getDepth():
      self.newChatMessage("No puedo saltar allí", 1)
      return
    self.setHeading(heading)
    self.setDestination(dest)
    self.setPosition(dest, 1)

  def turnRight(self):
    heading = {1: "topleft", 2: "up", 3: "topright", 4: "right",
           5: "bottomright", 6: "down", 7: "bottomleft", 8: "left"}
    for i in range(1, 9):
      if heading[i] == self.__heading:
        if i == 8:
          self.setHeading(heading[1])
          return
        else:    
          self.setHeading(heading[i+1])
          return

  def turnLeft(self):
    heading = {1: "topleft", 2: "up", 3: "topright", 4: "right",
           5: "bottomright", 6: "down", 7: "bottomleft", 8: "left"}
    for i in range(1, 9):
      if heading[i] == self.__heading:
        if i == 1:
          self.setHeading(heading[8])
          return
        else:    
          self.setHeading(heading[i-1])
          return

  def isExchange(self):
    return self.__exchangeTo

  def initExchangeTo(self,player, list = []):
    self.setUnselectedItem()
    if not self.__exchangeTo:
      self.__exchangeTo = player
      self.triggerEvent('initExchange', list = list)

  def cancelExchangeTo(self, step):
    if not step == 1:
      self.__exchangeTo.cancelExchangeTo(1)
    
    self.__exchangeTo = None
    self.triggerEvent('cancelExchange')

  def acceptExchangeTo(self, step, list):
    print step
    if step == 1:
      self.__exchangeTo.initExchangeTo(self, list)
    elif step == 2:
      self.__exchangeTo.triggerEvent("listExchange", list = list)

  def finishExchange(self, listIn, listOut):

    for item in listOut:
      self.removeFromInventory(item)
      self.__exchangeTo.addToInventoryFromVoid(item, self.getPosition())
    for item in listIn:
      self.addToInventoryFromVoid(item, self.__exchangeTo.getPosition())
      self.__exchangeTo.removeFromInventory(item)

    self.__exchangeTo.cancelExchangeTo(1)
    self.cancelExchangeTo(1)
    
  # contacts, private chat & agenda  
  
  def getContact(self, name):
    for contact in self.__agenda:
      if contact.getPlayer().username == name:
        return contact
    return None
    
  def addContactTEST(self, player):  
    self.__agenda.append(GG.model.private_contact.PrivateContact(player))
    
  def getAgenda(self):
    return self.__agenda
    
  def getAgendaData(self):
    data = {}
    for contact in self.__agenda:
      data[contact.getPlayer().username] = contact.getPlayer().getImageLabel()
    return data  
    
  def removeContact(self, contact):
      for item in self.__agenda:
        if item.getPlayer().username == contact.username:
          self.__agenda.remove(item)
          return
        
  def removeContactRemote(self, contact):  
    self.removeContact(contact)  
    self.triggerEvent("removeContactRemote", contact=contact)  
    
  def checkContact(self, player):
    if self.checkContactOnAgenda(player):
      player.newChatMessage("Ya tienes a " + self.username + " en tu agenda.", 1)
    else:
      player.newChatMessage("Preguntando a " + self.username + "...", 1)  
      self.triggerEvent("contactDialog", contact=player)
    
  def addContact(self, player):
    if self.checkContactOnAgenda(player):
      player.newChatMessage("Ya tienes a " + self.username + " en tu agenda.", 1)
      return
    self.__agenda.append(GG.model.private_contact.PrivateContact(player))
    self.triggerEvent("contactAdded", contact=player)
    
  def checkContactOnAgenda(self, contact):
    for cont in self.__agenda:
      if cont.getPlayer().username == contact.username:
        return True
    return False  

  def newChatForPlayer(self, string, player):
    for item in self.__agenda:
      print player  
      if item.getPlayer().username == player.username:
        item.addChatLine(player, string)        

  def newPrivateChatReceived(self, line, player):
    self.triggerEvent("privateChatReceived", chat=line, player=player)
    
  
