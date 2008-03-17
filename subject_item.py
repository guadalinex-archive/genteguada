from subject import *

#******************************************************************************
# CLASE SUB_ITEM (subclase de SUBJECT)
# Subject que define un objeto generico

class SubjectItem(Subject):
  
  def __init__(self, name, id, sprite, size, position):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.id = id
    
  def getPosition(self):
    return self.position

  def setPosition(self, position):
    self.position = position