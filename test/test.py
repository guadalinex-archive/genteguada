import sys
import pygame
import unittest

sys.path.append("../client")
sys.path.append("../common")

from ggclient.utils import *
import ggclient.room
import ggclient.player
import ggclient.isoview_room
import ggclient.isoview_player


class TestEventos(unittest.TestCase):
  
  def setUp(self):
    self.name = None
    self.eventCount = 0
    self.lastEvent = None
 
  def testCreateRoom(self):
    room = ggclient.room.Room("room1", 0, TILE_STONE)
    assert room.id == 0
  
  def testSetDestination(self):
    player = ggclient.player.Player("player", 0, PLAYER_SPRITE1, CHAR_SZ, (2, 0, 2))
    player.onEvent('destination', self.positionEventFired)
    player.setDestination(1, [2, 0, 1])
    assert self.eventCount == 1
    assert self.lastEvent.params['destination'] == [2, 0, 1]
    assert self.lastEvent.producer == player
    assert self.lastEvent.name == 'destinationte'

  def testDeleteEventByType(self):
    player = ggclient.player.Player("player", 0, PLAYER_SPRITE1, CHAR_SZ, (2, 0, 2))
    assert self.eventCount == 0
    assert self.lastEvent == None
    player.onEvent('destination', self.positionEventFired)
    player.setDestination(1, [2, 0, 1])
    assert self.eventCount == 1
    assert self.lastEvent.params['destination'] == [2, 0, 1]
    assert self.lastEvent.producer == player
    assert self.lastEvent.name == 'destination'
    player.deleteEvent('destination')
    assert len(player.events) == 0
    
  def testDeleteAllEvents(self):
    player = ggclient.player.Player("player", 0, PLAYER_SPRITE1, CHAR_SZ, (2, 0, 2))
    assert self.eventCount == 0
    assert self.lastEvent == None
    player.onEvent('destination', self.positionEventFired)
    player.setDestination(1, [2, 0, 1])
    assert self.eventCount == 1
    assert self.lastEvent.params['destination'] == [2, 0, 1]
    assert self.lastEvent.producer == player
    assert self.lastEvent.name == 'destination'
    player.onEvent('change name', self.positionEventFired)
    player.setName("player")
    assert self.eventCount == 2
    assert self.lastEvent.params['name'] == "player"
    assert self.lastEvent.producer == player
    assert self.lastEvent.name == 'change name'
    player.deleteEvent()
    assert len(player.events) == 0
  
  def testDeleteEventSingle(self):
    player1 = ggclient.player.Player("player1", 0, PLAYER_SPRITE1, CHAR_SZ, (2, 0, 2))
    player2 = ggclient.player.Player("player2", 0, PLAYER_SPRITE1, CHAR_SZ, (4, 0, 4))
    assert self.eventCount == 0
    assert self.lastEvent == None
    player1.onEvent('destination', self.positionEventFired)
    player2.onEvent('change name', self.nameEventFired)
    player1.setDestination(1, [2, 0, 1])
    assert self.eventCount == 1
    assert self.name == None
    assert self.lastEvent.params['destination'] == [2, 0, 1]
    assert self.lastEvent.producer == player1
    assert self.lastEvent.name == 'destination'
    player2.setName("player2")
    assert self.eventCount == 2
    assert self.name == "player2"
    self.name = None
    player2.deleteEvent()
    player1.deleteEvent("change name")
    assert len(player2.events) == 0
    assert len(player1.events) == 1
    player2.setName("player2")
    assert self.name == None
    
  def positionEventFired(self, event):
    self.eventCount += 1
    self.lastEvent = event

  def nameEventFired(self, event):
    self.eventCount += 1
    self.lastEvent = event
    self.name = event.params['name']

if __name__ == "__main__":
  test = unittest.main()
