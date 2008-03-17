from subject import *

#******************************************************************************
# CLASE SUB_ROOM (subclase de SUBJECT)
# Subject de tipo habitacion. Incluye informacion del suelo

class SubjectRoom(Subject):

  def __init__(self, name, id, sprite):
    self.name = name
    self.id = id
    self.sprite = sprite
    self.observers = []
    self.players = []
    self.objects = []
    
  def insertFloor(self, floor):
    self.floor = floor

  def insertPlayer(self, player):
    self.players.append(player)
    
  def insertObject(self, object):
    self.objects.append(object)
    
  def setPlayerDestination(self, player, destination):  
    for ind in range(self.players.__len__()):
      if self.players[ind].getId() == player:
        self.player[ind].setDestination(destination)
    
  def notify(self):
    self.notify_observers(id)
    for player in self.players:
      player.notify()  
  
  def tick(self):
    for player in self.players:
      player.tick()  