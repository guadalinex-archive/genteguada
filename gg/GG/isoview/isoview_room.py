import pygame
import random
import GG.utils
import isoview
import isoview_tile
import GG.model.player

class GroupSprite(pygame.sprite.Group):
  """ GroupSprite class.
  Redefines an OrderedUpdates sprite group class.
  """
  
  def __init__(self, *sprites):
    """ Constructor method.
    *sprites: sprites list.
    """
    pygame.sprite.Group.__init__(self, *sprites)
  
  def sprites(self):
    """ Order the group sprites according to their position.
    """
    #def sortFunct(x, y):
    #  return (x.rect[1]+x.rect[3]) - (y.rect[1]+y.rect[3])      
    keys = self.spritedict.keys()
    keys.sort(lambda x, y : (x.rect[1]+x.rect[3]) - (y.rect[1]+y.rect[3]))
    #keys.sort(lambda x, y : sortFunct(x, y))
    return keys
  
  
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
    bgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.BG_BLACK)
    self.__bg = pygame.sprite.Sprite()
    self.__bg.image = pygame.image.load(bgPath).convert_alpha()
    self.__bg.rect = self.__bg.image.get_rect()
    self.__bg.rect.topleft = GG.utils.BG_FULL_OR
    self.__isoViewItems = []
    self.__allPlayers = GroupSprite()
    self.__spritesDict = {}
    self.__bottomSpritesDict = {}
    self.__allTopPlayers = GroupSprite()
    self.__allBackground = GroupSprite()
    
    self.__insertedIVItem = None
    
    self.__tileList = []
    
    tiles = model.getTiles()
    
    specialTiles = model.getSpecialTiles()
    
    for corx in range(model.size[0]):
      listTile = []
      for corz in range(model.size[1]):
        varPos = GG.utils.p3dToP2d([corx, 0, corz], GG.utils.FLOOR_SHIFT)
        pos = [int(varPos[0]), int(varPos[1])]
        k = 0
        
        for specTile in specialTiles:
          if specTile[0] == [corx, 0, corz]:    
            isotile = isoview_tile.IsoViewTile(tiles[corx][corz], [pos[0], pos[1]], \
                    [pos[0] + GG.utils.TILE_SZ[0], pos[1] + GG.utils.TILE_SZ[1]], [corx, 0, corz], specTile[1], self.__parent)
            k = 1
        if k == 0:
          isotile = isoview_tile.IsoViewTile(tiles[corx][corz], [pos[0], pos[1]], \
                    [pos[0] + GG.utils.TILE_SZ[0], pos[1] + GG.utils.TILE_SZ[1]], [corx, 0, corz], \
                    tiles[corx][corz].spriteName, self.__parent)
        
        self.__allBackground.add(isotile.getImg())
        self.__bottomSpritesDict[isotile.getImg()] = isotile
        listTile.append(isotile)
      self.__tileList.append(listTile)
    
    for item in self.getModel().getItems():
      isoviewitem = item.defaultView(self.getScreen(), self, self.__parent)
      self.__isoViewItems.append(isoviewitem)
      self.__allPlayers.add(isoviewitem.getImg())
      self.__spritesDict[isoviewitem.getImg()] = isoviewitem
      #print "Insercion en ", pos, ": ", isoviewitem.getModel()
      pos = item.getPosition()
      
    self.getModel().subscribeEvent('addItemFromVoid', self.itemAddedFromVoid)
    self.getModel().subscribeEvent('addItemFromInventory', self.itemAddedFromInventory)
    self.getModel().subscribeEvent('removeItem', self.itemRemoved)
    self.getModel().subscribeEvent('setSpecialTile', self.specialTileAdded)
  
  def stopAnimations(self):
    for item in self.__isoViewItems:
      item.stopAnimation()
  
  def getIsoViewItems(self):
    """ Returns the isometric view handler.
    """
    return self.__isoViewItems
  
  def updateFrame(self, ellapsedTime):
    """ Paints floor, players and items on the room.
    screen: screen handler.
    """
    for isoitem in self.__isoViewItems:
      isoitem.updateFrame(ellapsedTime)

    screen = self.getScreen()
    bg_image = self.__bg.image
    
    # These 3 first sentences clean the unused part of the screen.
    self.__allPlayers.clear(screen, bg_image)
    self.__allTopPlayers.clear(screen, bg_image)
    self.__allBackground.clear(screen, bg_image)

    self.__allBackground.draw(screen)
    self.__allPlayers.draw(screen)
    self.__allTopPlayers.draw(screen)
    
  def getIsoviewPlayers(self):
    """ Returns the isometric view players list.
    """
    return self.__isoViewItems
    
  def findTile(self, pos):
    """ Gets the 3d tile coords that match a 2d point.
    pos: 2d coords.
    """
    for image in self.__spritesDict:
      if self.__spritesDict[image].checkClickPosition(pos):
        return self.__spritesDict[image].getModel().getPosition()
    for image in self.__bottomSpritesDict:
      if self.__bottomSpritesDict[image].checkClickPosition(pos):
        return self.__bottomSpritesDict[image].getModel().position
    return [-1, -1, -1]
  
  def itemAddedFromVoid(self, event):
    """ Updates the room view when an item add event happens.
    event: even info.
    """
    for ivitem in self.__isoViewItems:
      if isinstance(ivitem.getModel(), GG.model.player.GGPlayer) and isinstance(event.getParams()['item'], GG.model.player.GGPlayer):
        if ivitem.getModel().username == event.getParams()['item'].username:
          return
          #raise "Ya existe el usuario dentro de la habitacion" 
    ivItem = event.getParams()['item'].defaultView(self.getScreen(), self, self.__parent)
    self.addIsoViewItem(ivItem)
    
  def itemAddedFromInventory(self, event):
    """ Updates the room view when an item add event happens.
    event: even info.
    """
    for ivitem in self.__isoViewItems:
      if isinstance(ivitem.getModel(), GG.model.player.GGPlayer) and isinstance(event.getParams()['item'], GG.model.player.GGPlayer):
        if ivitem.getModel().username == event.getParams()['item'].username:
          return
          #raise "Ya existe el usuario dentro de la habitacion" 
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
    #self.removeSprite(ivItem.getImg())
    self.removeIsoViewItem(ivItem)
        
  def addIsoViewItem(self, ivItem):
    """ Inserts a new item view.
    ivItem: item view.
    """
    self.__isoViewItems.append(ivItem)
    self.__allPlayers.add(ivItem.getImg())
    self.__spritesDict[ivItem.getImg()] = ivItem
    pos = ivItem.getModel().getPosition()
    self.updateScreenPositionsOn(pos)

  def removeIsoViewItem(self, ivPlayer):
    """ Removes an isometric player viewer from the viewers list.
    ivPlayer: ivPlayer view to be removed.
    """
    self.removeSprite((ivPlayer.getImg()))
    for image in self.__spritesDict:
      if self.__spritesDict[image] == ivPlayer:
        self.removeSprite(image)  
    self.__isoViewItems.remove(ivPlayer)
    ivPlayer.unsubscribeAllEvents()
    
  def updateScreenPositionsOn(self, pos):
    tile = self.__tileList[pos[0]][pos[2]].getModel()
    itemList = tile.getItems()
    accHeight = tile.anchor[0]
    accWidth = tile.anchor[1]
    for item in itemList:
      scPos = GG.utils.p3dToP2d(item.getPosition(), item.anchor)  
      ivIt = self.__parent.findIVItem(item)
      if ivIt != None:  
        ivIt.setScreenPosition([scPos[0] + accWidth, scPos[1] - accHeight])
        accWidth += item.topAnchor[0] 
        accHeight += item.topAnchor[1] 
          
  def getFutureScreenPosition(self, ivItem, pos):
    tile = self.__tileList[pos[0]][pos[2]].getModel()
    itemList = tile.getItems()
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
    self.__isoViewItems.append(ivChatItem)
    self.__allPlayers.add(ivChatItem.getImg())
  
  def specialTileAdded(self, event):
    pos = event.getParams()['position']
    imageName = event.getParams()['imageName']
    tile = self.__tileList[pos[0]][pos[2]].getImg()
    for img in self.__allBackground:
      if img == tile:
        img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(imageName)).convert_alpha()
        self.__tileList[pos[0]][pos[2]].setImg(imageName)
        return
    
  def unsubscribeAllEvents(self):
    """ Unsubscribe this view ands its children from all events.
    """
    for item in self.__isoViewItems:
      item.unsubscribeAllEvents()
    isoview.IsoView.unsubscribeAllEvents(self)

  def itemSelected(self,item):
    """ Sets an item on the room as selected.
    """
    items = self.getModel().getTile(item.getPosition()).getItems()
    for item in items:
      self.findIVItem(item).selected()

  def itemUnselected(self,item):
    """ Sets an item on the room as unselected.
    """
    items = self.getModel().getTile(item.getPosition()).getItems()
    for item in items:
      self.findIVItem(item).unselected()
    
  def setItemOnTile(self, item, position):
    if item == None:
      self.__tileList[position[0]][position[2]].removeTopMostItem()
    else:
      self.__tileList[position[0]][position[2]].addIsoItem(item)      

  def findIVItem(self, item):
    for ivItem in self.__isoViewItems:
      if ivItem.getModel() == item:
        return ivItem
    return None  

  def addSprite(self, sprite):
    self.__allPlayers.add(sprite)
        
  def addTopSprite(self, sprite):
    self.__allTopPlayers.add(sprite)
  
  def removeSprite(self, sprite):
    print "eliminando: ", self.__allPlayers  
    self.__allPlayers.remove(sprite)
    if sprite in self.__spritesDict:
      del self.__spritesDict[sprite]
    print "eliminado: ", self.__allPlayers
    
  def removeTopSprite(self, sprite):
    self.__allTopPlayers.remove(sprite)    
