# -*- coding: utf-8 -*-

import os
import pygame
import ocempgui.widgets
import GG.utils
import sys
import time

from pygame.locals import * # faster name resolution


class Login:
  """ Login class.
  Defines attributes and methods for a Login class.
  """
    
  def __init__(self, screen, parent):
    """ Class constructor.
    screen: screen handler.
    parent: 
    """
    self.__screen = screen
    self.__textFieldUsername = None
    self.__textFieldPassword = None
    self.__finish = False
    self.__parent = parent
    self.__session = None
    self.dialog = None
  
  def draw(self, user=None, passw=None):
    if user and passw:
      return self.autoLogin(user, passw)

    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.__screen)
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0],GG.utils.SCREEN_SZ[1])  
    self.__paintScreen()
    self.__paintTextLabels()
    self.__paintTextEntrys()
    self.__paintButtons()
    self.widgetContainer.add_widget(self.window)
    self.__textFieldUsername.set_focus()
    return self.__start()
  
  def __start(self):
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

  def __paintScreen(self):
    imgBackgroundRight = GG.utils.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/startGG.png"))
    imgBackgroundRight.topleft = 0,0
    self.window.add_child(imgBackgroundRight)

  def __paintTextLabels(self):
    self.__usernameLabel = GG.utils.OcempLabel("Usuario: ", 80, ocempgui.widgets.WidgetStyle(GG.utils.STYLES["labelLogin"]))
    self.__usernameLabel.topleft = 670,400
    self.__usernameLabel.border = 1
    self.__usernameLabel.set_minimum_size(230,40)
    self.window.add_child(self.__usernameLabel)

    self.__passwordLabel = GG.utils.OcempLabel("Password:", 80, ocempgui.widgets.WidgetStyle(GG.utils.STYLES["labelLogin"]))
    self.__passwordLabel.topleft = 670,510
    self.__passwordLabel.border = 1
    self.__passwordLabel.set_minimum_size(230,40)
    self.window.add_child(self.__passwordLabel)

  def __paintTextEntrys(self):
    self.__textFieldUsername = ocempgui.widgets.Entry("")
    self.__textFieldUsername.topleft = 700,460
    self.__textFieldUsername.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["textFieldLogin"]))
    self.__textFieldUsername.border = 1
    self.__textFieldUsername.set_minimum_size(230,40)
    self.window.add_child(self.__textFieldUsername)

    self.__textFieldPassword = ocempgui.widgets.Entry("")
    self.__textFieldPassword.topleft = 700,570
    self.__textFieldPassword.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["textFieldLogin"]))
    self.__textFieldPassword.border = 1
    self.__textFieldPassword.set_minimum_size(230,40)
    self.__textFieldPassword.set_password(True)
    self.window.add_child(self.__textFieldPassword)

  def __paintButtons(self):
    imgPath = "interface/editor/ok_button.png"
    buttonOK = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath))
    buttonOK.topleft = [750, 690]
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.acceptLogin)
    self.window.add_child(buttonOK)
     
    imgPath = "interface/editor/cancel_button.png"
    buttonCancel = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath))
    buttonCancel.topleft = [870, 690]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.cancelLogin)
    self.window.add_child(buttonCancel)

  def acceptLogin(self):
    user = self.__textFieldUsername.text 
    passw = self.__textFieldPassword.text
    loginData = self.__parent.system.login(user,passw)
    print loginData
    if loginData[0] == True:
      self.__session = loginData[1]
      self.finishLogin()
    else:
      self.__showErrorDialog(loginData[1])

  def __showErrorDialog (self, errorText):

     if self.dialog:
       return
   
     self.container = ocempgui.widgets.Box(516,197)

     filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/alertWindow.png")
     imgBackground = GG.utils.OcempImageMapTransparent(filePath)
     imgBackground.topleft = 0,0
     self.container.add_child(imgBackground)
    
     self.dialog = ocempgui.widgets.DialogWindow("Error")
     self.dialog.topleft = 254, 50
     self.dialog.child = self.container
     self.widgetContainer.add_widget(self.dialog)
     
     buttonCancel = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "cancel_button.png"))
     buttonCancel.topleft = [400, 140]
     buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.__closeDialog)
     self.container.add_child(buttonCancel)
     
     labelAlert = GG.utils.LabelTransparent("Error: Usuario o password incorrectos.",GG.utils.STYLES["dialogFont"])
     labelAlert.topleft = 180, 80
     self.container.add_child(labelAlert)

     return self.dialog

  def __closeDialog (self):
    self.widgetContainer.remove_widget(self.dialog)
    self.dialog.destroy ()
    self.dialog = None
    self.__textFieldUsername.text = ""
    self.__textFieldPassword.text = ""

  def cancelLogin(self):
    sys.exit(0)

  def finishLogin(self):
    self.__screen.fill((0, 0, 0))
    self.__finish = True
  
  def autoLogin(self,user,passw):
    loginData = self.__parent.system.login(user,passw)
    if loginData[0] == True:
      return loginData[1]
    else:
      print loginData[1]
      sys.exit(0)

