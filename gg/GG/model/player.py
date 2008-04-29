import item
import GG.isoview.isoview_player
import dMVC.model

class GGPlayer(item.GGItem):
  """ Player class.
  Defines a player object behaviour.
  """
 
  def __init__(self, sprite, size, position, offset, username, password):
    """ Class builder.
    sprite: sprite used to paint the player.
    size: player sprite size.
    position: player position.
    offset: image offset on screen.
    username: user name.
    password: user password.
    """
    item.GGItem.__init__(self, sprite, size, position, offset)
    self.username = username
    self.__heading = "down"
    self.__state = "standing"
    self.__destination = position
    self.__password = password
    self.__visited = []

  def variablesToSerialize(self):
    return ['username']
  
  @dMVC.model.localMethod 
  def getUsername(self):
    """ Returns the user name.
    """
    return self.username

  def getHeading(self):
    """ Returns the direction the player is heading to.
    """
    return self.__heading
  
  def getState(self):
    """ Returns the player's state.
    """
    return self.__state
  
  def getPassword(self):
    """ Returns the user password.
    """
    return self.__password
  
  def getDestination(self):
    """ Returns the player's movement destination.
    """
    return self.__destination
  
  def setHeading(self, heading):
    """ Sets a new heading direction for the item.
    """
    if self.__heading <> heading:
      self.__heading = heading
      self.triggerEvent('headingChanged', heading=heading)

  def setState(self, state):
    """ Sets a new state for the item.
    """
    if self.__state <> state:
      self.__state = state
      self.triggerEvent('stateChanged', state=state)

  def setDestination(self, destination):
    """ Sets a new destination for the player movement.
    heading: movement direction.
    destination: movement destination.
    """
    if self.__destination <> destination:
      self.__destination = destination
      self.triggerEvent('destinationChanged', destination=destination)

  def checkUser(self, username, password):
    """ Searchs for an user by his user name and password.
    username: user name.
    password: user password.
    """
    if self.getUsername() == username and self.getPassword() == password:
      return 1
    return 0
  
  @dMVC.model.localMethod
  def defaultView(self, screen, room, parent):
    """ Creates a view object associated with this player.
    screen: screen handler.
    room: room view object.
    parent: hud or session view object.
    """
    return GG.isoview.isoview_player.IsoViewPlayer(self, screen, room, parent)
  
  def hasBeenVisited(self, pos):
    """ Checks if a tile has been visited by the player on the last movement.
    pos: tile position.
    """
    for i in range(0, len(self.__visited)):
      if self.__visited[i] == pos:
        return 1
    return 0
  
  def tick(self):
    """ Calls for an update on player's position an movement direction.
    """
    if self.getPosition() == self.__destination:
      self.setState("standing")
      return
    direction = self.getRoom().getNextDirection(self, self.getPosition(), self.getDestination())
    if direction == "none":
      self.setDestination(self.getPosition())
      return
    pos = self.getPosition()
    self.setState("walking")
    self.setHeading(direction)
    if self.getHeading() == "up":
      next = [pos[0], pos[1], pos[2] - 1]
    if self.getHeading() == "down":
      next = [pos[0], pos[1], pos[2] + 1]
    if self.getHeading() == "left":
      next = [pos[0] - 1, pos[1], pos[2]]
    if self.getHeading() == "right":
      next = [pos[0] + 1, pos[1], pos[2]]
    if self.getHeading() == "topleft":
      next = [pos[0] - 1, pos[1], pos[2] - 1]
    if self.getHeading() == "bottomright": 
      next = [pos[0] + 1, pos[1], pos[2] + 1]
    if self.getHeading() == "bottomleft":
      next = [pos[0] - 1, pos[1], pos[2] + 1]
    if self.getHeading() == "topright":
      next = [pos[0] + 1, pos[1], pos[2] - 1]
    self.setPosition(next)
