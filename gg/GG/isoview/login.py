import os
import pygame
import pygame.locals
import ocempgui.widgets
import GG.utils
import time

class Login:
    
  def __init__(self, screen):
    self.__screen = screen
    self.__textFieldUsername = None
    self.__textFieldPassword = None
    self.__frameTags = None
    self.__widgetContainer = ocempgui.widgets.Renderer()
    self.__widgetContainer.set_screen(self.__screen)
    self.__ok = 0
    
  def start(self):
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.LOGIN_SCREEN)
    img = pygame.sprite.Sprite()
    img = pygame.image.load(imgPath).convert_alpha()
    self.__screen.blit(img, (0, 0))
    pygame.display.flip()
      
    self.__textFieldUsername = ocempgui.widgets.Entry()
    self.__textFieldUsername.border = 1
    self.__textFieldUsername.topleft = GG.utils.LOGIN_USERNAME_OR[0], GG.utils.LOGIN_USERNAME_OR[1]
    self.__textFieldUsername.set_minimum_size(GG.utils.LOGIN_USERNAME_SZ[0], GG.utils.LOGIN_USERNAME_SZ[1])
    self.__widgetContainer.add_widget(self.__textFieldUsername)
    
    self.__textFieldPassword = ocempgui.widgets.Entry()
    self.__textFieldPassword.border = 1
    self.__textFieldPassword.topleft = GG.utils.LOGIN_PASSWORD_OR[0], GG.utils.LOGIN_PASSWORD_OR[1]
    self.__textFieldPassword.set_minimum_size(GG.utils.LOGIN_PASSWORD_SZ[0], GG.utils.LOGIN_PASSWORD_SZ[1])
    self.__widgetContainer.add_widget(self.__textFieldPassword)

    self.__frameTags = ocempgui.widgets.Frame.VFrame()
    self.__frameTags.set_border(0)
    self.__frameTags.topleft = GG.utils.LOGIN_OKBUTTON_OR
    okButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, "key.png"))
    okButton.border = 0
    #imgTag.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.paintCustomizeZone, pos)
    self.__frameTags.add_child(okButton)
    self.__widgetContainer.add_widget(self.__frameTags)

  def login(self):
    #time.sleep(4)
    return ["pepe", "1234"]
    
  def finish(self):
    self.__screen.fill((0, 0, 0))