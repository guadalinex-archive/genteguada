import room_item
import GG.utils

class GGWebItem(room_item.GGRoomItem):
  """ GGWebItem class.
  """
 
  def __init__(self, sprite, anchor, topAnchor, url, label):
    """ Class builder.
    sprite: sprite used to paint the cube.
    position: penguin position.
    anchor: image anchor on screen.
    url:
    """
    room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor)
    self.__url = url
    self.label = label
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['label']
  
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["url"]
      
  def getAdminActions(self):
    dic = {"Position": self.getTile().position, "Url": [self.__url]}
    return dic  
        
  def getName(self):
    return self.label
  
  def getImageLabel(self):
    return self.spriteName

  def getUrl(self):
    return self.__url  
  
  def setUrl(self, url):
    self.__url = url  
  def checkSimilarity(self, item):
    if room_item.GGRoomItem.checkSimilarity(self, item):
      if item.getUrl() == self.getUrl():
        return True
    return False   

  def clickedBy(self, clicker):
    """ Triggers an event when the npc receives a click by a player.
    clicker: player who clicks.
    """
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    
  
#================================================================================

class GGWebPannel(GGWebItem):
  """ GGWebPannel class.
  """
 
  def __init__(self, sprite, anchor, topAnchor, url, label):
    GGWebItem.__init__(self, sprite, anchor, topAnchor, url, label)
    self.__pannels = []
    #self.addPannels(self)
    
  def addPannels(self, *pannels):
    for pannel in pannels:
      self.__pannels.append(pannel)
    
  def removePannels(self, *pannels):
    for pannel in pannels:
      self.__pannels.remove(pannel)    

  def distributedSetUrl(self, url):
    self.setUrl(url)
    for pannel in self.__pannels:
      pannel.setUrl(url)  

  def clickedBy(self, clicker):
    """ Triggers an event when the npc receives a click by a player.
    clicker: player who clicks.
    """
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItemWithoutHighlight(self)
    else:
      return False    

  def __del__(self):
    for pannel in self.__pannels:
      pannel.removePannels(self)    

#================================================================================
