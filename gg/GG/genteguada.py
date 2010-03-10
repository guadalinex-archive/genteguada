# -*- coding: utf-8 -*-

import sys
import datetime
import os
import pygame
import pygame.locals
import time
import dMVC.remoteclient
import ocempgui.widgets
import GG.isoview.login
import GG.utils
import GG.isoview.guiobjects

#Constants
VERSION = "0.17.1-3"
VERSION_TITLE = "GenteGuada "+VERSION
CLEAR_CACHE_WEEKS = 4
LOADING_BACKGROUND = os.path.join(GG.utils.INIT_IMAGE_PATH, "loadingGG.png")
LOADING_BACKGROUND_POSITION = [0, 0]
LOADING_LABEL = "Cargando..."
LOADING_LABEL_POSITION = [350, 300]
WAITING_LABEL_POSITION = [314, 335]
UPLOAD_MASK = os.path.join(GG.utils.PATH_PHOTO_MASK,"imgUpload.png")
ERROR_CONNECTION = "No hay conexion con el servidor"
FPS = 30
ICON = os.path.join(GG.utils.INIT_IMAGE_PATH, "icon64.png") 

class GenteGuada:
  """ GenteGuada class.
  This is the program's main class. It starts all services and runs the game.
  """  

  def __init__(self):
    """ Class constructor.
    """  
    self.__screen = None
    self.__system = None
    self.__isoHud = None
    self.__session = None
    self.__client = None
    self.__fullScreen = None
    self.__avatarDownloadImages = []
    self.__exitCondition = None
    self.__singleMode = False
    self.__clearCache()
    self.avatarConfigurationData = None
    GenteGuada.instance = self
    
  @staticmethod
  def getInstance():
    """ Returns this class's instance.
    """  
    return GenteGuada.instance

  def getSession(self):
    """ Returns the active session object.
    """  
    return self.__session
  
  def __input(self, events):
    """ Handles the keyboard and window input events.
    """  
    for event in events:
      if event.type == pygame.locals.QUIT:
        self.finish()
      if event.type == pygame.locals.KEYDOWN:
        if event.key == pygame.locals.K_ESCAPE:
          self.finish()
    
  def finish(self):
    """ Closes the program and all its services.
    """  
    if self.__session:
      self.__session.getPlayer().setState(GG.utils.STATE[1])    
    if self.__exitCondition is None:
      sys.exit(0)
    self.__isoHud.getModel().unsubscribeEvents()
    self.__isoHud.getIVRoom().getModel().exitPlayer(self.__isoHud.getPlayer())
    self.__isoHud.unsubscribeAllEvents()
    pygame.mixer.music.stop()
    self.__exitCondition = True

  def __connectScreen(self):
    """ Loads the "loading screen".
    """  
    widgetContainer = ocempgui.widgets.Renderer()
    widgetContainer.set_screen(self.__screen)
    window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0], GG.utils.SCREEN_SZ[1])
    imgPath = LOADING_BACKGROUND
    imgBackgroundRight = GG.isoview.guiobjects.OcempImageMapTransparent(imgPath)
    imgBackgroundRight.topleft = LOADING_BACKGROUND_POSITION
    window.add_child(imgBackgroundRight)
    loadingLabel = GG.isoview.guiobjects.OcempLabel("Conectando ...", GG.isoview.guiobjects.STYLES["labelWaiting"])
    loadingLabel.topleft = WAITING_LABEL_POSITION
    window.add_child(loadingLabel)
    widgetContainer.add_widget(window)

  def __loadingScreen(self):
    """ Loads the "loading screen".
    """  
    widgetContainer = ocempgui.widgets.Renderer()
    widgetContainer.set_screen(self.__screen)
    window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0], GG.utils.SCREEN_SZ[1])
    imgPath = LOADING_BACKGROUND
    imgBackgroundRight = GG.isoview.guiobjects.OcempImageMapTransparent(imgPath)
    imgBackgroundRight.topleft = LOADING_BACKGROUND_POSITION
    window.add_child(imgBackgroundRight)
    loadingLabel = GG.isoview.guiobjects.OcempLabel(LOADING_LABEL, GG.isoview.guiobjects.STYLES["labelLoading"])
    loadingLabel.topleft = LOADING_LABEL_POSITION
    window.add_child(loadingLabel)
    widgetContainer.add_widget(window)
  
  def __waitScreen(self):
    """ Loads the "waiting screen".
    """  
    widgetContainer = ocempgui.widgets.Renderer()
    widgetContainer.set_screen(self.__screen)
    window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0], GG.utils.SCREEN_SZ[1])
    imgPath = self.getDataPath(LOADING_BACKGROUND)
    imgBackgroundRight = GG.isoview.guiobjects.OcempImageMapTransparent(imgPath)
    imgBackgroundRight.topleft = LOADING_BACKGROUND_POSITION
    window.add_child(imgBackgroundRight)
    loadingLabel = GG.isoview.guiobjects.OcempLabel("Salas ocupadas. Espere...", GG.isoview.guiobjects.STYLES["labelWaiting"])
    loadingLabel.topleft = WAITING_LABEL_POSITION
    window.add_child(loadingLabel)
    widgetContainer.add_widget(window)
  
  def start(self, params):
    """ Creates all necessary objects and initializes attributes.
    params: application start parameters.
    """  
    pygame.init()
    pygame.display.set_caption(VERSION_TITLE)
    icon = pygame.image.load(ICON)
    pygame.display.set_icon(icon) 
    self.__screen = pygame.display.set_mode(GG.utils.SCREEN_SZ, pygame.HWSURFACE | pygame.DOUBLEBUF, 0)
    if params.fullscreen:
      pygame.display.toggle_fullscreen()
    self.__fullScreen = params.fullscreen
    self.__connectScreen()
    self.__setSystem(params.ip, params.port)
    if self.__system is None:
      errorConnection = GG.isoview.login.ErrorConnection(self.__screen, self)
      errorConnection.draw()
    self.__loadingScreen()
    winLogin = GG.isoview.login.Login(self.__screen, self)
    self.__session = winLogin.draw()
    #self.__session = winLogin.draw(params.user, params.password)
    self.__loadingScreen()
    user = self.__session.getPlayer()
    #userAdmin = False
    if user.admin:
    #  userAdmin = winLogin.drawAccessMode()  
    #  user.setAccessMode(userAdmin)
      user.setAccessMode(True)
    self.__loadingScreen()
    #self.__initGame(user, userAdmin)
    self.__initGame(user)

  def getSystem(self):
    """ Returns the system object.
    """  
    return self.__system

  def __setSystem(self, ipAddress, port):
    """ Loads a new system object from a remote location.
    ipAddress: remote location ip address.
    port: remote location port.
    """  
    if ipAddress:
      try:
        self.__client = dMVC.remoteclient.RClient(ipAddress, port = port, autoEvents=False)
      except Exception, excep:
        print excep, ERROR_CONNECTION
      if self.__client is not None:
        self.__system = self.__client.getRootModel()
        if not self.validateVersion(self.__client.getVersion()):
          import GG.isoview.login
          errorVersion = GG.isoview.login.ErrorVersion(self.__screen, self)
          errorVersion.draw()
    else:
      import GG.model.ggsystem
      self.__singleMode = True
      self.__system = GG.model.ggsystem.GGSystem()

  def validateVersion(self, version):
    if version in [VERSION,"0.17.1-1"]:
      return True
    return False

  #def __initGame(self, user, accesMode):
  def __initGame(self, user):
    """ Initializes all start parameters and runs the game's main process.
    """  
    #self.__isoHud = self.__session.defaultView(self.__screen, self.__fullScreen, user, accesMode)
    self.__isoHud = self.__session.defaultView(self.__screen, self.__fullScreen, user)
    self.__screen.fill([0, 0, 0])
    self.__isoHud.draw()
    isohud = self.__isoHud
    intentedFPS = 30
    frameCounter = 0
    theClock = pygame.time.Clock()
    theClock_tick = theClock.tick
    get_ticks = pygame.time.get_ticks
    pygame_event_get = pygame.event.get
    time_sleep = time.sleep
    if self.__client:
      client_processEvents = self.__client.processEvents
    else:
      client_processEvents = lambda : None  # Do nothing!
    last = get_ticks()
    self.__exitCondition = False
    while not self.__exitCondition:
      time_sleep(0.01) # Minor sleep to give opportunity to another thread to execute
      theClock_tick(FPS)
      client_processEvents()
      now = get_ticks()
      self.checkUploadFileMaskFinish()
      isohud.updateFrame(pygame_event_get(), now)
    self.__exitCondition = None
    pygame.quit()

  def getDataPath(self, img):
    """ Returns the data path for an item image, being local or remote.
    """  
    if self.__singleMode:
      return os.path.join(GG.utils.DATA_PATH, img)
    else:
      pathFile = os.path.join(GG.utils.LOCAL_DATA_PATH, img)
      if not os.path.isfile(pathFile):
        imgData = self.__system.getResource(img) 
        if imgData:
          if not os.path.isdir(os.path.dirname(pathFile)):
            GG.utils.createRecursiveDir(os.path.dirname(pathFile))
          imgFile = open(pathFile, "wb")
          imgFile.write(imgData)
          imgFile.close()
        else:
          return GG.utils.IMG_ERROR
      return pathFile

  def getListDataPath(self, imgList):
    """ Returns the data path for an item image list.
    imgList: image list.
    """  
    result = []
    for imgName in imgList:
      result.append(self.getDataPath(imgName))
    return result
  
  def __clearCache(self):
    """ Clears the local cache folder.
    """  
    now = datetime.datetime.today()
    limitDate = now - datetime.timedelta(weeks=CLEAR_CACHE_WEEKS)
    limitTime = time.mktime(limitDate.timetuple())
    GG.utils.clearCache(GG.utils.LOCAL_DATA_PATH, limitTime)

  def uploadFile(self, upFile, dirDest=None):
    """ Uploads a new file and copies it.
    upFile: uploaded file.
    dirDest: file copy location.
    """  
    if not os.path.isfile(upFile):
      return None
    filepath, fileName = os.path.split(upFile)
    name, ext = os.path.splitext(fileName)
    try:
      uploadedFile = open(file , "rb")
      dataFile = uploadedFile.read()
      uploadedFile.close()
    except:
      return None
    return self.__system.uploadFile([name, ext], dataFile, dirDest)
 
  def asyncUploadFile(self, upFile, finishMethod, dirDest = None):
    """ Uploads a new file  on asynchronous mode and copies it.
    upFile: uploaded file.
    finishMethod: method executed on upload end. 
    dirDest: file copy location.
    """  
    if not os.path.isfile(upFile):
      finishMethod(None)
      return 
    filepath, fileName = os.path.split(upFile)
    name, ext = os.path.splitext(fileName)
    try:
      uploadedFile = open(upFile , "rb")
      dataFile = uploadedFile.read()
      uploadedFile.close()
    except:
      finishMethod(None)
      return 
    self.__system.async(self.__system.uploadFile, finishMethod, [name, ext], dataFile, dirDest)
 
  def checkUploadFileMaskFinish(self):
    if self.avatarConfigurationData:
      if self.avatarConfigurationData["mask"]:
        self.__system.changeAvatarConfiguration(self.avatarConfigurationData["configuracion"], self.avatarConfigurationData["player"], self.avatarConfigurationData["mask"])
        self.avatarConfigurationData = None

  def uploadAvatarConfiguration(self, configuration, player):
    """ Uploads an avatar configuration.
    configuration: avatar configuration data.
    player: avatar's owner.
    """  
    if configuration["mask"]:
      self.avatarConfigurationData = {}
      self.avatarConfigurationData["configuracion"] = configuration
      self.avatarConfigurationData["player"] =  player
      self.avatarConfigurationData["mask"] = None
      self.asyncUploadFile(UPLOAD_MASK, self.uploadMaskFileFinish)
    else:
      self.__system.changeAvatarConfiguration(configuration, player, None) 

  def uploadMaskFileFinish(self, resultado):
    """ Changes the avatar's mask after upload is finished.
    resultado: upload result.
    """  
    if resultado:
      self.avatarConfigurationData["mask"] = resultado

  def getRoom(self, label):
    """ Returns an specific room.
    label: room's label.
    """  
    return self.__system.getRoom(label)  

  def createRoom(self, label, size, image, maxUsers, enabled, startRoom, copyRoom=None):
    """ Creates a new room.
    label: room label.
    size: room size.
    image: sprite used to paint the room floor.
    maxUsers: max users per room.
    enabled: enabled room flag.
    starterRoom: sets this room as starter or not.
    copyRoom: room to be copied.
    """  
    return self.__system.createRoom(image, label, size, maxUsers, enabled, startRoom, copyRoom)

  def deleteRoom(self, label):
    """ Deletes a room from the system.
    label: room's label.
    """  
    return self.__system.deleteRoom(label)  

  def getAvatarImages(self, avatar):
    """ Creates avatar images.
    avatar: curren player's avatar.
    """  
    if not avatar.username in self.__avatarDownloadImages:
      self.__avatarDownloadImages.append(avatar.username)
      self.__system.async(self.__system.getAvatarImages, self.getAvatarImagesFinish, avatar)

  def getAvatarImagesFinish(self, resultado):
    """ Saves all created avatar images.
    resultado: avatar images creation result.
    """  
    path = resultado["path"]
    if not os.path.isdir(os.path.join(GG.utils.LOCAL_DATA_PATH, path)):
      GG.utils.createRecursiveDir(os.path.join(GG.utils.LOCAL_DATA_PATH, path)) 
    for key in resultado.keys():
      if not key in ["path", "avatar", "timestamp"]:
        avatarImage = open(os.path.join(GG.utils.LOCAL_DATA_PATH, path, key), "wb")
        avatarImage.write(resultado[key])
        avatarImage.close()
    self.__isoHud.changeAvatarImages(resultado["avatar"], resultado["path"], resultado["timestamp"])
    if resultado["avatar"].username in self.__avatarDownloadImages:
      self.__avatarDownloadImages.remove(resultado["avatar"].username)

  def isSingleMode(self):
    """ Checks wether the game is in sigle player mode or multiplayer mode.
    """  
    return self.__singleMode

  def isAvatarDownload(self, avatar):
    return avatar.username in self.__avatarDownloadImages

  def sendError(self):
    if os.path.isfile("error.txt"):
      fileError = open("error.txt","r")
      errorData = fileError.read()
      fileError.close()
      send = self.__system.sendError(errorData)
      if send:
        os.remove("error.txt")

