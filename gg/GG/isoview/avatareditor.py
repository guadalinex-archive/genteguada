import os
import sys
import time
import ocempgui.widgets
import GG.utils
import pygame
import pygame.locals



class AvatarEditor:
  """ AvatarEditor class.
  Defines the Avatar Editor
  """

  def __init__(self):
    """ Class constructor.
    """
    print "Iniciando Avatar Editor"
    #Iniciar las ventanas pygame
    pygame.init()
    #self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ,pygame.HWSURFACE|pygame.FULLSCREEN,0)
    self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ)
    pygame.display.set_caption("DEMO AVATAR GENERATOR")
    
    self.activeWidget = []
    self.activeOption = 0
    self.draw()
    #Creamos el Renderer
    while True:
      time.sleep(0.4)
      self.input(pygame.event.get())

  def paintScreen(self):
    """Paint the Avatar Editor background on screen.
    """
    print "Pinta la pantalla"
    #background = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
    #self.screen.fill(GG.utils.GUADALINEX_BLUE, background)
    
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.BACKGROUNDLEFT)
    self.backgroundLeftImage = pygame.image.load(imgPath)
    self.screen.blit(self.backgroundLeftImage, (0,0))
    
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.BACKGROUNDMIDDLE)
    self.backgroundMiddleImage = pygame.image.load(imgPath)
    self.screen.blit(self.backgroundMiddleImage, (288,0))
    
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.BACKGROUNDRIGHT)
    self.backgroundRightImage = pygame.image.load(imgPath)
    self.screen.blit(self.backgroundRightImage, (385,0))
    
    pygame.display.update()
    
    #customizeZone = pygame.Rect(0, 0, 386, 768)
    #self.screen.fill((110,171,234), customizeZone)
    

    
  def paintAvatar(self):
    """Paint the Composite Avatar Zone.
    """
    print "Pinta el avatar"
    imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_DUMMY)
    dummyImage = pygame.image.load(imgPath)
    self.screen.blit(dummyImage, (528,114))
    pygame.display.update()

    
  def paintTags(self):
    """Paint the Tags Zone.
    """
    print "Pinta las pestanas"
    
    for pos in range(len(GG.utils.TAGS)):
      #img = pygame.image.load(os.path.join(GG.utils.DATA_PATH, GG.utils.TAGS[pos])).convert_alpha()
      imgTag = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.TAGS[pos]))
      #print dir(imgTag)
      imgTag.padding = 0
      imgTag.border = 0
      imgTag.border = ocempgui.widgets.Constants.BORDER_NONE
      imgTag.topleft = [288, GG.utils.TAG_OFFSET*pos]
      print imgTag.topleft
      imgTag.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.paintCustomizeZone, pos)
      self.renderer.add_widget(imgTag)
    
  def paintCustomizeZone(self,idTag):
    """Paint the Customize Zone.
    """
    print "Pinta la zona de personalizacion"
    if idTag == 0:
      maleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_BTN))
      maleButton.border = 0
      maleButton.padding = 0
      maleButton.topleft = [73, 191]
      maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "male")
      self.renderer.add_widget(maleButton)
      self.activeWidget.append(maleButton)
      
      femaleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_BTN))
      femaleButton.border = 0
      femaleButton.padding = 0
      femaleButton.topleft = [73, 441]
      femaleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "female")
      self.renderer.add_widget(femaleButton)
      self.activeWidget.append(femaleButton)
    else:
      self.screen.blit(self.backgroundLeftImage, (0,0))
      for widget in self.activeWidget:
        self.renderer.remove_widget(widget)

  def paintGenderFrame(self):
    maleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_BTN))
    maleButton.border = 0
    maleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "male")
    femaleButton = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_BTN))
    femaleButton.border = 0
    femaleButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.updateGender, "female")
    
  def updateGender(self, gender):
    """ Update the Avatar Composite Zone with the appropiate gender.
    """
    if gender == "male":
      print "genero actualizado"
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.MALE_DUMMY)
    elif gender == "female":
      imgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.FEMALE_DUMMY)
    dummyImage = pygame.image.load(imgPath)
    self.screen.blit(self.backgroundRightImage, (285,0))
    self.screen.blit(dummyImage, (528,114))
    pygame.display.update()
    
  def draw(self):
    self.paintScreen()
    self.paintAvatar()
    self.renderer = ocempgui.widgets.Renderer()
    self.renderer.set_screen(self.screen)
    self.paintTags()
    self.paintCustomizeZone(self.activeOption)
    
  def input(self,events):
    for event in events:
      if event.type == pygame.locals.QUIT:
        sys.exit(0)
    self.renderer.distribute_events(*events)



if __name__=="__main__":
  AvatarEditor()
