# -*- coding: utf-8 -*-

import dMVC.model
import GG.utils
import GG.model.room
import GG.model.ggsession
import GG.model.giver_npc
import thread
import time
import os
import stat
import random
import GG.avatargenerator.generator
import Queue
import ggmodel

import urllib2
import urllib

class GGSystem(dMVC.model.Model):
  """ GGSystem class.
  Includes room and player objects, and some procedures to manage data.
  """
    
  def __init__(self):
    """ Initializes the model attributes and both room and player lists.
    """
    dMVC.model.Model.__init__(self)
    self.__rooms = []
    self.__startRooms = []
    self.__players = []
    self.__sessions = [] # Variable privada solo para uso interno.
    self.__avatarGeneratorHandler = GG.avatargenerator.generator.AvatarGenerator()
    self.__avatarGeneratorProcessQueue = Queue.Queue()
    thread.start_new(self.__start, ())
    GGSystem.instance = self
    self.__loadData()
     
  def getEntryRoom(self):
    """ Returns the room used as lobby for all new players.
    """
    roomsCopy = self.__startRooms
    for x in range(0, len(self.__startRooms)):
      room = roomsCopy[random.randint(0, len(roomsCopy)-1)]
      if room.isFull() or not room.getEnabled():
        roomsCopy.remove(room)
      else:
        return room    
    return None
      
  def getEntryRooms(self):
    """ Returns all start rooms.
    """  
    return self.__startRooms      
      
  # self.__players
  
  def getPlayers(self):
    """ Returns the players list.
    """
    return self.__players
  
  def setPlayers(self, players):
    """ Sets a new players list.
    players: new players list.
    """
    if not self.__players == players:
      self.__players = players
      self.triggerEvent('players', players=players)
      return True
    return False
    
  def addPlayer(self, player):
    """ Adds a new player to the players list.
    player: new player.
    """
    if not player in self.__players:
      self.__players.append(player)
      self.triggerEvent('addPlayer', player=player)
      return True
    return False
    
  def removePlayer(self, player):
    """ Remove a player from the players list.
    player: player to be removed.
    """
    if player in self.__players:
      self.__players.remove(player)
      self.triggerEvent('removePlayer', player=player)
      return True
    return False

  def getPlayerObject(self, username):
    for sess in self.__sessions:
      if sess.getPlayer().username == username:
        return sess.getPlayer()
    return None

  def login(self, username, password):
    """ Attempts to login on an user. If succesfull, returns a ggsession model.
    username: user name.
    password: user password.
    """
    for sess in self.__sessions:
      if sess.getPlayer().checkUser(username):
        return False, "El usuario tiene una sesion abierta"    
    accessMode = self.loginGuadalinex(username, password)
    if not accessMode:
      return False, "No se ha podido autenticar en guadalinex"
    user = self.__getPlayer(username, accessMode)
    if not self.__accessUserIntoRoom(user):
      return False, "No existen habitaciones disponibles"  
    session = GG.model.ggsession.GGSession(user, self)
    self.__sessions.append(session)
    return True, session 

  @dMVC.synchronized.synchronized(lockName='accessRoom')
  def __accessUserIntoRoom(self, user):
    newRoom = user.getRoom()
    if not newRoom:
      newRoom = self.getEntryRoom()
      if not newRoom:
        return False
    else:
      #comprobar que hay sitio en la habitacion
      user.clearRoom()
    user.changeRoom(newRoom, newRoom.getNearestEmptyCell([1, 1]))
    return True

  def __getPlayer(self, username, accessMode):
    player = ggmodel.GGModel.read(username, "player")
    if not player:
      player = GG.model.player.GGPlayer(username, "")
    if accessMode == "A":
      player.admin = True
    return player
  
  def loginGuadalinex(self, user, passwd):
    """ Logs in an user.
    user: user name.
    passwd: user password.
    """  
    return "A"
    #return True
    params = urllib.urlencode({"usuario": user, "password": passwd})  
    guadalinexLogin = urllib2.urlopen("http://www.guadalinex.org/usrdata?" +params)  
    result = guadalinexLogin.read()  
    guadalinexLogin.close()  
    data = result.split(";")
    if not len(data) == 4:
      return False
    return data[3]
    
  def logout(self, session):
    """ Logs out a player and ends his session.
    session: player's session.
    """  
    #session.getPlayer().getRoom().removeItem(session.getPlayer())  
    self.__sessions.remove(session)

  def __loadData(self):
    """ Loads all system data.
    """  
    """
    import createworld
    world = createworld.CreateWorld(self)
    world.create()
    """
    roomList = ggmodel.GGModel.readAll("room") 
    for room in roomList:
      self.__rooms.append(room)
      if room.getStartRoom():
        self.__startRooms.append(room) 

  def setStartRoom(self, room, startRoom):
    """ Sets a room as start room or not.
    room: room to be changed.
    startRoom: start room flag.
    """  
    foundRoom = None
    for oneRoom in self.__startRooms:
      if oneRoom.label == room.label:
        foundRoom = oneRoom
    if foundRoom and not startRoom:
      self.__startRooms.remove(foundRoom)
    elif not foundRoom and startRoom:
      self.__startRooms.append(room)

  def createRoom(self, spriteFull, label, size, maxUsers, enabled, startRoom, copyRoom=None):
    """ Creates a new room.
    spriteFull: sprite used to paint the room floor.
    label: room label.
    size: room size.
    maxUsers: max users per room.
    enabled: enabled room flag.
    starterRoom: sets this room as starter or not.
    copyRoom: room to be copied.
    """
    if self.getRoom(label):
      return None  
    newRoom = GG.model.room.GGRoom(spriteFull, label, size, maxUsers, enabled, startRoom)
    if copyRoom:
      items = copyRoom.getItems()
      for item in items:
        if not hasattr(item, "username"):  
          pos = item.getPosition()
          if (pos[0] < size[0]) and (pos[1] < size[1]):
            newRoom.addItemFromVoid(item.copyObject(), item.getPosition())  
    self.__rooms.append(newRoom)
    if startRoom:
      self.__startRooms.append(newRoom)    
    return newRoom

  def deleteRoom(self, label):
    """ Deletes a room.
    label: room label.
    """  
    for room in self.__rooms:
      if room.label == label:
        chosenRoom = room
      else:
        itemsList = room.getItems()
        for item in itemsList:
          if isinstance(item, GG.model.teleport.GGTeleport):
            if item.getDestinationRoom() == label: 
              item.setDestinationRoom(None)
    self.__rooms.remove(chosenRoom)
    chosenRoom.deleteObject("room")
    del chosenRoom
    chosenRoom = None
    return True
      
  def createPlayer(self, player):
    """ Creates a new player.
    player: new player.
    """
    if player in self.__players:
      return False
    self.__players.append(player)
    return True
    
  def insertItemIntoRoom(self, item, room, isPlayer):
    """ Inserts a new item into a room.
    item: new item.
    room: existing room.
    isPlayer: flag used to check it the item is a player or not.
    """
    if room.addItem(item):
      if isPlayer:
        if item in self.__players:
          return
        self.__players.append(item)
    
  def removeItem(self, item, isPlayer):
    """ Removes an item.
    item: existing item.
    isPlayer: flag used to check it the item is a player or not.
    """
    if item.getRoom():
      item.getRoom().removeItem(item)    
    if isPlayer and item in self.__players:
      self.__players.remove(item)

  def __start(self):
    """ Starts the program.
    """
    time_time = time.time
    time_sleep = time.sleep
    delay = GG.utils.TICK_DELAY
    try:
      while True:
        time_sleep(delay)
        self.__tick(time_time()*1000)
    except:
      dMVC.utils.logger.exception('Exception in __start')
    
  def __tick(self, now):
    """ Calls for a time tick on all rooms.
    now: timestamp.
    """
    for room in self.__rooms:
      room.tick(now)    

  def getResource(self, img):
    """ Returns a resource path.
    img: resource path.
    date: current date.
    """
    imgFile = open(os.path.join(GG.utils.DATA_PATH, img), "rb")
    imgData = imgFile.read()
    imgFile.close()
    return imgData

  def uploadFile(self, fileName, fileData, dirDest = None):
    """ Uploads a new file to the system.
    fileName: file name.
    fileData: file copy name.
    dirDest: file copy path.
    """  
    name = fileName[0] + "_" + str(int(time.time())) + fileName[1]
    try:
      if dirDest:
        upFile = open(os.path.join(GG.utils.DATA_PATH, dirDest, name), "wb")
      else:
        upFile = open(os.path.join(GG.utils.DATA_PATH, name), "wb")
      upFile.write(fileData)
      upFile.close()
    except:
      return None
    return name

  def changeAvatarConfiguration(self, configuration, player, nameMask):
    """ Changes the avatar configuration.
    configuration: new config.
    player: player to change the configuration for.
    nameMask: mask filename.
    """  
    self.__avatarGeneratorProcessQueue.put([configuration, player, nameMask])
    self.__throwAvatarGeneratorCommand()

  def __throwAvatarGeneratorCommand(self):
    """ Starts the avatar generation process.
    """  
    if not self.__avatarGeneratorHandler.isFullProcess():
      try:
        processOptions = self.__avatarGeneratorProcessQueue.get_nowait()
        thread.start_new(self.__changeAvatarConfiguration, (processOptions[0], processOptions[1], processOptions[2]))
      except Queue.Empty:
        pass

  def __changeAvatarConfiguration(self, configuration, player, nameMask):
    """ Changes the avatar configuration.
    configuration: new config.
    player: player to change the configuration for.
    nameMask: mask filename.
    """  
    self.__avatarGeneratorHandler.incNumProcess()
    if nameMask:
      maskFile = open(os.path.join(GG.utils.DATA_PATH, nameMask), "rb")
      data = maskFile.read()
      maskFile.close()
      self.__avatarGeneratorHandler.copyImageMask(nameMask, data)
      maskFile = open(os.path.join(GG.utils.DATA_PATH, "avatars/masks", player.username + ".png"),"wb")
      maskFile.write(data)
      maskFile.close()
      os.remove(os.path.join(GG.utils.DATA_PATH, nameMask))
    else:
      if os.path.isfile(os.path.join(GG.utils.DATA_PATH, "avatars/masks", player.username + ".png")):
        os.remove(os.path.join(GG.utils.DATA_PATH, "avatars/masks", player.username + ".png"))
    execCommand = self.__avatarGeneratorHandler.executeCommand(configuration, player, nameMask)
    if execCommand:
      images = self.__avatarGeneratorHandler.getImages(player)
      timestamp = self.__copyImages(images, player)
      self.__avatarGeneratorHandler.deleteImages(player)
      player.setAvatarConfiguration(configuration, timestamp)
    self.__avatarGeneratorHandler.decNumProcess()

  def __copyImages(self, images, player):
    """ Copies images for a given player.
    images: images to copy.
    player: given player.
    """  
    #dir = "/home/jmariscal/proyectos/genteguada/src/gg/GG/data/avatars"
    dirImage = GG.utils.DATA_PATH + "/avatars/"+player.username
    if os.path.isdir(dirImage):
      for fileName in os.listdir(dirImage):
        os.remove(os.path.join(dirImage, fileName))
    else:
      os.mkdir(dirImage)
    timestamp = int(time.time())
    for image in images.keys():
      f = open(os.path.join(dirImage, image + "_" + str(timestamp)), "wb")
      f.write(images[image])
      f.close()
    return timestamp

  @staticmethod
  def getInstance():
    return GGSystem.instance

  def getRoom(self, label):
    """ Returns a selected room.
    label: room's label.
    """  
    for room in self.__rooms:
      if room.label == label:
        return room
    return None

  def existsRoom(self, name):
    """ Checks if a room exists.
    name: room label.
    """  
    for room in self.__rooms:
      if room.label == name:
        return room  
    return None

  def getRoomLabels(self):
    """ Returns a list containing all room labels.
    """  
    listLabels = []
    for room in self.__rooms:
      listLabels.append(room.label)
    return listLabels  

  def labelChange(self, oldLabel, newLabel):
    """ Changes an item label.
    oldLabel: old item label.
    newLabel: new item label.
    """  
    for room in self.__rooms:
      room.labelChange(oldLabel, newLabel)

  def getAvatarImages(self, avatar):
    """ Returns the avatar images.
    avatar: player's avatar.
    """  
    dirPlayerImages = os.path.join(GG.utils.DATA_PATH, avatar.getImagePath())
    files = {}
    files["path"] = avatar.getImagePath()
    files["avatar"] = avatar
    for playerImage in os.listdir(dirPlayerImages):
      if os.path.isfile(os.path.join(dirPlayerImages, playerImage)):
        filePlayerImage = open(os.path.join(dirPlayerImages, playerImage), "rb")
        files[playerImage] = filePlayerImage.read()
        filePlayerImage.close()
    return files
    
  def getPlayersList(self):
    """ Returns the active players list.
    """  
    pList = []  
    for session in self.__sessions:
      pList.append(session.getPlayer().username)
    return pList

  def getRooms(self):
    """ Returns the rooms list.
    """  
    return self.__rooms  

  def getSpecificPlayer(self, name):
    """ Returns a specific player.
    name: player name.
    """  
    for player in self.__players:
      if player.getName() == name:
        return player
    return None  

  def newBroadcastMessage(self, line, player):
    """ Sends a new broadcast message.
    line: message text.
    player: message sender.
    """  
    for room in self.__rooms:
      room.newChatMessage(line, player, 3)    

  def deleteGift(self, idGift, username=None):
    """ Deletes a web gift from the game.
    idGift: gift id.
    username: gift owner.
    """  
    markedItem = None
    markedRoom = None
    markedPlayer = None
    if username:
      player = self.getSpecificPlayer(username)  
      if player:
        inventory = player.getInventory()
        for item in inventory:
          if isinstance(item, GG.model.generated_inventory_item.GGGeneratedGift):
            if item.getIdGift() == idGift:
              markedItem = item
              markedPlayer = player
    else:
      for player in self.__players:
        inventory = player.getInventory()
        for item in inventory:
          if isinstance(item, GG.model.generated_inventory_item.GGGeneratedGift):
            if item.getIdGift() == idGift:
              markedItem = item
              markedPlayer = player
    if markedItem:
      markedPlayer.removeFromInventory(markedItem)
      return True
    markedItem = None
    markedRoom = None
    markedPlayer = None
    for room in self.__rooms:
      items = room.getItems()
      for item in items:
        if isinstance(item, GG.model.giver_npc.WebGift):
          if item.getIdGift() == idGift:
            markedItem = item
            markedRoom = room
    if markedItem:
      markedRoom.removeItem(markedItem)
      return True
    return False  
            
  def deletePlayer(self, username):
    """ Deletes a player and all references to him from the game.
    username: player name.
    """  
    markedPlayer = None
    markedSession = None
    for player in self.__players:
      if player.username == username:
        markedPlayer = player
      else:
        player.removePlayerContactFromAgenda(username)  
    if not markedPlayer:
      return False
    markedPlayer.kick()
    markedPlayer.removeAllData()
    self.__players.remove(markedPlayer)
    return True
    
