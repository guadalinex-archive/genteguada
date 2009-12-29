# -*- coding: utf-8 -*-

import item_with_inventory
import room_item
import chat_message
import private_contact
import GG.utils
import time
import dMVC.model
import shutil
import os

# ======================= CONSTANTS ===========================
MAX_DEPTH = 1
# =============================================================

class GGPlayer(item_with_inventory.GGItemWithInventory):
  """ Player class.
  Defines a player object behaviour.
  """
 
  def __init__(self, username, timestamp):
    """ Class builder.
    spriteList: sprite list used to paint the player.
    username: user name.
    password: user password.
    timestamp: last update on avatar configuration.
    admin: sets the player as game administrator.
    """
    filename = GG.utils.getSpriteName(GG.utils.STATE[1], GG.utils.HEADING[2], 0, timestamp)
    item_with_inventory.GGItemWithInventory.__init__(self, filename)
    self.username = username
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
    self.__exp = 0    
    self.__expRooms = []
    self.__avatarConfiguration = self.__dictAvatarConfiguration()
    self.__exchangeTo = None
    self.__agenda = []
    self.__timestamp = timestamp
    if not self.__timestamp == "":
      self.setImagePath(os.path.join(GG.utils.INTERFACE_AVATARS, self.username))
    else:
      self.setImagePath(os.path.join(GG.utils.INTERFACE_AVATARS, "ghost"))
    self.admin = False 
    self.__accessMode = False
    self.startSessionTiming()
    self.numEntradasForo = 0
    self.save("player")

  def objectToPersist(self):
    dict = item_with_inventory.GGItemWithInventory.objectToPersist(self)
    dict["username"] = self.username
    dict["pointsGivers"] = self.__pointGivers
    dict["points"] = self.__points
    dict["playedTime"] = self.__playedTime
    dict["exp"] = self.__exp
    dict["expRooms"] = self.__expRooms
    dict["avatarConfiguration"] = self.__avatarConfiguration
    contactList = []
    for contact in self.__agenda:
      contactList.append(contact.getPlayer())
    dict["agenda"] = contactList
    dict["timestamp"] = self.__timestamp
    return dict

  def load(self, dict):
    item_with_inventory.GGItemWithInventory.load(self, dict)
    self.username = dict["username"]
    self.__visited = []
    self.__heading = GG.utils.HEADING[2]
    self.__state = GG.utils.STATE[1]
    self.__destination = None
    self.__visited = []
    self.__selected = None
    self.__pointGivers = dict["pointsGivers"] 
    self.__points = dict["points"] 
    self.__playedTime = dict["playedTime"] 
    self.__startPlayedTime = 0
    self.__exp = dict["exp"]
    self.__expRooms = dict["expRooms"] 
    self.__avatarConfiguration = dict["avatarConfiguration"] 
    self.__exchangeTo = None
    self.__agenda = []
    for contact in dict["agenda"]:
      self.__agenda.append(private_contact.PrivateContact(contact))
    self.__timestamp = dict["timestamp"]
    self.admin = False 
    self.__accessMode = False
    self.startSessionTiming()

  def getPlayerBuildPackage(self):
    """ Returns item info used to create the isometric view object.
    """      
    infoPackage = {}
    infoPackage["timestamp"] = self.getTimestamp()
    infoPackage["heading"] = self.getHeading()
    infoPackage["state"] = self.getState()
    infoPackage["imagepath"] = self.getImagePath()
    return infoPackage

  def getExpInforPackage(self):
    """ Returns player's achievement info.
    """      
    infoPackage = {}
    infoPackage["points"] = self.__points
    infoPackage["playedTime"] = self.__playedTime
    infoPackage["exp"] = self.__exp
    infoPackage["imageLabel"] = self.getImageLabel()
    return infoPackage

  def getAccessMode(self):
    """ Returns the access mode.
    """  
    return self.__accessMode  

  def setAccessMode(self, mode):
    """ Sets a new access mode.
    mode: access mode.
    """  
    self.__accessMode = mode

  def getTimestamp(self):
    """ Returns the player's timestamp.
    """  
    return self.__timestamp

  def setTimestamp(self, timestamp):
    """ Sets a new timestamp.
    timestamp: new timestamp.
    """  
    if self.__timestamp == "":
      self.spriteName = self.spriteName+"_"+str(timestamp)
    else:
      dataSpriteName = self.spriteName.split("_")
      dataSprite = dataSpriteName[:-1]
      spriteNameTemp = ""
      for data in dataSprite:
        spriteNameTemp += data+"_"
      spriteNameTemp += str(timestamp)
      self.spriteName = spriteNameTemp
    timestamp = str(timestamp)
    self.__timestamp = timestamp
    self.setImagePath(os.path.join(GG.utils.INTERFACE_AVATARS, self.username))
    self.triggerEvent('timestamp', timestamp=timestamp, imgPath = os.path.join(GG.utils.INTERFACE_AVATARS, self.username))
    self.save("player")
      
  def getName(self):
    """ Returns the player's username.
    """  
    return self.username
  
  def getImageLabel(self):
    """ Returns the player's mask filename.
    """  
    if os.path.isfile(os.path.join(GG.utils.DATA_PATH, GG.utils.MASKS_DIR, self.username + ".png")):
      return os.path.join(GG.utils.MASKS_DIR, self.username+".png")
    else:
      return os.path.join(GG.utils.EDITOR, "masko.png")

  def startSessionTiming(self):
    """ Saves the current time.
    """  
    tmp = time.localtime(time.time())
    self.__startPlayedTime = tmp

  def updateSessionTiming(self, now):
    """ Updates the session playing time.
    """  
    self.__startPlayedTime = now  
    self.__playedTime += 1
    self.save("player")
    self.triggerEvent('clock', clock=self.__playedTime)
  
  def updateExp(self, room):
    """ Updates the player's experience after entering on a new room.
    room: new room.
    """ 
    if not room.label in self.__expRooms:
      self.__expRooms.append(room.label)  
      self.__exp += 1
      self.triggerEvent('exp', exp=self.__exp)
  
  def __dictAvatarConfiguration(self):
    """ Creates the avatar configuration.
    """  
    avatarDict = {}
    avatarDict["gender"] = "boy"
    avatarDict["headSize"] = "S"
    avatarDict["mask"] = None
    avatarDict["hairStyle"] = "1"
    avatarDict["hairColor"] = "1"
    avatarDict["skin"] = "1"
    avatarDict["bodySize"] = "S"
    avatarDict["typeShirt"] = "short"
    avatarDict["shirt"] = "3"
    avatarDict["typeTrousers"] = "short"
    avatarDict["trousers"] = "5"
    avatarDict["typeSkirt"] = "short"
    avatarDict["skirt"] = "3"
    avatarDict["shoes"] = "9"
    return avatarDict

  def getAvatarConfiguration(self):
    """ Returns the avatar configuration.
    """  
    return self.__avatarConfiguration

  def setAvatarConfiguration(self, avatarConfiguration, timestamp):
    """ Sets a new configuration for the avatar.
    avatarConfiguration: new avatar configuration.
    timestamp: current timestamp.
    """
    self.setImagePath(os.path.join(GG.utils.INTERFACE_AVATARS, self.username))
    self.__avatarConfiguration = avatarConfiguration
    self.triggerEvent('avatarConfiguration', avatarConfiguration=avatarConfiguration, imageLabel = self.getImageLabel())
    self.setTimestamp(timestamp)
    for contact in self.__agenda:
      contact.getPlayerObject().changeMaskContact(self.username, self.getImageLabel())
    self.save("player")
    
  def changeMaskContact(self, name, imageLabel):
    """ Changes a contact's mask.
    name: contact's name.
    imageLabel: contact's mask image name.
    """  
    self.triggerEvent('contactMask', playerName = name, imageLabel = imageLabel)

  def getOptions(self):
    """ Returns player's available options.
    """
    #return ["privateChat", "exchange", "giveCard"]
    return ["exchange", "giveCard"]
        
  def getPoints(self):
    """ Returns player's points.
    """  
    return self.__points

  def getAdminActions(self):
    """ Returns player's available options.
    """
    return None

  def addPointsSinGiver(self, points):
    self.__points += points
    if points != 0:
      self.triggerEvent('points', points=self.__points)
    self.save("player")

  def addPoints(self, points, giverLabel):
    """ Adds points to the player's point pool.
    points: points added.
    giverLabel: points giver.
    """  
    if giverLabel in self.__pointGivers:
      return
    self.__points += points
    self.__pointGivers.append(giverLabel)
    if points != 0:
      self.triggerEvent('points', points=self.__points)
    self.save("player")
    
  def checkPointGiver(self, pointGiver):
    """ Checks if a given item has already given points to the player,
    pointsGiver: item to check.
    """  
    if pointGiver in self.__pointGivers:
      return True
    return False

  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['username', 'admin']
  
  # self.__heading

  def getHeading(self):
    """ Returns the direction the player is heading to.
    """
    return self.__heading
  
  def setHeading(self, heading):
    """ Sets a new heading direction for the item.
    heading: new heading direction.
    """
    if heading != None:
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
      if self.getRoom():
        listItemsTile = self.getRoom().getTile(self.getPosition()).getItems()
        self.__state = state
        self.triggerEvent('state', state=state, position=self.getPosition(), listItemsTiles=listItemsTile)
  
  # self.__destination
  
  def getDestination(self):
    """ Returns the player's movement destination.
    """
    return self.__destination
  
  def setDestination(self, destination):
    """ Sets a new destination for the player movement.
    destination: movement destination.
    """
    if not self.__destination == destination:
      listItemsTile = self.getRoom().getTile(self.getPosition()).getItems()
      self.__visited = []
      self.__destination = destination
      self.triggerEvent('destination', destination=destination, listItemsTiles=listItemsTile)
    
  def setStartDestination(self, destination):
    """ Sets a new destination for the player movement without calling for a 'destination' event.
    destination: movement destination.
    """
    if self.__destination != destination:
      for vis in self.__visited:
        self.__visited.remove(vis)
      self.__visited = []
      self.__destination = destination
      
  @dMVC.model.localMethod
  def defaultView(self, screen, room, parent, position=None, imagePath=None, image=None):
    """ Creates a view object associated with this player.
    screen: screen handler.
    room: room view object.
    parent: hud or session view object.
    position: player position.
    image: image used to paint the player on screen.
    """
    import GG.isoview.isoview_player
    return GG.isoview.isoview_player.IsoViewPlayer(self, screen, room, parent)
  
  def addToInventoryFromRoom(self, item):
    """ Adds a new item from room to the inventory.
    item: new item.
    """ 
    tile = item.getTile()
    itemList = tile.getItemsFrom(item)
    itemList.reverse()
    for itemToInv in itemList:
      self.addPoints(itemToInv.points, itemToInv.label)
      item_with_inventory.GGItemWithInventory.addToInventory(self, itemToInv)
    self.save("player")
    
  def addToRoomFromInventory(self, item):
    """ Removes an item from the inventory and drops it in front of the player.
    item: item to drop.
    """
    dropLocation = GG.utils.getFrontPosition(self.getPosition(), self.__heading, self.getRoom().size)
    if not self.getRoom().getTile(dropLocation).stepOn() or dropLocation == [-1, -1]:
      self.newChatMessage("No puedo soltarlo ahí", 1)
    else:    
      item_with_inventory.GGItemWithInventory.addToRoomFromInventory(self, item, dropLocation)
    self.save("player")
    
  def checkUser(self, username):
    """ Searches for an user by his user name and password.
    username: user name.
    password: user password.
    """
    if self.username == username:
      return True
    return False
  
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
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    
  def tick(self, now):
    """ Calls for an update on player's position an movement direction.
    now: current timestamp.
    """
    if self.getRoom():
      tmp = time.localtime(time.time())
      playedTime = tmp[4] - self.__startPlayedTime[4]
      if playedTime:
        self.updateSessionTiming(tmp)
      if self.getPosition() == self.__destination:
        if self.__selected and not self.__selected.getPlayer():
          self.setHeading(GG.utils.getNextDirection(self.getPosition(), self.__selected.getPosition()))
        if self.__state == GG.utils.STATE[2]:
          self.setState(GG.utils.STATE[1])
          return
        if self.__state == GG.utils.STATE[4]:
          self.setState(GG.utils.STATE[3])
          return
        return
      pos = self.getPosition()
      end = self.getDestination()
      if GG.utils.checkNeighbour(pos, end):
        direction = GG.utils.getNextDirection(pos, end)
        nextPos = end
      else:
        direction, nextPos = self.getRoom().getNextDirection(pos, end, self)
      if direction == GG.utils.HEADING[0]:
        self.newChatMessage("No puedo llegar hasta ese lugar.", 2)
        self.setDestination(self.getPosition())
        return
      if self.__state == GG.utils.STATE[1]:
        self.setState(GG.utils.STATE[2])
      elif self.__state == GG.utils.STATE[3]:
        self.setState(GG.utils.STATE[4])
      self.setHeading(direction)
      self.__visited.append(nextPos)
      items = self.getTile().getItemsFrom(self)
      for item in items:
        item.setPosition(nextPos)

  def changeRoom(self, room, pos):
    """ Changes the player's room.
    room: new room.
    pos: starting position on the new room.
    """
    if room:
      self.updateExp(room)
    room_item.GGRoomItem.changeRoom(self, room, pos)
    self.save("player")
    
  def newChatMessageEntered(self, message):
    """ Receives a new chat message and sends it to the room.
    message: new chat message.
    """  
    self.getRoom().newChatMessage(message, self, 0)  
  
  def newChatMessage(self, message, msgType):
    """ Triggers a new event after receiving a new chat message.
    message: new chat message.
    """
    header = time.strftime("%H:%M", time.localtime(time.time())) + " [" + self.username + "]: "
    self.triggerEvent('chatAdded', message=chat_message.ChatMessage(message, self.username, \
                    GG.utils.TEXT_COLOR["black"], self.getPosition(), msgType), text=message, header=header)

  def getSelected(self):
    """ Returns player's selected item.
    """  
    return self.__selected  
  
  def setSelectedItem(self, item, inventory = None):
    """ Sets an item as selected.
    item: selected item.
    """
    if inventory:
      self.setUnselectedItem()
    if self.__selected != item:
      self.__selected = item
      self.triggerEvent('selectedItem', item=item, position=self.getPosition(), name=item.getName(), 
                        imageLabel=item.getImageLabel(), inventoryOnly=item.inventoryOnly(), 
                        options=item.getOptions(), adminActions=item.getAdminActions(), isTile=item.isTile(), 
                        highlight=True)
  
  def setSelectedItemWithoutHighlight(self, item):
    """ Sets an item as selected, but it doesn't highlights it.
    item: selected item.
    """
    if self.__selected != item:
      self.__selected = item
      self.triggerEvent('selectedItem', item=item, position=self.getPosition(), name=item.getName(), 
                        imageLabel=item.getImageLabel(), inventoryOnly=item.inventoryOnly(), 
                        options=item.getOptions(), adminActions=item.getAdminActions(), isTile=item.isTile(), 
                        highlight=1)
    
  def setUnselectedItem(self):
    """ Sets an item as unselected.
    """
    if self.__selected:
      self.__selected = None
      self.triggerEvent('unselectedItem')
    
  def setStartPosition(self, pos):
    """ Sets a new position for the player.
    pos: new position.
    """  
    self.__destination = pos
    room_item.GGRoomItem.setStartPosition(self, pos)
    
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
      self.newChatMessage("Ya tengo algo cogido. !No puedo aguantar más peso!", 1)
      self.setUnselectedItem()
      return
    self.setState(GG.utils.STATE[3])
    item.setPosition(self.getPosition())
    self.triggerEvent('liftItem', item=item, position=item.getPosition(), itemList = item.getItemsOnMyTile())
    self.setUnselectedItem()
    
  def drop(self, item):
    """ Drops an item.
    item: item to drop.
    """
    if not (self.__state == GG.utils.STATE[3] or self.__state == GG.utils.STATE[4]):
      return
    dropLocation = GG.utils.getFrontPosition(self.getPosition(), self.__heading, self.getRoom().size)
    tile = self.getRoom().getTile(dropLocation)
    if tile.getDepth():
      if not tile.getTopItem().stepOn():  
        self.newChatMessage("No puedo soltarlo encima de eso, podría aplastarlo.", 1)
        self.setUnselectedItem()
      else:
        self.setState(GG.utils.STATE[1])
        item.setPosition(dropLocation)
        self.triggerEvent('dropItem', item=item, position=item.getPosition())
        self.setUnselectedItem()
    else:
      if dropLocation == [-1, -1]:
        self.newChatMessage("No puedo soltarlo ahi.", 1)
        self.setUnselectedItem()
        return
      self.setState(GG.utils.STATE[1])
      item.setPosition(dropLocation)
      self.triggerEvent('dropItem', item=item, position=item.getPosition(), itemList = item.getItemsOnMyTile())
      self.setUnselectedItem()
  
  def climb(self, itemToClimb):
    """ Climbs over an item.
    itemToClimb: item to climb.
    """  
    tile = itemToClimb.getTile()  
    if tile.getDepth() <= MAX_DEPTH and tile.stepOn():
      self.setDestination(itemToClimb.getPosition())
      self.setUnselectedItem()
    else:
      self.newChatMessage("No puedo subirme ahí", 1)

  def jump(self):
    """ Jumps on the current position.
    """  
    if not self.isTopItem():
      self.newChatMessage("No puedo saltar con tanto peso", 1)
      return
    self.triggerEvent('jump', position=self.getPosition())
    
  def jumpOver(self):  
    """ Jumps over an item.
    """  
    if not self.isTopItem():
      self.newChatMessage("No puedo saltar con tanto peso", 1)
      return
    heading = GG.utils.getNextDirection(self.getPosition(), self.__selected.getPosition())
    if heading:
      dest = GG.utils.getJumpDestination(self.getPosition(), heading, self.getRoom().size)
      if dest == None or self.getRoom().getTile(dest).getDepth():
        self.newChatMessage("No puedo saltar allí", 1)
        return
      self.setUnselectedItem()
      self.setHeading(heading)
      self.setDestination(dest)
      self.setPosition(dest, 1)
    
  def turnRight(self):
    """ Turns the player to the right.
    """  
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
    """ Turns the player to the left.
    """  
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
    """ Returns the current exchange partner.
    """  
    return self.__exchangeTo

  def initExchangeTo(self, player, itemList = []):
    """ Starts the exchange process with another player.
    player: player to exchange items with.
    itemList: items to exchange.
    """  
    self.setUnselectedItem()
    if not self.__exchangeTo:
      self.__exchangeTo = player
      self.triggerEvent('initExchange', itemList = itemList)

  def cancelExchangeTo(self, step):
    """ Cancels the exchange process.
    step: current exchange process step.
    """  
    if not step == 1:
      self.__exchangeTo.cancelExchangeTo(1)
    self.__exchangeTo = None
    self.triggerEvent('cancelExchange')

  def acceptExchangeTo(self, step, itemList):
    """ Agrees to exchange items with another player.
    step: current exchange process step.
    itemList: items to exchange.
    """  
    if step == 1:
      self.__exchangeTo.initExchangeTo(self, itemList)
    elif step == 2:
      self.__exchangeTo.triggerEvent("listExchange", list = itemList)

  def finishExchange(self, listIn, listOut):
    """ Finishes the exchange process.
    listIn: items received.
    listOut: items given.
    """
    for item in listOut:
      self.removeFromInventory(item)
      self.__exchangeTo.addToInventory(item, self.getPosition())
    for item in listIn:
      self.addToInventory(item, self.__exchangeTo.getPosition())
      self.__exchangeTo.removeFromInventory(item)
    self.__exchangeTo.cancelExchangeTo(1)
    self.cancelExchangeTo(1)
    
  # contacts, private chat & agenda  
  
  def getContact(self, name):
    """ Returns a contact from the player's agenda.
    name: contact's name.
    """  
    for contact in self.__agenda:
      if contact.getPlayer() == name:
        return contact 
    return None
    
  def getAgenda(self):
    """ Returns the player's agenda.
    """  
    return self.__agenda
    
  def getAgendaData(self):
    """ Returns the agenda data.
    """  
    data = {}
    for contact in self.__agenda:
      data[contact.getPlayer()] = contact.getImageLabel()
    return data  
    
  def removeContact(self, contact):
    """ Removes a contact from the agenda.
    contact: contact to be removed.
    """  
    contactSelected = None
    for item in self.__agenda:
      if item.getPlayer() == contact:
        contactSelected = item
        break
    if contactSelected:
      self.__agenda.remove(contactSelected)
    self.save("player")
        
  def removeContactRemote(self, contact):
    """ Removes a contact from the agenda. This method is called from another player's agenda.
    contact: contact to be removed.
    """  
    self.removeContact(contact)  
    self.triggerEvent("removeContactRemote", contact=contact)
    self.save("player")
    
  def removePlayerContactFromAgenda(self, playerName):
    """ Removes a contact from the agenda.
    playerName: contact name.
    """  
    contactSelected = None
    for item in self.__agenda:
      if item.getPlayer() == playerName:
        contactSelected = item
        break
    if contactSelected:
      self.__agenda.remove(contactSelected)
      self.triggerEvent("removeContactRemote", contact=contactSelected)
    self.save("player")
    
  def checkContact(self, player):
    """ Checks if a contact already exists on the agenda.
    player: new contact.
    """  
    if self.checkContactOnAgenda(player):
      player.newChatMessage("Ya tienes a " + self.username + " en tu agenda.", 1)
    else:
      player.newChatMessage("Preguntando a " + self.username + " ...", 1)  
      self.triggerEvent("contactDialog", contact=player)
    
  def addContact(self, player):
    """ Adds a new contact to the agenda.
    player: new contact.
    """  
    if self.checkContactOnAgenda(player):
      player.newChatMessage("Ya tienes a " + self.username + " en tu agenda.", 1)
      return
    self.__agenda.append(private_contact.PrivateContact(player.username))
    self.triggerEvent("contactAdded", contact=player)
    self.save("player")
    
  def checkContactOnAgenda(self, contact):
    """ Checks if a contact already exists on the agenda.
    contact: new contact.
    """  
    for cont in self.__agenda:
      if cont.getPlayer() == contact.username:
        return True
    return False  

  def newChatForPlayer(self, string, player):
    """ Adds a new message from a contact.
    string: new message.
    player: message emitter.
    """
    for item in self.__agenda:
      if item.getPlayer() == player.username:
        item.addChatLine(player, string)        

  def newPrivateChatReceived(self, line, player):
    """ Triggers an event after receiving a new chat message.
    line: new chat line.
    player: message emitter.
    """  
    self.triggerEvent("privateChatReceived", chat=line, player=player)
    
  def kick(self):
    """ Kicks this player from the game.
    """  
    self.triggerEvent("finish")
    
  def setPosition(self, pos, jump=None):
    """ Sets a new position and modifies player's state whenever necessary.
    pos: new position.
    jump: sets the movement as a jump or not.
    """  
    if self.isTopItem():
      if self.getState() == GG.utils.STATE[3]:
        self.setState(GG.utils.STATE[1])
      if self.getState() == GG.utils.STATE[4]:
        self.setState(GG.utils.STATE[2])
    else:
      if self.getState() == GG.utils.STATE[1]:
        self.setState(GG.utils.STATE[3])
      if self.getState() == GG.utils.STATE[2]:
        self.setState(GG.utils.STATE[4])  
    item_with_inventory.GGItemWithInventory.setPosition(self, pos, jump)
    
  def tryToInventory(self, item):
    """ Attempts to add a new item to the player's inventory.
    item: new item.
    """  
    if item.isTopItem():  
      if item.capture():
        self.addToInventory(item)
        self.setUnselectedItem()
        item.setEnabled()
      else:
        self.newChatMessage("alguien se nos ha adelantado", 1)
    else:      
      self.newChatMessage('No puedo coger eso, hay algo encima', 1)  
  
  def tryToInventoryCopy(self, item):
    itemCopy, pos = item.getCopyFor(self) 
    if itemCopy:
      self.addToInventory(itemCopy, pos)
      self.setUnselectedItem()
    
  def tryToPocket(self, item):
    """ Attempts to pick a new paper money item.
    item: new paper money item.
    """  
    if item.isTopItem():
      if item.capture():
        self.setUnselectedItem()
        self.__points += item.points
        self.triggerEvent('points', points=self.__points)
        self.save("player")
        item.setEnabled()
        return True  
      else:
        self.newChatMessage("alguien se nos ha adelantado", 1)
    return False
  
  def removeAllData(self):
    """ Removes all data for this player.
    """  
    imagesPath = os.path.join(os.path.join(GG.utils.DATA_PATH, GG.utils.INTERFACE_AVATARS), self.username)
    interfacePath = os.path.join(GG.utils.DATA_PATH, GG.utils.INTERFACE_AVATARS)
    maskPath = os.path.join(interfacePath, GG.utils.MASKS_PATH)
    maskImage = os.path.join(maskPath, (self.username + ".png"))
    if os.path.isdir(imagesPath):
      shutil.rmtree(imagesPath)
    if os.path.isfile(maskImage):
      os.remove(maskImage)  

  def tryOutToInventory(self, item):
    if item.inventoryOnly():
      self.newChatMessage("Mejor no. Creo que puede ser util más adelante.", 2) 
    else:   
      self.addToRoomFromInventory(item)
      self.setUnselectedItem()

  def deleteGift(self, idGift):
    dictItems = self.getInventory()
    for key in dictItems.keys():
      item = dictItems[key]["object"]
      if isinstance(item, GG.model.generated_inventory_item.GGGeneratedGift):
        if item.getIdGift() == idGift:
          self.removeFromInventory(item)
          return True
    return False

  def setNumEntradasForo(self, numEntradasForo):
    self.numEntradasForo = numEntradasForo
  
  def checkEntradasForo(self, numEntradasForo):
    if self.numEntradasForo < numEntradasForo:
      return False
    else:
      return True
