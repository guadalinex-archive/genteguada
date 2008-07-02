import room_item
import GG.utils
import time
import GG.isoview.isoview_item

class GGMP3Lobby(room_item.GGRoomItem):
  """ GGMP3Lobby class.
  Defines a temporary pickable item behaviour.
  """
    
  def __init__(self, spriteName, topAnchor, anchor, spriteInventory, label, time, startRoom):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    anchor: image anchor on screen.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
    time: item's life time.
    startRoom: item's starting room.
    """
    room_item.GGRoomItem.__init__(self, spriteName, anchor, topAnchor)
    self.spriteInventory = spriteInventory
    self.label = label
    self.__startPosition = position
    self.__time = time*1000
    self.__startRoom = startRoom
    self.__startTime = 0
  
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['spriteInventory', 'label']
      
  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteInventory
  
  def getStartRoom(self):
    """ Returns the item's starting room.
    """
    return self.__startRoom
  
  def setPlayer(self, player):
    if player == None:
      self.__startTime = 0
    room_item.GGRoomItem.setPlayer(self, player)
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    if self.getRoom():
      return ["inventory"]
    else:
      return ["removeInventory"]
  
  def tick(self, now):
    """ Call for an update on item.
    """
    if self.getPlayer() == None and self.getLowerItem() == None and self.getRoom() == self.__startRoom \
        and self.getPosition() == self.__startPosition:  
      return
    if self.__startTime == 0:
      self.__startTime = now    
    if (now - self.__startTime) > self.__time: 
      if self.getPlayer() == None:
        # Esta en el suelo  
        if self.getLowerItem() == None:
          # No hay objetos debajo
          
          if self.getUpperItem() == None:
            # Ni arriba, esta solo en la celda
            if self.getRoom() != self.__startRoom: 
              # Colocado en una habitacion diferente
              self.clearRoom()
              self.setPosition(self.__startPosition)
              self.setRoom(self.__startRoom)
            else:
              # Colocado en la misma habitacion.
              self.setPosition(self.__startPosition)
              
          else:
            # Tiene objetos arriba
            self.getUpperItem().setPosition(self.getPosition())
            self.getUpperItem().setLowerItem(None)
            self.setUpperItem(None)
            if self.getRoom() != self.__startRoom: 
              # Colocado en una habitacion diferente
              self.clearRoom()
              self.setPosition(self.__startPosition)
              self.setRoom(self.__startRoom)
            else:
              # Colocado en la misma habitacion.
              self.setPosition(self.__startPosition)
          self.__startTime = 0
              
        else:
          # Si hay objetos debajo
          if self.getUpperItem() == None:
            # No hay objetos arriba, esta en la cima
            self.getLowerItem().setUpperItem(None)
            self.setLowerItem(None)
            if self.getRoom() != self.__startRoom: 
              # Colocado en una habitacion diferente
              self.clearRoom()
              self.setPosition(self.__startPosition)
              self.setRoom(self.__startRoom)
            else:
              # Colocado en la misma habitacion.
              self.setPosition(self.__startPosition)
            self.__startTime = 0
          else:
            # Y arriba
            low = self.getLowerItem()
            upp = self.getUpperItem()
            self.getLowerItem().setUpperItem(upp)
            self.getUpperItem().setLowerItem(low)
            self.setLowerItem(None)
            self.setUpperItem(None)
            if self.getRoom() != self.__startRoom: 
              # Colocado en una habitacion diferente
              self.clearRoom()
              self.setPosition(self.__startPosition)
              self.setRoom(self.__startRoom)
            else:
              # Colocado en la misma habitacion.
              self.setPosition(self.__startPosition)
            self.__startTime = 0
      else:
        # Esta en el inventario de un jugador      
        self.getPlayer().removeFromInventory(self)
        self.__startRoom.addItemFromInventory(self, self.__startPosition)
        self.__startTime = 0
    
  def timeLeft(self):
    """ Returns the item's time left.
    """
    if self.__time > self.__elapsedTime:
      return True
    else:
      return False
    
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    
  def isStackable(self):
    return True
