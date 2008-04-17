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
          self.room.clickedByPlayer(self.activePlayer, [dest[0], 0, dest[1]])

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
    pygame.init()
    self.screen = pygame.display.set_mode(utils.SCREEN_SZ)
    pygame.display.set_caption(utils.VERSION)

    self.activeRoom = 0
    self.activePlayer = 0
    
    self.hud = hud.Hud()
    self.room = room.Room("Lobby", self.activeRoom, utils.TILE_STONE, utils.BG_FULL)
    self.room.subscribeEvent('click on tile', self.clickOnTileEventFired)
    self.player1 = player.Player("Blue Player", 0, utils.PLAYER_SPRITE1, utils.CHAR_SZ, [0, 0, 0], [utils.CHAR_SZ[0], utils.CHAR_SZ[1]/4])
    self.player2 = player.Player("Red Player", 1, utils.PLAYER_SPRITE2, utils.CHAR_SZ, [4, 0, 4], [utils.CHAR_SZ[0], utils.CHAR_SZ[1]/4])
    self.book1 = player.Player("Book", 2, utils.OBJ_BOOK_SPRITE1, [50, 35], [6, 0, 4], [58, -15])
    self.player1.subscribeEvent('position', self.startMovementEventFired)
    self.player1.subscribeEvent('destination', self.startMovementEventFired)
    self.player1.subscribeEvent('click on player', self.clickOnPlayerEventFired)
    self.player2.subscribeEvent('position', self.startMovementEventFired)
    self.player2.subscribeEvent('destination', self.startMovementEventFired)
    self.player2.subscribeEvent('click on player', self.clickOnPlayerEventFired)
    self.book1.subscribeEvent('click on player', self.clickOnPlayerEventFired)
    
    self.room.insertPlayer(self.player1)
    self.room.insertPlayer(self.player2)
    self.room.insertPlayer(self.book1)
    
    self.isoviewHud = isoview_hud.IsoViewHud("<observer Hud", self.screen, self.hud)
    self.isoviewRoom = isoview_room.IsoViewRoom("<observer Room>", self.screen, self.room)
    self.isoViewPlayer1 = isoview_player.IsoViewPlayer("<Blue Player observer>", 0, self.screen, self.player1)
    self.isoViewPlayer2 = isoview_player.IsoViewPlayer("<Red Player observer>", 0, self.screen, self.player2)
    self.isoViewPlayer3 = isoview_player.IsoViewPlayer("<Book observer>", 0, self.screen, self.book1)
    
    self.isoviewRoom.insertIsoViewPlayer(self.isoViewPlayer1)
    self.isoviewRoom.insertIsoViewPlayer(self.isoViewPlayer2)
    self.isoviewRoom.insertIsoViewPlayer(self.isoViewPlayer3)

    self.textFont = pygame.font.Font(None, 22)
    self.textRect = pygame.Rect((utils.CHAT_OR[0], utils.CHAT_OR[1], utils.CHAT_SZ[0], utils.CHAT_SZ[1]))
    
    self.isoviewRoom.drawFirst()
    self.isoviewHud.paint()
    pygame.display.update()
    
    insertado = 0
    accTime = 0
    clock = pygame.time.Clock()
    
    while True:
      """
      time.sleep(utils.TICK_DELAY)
      accTime = accTime + clock.tick(30)
      if accTime/1000.0 >= 2 and insertado == 0:
        accTime = 0
        self.player3 = player.Player("Jugador Azul2", self.activePlayer, utils.PLAYER_SPRITE1, utils.CHAR_SZ, [5, 0, 3])
        self.player3.subscribeEvent('click on player', self.clickOnPlayerEventFired)
        self.room.insertPlayer(self.player2)
        self.isoViewPlayer.addModel(self.player2)
        self.isoviewRoom.insertIsoViewPlayer(self.isoViewPlayer)
        self.isoviewRoom.drawFirst()
        pygame.display.update()
        self.printOnChat("Jugador Azul2 insertado")
        insertado = 1
      """  
      self.room.tick()
      self.input(pygame.event.get())
      