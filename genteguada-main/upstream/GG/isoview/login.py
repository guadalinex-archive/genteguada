# -*- coding: utf-8 -*-

import os
import pygame
import ocempgui.widgets
import GG.utils
import sys
import time
import guiobjects

from pygame.locals import * # faster name resolution

BUTTON_CANCEL = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "cancel_button.png")
BUTTON_OK = os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "ok_button.png")

class ErrorVersion:

  def __init__(self, screen, parent):
    self.__screen = screen

  def draw(self):
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.__screen)
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0], GG.utils.SCREEN_SZ[1])  
    self.__paintScreen()
    self.__paintTextLabels()
    self.__paintButtons()
    self.widgetContainer.add_widget(self.window)
    return self.__start()

  def __paintScreen(self):
    """ Paints the screen background. 
    """  
    imgBackgroundRight = guiobjects.OcempImageMapTransparent(os.path.join(GG.utils.INIT_IMAGE_PATH, "startGG.png"))
    imgBackgroundRight.topleft = 1, 0
    self.window.add_child(imgBackgroundRight)

  def __paintTextLabels(self):
    """ Paints text labels on screen.
    """  
    usernameLabel = guiobjects.OcempLabel("Versión no", ocempgui.widgets.WidgetStyle(guiobjects.STYLES["labelWaiting"]))
    usernameLabel.topleft = 650, 390
    usernameLabel.border = 1
    usernameLabel.set_minimum_size(230, 40)
    self.window.add_child(usernameLabel)
    passwordLabel = guiobjects.OcempLabel("compatible con", ocempgui.widgets.WidgetStyle(guiobjects.STYLES["labelWaiting"]))
    passwordLabel.topleft = 650, 435
    passwordLabel.border = 1
    passwordLabel.set_minimum_size(230, 40)
    self.window.add_child(passwordLabel)
    Label = guiobjects.OcempLabel("el servidor,", ocempgui.widgets.WidgetStyle(guiobjects.STYLES["labelWaiting"]))
    Label.topleft = 650, 480
    Label.border = 1
    Label.set_minimum_size(230, 40)
    self.window.add_child(Label)
    Label = guiobjects.OcempLabel("Actualize", ocempgui.widgets.WidgetStyle(guiobjects.STYLES["labelWaiting"]))
    Label.topleft = 650, 525
    Label.border = 1
    Label.set_minimum_size(230, 40)
    self.window.add_child(Label)
    Label = guiobjects.OcempLabel("GenteGuada", ocempgui.widgets.WidgetStyle(guiobjects.STYLES["labelWaiting"]))
    Label.topleft = 650, 570
    Label.border = 1
    Label.set_minimum_size(230, 40)
    self.window.add_child(Label)


  def __paintButtons(self):
    """ Paints accept and cancel buttons on screen.
    """  
    imgPath = os.path.join(GG.utils.INIT_IMAGE_PATH, "cancel_button.png")
    buttonCancel = guiobjects.OcempImageButtonTransparent(imgPath)
    buttonCancel.topleft = [870, 690]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.cancelLogin)
    self.window.add_child(buttonCancel)

  def cancelLogin(self):
    """ Cancels the login dialog.
    """  
    sys.exit(0)

  def __start(self):
    """ Starts the keyboard input event capture.
    """  
    while True:
      time.sleep(0.02)
      events = pygame.event.get()
      for event in events:
        if event.type == QUIT:
          sys.exit(0)
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            sys.exit(0)
      self.widgetContainer.distribute_events(*events)



class ErrorConnection:

  def __init__(self, screen, parent):
    self.__screen = screen
    #self.__finish = False
    #self.__parent = parent
    #self.__session = None

  def draw(self):
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.__screen)
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0], GG.utils.SCREEN_SZ[1])  
    self.__paintScreen()
    self.__paintTextLabels()
    self.__paintButtons()
    self.widgetContainer.add_widget(self.window)
    return self.__start()

  def __paintScreen(self):
    """ Paints the screen background. 
    """  
    imgBackgroundRight = guiobjects.OcempImageMapTransparent(os.path.join(GG.utils.INIT_IMAGE_PATH, "startGG.png"))
    imgBackgroundRight.topleft = 1, 0
    self.window.add_child(imgBackgroundRight)

  def __paintTextLabels(self):
    """ Paints text labels on screen.
    """  
    usernameLabel = guiobjects.OcempLabel("No hay conexión", ocempgui.widgets.WidgetStyle(guiobjects.STYLES["labelWaiting"]))
    usernameLabel.topleft = 650, 390
    usernameLabel.border = 1
    usernameLabel.set_minimum_size(230, 40)
    self.window.add_child(usernameLabel)
    passwordLabel = guiobjects.OcempLabel("con el servidor", ocempgui.widgets.WidgetStyle(guiobjects.STYLES["labelWaiting"]))
    passwordLabel.topleft = 650, 450
    passwordLabel.border = 1
    passwordLabel.set_minimum_size(230, 40)
    self.window.add_child(passwordLabel)


  def __paintButtons(self):
    """ Paints accept and cancel buttons on screen.
    """  
    imgPath = os.path.join(GG.utils.INIT_IMAGE_PATH, "cancel_button.png")
    buttonCancel = guiobjects.OcempImageButtonTransparent(imgPath)
    buttonCancel.topleft = [870, 690]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.cancelLogin)
    self.window.add_child(buttonCancel)

  def cancelLogin(self):
    """ Cancels the login dialog.
    """  
    sys.exit(0)

  def __start(self):
    """ Starts the keyboard input event capture.
    """  
    while True:
      time.sleep(0.02)
      events = pygame.event.get()
      for event in events:
        if event.type == QUIT:
          sys.exit(0)
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            sys.exit(0)
      self.widgetContainer.distribute_events(*events)

class Login:
  """ Login class.
  Defines attributes and methods for a Login class.
  """
    
  def __init__(self, screen, parent):
    """ Class constructor.
    screen: screen handler.
    parent: genteguada object.
    """
    self.__screen = screen
    self.__textFieldUsername = None
    self.__textFieldPassword = None
    self.__finish = False
    self.__parent = parent
    self.__session = None
    self.dialog = None
    self.__accessMode = None
    self.__urlPolicy = None
  
  def draw(self, user=None, passw=None):
    """ Draws the login screen.
    user: user name.
    passw: user password.
    """  
    if user and passw:
      return self.autoLogin(user, passw)
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.__screen)
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0], GG.utils.SCREEN_SZ[1])  
    self.__paintScreen()
    self.__paintTextLabels()
    self.__paintTextEntrys()
    self.__paintButtons()
    self.widgetContainer.add_widget(self.window)
    self.__textFieldUsername.set_focus()
    return self.__start()
  
  def __start(self):
    """ Starts the keyboard input event capture.
    """  
    while not self.__finish:
      #time.sleep(GG.utils.TICK_DELAY)
      time.sleep(0.02)
      events = pygame.event.get()
      for event in events:
        if event.type == QUIT:
          sys.exit(0)
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            if self.dialog:
              self.__closeDialog()
            else:
              sys.exit(0)
          elif event.key == K_RETURN: 
            if self.dialog:
              self.__closeDialog()
            else:
              self.acceptLogin()
      self.widgetContainer.distribute_events(*events)
    if self.__session:
      return self.__session
    self.cancelLogin()

  def drawAccessMode(self):
    """ Draws the admin access screen.
    """  
    self.__finish = False
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.__screen)
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0], GG.utils.SCREEN_SZ[1])
    
    imgBackgroundRight = guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.BACKGROUNDS, "TEMP_accessMode.png")))
    imgBackgroundRight.topleft = 0, 0
    self.window.add_child(imgBackgroundRight)
   
    cad = "¿Desea entrar como administrador?"
    notificationLabel = guiobjects.OcempLabel(cad, ocempgui.widgets.WidgetStyle(guiobjects.STYLES["labelLogin"]))
    notificationLabel.topleft = 100, 300
    notificationLabel.border = 1
    notificationLabel.set_minimum_size(230, 40)
    self.window.add_child(notificationLabel)
    
    imgPath = os.path.join(GG.utils.EDITOR, "ok_button.png")
    buttonOK = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath))
    buttonOK.topleft = [370, 450]
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.accessModeAdmin)
    self.window.add_child(buttonOK)
     
    imgPath = os.path.join(GG.utils.EDITOR, "cancel_button.png")
    buttonCancel = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath))
    buttonCancel.topleft = [550, 450]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.accessModeNormal)
    self.window.add_child(buttonCancel)
    
    self.widgetContainer.add_widget(self.window)
    return self.__startAccessMode()
  
  def __startAccessMode(self):
    """ Starts the keyboard input event capture for an admin user.
    """  
    while not self.__finish:
      time.sleep(0.02)
      events = pygame.event.get()
      for event in events:
        if event.type == QUIT:
          sys.exit(0)
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            sys.exit(0)
          elif event.key == K_RETURN: 
            self.accessModeAdmin()
      self.widgetContainer.distribute_events(*events)
    if self.__accessMode:
      return self.__accessMode
    self.accessModeNormal()
    
  def accessModeAdmin(self):
    """ Sets the access mode as admin.
    """  
    self.__accessMode = True
    self.__finish = True
    
  def accessModeNormal(self):
    """ Sets the access mode as user.
    """  
    self.__accessMode = False
    self.__finish = True
    
  def __paintScreen(self):
    """ Paints the screen background. 
    """  
    imgBackgroundRight = guiobjects.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.BACKGROUNDS, "startGG.png")))
    imgBackgroundRight.topleft = 1, 0
    self.window.add_child(imgBackgroundRight)

  def __paintTextLabels(self):
    """ Paints text labels on screen.
    """  
    self.__usernameLabel = guiobjects.OcempLabel("Usuario: ", ocempgui.widgets.WidgetStyle(guiobjects.STYLES["labelLogin"]))
    #self.__usernameLabel.topleft = 670,408
    self.__usernameLabel.topleft = 670, 390
    self.__usernameLabel.border = 1
    self.__usernameLabel.set_minimum_size(230, 40)
    self.window.add_child(self.__usernameLabel)

    self.__passwordLabel = guiobjects.OcempLabel("Password:", ocempgui.widgets.WidgetStyle(guiobjects.STYLES["labelLogin"]))
    #self.__passwordLabel.topleft = 670,518
    self.__passwordLabel.topleft = 670, 500
    self.__passwordLabel.border = 1
    self.__passwordLabel.set_minimum_size(230, 40)
    self.window.add_child(self.__passwordLabel)

  def __paintTextEntrys(self):
    """ Paints text entry boxes on screen.
    """  
    self.__textFieldUsername = ocempgui.widgets.Entry("")
    self.__textFieldUsername.topleft = 700, 460
    self.__textFieldUsername.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldLogin"]))
    self.__textFieldUsername.border = 1
    self.__textFieldUsername.set_minimum_size(230, 40)
    self.window.add_child(self.__textFieldUsername)

    self.__textFieldPassword = ocempgui.widgets.Entry("")
    self.__textFieldPassword.topleft = 700, 570
    self.__textFieldPassword.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldLogin"]))
    self.__textFieldPassword.border = 1
    self.__textFieldPassword.set_minimum_size(230, 40)
    self.__textFieldPassword.set_password(True)
    self.window.add_child(self.__textFieldPassword)

  def __paintButtons(self):
    """ Paints accept and cancel buttons on screen.
    """  
    imgPath = os.path.join(GG.utils.EDITOR, "ok_button.png")
    buttonOK = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath))
    buttonOK.topleft = [750, 690]
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.acceptLogin)
    self.window.add_child(buttonOK)
     
    imgPath = os.path.join(GG.utils.EDITOR, "cancel_button.png")
    buttonCancel = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath))
    buttonCancel.topleft = [870, 690]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.cancelLogin)
    self.window.add_child(buttonCancel)

  def acceptLogin(self):
    """ Accepts the login user info.
    """  
    user = self.__textFieldUsername.text 
    passw = self.__textFieldPassword.text
    loginData = self.__parent.getSystem().login(user, passw)
    if loginData[0] == "Condiciones":
      self.__urlPolicy = loginData[1]
      self.__showPolicyDialog()
    elif loginData[0] == True:
      self.__session = loginData[1]
      self.finishLogin()
    else:
      self.__showErrorDialog()

  def __showPolicyDialog(self):
    if self.dialog:
      return
    self.container = ocempgui.widgets.Box(516, 197)
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.BACKGROUNDS, "alertWindow.png"))
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0, 0
    self.container.add_child(imgBackground)
    self.dialog = ocempgui.widgets.DialogWindow("Error")
    self.dialog.topleft = 254, 50
    self.dialog.child = self.container
    self.widgetContainer.add_widget(self.dialog)
    buttonCancel = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_CANCEL))
    buttonCancel.topleft = [400, 140]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.__closeDialog)
    self.container.add_child(buttonCancel)
    buttonOK = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_OK))
    buttonOK.topleft = [280, 140]
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.__showPolicy)
    self.container.add_child(buttonOK)

    labelAlert = guiobjects.OcempLabel("Debe aceptar las normas del juego", guiobjects.STYLES["dialogFont"])
    labelAlert.topleft = 160, 50
    labelAlert2 = guiobjects.OcempLabel("antes de poder acceder", guiobjects.STYLES["dialogFont"])
    labelAlert2.topleft = 160, 65
    labelAlert3 = guiobjects.OcempLabel("Continuar .... ", guiobjects.STYLES["dialogFont"])
    labelAlert3.topleft = 160, 100
    self.container.add_child(labelAlert)
    self.container.add_child(labelAlert2)
    self.container.add_child(labelAlert3)
    return self.dialog

  def __showPolicy(self):
    import webbrowser
    webbrowser.open(self.__urlPolicy)
    self.__closeDialog()

  def __showErrorDialog (self):
    """ Shows an error dialog.  
    """
    if self.dialog:
      return
    self.container = ocempgui.widgets.Box(516, 197)
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.BACKGROUNDS, "alertWindow.png"))
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0, 0
    self.container.add_child(imgBackground)
    self.dialog = ocempgui.widgets.DialogWindow("Error")
    self.dialog.topleft = 254, 50
    self.dialog.child = self.container
    self.widgetContainer.add_widget(self.dialog)
    buttonCancel = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(BUTTON_CANCEL))
    buttonCancel.topleft = [400, 140]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.__closeDialog)
    self.container.add_child(buttonCancel)
    labelAlert = guiobjects.OcempLabel("Error: Usuario o password incorrectos.", guiobjects.STYLES["dialogFont"])
    labelAlert.topleft = 160, 80
    self.container.add_child(labelAlert)
    return self.dialog

  def __closeDialog (self):
    """ Closes the error dialog.
    """  
    self.widgetContainer.remove_widget(self.dialog)
    self.dialog.destroy ()
    self.dialog = None
    self.__textFieldUsername.text = ""
    self.__textFieldPassword.text = ""

  def cancelLogin(self):
    """ Cancels the login dialog.
    """  
    sys.exit(0)

  def finishLogin(self):
    """ Finishes the login process.
    """  
    self.__screen.fill((0, 0, 0))
    self.__finish = True
  
  def autoLogin(self, user, passw):
    """ Logs an user automatically.
    user: user name.
    passw: user password.
    """  
    loginData = self.__parent.getSystem().login(user, passw)
    if loginData[0] == True:
      return loginData[1]
    else:
      sys.exit(0)



  
