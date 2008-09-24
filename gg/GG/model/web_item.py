# -*- coding: utf-8 -*-

import room_item
import GG.utils

class GGWebItem(room_item.GGRoomItem):
  """ GGWebItem class.
  Defines a web item object.  
  """
 
  def __init__(self, sprite, anchor, topAnchor, url, label):
    """ Class builder.
    sprite: sprite used to paint the item.
    anchor: image anchor on screen.
    topAnchor: image top anchor on screen.
    url: internet address.
    label: item's label.
    """
    room_item.GGRoomItem.__init__(self, sprite, anchor, topAnchor, label)
    self.__url = url
    
  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGWebItem(self.spriteName, self.anchor, self.topAnchor, self.__url, self.getName())
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["url", "jumpOver"]
      
  def getAdminActions(self):
    """ Returns the item's available admin actions.
    """  
    dic = {"Position": self.getTile().position, "Url": [self.__url], "Label": [self.getName()]}
    return dic  
        
  def getImageLabel(self):
    """ Returns the item's image file name.
    """  
    return self.spriteName
  
  def getUrl(self):
    """ Returns saved internet address.
    """  
    return self.__url  
  
  def setUrl(self, url):
    """ Sets a new internet address.
    url: internet address.
    """  
    self.__url = url  
  
  def clickedBy(self, clicker):
    """ Triggers an event when the npc receives a click by a player.
    clicker: player who clicks.
    """
    room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    
  
# ===============================================================

class GGWebPannel(GGWebItem):
  """ GGWebPannel class.
  Defines a web pannel object.
  """
 
  def __init__(self, sprite, anchor, topAnchor, url, label):
    """ Class builder.
    sprite: sprite used to paint the item.
    anchor: image anchor on screen.
    topAnchor: image top anchor on screen.
    url: internet address.
    label: item's label.
    """
    GGWebItem.__init__(self, sprite, anchor, topAnchor, url, label)
    self.__pannels = []

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGWebPannel(self.spriteName, self.anchor, self.topAnchor, self.getUrl(), self.getName())
    
  def addPannels(self, *pannels):
    """ Adds new pannels to the pannel group.
    pannels: new pannels. 
    """  
    for pannel in pannels:
      self.__pannels.append(pannel)
    
  def removePannels(self, *pannels):
    """ Remove pannels from the pannel grou.
    pannels: pannels to be removed.
    """  
    for pannel in pannels:
      self.__pannels.remove(pannel)    

  def distributedSetUrl(self, url):
    """ Distributes a new url to the associated pannels.
    url: new url.
    """  
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
    """ Class destructor.
    """  
    for pannel in self.__pannels:
      pannel.removePannels(self)    
