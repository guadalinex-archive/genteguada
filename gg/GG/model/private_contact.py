# -*- coding: utf-8 -*-

import ggmodel
import os
import GG.utils
import ggsystem

class PrivateContact(ggmodel.GGModel):
  """ PrivateContact class.
  Defines a private contact.
  """
  
  def __init__(self, player):
    """ Class constructor.
    player: contact.
    """  
    ggmodel.GGModel.__init__(self)
    self.__player = player
    self.__chat = []

  def getPlayerObject(self):
    return ggsystem.GGSystem.getInstance().getPlayerConnected(self.__player)

  def getPlayer(self):
    """ Returns the contact.
    """  
    return self.__player

  def getChat(self):
    """ Returns the chat log.
    """  
    return self.__chat

  def addChatLine(self, player, line):
    """ Adds a new chat message from a player.
    player: message emitter.
    line: chat message.
    """  
    self.__chat.append([player, line])

  def clearChat(self):
    """ Clears the chat log.
    """  
    self.__chat = []

  def getImageLabel(self):
    """ Returns the player's mask filename.
    """  
    if os.path.isfile(os.path.join(GG.utils.DATA_PATH, GG.utils.MASKS_DIR, self.__player + ".png")):
      return os.path.join(GG.utils.MASKS_DIR, self.__player+".png")
    else:
      return os.path.join(GG.utils.EDITOR, "masko.png")

