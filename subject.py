from utils import *

#******************************************************************************
# CLASE SUBJECT
# Subject generico

class Subject:
  
  def __init__(self, name, id, sprite, size):
    self.name = name
    self.sprite = sprite
    self.size = size
    self.id = id
    self.observers = []
    
  def register(self, observer):
    self.observers.append(observer)
    
  def unregister(self, observer):
    self.observers.remove(observer)
    
  def getName(self):
    return self.name

  def getSprite(self):
    return self.sprite
  
  def getSize(self):
    return self.size
