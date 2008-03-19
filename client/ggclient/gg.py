import math
import os
import sys
import time
import signal
import pygame

from pygame.locals import *

from isoview_hud import *
from isoview_room import *
from isoview_item import *
from isoview_player import *

from hud import *
from room import *
from item import *
from player import *

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
      if event.type == KEYDOWN:
        if event.key == K_UP:
          subPlayer1.moveOne(1)
        if event.key == K_DOWN:
          subPlayer1.moveOne(2)
        if event.key == K_LEFT:
          subPlayer1.moveOne(3)
        if event.key == K_RIGHT:
          subPlayer1.moveOne(4)
        if event.key == K_ESCAPE:
          sys.exit(0)
      if event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        dest = self.isoviewRoom.findTile([x,y])
        if dest <> [-1, -1]:
          self.room.setPlayerDestination(0, [dest[0], 0, dest[1]])
          
  def start(self):
    """ Inicia el programa. Crea e inicializa subjects y observers y pone en \
    marcha el bucle principal.
    """
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SZ)
    pygame.display.set_caption('GenteGuada 0.01')

    hud = Hud("hud", 0, " ", HUD_SZ)
    self.room = Room("room1", 0, TILE_STONE)
    player1 = Player("player", 0, PLAYER_SPRITE1, CHAR_SZ, (2, 0, 2))
    item = Item("libro", 0, OBJ_BOOK_SPRITE1, [40, 40], (5, 0, 5))
    self.room.insertPlayer(player1)
    self.room.insertItem(item)

    isoViewHud = IsoViewHud("<observer Hud>")
    self.isoviewRoom = IsoViewRoom("<observer Room>")
    self.isoviewRoom.addModel(self.room)
    isoViewPlayer = IsoViewPlayer("<observer Player>")
    isoViewPlayer.addModel(player1)
    isoViewItem = IsoViewItem("<observer Item>")
    isoViewItem.addModel(item)
    self.isoviewRoom.insertPlayer(isoViewPlayer)
    self.isoviewRoom.insertItem(isoViewItem)

    isoViewHud.paintHud()

    timePassed = 0
    clock = pygame.time.Clock()

    while True:
      clock = pygame.time.Clock()
      timePassed = timePassed + clock.tick(30)
      timePassedSeconds = timePassed / 1000.0
      if timePassedSeconds >= 0.02:
        timePassed = 0
        self.room.tick()
        self.isoviewRoom.draw(screen)
      self.input(pygame.event.get()) 