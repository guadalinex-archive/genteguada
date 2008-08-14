import ggmodel
import dMVC.model

class GGInventoryItem(ggmodel.GGModel):
  """GGInventoryItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName):
    """ Class constructor.
    spriteName: image name.
    """
    ggmodel.GGModel.__init__(self)
    self.__player = None
    self.spriteName = spriteName
    self.spriteInventory = None
    self.setImagePath("")
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['spriteName', 'spriteInventory']
  
  def getAdminActions(self):
    """ Returns all possible admin actions for this item.
    """  
    return None
  
  def getImagePath(self):
    return self.__imagePath  
  
  def setImagePath(self, imagePath):
    self.__imagePath = imagePath 
  
  # self.__player
  
  def getPlayer(self):
    """ Returns this item's owner.
    """  
    return self.__player

  def setPlayer(self, player):
    """ Sets a new player as owner of this item.
    """  
    self.__player = player  

  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    room: item's room.
    parent: isoview hud handler.
    """
    import GG.isoview.isoview_item
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)

  def inventoryOnly(self):
    """ Checks if this is an inventory item or not.
    """  
    return True
  
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    pass
    
  def tick(self, now):
    """ Call for an update on item.
    Not used at the moment.
    """
    pass

  def isTile(self):
    return False  