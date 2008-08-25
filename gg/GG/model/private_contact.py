# -*- coding: utf-8 -*-

import ggmodel

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
