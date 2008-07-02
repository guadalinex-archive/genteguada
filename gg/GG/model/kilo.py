import ggmodel
import GG.utils
import room_item
import kilo_temp
import GG.isoview.isoview_item
import dMVC.model

class GGKilo(room_item.GGRoomItem):
  """GGKilo class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName, anchor, topAnchor, spriteInventory, label):
    """ Class constructor.
    spriteName: image name.
    """
    room_item.GGRoomItem.__init__(self, spriteName, anchor, topAnchor)
    self.spriteInventory = spriteInventory
    self.label = label
    self.points = 0
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label', 'points']

  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["copy"]   
      
  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteInventory

  def setPoints(self, points):
    self.points = points
  
  """
  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)
    #return GG.isoview.isoview_inventoryitem.IsoViewInventoryItem(self, screen, parent)
  """
  
  def getCopyFor(self, player):
    #if player.hasItemLabeledInInventory("Regalo"):
    kilo = GG.model.kilo_temp.GGKiloTemp(self.spriteName, self.getPosition(), self.anchor, self.spriteInventory, "Pesa", 6)
    kilo.setTile(self.getTile())
    return kilo
    
  def clickedBy(self, clicker):
    """ Triggers an event when the item receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
  
  def checkSimilarity(self, item):
    if room_item.GGRoomItem.checkSimilarity(self, item):
      if item.label == self.label:
        if item.points == self.points:
          if item.spriteInventory == self.spriteInventory:
            return True
    return False   
  
  def inventoryOnly(self):
    return False
  
  def tick(self, now):
    """ Call for an update on item.
    Not used at the moment.
    """
    pass
  
  def isStackable(self):
    return False
