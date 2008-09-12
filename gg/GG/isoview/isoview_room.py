# -*- coding: utf-8 -*- 

import os
import GG.utils
import isoview
import isoview_tile
import isoview_player

class IsoViewRoom(isoview.IsoView):
  """ IsoViewRoom class.
  Defines the room view.
  """

  def __init__(self, model, screen, hud):
    """ Class constructor.
    model: room model.
    screen: screen handler.
    hud: hud object.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__parent = hud
    self.__isoViewItems = []
    self.__spritesDict = {}
    self.__bottomSpritesDict = {}
    self.__insertedIVItem = None
    self.__tileList = []
    tiles = model.getTiles()
    specialTiles = model.getSpecialTiles()
    for corx in range(model.size[0]):
      listTile = []
      for corz in range(model.size[1]):
        varPos = GG.utils.p3dToP2d([corx, corz], GG.utils.FLOOR_SHIFT)
        pos = [int(varPos[0]), int(varPos[1])]
        k = 0
        for specTile in specialTiles:
          if specTile[0] == [corx, 0, corz]:    
            isotile = isoview_tile.IsoViewTile(tiles[corx][corz], [pos[0], pos[1]], \
                    [pos[0] + GG.utils.TILE_SZ[0], pos[1] + GG.utils.TILE_SZ[1]], [corx, corz], specTile[1], self.__parent)
            k = 1
        if k == 0:
          isotile = isoview_tile.IsoViewTile(tiles[corx][corz], [pos[0], pos[1]], \
                    [pos[0] + GG.utils.TILE_SZ[0], pos[1] + GG.utils.TILE_SZ[1]], [corx, corz], \
                    tiles[corx][corz].spriteName, self.__parent)
        self.__parent.addSprite(isotile.getImg())
        self.__bottomSpritesDict[isotile.getImg()] = isotile
        listTile.append(isotile)
      self.__tileList.append(listTile)
    itemsDict = self.getModel().getPositionItems()
    for item in itemsDict:
      isoviewitem = item["obj"].defaultView(self.getScreen(), self, self.__parent, item["position"], item["image"])
      self.__isoViewItems.append(isoviewitem)
      self.__parent.addSprite(isoviewitem.getImg())
      self.__spritesDict[isoviewitem.getImg()] = isoviewitem  
    """  
    for item in self.getModel().getItems():
      isoviewitem = item.defaultView(self.getScreen(), self, self.__parent)
      self.__isoViewItems.append(isoviewitem)
      self.__parent.addSprite(isoviewitem.getImg())
      self.__spritesDict[isoviewitem.getImg()] = isoviewitem
    """  
    self.getModel().subscribeEvent('addItemFromVoid', self.itemAddedFromVoid)
    self.getModel().subscribeEvent('addItemFromInventory', self.itemAddedFromInventory)
    self.getModel().subscribeEvent('removeItem', self.itemRemoved)
    self.getModel().subscribeEvent('setSpecialTile', self.specialTileAdded)
    self.getModel().subscribeEvent('updateScreenPos', self.updateScreenPos)
    self.getModel().subscribeEvent('floorChanged', self.floorChanged)
    
  def getSpritesDict(self):
    """ Returns the sprites dictionary.
    """
    return self.__spritesDict

  def getBottomSpritesDict(self):
    """ Returns the bottom sprites dictionary.
    """  
    return self.__bottomSpritesDict
  
  def stopAnimations(self):
    """ Stop all room current animations.
    """  
    for item in self.__isoViewItems:
      item.stopAnimation()
  
  def getIsoViewItems(self):
    """ Returns the item's isometric view handlers.
    """
    return self.__isoViewItems
  
  def updateFrame(self, elapsedTime):
    """ Paints floor, players and items on the room.
    elapsedTime: elapsed time since the game start.
    """
    for isoitem in self.__isoViewItems:
      isoitem.updateFrame(elapsedTime)
    
  def getIsoviewPlayers(self):
    """ Returns the isometric view players list.
    """
    return self.__isoViewItems
    
  def findTile(self, pos):
    """ Gets the game coords that match a screen point.
    pos: screen coords.
    """
    images = self.__spritesDict.keys()
    images.sort(GG.utils.compare)  
    for image in images:
      if self.__spritesDict[image].checkClickPosition(pos):
        item = self.__spritesDict[image].getModel() 
        return self.__spritesDict[image].getPosition(), item
    for image in self.__bottomSpritesDict:
      if self.__bottomSpritesDict[image].checkClickPosition(pos):
        return self.__bottomSpritesDict[image].getModel().position, None
    return [-1, -1], None

  def findTileOnly(self, pos):
    """ Gets the game coords that match a screen point.
    pos: screen coords.
    """
    images = self.__spritesDict.keys()
    images.sort(GG.utils.compare)  
    for image in self.__bottomSpritesDict:
      if self.__bottomSpritesDict[image].checkClickPosition(pos):
        return self.__bottomSpritesDict[image].getModel().position
    return [-1, -1]
  
  def itemAddedFromVoid(self, event):
    """ Updates the room view when an item add event happens.
    event: even info.
    """
    ivitem = self.findIVItem(event.getParams()['item'])
    if ivitem:
      self.__parent.addItemToRoomFromVoid(ivitem)  
      return
    ivItem = event.getParams()['item'].defaultView(self.getScreen(), self, self.__parent)
    self.addIsoViewItem(ivItem)
    self.__parent.addItemToRoomFromVoid(ivItem)
    
  def itemAddedFromInventory(self, event):
    """ Updates the room view when an item add event happens.
    event: even info.
    """
    """
    for ivitem in self.__isoViewItems:
      if isinstance(ivitem, isoview_player.IsoViewPlayer):
        if ivitem.getModel().username == event.getParams()['item'].username:
          return
    """      
    ivItem = event.getParams()['item'].defaultView(self.getScreen(), self, self.__parent)
    self.addIsoViewItem(ivItem)
    self.__parent.addItemToRoomFromInventory(ivItem)
        
  def itemRemoved(self, event):
    """ Updates the room view when an item remove event happens.
    event: even info.
    """
    item = event.getParams()['item']
    ivItem = self.findIVItem(item)
    if ivItem == None:
      raise Exception("Error: vista de item no eliminada")
    self.removeIsoViewItem(ivItem)
        
  def addIsoViewItem(self, ivItem):
    """ Inserts a new item view.
    ivItem: item view.
    """
    self.__isoViewItems.append(ivItem)
    self.__parent.addSprite(ivItem.getImg())
    self.__spritesDict[ivItem.getImg()] = ivItem
    pos = ivItem.getPosition()
    print "addIsoViewItem"
    self.updateScreenPositionsOn(pos)

  def removeIsoViewItem(self, ivPlayer):
    """ Removes an isometric player viewer from the viewers list.
    ivPlayer: ivPlayer view to be removed.
    """
    aux = None
    self.__parent.itemUnselectedSoft(ivPlayer.getModel())
    self.__parent.removeSprite((ivPlayer.getImg()))
    for image in self.__spritesDict:
      if self.__spritesDict[image] == ivPlayer:
        aux = image
        self.__parent.removeSprite(image)
    if aux:
      del self.__spritesDict[aux]
    self.__isoViewItems.remove(ivPlayer)
    ivPlayer.unsubscribeAllEvents()
    
  def updateScreenPos(self, event):    
    print "updateScreenPos"
    self.updateScreenPositionsOn(event.getParams()['position'])
    
  def floorChanged(self, event):
    newTiles = event.getParams()['newTile']
    #print ">>>", newTile
    for x in range(len(self.__tileList)):
      for y in range(len(self.__tileList[x])):
        self.__tileList[x][y].setImg(os.path.join(GG.utils.TILE, newTiles[x][y]))
    
  def updateScreenPositionsOn(self, pos, itemList = None):
    """ Updates the screen cords of all items on a room position.
    pos: room position.
    """  
    tile = self.__tileList[pos[0]][pos[1]].getModel()
    if not itemList:
      itemList = tile.getItems()
    accHeight = tile.anchor[0]
    accWidth = tile.anchor[1]
    i = 0
    for item in itemList:
      ivIt = self.__parent.findIVItem(item)
      if ivIt:  
        scPos = GG.utils.p3dToP2d(ivIt.getPosition(), item.anchor)
        if i == 0:
          zOrder = ivIt.getZOrder()
          i = 1
        else:
          zOrder += 2
        ivIt.setScreenPosition([scPos[0] + accWidth, scPos[1] - accHeight])
        ivIt.updateZOrder(zOrder)
        accWidth += item.topAnchor[0] 
        accHeight += item.topAnchor[1]
          
  def getFutureScreenPosition(self, ivItem, pos, itemList):
    """ Returns the future screen cords for an item moving to a room position.
    ivItem: item.
    pos: room position.
    """  
    tile = self.__tileList[pos[0]][pos[1]].getModel()
    accHeight = tile.anchor[0]
    accWidth = tile.anchor[1]
    itemModel = ivItem.getModel()
    listaAux = itemList[:len(itemList)-1]
    for item in listaAux:
      accWidth += item.topAnchor[0] 
      accHeight += item.topAnchor[1]
    scPos = GG.utils.p3dToP2d(pos, itemModel.anchor)
    return [scPos[0] - accWidth, scPos[1] - accHeight]
          
  def addIsoViewChatItem(self, ivChatItem):
    """ Adds a new isometric view chat item.
    ivChatItem: isometric view chat item.
    """  
    self.__isoViewItems.append(ivChatItem)
    self.__parent.addSprite(ivChatItem.getImg())
  
  def specialTileAdded(self, event):
    """ Triggers after receiving a new special tile added event.
    event: event info.
    """  
    pass # Do NOT delete
    
  def unsubscribeAllEvents(self):
    """ Unsubscribe this view ands all its children from all events.
    """
    for item in self.__isoViewItems:
      item.unsubscribeAllEvents()
    isoview.IsoView.unsubscribeAllEvents(self)

  def itemSelected(self, item):
    """ Sets an item on the room as selected.
    item: selected item.
    """
    ivItem = self.findIVItem(item)
    if ivItem:
      ivItem.selected()
    
  def itemUnselected(self, item):
    """ Sets an item on the room as unselected.
    item: unselected item.
    """
    cosa = self.findIVItem(item)
    if cosa:
      cosa.unselected()
    
  def setItemOnTile(self, item, position):
    """ Adds an item to a room position.
    item: item to add.
    position: room position.
    """  
    if item == None:
      self.__tileList[position[0]][position[2]].removeTopMostItem()
    else:
      self.__tileList[position[0]][position[2]].addIsoItem(item)      

  def findIVItem(self, item):
    """ Returns the isometric view object that contains a given item.
    item: given item.
    """  
    for ivItem in self.__isoViewItems:
      if ivItem.getModel() == item:
        return ivItem
    return None  

  def changeAvatarImages(self, avatar, path):
    isoAvatar = self.findIVItem(avatar)
    if isoAvatar:
      isoAvatar.changeAvatarImages(path) 
      
  def updateScreenPositions(self):
    itemPositions = {}  
    for ivItem in self.__isoViewItems:
      #pos = ivItem.getPosition()
      if ivItem in itemPositions.keys():
        itemPositions[ivItem] = 1
      else:  
        itemPositions[ivItem] = 0
    keys = itemPositions.keys()
    for key in keys:
      if itemPositions[key] == 1:
        print "updateScreenPositions"
        self.updateScreenPositionsOn(key.getPosition())  
    #for ivItem in self.__isoViewItems:
    #  self.updateScreenPositionsOn(ivItem.getPosition())      

  def getTile(self, pos):
    return self.__tileList[pos[0]][pos[1]] 
