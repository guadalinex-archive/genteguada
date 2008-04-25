import item
import GG.isoview.isoview_player
import dMVC.model
#import ggcommon.eventos

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
    self.__heading = "standing_down"
    self.__stateFrame = 0
    self.__destination = position
    self.__currentRoom = None
    self.__username = username
    self.__password = password
    self.__visited = []

  def getCurrentRoom(self):
    """ Returns the room where the player is.
    """
    return self.__currentRoom
  
  def getPassword(self):
    """ Returns the user password.
    """
    return self.__password
  
  def getUsername(self):
    """ Returns the user name.
    """
    return self.__username
  
  def getHeading(self):
    """ Returns the direction the player is heading to.
    """
    return self.__heading
  
  def getDestination(self):
    """ Returns the player's movement destination.
    """
    return self.__destination
  
  def setDestination(self, heading, destination):
    """ Sets a new destination for the player movement.
    heading: movement direction.
    destination: movement destination.
    """
    self.__heading = heading
    self.__destination = destination
  
  def setCurrentRoom(self, room):
    """ Sets a new room for the player.
    room: new room.
    """
    self.__currentRoom = room
  
  def setNewPosition(self, position):
    """ Sets a new location for the player.
    position: new location.
    """
    if self.getDestination() == position:
      self.__visited = []
    self.__visited.append(position)
    pActualAux = self.getPosition()
    self.setPosition(position)
    self.triggerEvent('position', player=self, pActual=pActualAux, pDestin=self.getPosition(), dir=self.getHeading())
  
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
  
  def tick(self, direction):
    """ Calls for an update on player's position an movement direction.
    direction: movement direction.
    """
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
