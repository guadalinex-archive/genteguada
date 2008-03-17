from subject_item import *

#******************************************************************************
# CLASE SUB_OBJECT (subclase de SUB_ITEM)
# Subject de tipo objeto no jugador

class SubjectObject(SubjectItem):
  
  def __init__(self, name, id, sprite, size, position):
    self.observers = []
    self.name = name
    self.sprite = sprite
    self.size = size
    self.position = position
    self.id = id
