# -*- coding: iso-8859-15 -*-

import pygame
import ocempgui.widgets
import GG.utils
import os
import copy

class PrivateChatWindow:
  """ AvatarEditor class.
  Defines the Avatar Editor
  """

  def __init__(self, title, player):
    self.hide = False
    self.window = ocempgui.widgets.Window(title)
    self.window.topleft = 200, 200
    self.window.zOrder = 10000
    self.player = player
    self.agenda = player.getAgenda()
    self.contactsList = []
    for contact in self.agenda:
      self.contactsList.append(contact.getPlayer().username)
    #self.contactsList = ["pepe","juan","pepa"]
    self.selected = None
    self.draw()

  def draw(self):
    self.container = ocempgui.widgets.Box(373,372)
    self.__paintBackground()
    self.__paintContactList()
    self.__paintDeleteButton()
    self.__paintChat()
    self.__paintChatArea()
    return self.window

  def __paintBackground(self):
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/privateChatWindow.png")
    imgBackground = GG.utils.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0,0
    self.container.add_child(imgBackground)
    self.window.child = self.container
    
  def __paintContactList(self):
    """ Paints the chat window on screen.
    """
    from PIL import Image
    #self.contactsArea = GG.utils.OcempImageContactList(162, 290,self.contactsList)
    self.contactsArea = GG.utils.OcempImageContactList(162, 290,self.agenda)
    self.contactsArea.topleft = 10, 10
    self.contactsArea.connect_signal (ocempgui.widgets.Constants.SIG_SELECTCHANGED, self.__selectionChange)
    self.container.add_child(self.contactsArea)

  def __selectionChange(self):
    name = self.contactsArea.getSelectedName()
    self.selected = self.player.getContact(name)
    print self.selected
    print name
    self.clearChatArea()
    chat = self.selected.getChat()
    for line in chat:    
      self.__layoutTextArea.add_child(self.createChatMessage(line[1]))
      self.textArea.vscrollbar.value = self.textArea.vscrollbar.maximum

  def __paintDeleteButton(self):
    deleteButton = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_EDITOR_INTERFACE, "cancel_button.png"), "eliminar contacto", self.showTooltip, self.removeTooltip)
    deleteButton.topleft = 6, 315
    deleteButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.deleteContacts)
    self.container.add_child(deleteButton)

  def showTooltip(self, label):
    self.tooltipWindow = ocempgui.widgets.TooltipWindow (label)
    x, y = pygame.mouse.get_pos ()
    self.tooltipWindow.topleft = x + 8 - self.window.topleft[0], y - 5 - self.window.topleft[1]
    self.tooltipWindow.depth = 99 # Make it the topmost widget.
    self.tooltipWindow.zOrder = 30000
    self.container.add_child(self.tooltipWindow)
      
  def removeTooltip(self): 
    if self.tooltipWindow:
      self.container.remove_child(self.tooltipWindow)  
      self.tooltipWindow.destroy ()
      self.tooltipWindow = None

  def deleteContacts(self):
    #self.player.removeContact  
    print "a eliminar toca!!!"
    pass

  def __paintChat(self):
    self.__textField = ocempgui.widgets.Entry()
    self.__textField.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["textFieldChat"]))
    self.__textField.border = 1
    self.__textField.topleft = 160, 330
    self.__textField.set_minimum_size(200, 30)
    self.container.add_child(self.__textField)

  def chatMessageEntered(self):
    text = self.selected.getPlayer().username + ": " + self.__textField.text
    self.selected.addChatLine(self.player, text)
    if not text.strip() == "" and self.contactsArea.getSelectedName():
      self.writeChatMessage(text)
      self.__textField.text = ""
  
  def __paintChatArea(self):
    self.textArea = ocempgui.widgets.ScrolledWindow(162, 290)
    self.textArea.set_scrolling(1)
    self.textArea.topleft = 190, 10
    self.__layoutTextArea= ocempgui.widgets.VFrame()
    self.__layoutTextArea.border = 0
    self.__layoutTextArea.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.textArea.child = self.__layoutTextArea
    self.container.add_child(self.textArea)
    
  def writeChatMessage(self, string):
    self.__layoutTextArea.add_child(self.createChatMessage(string))
    self.textArea.vscrollbar.value = self.textArea.vscrollbar.maximum

  def createChatMessage(self, string):
    hframe = ocempgui.widgets.HFrame()
    hframe.border = 0
    hframe.set_align(ocempgui.widgets.Constants.ALIGN_TOP) 
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.IMAGE_CHAT_MESSAGE)
    image = ocempgui.widgets.ImageLabel(imgPath)
    image.buttom = 0
    hframe.add_child(image)
    label = GG.utils.OcempLabel(string,300)
    hframe.add_child(label)
    return hframe

  def clearChatArea(self):
    children = copy.copy(self.__layoutTextArea.children)
    for child in children:
      self.__layoutTextArea.remove_child(child)
      child.destroy()
