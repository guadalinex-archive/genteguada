#-*- coding: utf-8 -*- 

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
    infoPackage = model.getRoomBuildPackage()
    tiles = infoPackage["tiles"]
    specialTiles = infoPackage["specialtiles"]
    itemsDict = infoPackage["positionitems"]
    populatedTiles = infoPackage["populatedtiles"] 
    for corx in range(model.size[0]):
      listTile = []
      for corz in range(model.size[1]):
        varPos = GG.utils.p3dToP2d([corx, corz], GG.utils.FLOOR_SHIFT)
        pos = [int(varPos[0]), int(varPos[1])]
        k = 0
        for specTile in specialTiles:
          if specTile[0] == [corx, corz]:    
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
    subscriptionChildList = []
    for item in itemsDict:
      isoviewitem = item["obj"].defaultView(self.getScreen(), self, self.__parent, item["position"], item["imagePath"], item["image"])
      self.__isoViewItems.append(isoviewitem)
      self.__parent.addSprite(isoviewitem.getImg())
      self.__spritesDict[isoviewitem.getImg()] = isoviewitem  
      subscriptionChildList.append([isoviewitem.getModel(), "position", isoviewitem.positionChanged])
    self.getModel().subscribeChildListEvent(subscriptionChildList)
    for singleTile in populatedTiles:
      pos = singleTile[0]
      listItems = singleTile[1]
      self.updateScreenPositionsOn(pos)
    subscriptionList = []
    subscriptionList.append(['addItemFromVoid', self.itemAddedFromVoid])
    subscriptionList.append(['addItemFromInventory', self.itemAddedFromInventory])
    subscriptionList.append(['removeItem', self.itemRemoved])
    subscriptionList.append(['setSpecialTile', self.specialTileAdded])
    subscriptionList.append(['updateScreenPos', self.updateScreenPos])
    subscriptionList.append(['floorChanged', self.floorChanged])
    subscriptionList.append(['tileImageChange', self.tileImageChange])
    self.getModel().subscribeListEvent(subscriptionList)
    
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
    event.getParams()['item'].subscribeEvent( "position", ivItem.positionChanged)
    self.addIsoViewItem(ivItem, event.getParams()["itemList"])
    self.__parent.addItemToRoomFromVoid(ivItem, event.getParams()["itemList"])
    
  def itemAddedFromInventory(self, event):
    """ Updates the room view when an item add event happens.
    event: even info.
    """
    ivItem = event.getParams()['item'].defaultView(self.getScreen(), self, self.__parent)
    event.getParams()['item'].subscribeEvent( "position", ivItem.positionChanged)
    listItems = event.getParams()['itemList']
    self.addIsoViewItem(ivItem, listItems)
    self.__parent.addItemToRoomFromInventory(ivItem, listItems )
        
  def itemRemoved(self, event):
    """ Updates the room view when an item remove event happens.
    event: even info.
    """
    item = event.getParams()['item']
    ivItem = self.findIVItem(item)
    self.removeIsoViewItem(ivItem)
        
  def addIsoViewItem(self, ivItem, itemList = None):
    """ Inserts a new item view.
    ivItem: item view.
    """
    self.__isoViewItems.append(ivItem)
    self.__parent.addSprite(ivItem.getImg())
    self.__spritesDict[ivItem.getImg()] = ivItem
    pos = ivItem.getPosition()
    self.updateScreenPositionsOn(pos, itemList)

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
    """ Updates the screen position for all items located on a specific position.
    event: event info.
    """      
    self.updateScreenPositionsOn(event.getParams()['position'])
    
  def floorChanged(self, event):
    """ Changes the floor tile's images.
    event: event info.
    """
    newTiles = event.getParams()['newTile']
    for x in range(len(self.__tileList)):
      for y in range(len(self.__tileList[x])):
        self.__tileList[x][y].setImg(os.path.join(GG.utils.TILE, newTiles[x][y]))
    
  def updateScreenPositionsOn(self, pos, itemList=None):
    """ Updates the screen cords of all items on a room position.
    pos: room position.
    itemList: items located on the selected room position.
    """
    tile = self.__tileList[pos[0]][pos[1]].getModel()
    if not itemList:
      itemList = tile.getItems()
    accHeight = 0
    accWidth = 0
    i = 0
    for item in itemList:
      ivIt = self.findIVItem(item)
      if ivIt:  
        scPos = GG.utils.p3dToP2d(ivIt.getPosition(), ivIt.anchor)
        if i == 0:
          zOrder = ivIt.getZOrder()
          i = 1
        else:
          zOrder += 2
        ivIt.setScreenPosition([scPos[0] + accWidth, scPos[1] - accHeight])
        ivIt.updateZOrder(zOrder)
        accWidth += ivIt.topAnchor[0] 
        accHeight += ivIt.topAnchor[1]
          
  def getFutureScreenPosition(self, ivItem, pos, itemList):
    """ Returns the future screen cords for an item moving to a room position.
    ivItem: item.
    pos: room position.
    itemList: items located on the selected room position.
    """  
    tile = self.__tileList[pos[0]][pos[1]].getModel()
    accHeight = 0
    accWidth = 0 
    itemModel = ivItem.getModel()
    listaAux = itemList
    for item in listaAux:
      ivIt = self.findIVItem(item)
      accWidth += ivIt.topAnchor[0] 
      accHeight += ivIt.topAnchor[1]
    scPos = GG.utils.p3dToP2d(pos, ivItem.anchor)
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
    #for item in self.__isoViewItems:
    #  item.unsubscribeAllEvents()
    observers = []
    for item in self.__isoViewItems:
      observers.append(item)
    self.getModel().unsubscribeEventListObserver(observers)
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
    itemSelected = self.findIVItem(item)
    if itemSelected:
      itemSelected.unselected()
    
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

  def changeAvatarImages(self, avatar, path, timestamp):
    """ Changes the avatar images.
    avatar: player's avatar.
    path: new images path.
    """  
    isoAvatar = self.findIVItem(avatar)
    if isoAvatar:
      isoAvatar.changeAvatarImages(path, timestamp) 
      
  def updateScreenPositions(self):
    """ Updates screen positions for all items on all room positions.
    """  
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
        self.updateScreenPositionsOn(key.getPosition())  

  def getTile(self, pos):
    """ Returns the tile located on selected position.
    pos: selected position.
    """  
    return self.__tileList[pos[0]][pos[1]] 

  def tileImageChange(self, event):
    """ Triggers after receiving a tile image change event.
    event: event info.
    """  
    pos = event.getParams()['pos']
    image = event.getParams()['image']
    self.__tileList[pos[0]][pos[1]].setImg(image)  
