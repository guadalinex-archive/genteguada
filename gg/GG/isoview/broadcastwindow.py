# -*- coding: iso-8859-15 -*-

import os
import pygame
import ocempgui.widgets
import GG.utils
import copy
import guiobjects

class BroadcastWindow:
  """ BroadcastWindow class.
  Defines the broadcast window.
  """

  def __init__(self, title, player, hud):
    """ Class constructor.
    title: private chat window title.
    player: private chat window owner.
    """
    self.hide = False
    self.window = ocempgui.widgets.Window(title)
    self.window.topleft = 0, 0
    self.window.zOrder = 10000
    self.player = player
    self.hud = hud
    self.selected = None
    self.draw()

  def draw(self):
    """ Draws window components on screen.
    """  
    self.container = ocempgui.widgets.Box(303, 123)
    self.__paintBackground()
    self.__paintChat()
    self.__paintSendButton()
    return self.window

  def setScreenPosition(self, x, y):
    """ Sets a new screen position for the chat window.
    """  
    self.window.topleft = x, y  

  def getScreenPosition(self):
    """ Returns the window screen position.
    """  
    return self.window.topleft

  def getSize(self):
    """ Returns the window size
    """  
    return self.container.width, self.container.height     

  def __paintBackground(self):
    """ Paints the window background.
    """  
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/broadcastWIndow.png")
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0,0
    self.container.add_child(imgBackground)
    self.window.child = self.container
    
    labelChat = guiobjects.OcempLabel("Mensaje", guiobjects.STYLES["userName"])
    labelChat.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["userName"]))
    #labelChat.topleft = 20, 20
    labelChat.topleft = 115, 10
    self.container.add_child(labelChat)
      
  def __paintChat(self):
    """ Paints the chat area.
    """  
    self.__textField = guiobjects.OcempEditLine()
    self.__textField.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["textFieldChat"]))
    self.__textField.border = 1
    self.__textField.topleft = 30, 50
    self.__textField.set_minimum_size(240, 20)
    self.container.add_child(self.__textField)  
    
  def __paintSendButton(self):
    """ Paints the send broadcast message button.
    """  
    #deleteButton = GG.utils.OcempImageButtonTransparent(os.path.join(GG.utils.PATH_HUD, "delcontact.png"), "Eliminar contacto", self.showTooltip, self.removeTooltip)
    sendButton = guiobjects.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(os.path.join(GG.utils.HUD_PATH, "tiny_ok_button.png")), "Enviar mensaje de sistema", self.showTooltip, self.removeTooltip)
    sendButton.topleft = 120, 80
    sendButton.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.sendBroadcast)
    self.container.add_child(sendButton)

  def sendBroadcast(self):
    """ Sends a broadcast message.
    """ 
    self.hud.newBroadcastMessage(self.__textField.text)
    self.__textField.text = ""

  def showTooltip(self, label):
    """ Show a button's tooltip.
    label: tooltip label.
    """  
    self.tooltipWindow = ocempgui.widgets.TooltipWindow (unicode(label))
    x, y = pygame.mouse.get_pos ()
    self.tooltipWindow.topleft = x + 8 - self.window.topleft[0], y - 5 - self.window.topleft[1]
    self.tooltipWindow.depth = 99
    self.tooltipWindow.zOrder = 30000
    self.container.add_child(self.tooltipWindow)
      
  def removeTooltip(self):
    """ Removes the tooltip from screen.
    """   
    if self.tooltipWindow:
      self.container.remove_child(self.tooltipWindow)  
      self.tooltipWindow.destroy ()
      self.tooltipWindow = None
