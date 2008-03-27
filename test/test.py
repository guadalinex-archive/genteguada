import sys
import pygame
import unittest

sys.path.append("../client")
sys.path.append("../common")

from ggclient.utils import *
import ggclient.player
import ggclient.isoview_player


class TestEventos(unittest.TestCase):
  
  def setUp(self):
    self.eventCount = 0
    self.lastEvent = None
  """
  def testRegistrar(self):
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SZ)
    pygame.display.set_caption('GenteGuada 0.01')
    player = ggclient.player.Player("player", 0, PLAYER_SPRITE1, CHAR_SZ, (2, 0, 2))
    isoViewPlayer = ggclient.isoview_player.IsoViewPlayer("<observer Player>", screen)
    isoViewPlayer.addModel(player)
    assert isoViewPlayer.modelList[0] == player, "achtung achtung"

  def testMover(self):
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SZ)
    pygame.display.set_caption('GenteGuada 0.01')
    player = ggclient.player.Player("player", 0, PLAYER_SPRITE1, CHAR_SZ, (2, 0, 2))
    print player.position
    player.moveOne(1)
    player.tick("walking_up")
    player.tick("walking_up")
    player.tick("walking_up")
    player.tick("walking_up")
    player.tick("walking_up")
    print player.position
    assert player.position[2] == 1, "achtung achtung"   
  """


    
  def testSimplestCase(self):                
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SZ)
    pygame.display.set_caption('GenteGuada 0.01')
    player = ggclient.player.Player("player", 0, PLAYER_SPRITE1, CHAR_SZ, (2, 0, 2))

    assert self.eventCount == 0
    assert self.lastEvent == None

    player.onEvent('destination', self.positionEventFired)

    player.setDestination(1, [2, 0, 1])

    assert self.eventCount == 1
    assert self.lastEvent.params['destination'] == [2, 0, 1]
    assert self.lastEvent.producer == player
    assert self.lastEvent.name == 'destination'


  def positionEventFired(self, event):
    self.eventCount += 1
    self.lastEvent = event


if __name__ == "__main__":
  unittest.main()

