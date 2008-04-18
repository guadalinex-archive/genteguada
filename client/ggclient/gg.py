import math
import os
import sys
import time
import signal
import pygame
import time
import string
    
from pygame.locals import *

import utils

import isoview_hud
import isoview_room
import isoview_player

import hud
import room
import player
import ggsystem

class GG:
  """ GG Class
  Main client class. Handles keyboard input and executes the main operations.
  """
    
  def __init__(self):
    """ Class constructor.
    """
    pass

  def input(self, events):
    """ Handles the events produced by mouse and keyboard input.
    events: input generated events. 
    """
    for event in events:
      if event.type == QUIT: 
        sys.exit(0)
      if event.type == KEYDOWN and event.key == K_ESCAPE:
        sys.exit(0)
      if event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        dest = self.isoviewRoom.findTile([x,y])
        if dest <> [-1, -1]:
          self.ggsystem.getRoom(self.activeRoom).clickedByPlayer(self.activePlayer, [dest[0], 0, dest[1]])
          #self.room.clickedByPlayer(self.activePlayer, [dest[0], 0, dest[1]])

  def startMovementEventFired(self, event):
    """ Starts some methods after receiving a movement event.
    event: movement event data.
    """
    self.isoviewRoom.newAction(event)
    #id=self.id, sprite=self.sprite, pActual=self.position, pDestin=self.destination, dir=self.state, state=0

  def clickOnTileEventFired(self, event):
    """ Starts some methods after receiving a screen click event.
    event: movement event data.
    """
    str1 = event.params['pl']
    cord0 = str(event.params['tg'][0])
    cord1 = str(event.params['tg'][1])
    cord2 = str(event.params['tg'][2])
    string = str1 + " clicked on tile (" + cord0 + ", " + cord1 + ", " + cord2 + ")"
    self.printOnChat(string)
    #self.isoviewRoom.newAction(event)
    #id=self.id, sprite=self.sprite, pActual=self.position, pDestin=self.destination, dir=self.state, state=0
  
  def clickOnPlayerEventFired(self, event):
    """ Starts some methods after receiving a clicked player event.
    event: movement event data.
    """
    string = event.params['clicker'] + " clicked on " + event.params['pl'] + " on room " + event.params['room']
    self.printOnChat(string)
    
  def printOnChat(self, string):
    """ Prints a string on the HUD chat window.
    string: the info that will be printed on screen.
    """
    renderedText = utils.renderTextRect(string, self.textFont, self.textRect, utils.CHAT_COLOR_FONT, utils.CHAT_COLOR_BG, 0)
    self.screen.blit(renderedText, self.textRect.topleft)
    pygame.display.update()
    
  def start(self):
    """ Begins the program. Creates models and views, and starts the main loop.
    """
    # Initializing screen handlers & attributes
    pygame.init()
    self.screen = pygame.display.set_mode(utils.SCREEN_SZ)
    pygame.display.set_caption(utils.VERSION)
    self.activeRoom = 0
    self.activePlayer = 0
    self.textFont = pygame.font.Font(None, 22)
    self.textRect = pygame.Rect((utils.CHAT_OR[0], utils.CHAT_OR[1], utils.CHAT_SZ[0], utils.CHAT_SZ[1]))
    
    # Creating Models
    self.hud = hud.Hud()
    self.ggsystem = ggsystem.GGSystem()
    self.ggsystem.createRoom("Lobby", 0, utils.TILE_STONE, utils.BG_FULL)
    self.ggsystem.createPlayer("Blue Player", 0, utils.PLAYER_SPRITE1, utils.CHAR_SZ, [0, 0, 0], [utils.CHAR_SZ[0], utils.CHAR_SZ[1]/4], "blueplayer", "1234")
    self.ggsystem.createPlayer("Red Player", 1, utils.PLAYER_SPRITE2, utils.CHAR_SZ, [4, 0, 4], [utils.CHAR_SZ[0], utils.CHAR_SZ[1]/4], "redplayer", "1234")
    self.ggsystem.createPlayer("Book", 2, utils.OBJ_BOOK_SPRITE1, [50, 35], [6, 0, 4], [58, -15], None, None)
    
    # Subscribing models to events
    self.ggsystem.getRoom(0).subscribeEvent('click on tile', self.clickOnTileEventFired)
    self.ggsystem.getPlayer(0).subscribeEvent('position', self.startMovementEventFired)
    self.ggsystem.getPlayer(0).subscribeEvent('destination', self.startMovementEventFired)
    self.ggsystem.getPlayer(0).subscribeEvent('click on player', self.clickOnPlayerEventFired)
    self.ggsystem.getPlayer(1).subscribeEvent('position', self.startMovementEventFired)
    self.ggsystem.getPlayer(1).subscribeEvent('destination', self.startMovementEventFired)
    self.ggsystem.getPlayer(1).subscribeEvent('click on player', self.clickOnPlayerEventFired)
    self.ggsystem.getPlayer(2).subscribeEvent('click on player', self.clickOnPlayerEventFired)
    
    # Adding players to active room
    self.ggsystem.insertPlayerIntoRoom(0, 0)
    self.ggsystem.insertPlayerIntoRoom(1, 0)
    self.ggsystem.insertPlayerIntoRoom(2, 0)
    
    # Creating views with associated models
    self.isoviewHud = isoview_hud.IsoViewHud("<observer Hud", self.screen, self.hud)
    self.isoviewRoom = isoview_room.IsoViewRoom("<observer Room>", self.screen, self.ggsystem.getRoom(0))
    self.isoViewPlayer1 = isoview_player.IsoViewPlayer("<Blue Player observer>", 0, self.screen, self.ggsystem.getPlayer(0))
    self.isoViewPlayer2 = isoview_player.IsoViewPlayer("<Red Player observer>", 0, self.screen, self.ggsystem.getPlayer(1))
    self.isoViewPlayer3 = isoview_player.IsoViewPlayer("<Book observer>", 0, self.screen, self.ggsystem.getPlayer(2))

    # Adding model views to active room view
    self.isoviewRoom.insertIsoViewPlayer(self.isoViewPlayer1)
    self.isoviewRoom.insertIsoViewPlayer(self.isoViewPlayer2)
    self.isoviewRoom.insertIsoViewPlayer(self.isoViewPlayer3)

    # Drawing interface & game zone for the first time
    self.isoviewRoom.drawFirst()
    self.isoviewHud.paint()
    pygame.display.update()
    
    # Main loop
    while True:
      time.sleep(utils.TICK_DELAY)
      self.ggsystem.tick()
      self.input(pygame.event.get())
      