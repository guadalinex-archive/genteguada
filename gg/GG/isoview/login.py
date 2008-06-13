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
    
  def draw(self, user=None, passw=None):
    if user and passw:
      return self.autoLogin(user, passw)
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.LOGIN_SCREEN)
    img = pygame.sprite.Sprite()
    img = pygame.image.load(imgPath).convert_alpha()
    self.__screen.blit(img, (0, 0))
    pygame.display.flip()
   
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.__screen)
    
    framelogin = ocempgui.widgets.VFrame()
    framelogin.topleft = [200,200]

    table = ocempgui.widgets.Table(3,2)

    table.add_child(0,0,ocempgui.widgets.Label("Usuario"))
    self.__textFieldUsername = ocempgui.widgets.Entry()
    table.add_child(0,1,self.__textFieldUsername)

    table.add_child(1,0,ocempgui.widgets.Label("Password"))
    self.__textFieldPassword = ocempgui.widgets.Entry()
    self.__textFieldPassword.set_password(True)
    table.add_child(1,1,self.__textFieldPassword)
    
    buttonOk = ocempgui.widgets.Button("Aceptar")
    buttonOk.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.acceptLogin)
    table.add_child(2,0,buttonOk)
    buttonCancel = ocempgui.widgets.Button("Cancelar")
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.cancelLogin)
    table.add_child(2,1,buttonCancel)


    framelogin.add_child(table)

    
    self.widgetContainer.add_widget(framelogin)

    while not self.__finish:
      time.sleep(GG.utils.TICK_DELAY)
      events = pygame.event.get()
      for event in events:
        if event.type == QUIT:
          sys.exit(0)
      self.widgetContainer.distribute_events(*events)
    if self.__session:
      return self.__session
    self.cancelLogin()

  def acceptLogin(self):
    user = self.__textFieldUsername.text 
    passw = self.__textFieldPassword.text
    loginData = self.__parent.system.login(user,passw)
    if loginData[0] == True:
      self.__session = loginData[1]
      self.finishLogin()
    else:
      self.__showError(loginData[1])
  
  def __showError(self,errorText):
    buttons = [ocempgui.widgets.Button ("#OK")]
    results = [ocempgui.widgets.Constants.DLGRESULT_OK]
    self.dialog = ocempgui.widgets.GenericDialog ("Error", buttons, results)
    lbl = ocempgui.widgets.Label (errorText)
    self.dialog.content.add_child (lbl)
    self.dialog.connect_signal (ocempgui.widgets.Constants.SIG_DIALOGRESPONSE, self.__closeDialog, self.dialog, lbl)
    self.dialog.topleft = 100, 100
    self.dialog.depth = 1
    self.widgetContainer.add_widget(self.dialog)
    
  def __closeDialog (self,result, dialog, label):
    if result == ocempgui.widgets.Constants.DLGRESULT_OK:
      self.dialog.destroy ()

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

