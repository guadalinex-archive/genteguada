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
import mailbox

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
    self.__mailBox = None
    self.__sessions = [] # Variable privada solo para uso interno.
    self.__avatarGeneratorHandler = GG.avatargenerator.generator.AvatarGenerator()
    self.__avatarGeneratorProcessQueue = Queue.Queue()
    thread.start_new(self.__start, ())
    GGSystem.instance = self
    self.__loadData()
     
  def __getEntryRoom(self):
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
  
  @dMVC.synchronized.synchronized(lockName='accessSession')
  def login(self, username, password):
    """ Attempts to login on an user. If succesfull, returns a ggsession model.
    username: user name.
    password: user password.
    """
    for sess in self.__sessions:
      if sess.getPlayer().checkUser(username):
        return False, "El usuario tiene una sesion abierta"    
    accessMode, numEntradaForo = self.loginGuadalinex(username, password)
    if not accessMode:
      if numEntradaForo is None:
        return False, "No se ha podido autenticar en guadalinex"
      else:
        return "Condiciones", numEntradaForo
    user = self.__getPlayer(username, accessMode)
    user.setNumEntradasForo(numEntradaForo)
    if not self.__accessUserIntoRoom(user):
      return False, "No existen habitaciones disponibles"  
    session = GG.model.ggsession.GGSession(user, self)
    self.__sessions.append(session)
    return True, session 

  @dMVC.synchronized.synchronized(lockName='accessRoom')
  def __accessUserIntoRoom(self, user):
    newRoom = user.getRoom()
    if not newRoom:
      newRoom = self.__getEntryRoom()
      if not newRoom:
        return False
    else:
      #comprobar que hay sitio en la habitacion
      user.clearRoom()
    user.changeRoom(newRoom, newRoom.getNearestEmptyCell([4, 4]))
    return True

  def __getPlayer(self, username, accessMode):
    player = ggmodel.GGModel.read(username, "player")
    if not player:
      player = GG.model.player.GGPlayer(username, "")
    if accessMode == "A":
      player.admin = True
    self.mailBox.newPlayerActive(player)
    return player
  
  def loginGuadalinex(self, user, passwd):
    """ Logs in an user.
    user: user name.
    passwd: user password.
    """  
    #return "A",10
    params = urllib.urlencode({"usuario": user, "password": passwd})  
    guadalinexLogin = urllib2.urlopen("http://www.guadalinex.org/usrdata?" +params)  
    result = guadalinexLogin.read()  
    guadalinexLogin.close()  
    data = result.split(";")
    if not len(data) == 4:
      if len(data) == 2:
        return False,data[1]
      return False,None
    try:
      numForo = int(data[0])
    except:
      numForo = 0
    return data[3],numForo
    
  @dMVC.synchronized.synchronized(lockName='accessSession')
  def logout(self, session):
    """ Logs out a player and ends his session.
    session: player's session.
    """  
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
      if room:
        self.__rooms.append(room)
        if room.getStartRoom():
          self.__startRooms.append(room) 
    if len(self.__rooms) == 0:
      import createworld
      word = createworld.CreateWorld(self)
      word.create()
      #newRoom = GG.model.room.GGRoom(GG.utils.TILES_SNOW, "Habitacion entrada", [8, 8], 12, True, True)
      #self.__rooms.append(newRoom)
      #self.__startRooms.append(newRoom)    
    self.mailBox = mailbox.MailBox()

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

  @dMVC.synchronized.synchronized(lockName='accessRoom')
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

  @dMVC.synchronized.synchronized(lockName='accessRoom')
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
    
  @dMVC.synchronized.synchronized(lockName='accessRoom')
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
    try:
      imgFile = open(os.path.join(GG.utils.DATA_PATH, img), "rb")
      imgData = imgFile.read()
      imgFile.close()
    except:
      imgData = None
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
      maskFile = open(os.path.join(GG.utils.DATA_PATH, GG.utils.MASKS_DIR, player.username + ".png"),"wb")
      maskFile.write(data)
      maskFile.close()
      os.remove(os.path.join(GG.utils.DATA_PATH, nameMask))
    else:
      if os.path.isfile(os.path.join(GG.utils.DATA_PATH, GG.utils.MASKS_DIR, player.username + ".png")):
        os.remove(os.path.join(GG.utils.DATA_PATH, GG.utils.MASKS_DIR, player.username + ".png"))
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
    dirImage = os.path.join(GG.utils.DATA_PATH, GG.utils.INTERFACE_AVATARS, player.username)
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

  @dMVC.synchronized.synchronized(lockName='accessRoom')
  def getRoom(self, label):
    """ Returns a selected room.
    label: room's label.
    """  
    for room in self.__rooms:
      if room.label == label:
        return room
    return None

  @dMVC.synchronized.synchronized(lockName='accessRoom')
  def getRoomLabels(self):
    """ Returns a list containing all room labels.
    """  
    listLabels = []
    for room in self.__rooms:
      listLabels.append(room.label)
    return listLabels  

  @dMVC.synchronized.synchronized(lockName='accessRoom')
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
    files["timestamp"] = avatar.getTimestamp()
    files["avatar"] = avatar
    for playerImage in os.listdir(dirPlayerImages):
      if os.path.isfile(os.path.join(dirPlayerImages, playerImage)):
        filePlayerImage = open(os.path.join(dirPlayerImages, playerImage), "rb")
        files[playerImage] = filePlayerImage.read()
        filePlayerImage.close()
    return files
    
  @dMVC.synchronized.synchronized(lockName='accessRoom')
  def getRooms(self):
    """ Returns the rooms list.
    """  
    return self.__rooms  

  @dMVC.synchronized.synchronized(lockName='accessRoom')
  def newBroadcastMessage(self, line, player):
    """ Sends a new broadcast message.
    line: message text.
    player: message sender.
    """  
    for room in self.__rooms:
      room.newChatMessage(line, player, 3)    

  @dMVC.synchronized.synchronized(lockName='accessRoom')
  def deleteGift(self, idGift, username=None):
    """ Deletes a web gift from the game.
    idGift: gift id.
    username: gift owner.
    """  
    if username:
      player = self.getPlayerConnected(username)
      if player:
        return player.deleteGift(idGift)
      else:
        return self.mailBox.newEventDeleteGift(self.getConnectedPlayers(), idGift, username)
    else:
      for room in self.__rooms:
        items = room.getItems()
        for item in items:
          if isinstance(item, GG.model.giver_npc.WebGift):
            if item.getIdGift() == idGift:
              room.removeItem(item)
              return True
      return self.mailBox.newEventDeleteGift(self.getConnectedPlayers(), idGift)
            
  def deletePlayer(self, username):
    """ Deletes a player and all references to him from the game.
    username: player name.
    """  
    playerDelete = self.getPlayerConnected(username)
    if playerDelete:
      playerDelete.kick()
    else:
      playerDelete = ggmodel.GGModel.read(username, "player")
    if playerDelete:
      self.mailBox.newEventDeletePlayer(self.getConnectedPlayers(), username)
      playerDelete.removeAllData()
      playerDelete.deleteObject("player")
      return True
    return False

  @dMVC.synchronized.synchronized(lockName='accessSession')
  def getPlayerConnected(self,username):
    for session in self.__sessions:
      player = session.getPlayer()
      if player.username == username:
        return player
    return None

  @dMVC.synchronized.synchronized(lockName='accessSession')
  def getConnectedPlayers(self):
    result = {}
    for session in self.__sessions:
      player = session.getPlayer()
      result[player.username] = player
    return result

  @dMVC.synchronized.synchronized(lockName='accessRoom')
  def changeItemRandomPosition(self, item, player):
    room = self.__rooms[random.randint(0, len(self.__rooms) - 1)]
    posX = random.randint(0, room.size[0] - 1)
    posY = random.randint(0, room.size[1] - 1)
    player.setUnselectedItem()
    item.changeRoom(room, [posX, posY]) 

  def sendError(self, errorData):
    fileName = os.path.join(GG.utils.DIR_FILES_CLIENT_ERROR, "error"+str(int(time.time()))+".txt" )
    fileError = open(fileName, "w")
    fileError.write(errorData)
    fileError.close()
    return True
