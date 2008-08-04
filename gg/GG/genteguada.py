# -*- coding: iso-8859-15 -*-

import datetime
import os
import pygame
import pygame.locals
import stat
import sys
import time

import dMVC.remoteclient

import ocempgui.widgets
import GG.isoview.login
import GG.utils
import GG.isoview.guiobjects


class GenteGuada:

  def __init__(self):
    self.screen = None
    self.system = None
    self.isoHud = None
    self.session = None
    self.client = None
    GenteGuada.instance = self
    self.activeScreen = None
    self.fs = None
    self.window = None
    self.widgetContainer = None
    self.clearCache()
    
  @staticmethod
  def getInstance():
    return GenteGuada.instance
  
  def input(self, events):
    for event in events:
      if event.type == pygame.locals.QUIT:
        self.finish()
      if event.type == pygame.locals.KEYDOWN:
        if event.key == pygame.locals.K_ESCAPE:
          self.finish()
    
  def finish(self):
    #print dMVC.utils.statClient.strClient()
    #print dMVC.utils.statEventTriggered.strEvent()
    self.isoHud.getModel().unsubscribeEvents()
    self.isoHud.getIVRoom().getModel().exitPlayer(self.isoHud.getPlayer())
    self.isoHud.unsubscribeAllEvents()
    pygame.mixer.music.stop()
    sys.exit(0)
  
  def start(self, params):
    pygame.init()
    #print pygame.display.list_modes()
    self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ,
                                          pygame.HWSURFACE | pygame.DOUBLEBUF,
                                          0)
    if params.fullscreen:
      pygame.display.toggle_fullscreen()
      self.fs = params.fullscreen
    else:
      self.fs = 0    

    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.screen)
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0], GG.utils.SCREEN_SZ[1])
    
    imgPath = self.getDataPath("interface/backgrounds/loadingGG.png")
    imgBackgroundRight = GG.isoview.guiobjects.OcempImageMapTransparent(imgPath)
    imgBackgroundRight.topleft = 0, 0
    self.window.add_child(imgBackgroundRight)
    
    loadingLabel = GG.isoview.guiobjects.OcempLabel("Cargando...", \
                            ocempgui.widgets.WidgetStyle(GG.isoview.guiobjects.STYLES["labelLoading"]))
    #loadingLabel.topleft = 372,347
    loadingLabel.topleft = 350, 300
    loadingLabel.border = 1
    loadingLabel.set_minimum_size(230, 40)
    self.window.add_child(loadingLabel)
    
    self.widgetContainer.add_widget(self.window)
    #time.sleep(3)
    
    pygame.display.set_caption(GG.utils.VERSION)

    #print pygame.display.Info()

    """
    if self.screen.get_flags() & pygame.DOUBLEBUF:
        print "Using Double Buffering!"
    else:
        print "*NOT* Using Double Buffering!"
    if self.screen.get_flags() & pygame.HWSURFACE:
        print "Using Hardware Surface!"
    else:
        print "*NOT* Using Hardware Surface!"
    print
    """

    self.__getSystem(params.ip) 
    winLogin = GG.isoview.login.Login(self.screen, self)
    self.session = winLogin.draw()
    #self.session = winLogin.draw(params.user, params.password)
    if self.session.getPlayer().admin:
      #print "probando el tema asincronico"
      #self.session.async(self.session.getRoom, "casa", self.start)
      #print "finaliza la prueba"
      value = winLogin.drawAccessMode()  
      if value == 1:
        self.session.getPlayer().setAccessMode(True)
      else:  
        self.session.getPlayer().setAccessMode(False)  

    while self.system.getEntryRoom().isFull():
      time.sleep(2) 
      self.input(pygame.event.get())
    self.initGame()

  def __getSystem(self, ipAddress):
    if ipAddress:
      try:
        self.client = dMVC.remoteclient.RClient(ipAddress, autoEvents=False)
      except Exception, excep:
        print excep, "No hay conexion con el servidor"
        self.finish()
      self.system = self.client.getRootModel()
    else:
      import GG.model.ggsystem
      self.system = GG.model.ggsystem.GGSystem()

  def initGame(self):
    self.isoHud = self.session.defaultView(self.screen, self.fs)
    self.screen.fill([0, 0, 0])
    self.isoHud.draw()
    self.activeScreen = self.isoHud

    intentedFPS = 30
    frameCounter = 0

    # Avoid name resolution inside the loop
    theClock = pygame.time.Clock()
    theClock_tick = theClock.tick
    get_ticks = pygame.time.get_ticks
    pygame_event_get = pygame.event.get
    time_sleep = time.sleep
    if self.client:
      client_processEvents = self.client.processEvents
    else:
      client_processEvents = lambda : None  # Do nothing!

    last = get_ticks()
    while True:
      time_sleep(0.01) # Minor sleep to give oportunity to other thread to execute
      theClock_tick(intentedFPS)

      client_processEvents()

      activeScreen = self.activeScreen
      activeScreen.processEvent(pygame_event_get())
      now = get_ticks()
      activeScreen.updateFrame(now)

      # FPS statistics
      if (frameCounter == intentedFPS):
        averageTimePerFrame = float(now - last) / frameCounter
        #print "Average: Time per Frame=" + str(averageTimePerFrame) +  "ms, FPS=" + str(1000 / averageTimePerFrame)

        frameCounter = 0
        last = now
      else:
        frameCounter += 1


  def getDataPath(self, img):
    #return os.path.join(GG.utils.DATA_PATH, img)
    #if isinstance(self.system,GG.model.ggsystem.GGSystem):
    if os.path.isdir(GG.utils.DATA_PATH):
      return os.path.join(GG.utils.DATA_PATH, img)
    else:
      newImgName = img.replace("/","-")
      pathFile = os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName)
      #if os.path.isfile(pathFile):
      #  dateFile = os.stat(pathFile)[stat.ST_MTIME]
      #else:
      #  dateFile = None
      if os.path.isfile(pathFile):
        return os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName)

      imgData = self.system.getResource(img, None)#dateFile) 
      if imgData:
        imgFile = open(os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName), "wb")
        imgFile.write(imgData)
        imgFile.close()
      return os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName)

  def getListDataPath(self, imgList):
    result = []
    for imgName in imgList:
      result.append(self.getDataPath(imgName))
    return result
  
  def clearCache(self):
    now = datetime.datetime.today()
    limitDate = now - datetime.timedelta(weeks=GG.utils.CLEAR_CACHE_WEEKS)
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

  def uploadFile(self, file):
    if not os.path.isfile(file):
      return None
    filepath, fileName = os.path.split(file)
    name, ext = os.path.splitext(fileName)
    try:
      uploadedFile = open(file , "rb")
      dataFile = uploadedFile.read()
      uploadedFile.close()
    except:
      return None
    return self.system.uploadFile([name, ext], dataFile)

  def uploadAvatarConfiguration(self, configuration, player):
    if configuration["mask"]:
      fileName = os.path.join(GG.utils.PATH_PHOTO_MASK,"imgUpload.png")
      nameMask = self.uploadFile(fileName)
    else:
      nameMask = None
    self.system.changeAvatarConfiguration(configuration, player, nameMask) 

  def getRoom(self, label):
    return self.system.getRoom(label)  

  def createRoom(self, label, size, image, maxUsers):
    return self.system.createRoom(image, label, size, maxUsers)
