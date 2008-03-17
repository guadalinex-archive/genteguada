import math
import os
import sys
import time
import signal
import pygame

from pygame.locals import *

from observer_hud import *
from observer_room import *
from observer_player import *

from subject_hud import *
from subject_room import *
from subject_player import *

#******************************************************************************

def input(events):

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
      destination = obsRoom.findTile([x,y])
      subRoom.setPlayerDestination("player",destination)
          
#******************************************************************************
  
pygame.init()
screen = pygame.display.set_mode(SCREEN_SZ)
pygame.display.set_caption('GenteGuada 0.01')

subRoom = SubjectRoom("room1", 0, TILE_STONE)
subPlayer1 = SubjectPlayer("player", 0, PLAYER_SPRITE1, CHAR_SZ, (2, 0, 2))
subRoom.insertPlayer(subPlayer1)

obsRoom = ObserverRoom("<observer Room>")
obsRoom.addSubject(subRoom)
observerPlayer = ObserverPlayer("<observer jugador>")
observerPlayer.addSubject(subPlayer1)
obsRoom.insertPlayer(observerPlayer)

timePassed = 0
clock = pygame.time.Clock()

while True:
  clock = pygame.time.Clock()
  timePassed = timePassed + clock.tick(30)
  timePassedSeconds = timePassed / 1000.0
  if timePassedSeconds >= 0.02:
    timePassed = 0
    subRoom.tick()
    obsRoom.draw(screen)
  input(pygame.event.get()) 
    
  