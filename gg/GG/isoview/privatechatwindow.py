# -*- coding: iso-8859-15 -*-

import pygame
import ocempgui.widgets
import GG.utils
import copy

class PrivateChatWindow:
  """ AvatarEditor class.
  Defines the Avatar Editor
  """

  def __init__(self, title, player):
    self.hide = False
    self.window = ocempgui.widgets.Window(title)
    self.window.topleft = 0, 0
    self.window.zOrder = 10000
    self.player = player
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

  def setScreenPosition(self, x, y):
    self.window.topleft = x, y  

  def getScreenPosition(self):
    return self.window.topleft

  def getSize(self):
    return self.container.width, self.container.height     

  def __paintBackground(self):
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/privateChatWindow.png")
    imgBackground = GG.utils.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0,0
    self.container.add_child(imgBackground)
    self.window.child = self.container
    
    labelChat = GG.utils.OcempLabel("Contactos", 280, GG.utils.STYLES["userName"])
    labelChat.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["userName"]))
    labelChat.topleft = 20, 20
    self.container.add_child(labelChat)
    
    labelContacts = GG.utils.OcempLabel("Chat", 280, GG.utils.STYLES["userName"])
    labelContacts.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["userName"]))
    labelContacts.topleft = 150, 20
    self.container.add_child(labelContacts)
    
  def __paintContactList(self):
    """ Paints the chat window on screen.
    """
    #from PIL import Image
    self.contactsArea = GG.utils.OcempImageContactList(130, 270, self.player.getAgenda())
    self.contactsArea.topleft = 20, 40
    self.contactsArea.connect_signal (ocempgui.widgets.Constants.SIG_SELECTCHANGED, self.__selectionChange)
    self.container.add_child(self.contactsArea)

  def __selectionChange(self):
    name = self.contactsArea.getSelectedName()
    if not name:
      self.selected = None  
      return
    if name.find(" ") > -1:
      name = name[0:name.find(" ")]
      self.contactsArea.restoreContactName()
    
    self.selected = self.player.getContact(name)
    self.clearChatArea()
    chat = self.selected.getChat()
    for line in chat:    
      self.__layoutTextArea.add_child(self.createChatMessage(self.sliceLine(line[1])))
      self.textArea.vscrollbar.value = self.textArea.vscrollbar.maximum

  def __paintDeleteButton(self):
    #deleteButton = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_HUD, "delcontact.png"), "Eliminar contacto", self.showTooltip, self.removeTooltip)
    deleteButton = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.HUD_PATH + "delcontact.png"), "Eliminar contacto", self.showTooltip, self.removeTooltip)
    deleteButton.topleft = 20, 315
    deleteButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.deleteContacts)
    self.container.add_child(deleteButton)

  def showTooltip(self, label):
    self.tooltipWindow = ocempgui.widgets.TooltipWindow (label)
    x, y = pygame.mouse.get_pos ()
    self.tooltipWindow.topleft = x + 8 - self.window.topleft[0], y - 5 - self.window.topleft[1]
    self.tooltipWindow.depth = 99
    self.tooltipWindow.zOrder = 30000
    self.container.add_child(self.tooltipWindow)
      
  def removeTooltip(self): 
    if self.tooltipWindow:
      self.container.remove_child(self.tooltipWindow)  
      self.tooltipWindow.destroy ()
      self.tooltipWindow = None

  def deleteContacts(self):
    if not self.selected:
      return    
    self.player.removeContact(self.selected.getPlayer())
    self.updateContactList()
    self.selected.getPlayer().removeContactRemote(self.player)
    self.selected = None
    self.clearChatArea()
    
  def updateContactList(self):
    self.contactsArea.setContacts(self.player.getAgendaData())
    
  def removeContactRemote(self, contact):
    self.player.removeContact(contact)
    self.__agenda = self.player.getAgenda()
    self.container.remove_child(self.contactsArea)
    self.selected = None
    self.__paintContactList()
    self.clearChatArea()
    
  def __paintChat(self):
    self.__textField = ocempgui.widgets.Entry()
    self.__textField.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["textFieldChat"]))
    self.__textField.border = 1
    self.__textField.topleft = 150, 320
    self.__textField.set_minimum_size(203, 20)
    self.container.add_child(self.__textField)

  def chatMessageEntered(self):
    if self.selected:
      text = self.selected.getPlayer().username + ": " + self.__textField.text
      self.selected.addChatLine(self.player, text)
      if not text.strip() == "" and self.contactsArea.getSelectedName():
        self.writeChatMessage(text)
        self.__textField.text = ""
    else:
      line = self.sliceLine("Seleccione un contacto para iniciar una conversacion")  
      self.__layoutTextArea.add_child(self.createChatMessage(line))
      self.textArea.vscrollbar.value = self.textArea.vscrollbar.maximum
      self.__textField.text = ""
  
  def __paintChatArea(self):
    self.textArea = ocempgui.widgets.ScrolledWindow(203, 270)
    self.textArea.set_scrolling(1)
    self.textArea.topleft = 150, 40
    self.__layoutTextArea= ocempgui.widgets.VFrame()
    self.__layoutTextArea.border = 0
    self.__layoutTextArea.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.textArea.child = self.__layoutTextArea
    self.container.add_child(self.textArea)
    
  def writeChatMessage(self, string):
    line = self.sliceLine(string)  
    self.selected.getPlayer().newPrivateChatReceived(line, self.player)
    self.__layoutTextArea.add_child(self.createChatMessage(line))
    self.textArea.vscrollbar.value = self.textArea.vscrollbar.maximum

  def incomingChatMessage(self, string, player):
    self.player.newChatForPlayer(string, player)
    if self.selected == None:
      self.contactsArea.addMessageHintForContact(player)
    elif self.selected.getPlayer().username == player.username:
      self.__layoutTextArea.add_child(self.createChatMessage(string))
      self.textArea.vscrollbar.value = self.textArea.vscrollbar.maximum
    else:
      self.contactsArea.addMessageHintForContact(player)

  def createChatMessage(self, string):
    hframe = ocempgui.widgets.HFrame()
    hframe.border = 0
    hframe.set_align(ocempgui.widgets.Constants.ALIGN_TOP) 
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.IMAGE_CHAT_MESSAGE)
    image = ocempgui.widgets.ImageLabel(imgPath)
    image.buttom = 0
    hframe.add_child(image)
    label = GG.utils.OcempLabelNotTransparent(string,300)
    hframe.add_child(label)
    return hframe

  def clearChatArea(self):
    children = copy.copy(self.__layoutTextArea.children)
    for child in children:
      self.__layoutTextArea.remove_child(child)
      child.destroy()

  def sliceLine(self, string):
    width = 20
    line = ""  
    cad = string
    while len(cad) > width:
      cad2aux = cad[0:width]
      blankPos = cad2aux.rfind(" ")
      if blankPos > 0:
        line = line + cad[0:blankPos] + "\n"     
        cad = cad[blankPos+1:]
      else:  
        line = line + cad[0:width] + "\n"     
        cad = cad[width:]  
    line = line + cad
    return line   

  def updateMaskPlayer(self, name, image):
    self.contactsArea.updateMaskPlayer(name, image)
    self.container.remove_child(self.contactsArea)
    self.__paintContactList()
