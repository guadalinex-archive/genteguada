from subject_item import *

#******************************************************************************
# CLASE SUB_PLAYER (subclase de SUB_ITEM)
# Subject de tipo Jugador

class SubjectPlayer(SubjectItem):
 
  def __init__(self, name, id, sprite, size, position):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.id = id
    self.state = "standing_down"
    self.stateFrame = 0
    
  def moveOne(self, dir):
    if self.stateFrame <> 0:
      pass
    else:
      if dir <> 0:
        self.stateFrame = 0
      if dir == 1 and self.position[2] > 0:
        self.state = "walking_up"  
      if dir == 2 and self.position[2] < (SCENE_SZ[1] - 1):
        self.state = "walking_down"  
      if dir == 3 and self.position[0] > 0:
        self.state = "walking_left"  
      if dir == 4 and self.position[0] < (SCENE_SZ[0] - 1):
        self.state = "walking_right"
  
  def getState(self):
    return self.state

  def getStateFrame(self):
    return self.stateFrame

  def getId(self):
    return self.id

  def getDir(self):
    if self.state == "standing_up" or self.state == "standing_down" or \
    self.state == "standing_left" or self.state == "standing_right":
      return 0
    if self.state == "walking_up":
      return 1
    if self.state == "walking_down":
      return 2
    if self.state == "walking_left":
       return 3
    if self.state == "walking_right":
      return 4

  def setDestination(self, destination):
    self.destination = destination

  def tick(self):
    if self.state == "walking_up" or self.state == "walking_down" or \
    self.state == "walking_left" or self.state == "walking_right":
      if self.stateFrame == (MAX_FRAMES - 1):
        pos = self.getPosition()
        if self.state == "walking_up":
          self.setPosition([pos[0], pos[1], pos[2] - 1])
        if self.state == "walking_down":
          self.setPosition([pos[0], pos[1], pos[2] + 1])
        if self.state == "walking_left":
          self.setPosition([pos[0] - 1, pos[1], pos[2]])  
        if self.state == "walking_right":
          self.setPosition([pos[0] + 1, pos[1], pos[2]])  
        self.state = "standing_down"
        self.stateFrame = 0
      else:
        self.stateFrame += 1
        
  def notify(self):
    self.notify_observers(self.state)