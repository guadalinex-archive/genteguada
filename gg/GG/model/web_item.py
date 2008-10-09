# -*- coding: utf-8 -*-

import room_item
import GG.utils
import ggmodel
import ggsystem

class GGWebItem(room_item.GGRoomItem):
  """ GGWebItem class.
  Defines a web item object.  
  """
 
  def __init__(self, sprite, url, label):
    """ Class builder.
    sprite: sprite used to paint the item.
    url: internet address.
    label: item's label.
    """
    room_item.GGRoomItem.__init__(self, sprite, label)
    self.__url = url
    
  def objectToPersist(self):
    dict = room_item.GGRoomItem.objectToPersist(self)
    dict["url"] = self.__url
    return dict

  def load(self, dict):
    room_item.GGRoomItem.load(self, dict)
    self.__url = dict["url"]

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGWebItem(self.spriteName, self.__url, self.getName())
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["url", "jumpOver"]
      
  def getAdminActions(self):
    """ Returns the admin available options.
    """  
    adminDict = room_item.GGRoomItem.getAdminActions(self)
    adminDict["Etiqueta"] = [self.getName()]
    adminDict["Url"] = [self.__url]
    return adminDict    

  def applyChanges(self, fields, player, room):
    keys = fields.keys()
    if "Etiqueta" in keys:
      oldLabel = self.getName()
      newLabel = fields["Etiqueta"]
      if self.setName(newLabel):
        ggsystem.GGSystem.getInstance().labelChange(oldLabel, newLabel)
    if "Url" in keys:
      self.setUrl(fields["Url"])
    return room_item.GGRoomItem.applyChanges(self, fields, player, room)

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
 
  def __init__(self, sprite, url, label):
    """ Class builder.
    sprite: sprite used to paint the item.
    url: internet address.
    label: item's label.
    """
    GGWebItem.__init__(self, sprite, url, label)
    self.__pannels = []

  def objectToPersist(self):
    dict = GGWebItem.objectToPersist(self)
    listPannels = []
    for pannel in self.__pannels:
      listPannels.append(pannel.getName())
    dict["pannels"] = listPannels
    return dict

  def load(self, dict):
    GGWebItem.load(self, dict)
    self.__pannels = []
    #for pannelDict in dict["pannels"]:
    #  self.__pannels.append(ggmodel.GGModel.read(pannelDict["id"], "room", pannelDict))

  def copyObject(self):
    """ Copies and returns this item.
    """  
    return GGWebPannel(self.spriteName, self.getUrl(), self.getName())
    
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
