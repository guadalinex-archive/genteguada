# -*- coding: iso-8859-15 -*-

import pygame
import ocempgui.widgets
import GG.utils

class myContactItem(ocempgui.widgets.components.FileListItem):
    
  def __init__(self, name, type):
    ocempgui.widgets.components.FileListItem.__init__(self, name, type)
    
  

class PrivateChatWindow:
  """ AvatarEditor class.
  Defines the Avatar Editor
  """

  def __init__(self,title):
    self.hide = False
    self.window = ocempgui.widgets.Window(title)
    self.window.topleft = 200, 200
    self.window.zOrder = 10000
    self.contactsList = ocempgui.widgets.components.ListItemCollection()
    prueba = myContactItem("pepe",1)
    self.contactsList.append(prueba)
    #self.window.opacity = 100
    
    self.draw()

  def draw(self):
    self.container = ocempgui.widgets.Box(373,372)
    #self.container.opacity = 100
    self.__paintBackground()
    self.paintChat()
    return self.window

  def __paintBackground(self):
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/privateChatWindow.png")
    imgBackground = GG.utils.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0,0
    self.container.add_child(imgBackground)
    self.window.child = self.container
    
  def paintChat(self):
    """ Paints the chat window on screen.
    """
    from PIL import Image
    self.contactsArea = ocempgui.widgets.ScrolledList(162, 264,self.contactsList)
    self.contactsArea.topleft = 10, 10
    self.container.add_child(self.contactsArea)
    
    
#    self.selectionmode = ocempgui.widgets.Constants.SELECTION_SINGLE
    
#    self.__layoutTextArea= ocempgui.widgets.VFrame()
#    self.__layoutTextArea.border = 0
#    self.__layoutTextArea.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
#    self.textArea.child = self.__layoutTextArea

    
#    self.item = ocempgui.widgets.HFrame()
#    self.item.border = 0
#    self.item.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
#    try: 
#      self.imguser = Image.open(GG.utils.PATH_PHOTO_MASK,"imgMaskUser.png")
#    except:
#      return 
#    size = 16,16
#    self.imguser.thumbnail(size, Image.ANTIALIAS)
#    self.container.add_child(self.imguser)

    
    #self.nameuser = GG.utils.OcempLabel('Eduardo', 16)
    #self.item.add_child(self.imguser)
    #self.item.add_child(self.nameuser)
    #self.textArea.items = self.item
    
#    listaux = ocempgui.widgets.components.ListItemCollection()
#    for i in xrange (5):
#        listaux.append(ocempgui.widgets.components.TextListItem ("Contacto no. %d" % i))
#    self.textArea.items = listaux
    
    
    

    
    