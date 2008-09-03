# -*- coding: utf-8 -*-

import sys
import datetime
import os
import pygame
import pygame.locals
import stat
import time
import dMVC.remoteclient
import ocempgui.widgets
import GG.isoview.login
import GG.utils
import GG.isoview.guiobjects

#Constants
VERSION = "GenteGuada 0.2.0-1"
CLEAR_CACHE_WEEKS = 4
LOADING_BACKGROUND = os.path.join(GG.utils.BACKGROUNDS, "loadingGG.png")
LOADING_BACKGROUND_POSITION = [0, 0]
LOADING_LABEL = "Cargando..."
LOADING_LABEL_POSITION = [350, 300]
ERROR_CONNECTION = "No hay conexion con el servidor"
FPS = 30

class GenteGuada:

  def __init__(self):
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
    GenteGuada.instance = self
    
  @staticmethod
  def getInstance():
    return GenteGuada.instance
  
  def __input(self, events):
    for event in events:
      if event.type == pygame.locals.QUIT:
        self.finish()
      if event.type == pygame.locals.KEYDOWN:
        if event.key == pygame.locals.K_ESCAPE:
          self.finish()
    
  def finish(self):
    #print dMVC.utils.statClient.strClient()
    #print dMVC.utils.statEventTriggered.strEvent()
    if self.__exitCondition is None:
      #pygame.quit()
      sys.exit(0)
    self.__isoHud.getModel().unsubscribeEvents()
    self.__isoHud.getIVRoom().getModel().exitPlayer(self.__isoHud.getPlayer())
    self.__isoHud.unsubscribeAllEvents()
    pygame.mixer.music.stop()
    self.__exitCondition = True

  def __loadingScreen(self):
    widgetContainer = ocempgui.widgets.Renderer()
    widgetContainer.set_screen(self.__screen)
    window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0], GG.utils.SCREEN_SZ[1])
    imgPath = self.getDataPath(LOADING_BACKGROUND)
    imgBackgroundRight = GG.isoview.guiobjects.OcempImageMapTransparent(imgPath)
    imgBackgroundRight.topleft = LOADING_BACKGROUND_POSITION
    window.add_child(imgBackgroundRight)
    loadingLabel = GG.isoview.guiobjects.OcempLabel(LOADING_LABEL, GG.isoview.guiobjects.STYLES["labelLoading"])
    loadingLabel.topleft = LOADING_LABEL_POSITION
    window.add_child(loadingLabel)
    widgetContainer.add_widget(window)
  
  def start(self, params):
    self.__setSystem(params.ip)
    pygame.init()
    pygame.display.set_caption(VERSION)
    self.__screen = pygame.display.set_mode(GG.utils.SCREEN_SZ, pygame.HWSURFACE | pygame.DOUBLEBUF, 0)
    if params.fullscreen:
      pygame.display.toggle_fullscreen()
    self.__fullScreen = params.fullscreen
    self.__loadingScreen()
    winLogin = GG.isoview.login.Login(self.__screen, self)
    #self.__session = winLogin.draw()
    self.__session = winLogin.draw(params.user, params.password)
    self.__loadingScreen()
    if self.__session.getPlayer().admin:
      value = winLogin.drawAccessMode()  
      self.__session.getPlayer().setAccessMode(value)
    self.__loadingScreen()
    while self.__system.getEntryRoom().isFull():
      time.sleep(2) 
      self.__input(pygame.event.get())
    self.__initGame()

  def getSystem(self):
    return self.__system

  def __setSystem(self, ipAddress):
    if ipAddress:
      try:
        self.__client = dMVC.remoteclient.RClient(ipAddress, autoEvents=False)
      except Exception, excep:
        print excep, ERROR_CONNECTION
        self.finish()
      self.__system = self.__client.getRootModel()
    else:
      import GG.model.ggsystem
      self.__singleMode = True
      self.__system = GG.model.ggsystem.GGSystem()

  def __initGame(self):
    self.__isoHud = self.__session.defaultView(self.__screen, self.__fullScreen)
    self.__screen.fill([0, 0, 0])
    self.__isoHud.draw()
    isohud = self.__isoHud
    intentedFPS = 30
    frameCounter = 0
    # Avoid name resolution inside the loop
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
      #theClock_tick(intentedFPS)
      client_processEvents()
      now = get_ticks()
      isohud.updateFrame(pygame_event_get(), now)
      """ 
      # FPS statistics
      if (frameCounter == intentedFPS):
        averageTimePerFrame = float(now - last) / frameCounter
        print "Average: Time per Frame=" + str(averageTimePerFrame) +  "ms, FPS=" + str(1000 / averageTimePerFrame)

        frameCounter = 0
        last = now
      else:
        frameCounter += 1
      """
    pygame.quit()

  def getDataPath(self, img):
    if self.__singleMode:
      return os.path.join(GG.utils.DATA_PATH, img)
    else:
      newImgName = img.replace(os.sep,"-")
      pathFile = os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName)
      print pathFile
      if not os.path.isfile(pathFile):
        imgData = self.__system.getResource(img) 
        imgFile = open(os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName), "wb")
        imgFile.write(imgData)
        imgFile.close()
      return os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName)

  def getListDataPath(self, imgList):
    result = []
    for imgName in imgList:
      result.append(self.getDataPath(imgName))
    return result
  
  def __clearCache(self):
    now = datetime.datetime.today()
    limitDate = now - datetime.timedelta(weeks=CLEAR_CACHE_WEEKS)
    limitTime = time.mktime(limitDate.timetuple())
    toRemove = []
    for fileName in os.listdir(GG.utils.LOCAL_DATA_PATH):
      pathFile = os.path.join(GG.utils.LOCAL_DATA_PATH, fileName) 
      if os.path.isfile(pathFile):
        accessTime = os.stat(pathFile)[stat.ST_ATIME]
        if accessTime < limitTime:
          toRemove.append(fileName)
    for fileName in toRemove:
      pathFile = os.path.join(GG.utils.LOCAL_DATA_PATH, fileName) 
      os.remove(pathFile)

  def uploadFile(self, upFile):
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
    return self.__system.uploadFile([name, ext], dataFile)
  
  def uploadAvatarConfiguration(self, configuration, player):
    if configuration["mask"]:
      fileName = os.path.join(GG.utils.PATH_PHOTO_MASK,"imgUpload.png")
      nameMask = self.uploadFile(fileName)
    else:
      nameMask = None
    self.__system.changeAvatarConfiguration(configuration, player, nameMask) 

  def getRoom(self, label):
    return self.__system.getRoom(label)  

  def createRoom(self, label, size, image, maxUsers, copyRoom=None):
    return self.__system.createRoom(image, label, size, maxUsers, copyRoom)

  def deleteRoom(self, label):
    return self.__system.deleteRoom(label)  

  def getAvatarImages(self, avatar):
    if not avatar in self.__avatarDownloadImages:
      self.__avatarDownloadImages.append(avatar)
      self.__system.async(self.__system.getAvatarImages, self.getAvatarImagesFinish, avatar)

  def getAvatarImagesFinish(self, resultado):
    #path = resultado["path"].replace("/", "-")
    path = resultado["path"].replace(os.sep, "-")
    for key in resultado.keys():
      if not key in ["path", "avatar"]:
        fileName = path + "-" + key
        avatarImage = open(os.path.join(GG.utils.LOCAL_DATA_PATH, fileName), "wb")
        avatarImage.write(resultado[key])
        avatarImage.close()
    print "ya he copiado todas las imagenes"    
    self.__isoHud.changeAvatarImages(resultado["avatar"], resultado["path"])
  
  def isSingleMode(self):
    return self.__singleMode
