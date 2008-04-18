import ggmodel
import ggcommon.eventos

class Player(ggmodel.GGModel):
  """ Player class.
  Defines an object behaviour, either if it is a player object or a non-player object.
  """
 
  def __init__(self, name, id, sprite, size, position, offset, username=None, password=None):
    """ Class builder.
    name: label.
    id: identifier.
    sprite: sprite used to paint the player.
    size: player sprite size.
    position: player position.
    """
    ggmodel.GGModel.__init__(self, name, id, sprite, size)
    self.__position = position
    self.__state = "standing_down"
    self.__stateFrame = 0
    self.__destination = position
    self.__offset = offset
    self.__currentRoom = None
    if username: self.__username = username
    if password: self.__password = password
    self.__visited = []
        
  def getPosition(self):
    """ Returns the player position.
    """
    return self.__position
 
  def getState(self):
    """ Returns the player state.
    """
    return self.__state

  def getStateFrame(self):
    """ Returns the player frame state.
    """
    return self.__stateFrame

  def getDestination(self):
    """ Returns the player movement destination.
    """
    return self.__destination
  
  def getDir(self):
    """ Returns the player movement direction.
    """
    for i in range (1, len(utils.DIR)+1):
      if self._state == utils.DIR[i]:
        return i
    return 0  
  
  def getPassword(self):
    """ Returns the player password.
    """
    return self.__password
  
  def getUsername(self):
    """ Returns the player username.
    """
    return self.__username
  
  def getOffset(self):
    """ Returns the player sprite offset.
    """
    return self.__offset
  
  def setPosition(self, position):
    """ Sets a new position for the player.
    position: new position.
    """
    if self.getDestination() == position:
      self.__visited = []
    self.__visited.append(position)
    pActualAux = self.getPosition()
    self.__position = position
    self.triggerEvent('position', id=self.getId(), sprite=self.getSprite(), \
                        pActual=pActualAux, pDestin=self.__position, dir=self.__state)
    
  def setState(self, state):
    """ Sets a new player state.
    state: new state.
    """
    self.__state = state

  def setStateFrame(self, stateFrame):
    """ Sets a new player state frame.
    stateFrame: new state frame.
    """
    self.__stateFrame = stateFrame

  def setDestination(self, state, destination):
    """ Sets a new movement destination point.
    state: direction for the next move.
    destiantion: movement destination.
    """
    self.__state = state
    self.__destination = destination
    
  def setCurrentRoom(self, room):
    """ Sets room where the player is.
    """
    self.__currentRoom = room
    
  def checkUser(self, username, password):
    """ Checks if username and password match for current player.
    """
    if self.getUsername() == username and self.getPassword() == password:
      return 1
    return 0
    
  def clickedByPlayer(self, player, clickerLabel, roomName):
    """ Triggers an event after being clicked by another player (clicker).
    player: clicker id.
    clickerLabel: clicker label.
    roomName: room label.
    """
    self.triggerEvent('click on player', pl=self.getName(), clicker=clickerLabel, target=self.getPosition(), room=roomName)
    
  def hasBeenVisited(self, pos):
    """ Checks if a tile has been visited since the player's last move.
    pos: tile to check.
    """
    for i in range(0, len(self.__visited)):
      if self.__visited[i] == pos:
        return 1
    return 0
    
  def tick(self, direction):
    """ This method updates the movement positions and animation states of the player.
    direction: direction of the next move.
    """
    if self.__position == self.__destination:
      self.__state = "standing_down"
      return
    if self.__state <> "standing_down":
      pos = self.getPosition()
      self._state = direction
      if self._state == "walking_up":
        next = [pos[0], pos[1], pos[2] - 1]
      if self._state == "walking_down":
        next = [pos[0], pos[1], pos[2] + 1]
      if self._state == "walking_left":
        next = [pos[0] - 1, pos[1], pos[2]]
      if self._state == "walking_right":
        next = [pos[0] + 1, pos[1], pos[2]]
      if self._state == "walking_topleft":
        next = [pos[0] - 1, pos[1], pos[2] - 1]
      if self._state == "walking_bottomright": 
        next = [pos[0] + 1, pos[1], pos[2] + 1]
      if self._state == "walking_bottomleft":
        next = [pos[0] - 1, pos[1], pos[2] + 1]
      if self._state == "walking_topright":
        next = [pos[0] + 1, pos[1], pos[2] - 1]
      self.setPosition(next)
      