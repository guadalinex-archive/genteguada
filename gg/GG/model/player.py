import item
import GG.isoview.isoview_player
import dMVC.model
#import ggcommon.eventos

class GGPlayer(item.GGItem):
  """ Player class.
  Defines an object behaviour, either if it is a player object or a non-player object.
  """
 
  def __init__(self, sprite, size, position, offset, username, password):
    """ Class builder.
    sprite: sprite used to paint the player.
    size: player sprite size.
    position: player position.
    """
    item.GGItem.__init__(self, sprite, size, position, offset)
    self.__heading = "standing_down"
    self.__stateFrame = 0
    self.__destination = position
    self.__currentRoom = None
    self.__username = username
    self.__password = password
    self.__visited = []

  def getCurrentRoom(self):
    return self.__currentRoom
  
  def setCurrentRoom(self, room):
    self.__currentRoom = room
  
  def checkUser(self, username, password):
    if self.getUsername() == username and self.getPassword() == password:
      return 1
    return 0
  
  def getPassword(self):
    return self.__password
  
  def getUsername(self):
    return self.__username
  
  def getHeading(self):
    return self.__heading
  
  @dMVC.model.localMethod
  def defaultView(self, screen):
    return GG.isoview.isoview_player.IsoViewPlayer(self, screen)
  
  def getDestination(self):
    return self.__destination
  
  def setNewPosition(self, position):
    if self.getDestination() == position:
      self.__visited = []
    self.__visited.append(position)
    pActualAux = self.getPosition()
    self.setPosition(position)
    self.triggerEvent('position', player=self, pActual=pActualAux, pDestin=self.getPosition(), dir=self.getHeading())
  
  def hasBeenVisited(self, pos):
    for i in range(0, len(self.__visited)):
      if self.__visited[i] == pos:
        return 1
    return 0
  
  def setDestination(self, heading, destination):
    self.__heading = heading
    self.__destination = destination
  
  def tick(self, direction):
    if self.getPosition() == self.__destination:
      self.__heading = "standing_down"
      return
    #if self.__heading <> "standing_down":
    pos = self.getPosition()
    self.__heading = direction
    if self.__heading == "walking_up":
      next = [pos[0], pos[1], pos[2] - 1]
    if self.__heading == "walking_down":
      next = [pos[0], pos[1], pos[2] + 1]
    if self.__heading == "walking_left":
      next = [pos[0] - 1, pos[1], pos[2]]
    if self.__heading == "walking_right":
      next = [pos[0] + 1, pos[1], pos[2]]
    if self.__heading == "walking_topleft":
      next = [pos[0] - 1, pos[1], pos[2] - 1]
    if self.__heading == "walking_bottomright": 
      next = [pos[0] + 1, pos[1], pos[2] + 1]
    if self.__heading == "walking_bottomleft":
      next = [pos[0] - 1, pos[1], pos[2] + 1]
    if self.__heading == "walking_topright":
      next = [pos[0] + 1, pos[1], pos[2] - 1]
    self.setNewPosition(next)
  
  """  
  def getState(self):
    return self.__state

  def getStateFrame(self):
    return self.__stateFrame

  
  def getDir(self):
    for i in range (1, len(utils.DIR)+1):
      if self._state == utils.DIR[i]:
        return i
    return 0  
  
  
  def setState(self, state):
    self.__state = state

  def setStateFrame(self, stateFrame):
    self.__stateFrame = stateFrame

    
    
    
    
    
  
  """    
