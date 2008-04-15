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
#import isoview_item
import isoview_player

import hud
import room
#import item
import player

"""
from isoview_hud import *
from isoview_room import *
from isoview_item import *
from isoview_player import *

from hud import *
from room import *
from item import *
from player import *
"""

class GG:
  """ Clase GG
  Clase principal del cliente. Maneja la entrada por teclado y ejecuta las \
  operaciones principales.
  """
    
  def __init__(self):
    """ Constructor de la clase.
    """
    pass

  def input(self, events):
    """ Maneja los eventos recibidos por teclado y raton.
    events: evento recibido por los dispositivos de entrada.
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
    """ Dispara una serie de metodos al detectar un evento de movimiento.
    event: datos del evento de movimiento.
    """
    self.isoviewRoom.newAction(event)
    #id=self.id, sprite=self.sprite, pActual=self.position, pDestin=self.destination, dir=self.state, state=0

  def clickOnTileEventFired(self, event):
    """ Dispara una serie de metodos al detectar un evento de clic en pantalla.
    event: datos del evento.
    """
    str1 = event.params['pl']
    cord0 = str(event.params['tg'][0])
    cord1 = str(event.params['tg'][1])
    cord2 = str(event.params['tg'][2])
    string = str1 + " hizo clic en la celda (" + cord0 + ", " + cord1 + ", " + cord2 + ")"
    self.printOnChat(string)
    #self.isoviewRoom.newAction(event)
    #id=self.id, sprite=self.sprite, pActual=self.position, pDestin=self.destination, dir=self.state, state=0
  
  def clickOnPlayerEventFired(self, event):
    """ Dispara una serie de metodos al detectar un evento de clic sobre otro jugador.
    event: datos del evento.
    """
    string = event.params['clicker'] + " hizo clic en " + event.params['pl'] + " de la habitacion " + event.params['room']
    self.printOnChat(string)
    
  def printOnChat(self, string):
    renderedText = utils.renderTextRect(string, self.textFont, self.textRect, utils.CHAT_COLOR_FONT, utils.CHAT_COLOR_BG, 0)
    self.screen.blit(renderedText, self.textRect.topleft)
    pygame.display.update()
    
  def start(self):
    """ Inicia el programa. Crea e inicializa subjects y observers y pone en \
    marcha el bucle principal.
    """
    pygame.init()
    self.screen = pygame.display.set_mode(utils.SCREEN_SZ)
    pygame.display.set_caption('GenteGuada 0.02')

    self.activeRoom = 0
    self.activePlayer = 0
    self.room = room.Room("Recibidor", self.activeRoom, utils.TILE_STONE, utils.BG_FULL)
    self.room.subscribeEvent('click on tile', self.clickOnTileEventFired)
    self.player1 = player.Player("Jugador Azul", self.activePlayer, utils.PLAYER_SPRITE1, utils.CHAR_SZ, [0, 0, 0])
    self.player2 = player.Player("Jugador Rojo", 1, utils.PLAYER_SPRITE2, utils.CHAR_SZ, [4, 0, 4])
    self.book1 = player.Player("Libro", 2, utils.OBJ_BOOK_SPRITE1, [50, 35], [6, 0, 4])
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
    #self.room.setBlockedTile([2, 0, 2])
    
    self.isoviewHud = isoview_hud.IsoViewHud("<observer Hud", self.screen)
    self.isoviewRoom = isoview_room.IsoViewRoom("<observer Room>", self.screen)
    self.isoviewRoom.addModel(self.room)
    self.isoViewPlayer = isoview_player.IsoViewPlayer("<observer Player>", 0, self.screen)
    self.isoViewPlayer.addModel(self.player1)
    self.isoViewPlayer.addModel(self.player2)
    self.isoViewPlayer.addModel(self.book1)
    self.isoviewRoom.insertIsoViewPlayer(self.isoViewPlayer)

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
      