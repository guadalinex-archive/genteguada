# -*- coding: utf-8 -*-

import GG.utils
import guiobjects
import ocempgui.widgets
import os

ADMIN_ACTIONS_BACKGROUND = os.path.join(GG.utils.HUD_PATH, "adminActions.png")
TINY_OK_IMAGE = os.path.join(GG.utils.HUD_PATH, "tiny_ok_button.png")
TINY_CANCEL_IMAGE = os.path.join(GG.utils.HUD_PATH, "tiny_cancel_button.png")

class AuxWindow:
  
  def __init__(self, hud):
    self.hide = True
    self.window = None
    self.hud = hud
    self.draw()

  def draw(self):
    pass

  def showOrHide(self):
    if self.hide:
      self.hud.addSprite(self.window)
      self.hud.widgetContainer.add_widget(self.window)
    else:
      self.hud.removeSprite(self.window)
      self.hud.widgetContainer.remove_widget(self.window)
      self.removeTooltip()
      self.hud.itemUnselected()
      self.hud.dropActionsItembuttons()
    self.hide = not self.hide

  def showTooltip(self, label):
    self.hud.showTooltip(label)
  
  def removeTooltip(self):
    self.hud.removeTooltip()

  def accept(self):
    pass

class TeleportWindow(AuxWindow):

  def __init__(self, hud):
    self.title = "Escoja destino"
    self.tooltipLabel = "Teleportar"
    self.listItems = hud.getModel().getRoomLabels()
    AuxWindow.__init__(self, hud)

  def draw(self):
    self.window = ocempgui.widgets.Box(150, 300)
    self.window.topleft = [GG.utils.SCREEN_SZ[0] - 151, 129]
    filePath =  GG.genteguada.GenteGuada.getInstance().getDataPath(ADMIN_ACTIONS_BACKGROUND)
    self.window.set_style(ocempgui.widgets.WidgetStyle(guiobjects.STYLES["buttonTopBar"]))
    imgBackground = guiobjects.OcempImageMapTransparent(filePath)
    imgBackground.topleft = 0, 0
    self.window.add_child(imgBackground)
    titleLabel = guiobjects.OcempLabel(self.title.decode("utf-8"), guiobjects.STYLES["teleportLabel"])
    titleLabel.topleft = 4, 0
    self.window.add_child(titleLabel)
    self.__roomLabels = guiobjects.OcempImageObjectList(110, 205, self.listItems)
    self.__roomLabels.topleft = 20, 40
    self.window.add_child(self.__roomLabels) 
    okButton = guiobjects.createButton(TINY_OK_IMAGE, [10, 262], [self.tooltipLabel, self.showTooltip, self.removeTooltip], self.accept)
    self.window.add_child(okButton)
    cancelButton = guiobjects.createButton(TINY_CANCEL_IMAGE, [80, 262], ["Cerrar menu", self.showTooltip, self.removeTooltip], self.showOrHide)
    self.window.add_child(cancelButton)
    self.window.zOrder = 10000

  def accept(self):
    roomLabel = self.__roomLabels.getSelectedName()
    self.showOrHide()
    self.hud.applyTeleport(roomLabel)


class DeleteRoomWindow(TeleportWindow):

  def __init__(self, hud):
    TeleportWindow.__init__(self, hud)

  def draw(self):
    self.title = "Eliminar habitación"
    self.tooltipLabel = "Eliminar habitación"
    TeleportWindow.draw(self)

  def accept(self):
    roomLabel = self.__roomLabels.getSelectedName()
    self.showOrHide()
    self.hud.applyDeleteRoom(roomLabel)

class KickPlayerWindow(TeleportWindow):

  def __init__(self, hud):
    TeleportWindow.__init__(self, hud)

  def draw(self):
    self.title = "Escaja jugador"
    self.tooltipLabel = "Expulsar jugador"
    self.listItems = self.hud.getModel().getPlayersList()
    TeleportWindow.draw(self)

  def accept(self):
    playerLabel = self.__roomLabels.getSelectedName()
    self.showOrHide()
    self.hud.applyKickPlayer(playerLabel)
