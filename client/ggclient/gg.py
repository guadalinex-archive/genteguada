import math
import os
import sys
import time
import signal
import pygame
import time
    
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
          self.room.setPlayerDestination(0, [dest[0], 0, dest[1]])

  def startMovementEventFired(self, event):
    """ Dispara una serie de metodos al detectar un evento de movimiento.
    event: datos del evento de movimiento.
    """
    self.isoviewRoom.newAction(event)
    #id=self.id, sprite=self.sprite, pActual=self.position, pDestin=self.destination, dir=self.state, state=0

  def start(self):
    """ Inicia el programa. Crea e inicializa subjects y observers y pone en \
    marcha el bucle principal.
    """
    pygame.init()
    screen = pygame.display.set_mode(utils.SCREEN_SZ)
    pygame.display.set_caption('GenteGuada 0.02')

    self.room = room.Room("room1", 0, utils.TILE_STONE, utils.BG_FULL)
    self.player1 = player.Player("player", 0, utils.PLAYER_SPRITE1, utils.CHAR_SZ, (0, 0, 0))
    self.player1.onEvent('position', self.startMovementEventFired)
    self.player1.onEvent('destination', self.startMovementEventFired)
    self.room.insertPlayer(self.player1)
    self.room.setBlockedTile([2, 0, 2])
    
    self.isoviewRoom = isoview_room.IsoViewRoom("<observer Room>")
    self.isoviewRoom.addModel(self.room)
    self.isoViewPlayer = isoview_player.IsoViewPlayer("<observer Player>", 0, screen)
    self.isoViewPlayer.addModel(self.player1)
    self.isoviewRoom.insertIsoViewPlayer(self.isoViewPlayer)

    self.isoviewRoom.drawFirst(screen)
    pygame.display.update()

    while True:
      time.sleep(utils.TICK_DELAY)
      self.room.tick()
      self.input(pygame.event.get()) 