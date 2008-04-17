import ggmodel
import ggcommon.eventos

class Player(ggmodel.GGModel):
  """ Player class.
  Defines an object behaviour, either if it is a player object or a non-player object.
  """
 
  def __init__(self, name, id, sprite, size, position, offset):
    """ Class builder.
    name: label.
    id: identifier.
    sprite: sprite used to paint the player.
    size: player sprite size.
    position: player position.
    """
    ggmodel.GGModel.__init__(self, name, id, sprite, size)
    self._position = position
    self._state = "standing_down"
    self._stateFrame = 0
    self._destination = position
    self._offset = offset
    self._visited = []
        
  def getPosition(self):
    """ Returns the player position.
    """
    return self._position
 
  def getState(self):
    """ Returns the player state.
    """
    return self._state

  def getStateFrame(self):
    """ Returns the player frame state.
    """
    return self._stateFrame

  def getDestination(self):
    """ Returns the player movement destination.
    """
    return self._destination
  
  def getDir(self):
    """ Returns the player movement direction.
    """
    for i in range (1, len(utils.DIR)+1):
      if self._state == utils.DIR[i]:
        return i
    return 0  
  
  def getOffset(self):
    """ Returns the player sprite offset.
    """
    return self._offset
  
  def testSetPosition(self, position):
    """ Public version for _setPosition. To be used ONLY on tests.
    """
    self._setPosition(position)
      
  def _setPosition(self, position):
    """ Sets a new position for the player.
    position: new position.
    """
    if self._destination == position:
      self._visited = []
    self._visited.append(position)
    pActualAux = self._position
    self._position = position
    self.triggerEvent('position', id=self._id, sprite=self.getSprite(), \
                        pActual=pActualAux, pDestin=self._position, dir=self._state)
    
  def _setState(self, state):
    """ Sets a new player state.
    state: new state.
    """
    self._state = state

  def _setStateFrame(self, stateFrame):
    """ Sets a new player state frame.
    stateFrame: new state frame.
    """
    self._stateFrame = stateFrame

  def setDestination(self, state, destination):
    """ Sets a new movement destination point.
    state: direction for the next move.
    destiantion: movement destination.
    """
    self._state = state
    self._destination = destination
    
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
    for i in range(0, len(self._visited)):
      if self._visited[i] == pos:
        return 1
    return 0
    
  def tick(self, direction):
    """ This method updates the movement positions and animation states of the player.
    direction: direction of the next move.
    """
    if self._position == self._destination:
      self._state = "standing_down"
      return
    if self._state <> "standing_down":
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
      self._setPosition(next)
      