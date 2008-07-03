import room_item
import GG.model.generated_golden_key
import GG.isoview.isoview_item

class GGPersistentKey(room_item.GGRoomItem):
  """ GGGoldenKeyRoom2 class.
  Defines a persistent item behaviour.
  """

  def __init__(self, spriteName, anchor, topAnchor, spriteInventory, label):
    """ Class builder.
    spriteName: sprite used to paint the item on the screen game zone.
    position: item position.
    anchor: image anchor on screen.
    spriteInventory: sprite used to paint the item on the screen inventory zone.
    label: item's label
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

  def setPlayer(self, player):
    self.__player = player
    
  def getPlayer(self):
    return self.__player  

  def getCopyFor(self, player):
    if  player.checkPointGiver(self.label):
      self.getRoom().triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage("Ya has obtenido una llave", \
                'Llave', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
      return None
    else:
      self.getRoom().triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage("Obtienes una llave", \
                'Llave', GG.utils.TEXT_COLOR["black"], self.getPosition(), 2))
      player.addPoints(0, 'Llave')
      #return GG.model.gift_inventory.GGGiftInventory(self.spriteInventory, "Regalo", self.anchor, self.getPosition())
      keyaux = GG.model.generated_golden_key.GGGeneratedGoldenKey(self.getImageLabel(), self.anchor, self.topAnchor, self.getImageLabel(), 'Llave')
      keyaux.setTile(self.getTile())
      return keyaux 

  
  def clickedBy(self, clicker):
    """ Triggers an event when the item receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)

  def isStackable(self):
    return False

  def stepOn(self):
    return False
