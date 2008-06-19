import pygame
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
    keys = self.spritedict.keys()
    keys.sort(lambda x, y : (x.rect[1]+x.rect[3]) - (y.rect[1]+y.rect[3]))
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
    self.__allTopPlayers = GroupSprite()
    self.__allBackground = GroupSprite()
    
    self.__insertedIVItem = None
    
    self.__tileList = []
    
    specialTiles = model.getSpecialTiles()
    
    for corx in range(model.size[0]):
      listTile = []
      for corz in range(model.size[1]):
        varPos = GG.utils.p3dToP2d([corx, 0, corz], GG.utils.FLOOR_SHIFT)
        pos = [int(varPos[0]), int(varPos[1])]
        k = 0
        for specTile in specialTiles:
          if specTile[0] == [corx, 0, corz]:    
            isotile = isoview_tile.IsoViewTile([pos[0], pos[1]], [pos[0] + GG.utils.TILE_SZ[0], pos[1] + GG.utils.TILE_SZ[1]], \
                specTile[1], [corx, 0, corz])
            k = 1
        if k == 0:
          isotile = isoview_tile.IsoViewTile([pos[0], pos[1]], [pos[0] + GG.utils.TILE_SZ[0], pos[1] + GG.utils.TILE_SZ[1]], \
                self.getModel().spriteFull, [corx, 0, corz])
        self.__allBackground.add(isotile.getImg())
        listTile.append(isotile)
      self.__tileList.append(listTile)
    
    for item in self.getModel().getItems():
      isoviewitem = item.defaultView(self.getScreen(), self, self.__parent)
      self.__isoViewItems.append(isoviewitem)
      self.__allPlayers.add(isoviewitem.getImg())
      #print "Insercion en ", pos, ": ", isoviewitem.getModel()
      pos = item.getPosition()
      self.__tileList[pos[0]][pos[2]].addIsoItem(isoviewitem)
    
    self.getModel().subscribeEvent('addItemFromVoid', self.itemAddedFromVoid)
    self.getModel().subscribeEvent('addItemFromInventory', self.itemAddedFromInventory)
    self.getModel().subscribeEvent('removeItem', self.itemRemoved)
    self.getModel().subscribeEvent('setSpecialTile', self.specialTileAdded)
    
    #self.getModel().subscribeEvent('changeActiveRoom', self.changeActiveRoom)
  
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
    
  #def paintPlayers(self):
  #  """ Paints all players on screen.
  #  """
  #  self.__allPlayers.update()                     
  #  self.__allPlayers.clear(self.getScreen(), self.__bg.image)
  #  pygame.display.update(self.__allPlayers.draw(self.getScreen()))
    
  #def paintFloorFull(self):
  #  """ Paints the room's floor using a single sprite.
  #  screen: screen handler.
  #  """
  #  self.getScreen().blit(self.__bg.image, self.__bg.rect)

  def findTile(self, pos):
    """ Gets the 3d tile coords that match a 2d point.
    pos: 2d coords.
    """
    round = self.getModel().size[0]*2 - 1
    halfRound = round/2
    line = round
    while line > 0:   
      if line > halfRound + 1:
        # Mitad inferior
        for x in range(line - (halfRound+1), halfRound + 1):
          z = line - x - 1 
          #print "checked [", x, ", ", z, "]", self.__tileList[x][z].getIsoItem() 
          if self.__tileList[x][z].contained(pos):
            return [x, z]
      elif line < halfRound + 1:
        # Mitad superior
        for x in range(0, line):
          z = line - x - 1
          #print "checked [", x, ", ", z, "]"
          if self.__tileList[x][z].contained(pos):
            return [x, z]
      else:
        # Diagonal media  
        for x in range(0, halfRound + 1):
          z = halfRound - x
          #print "checked [", x, ", ", z, "]"
          if self.__tileList[x][z].contained(pos):
            return [x, z]
      line -= 1
    return [-1, -1]
  
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
    pos = item.getPosition()
    for ivplayer in self.__isoViewItems:
      if ivplayer.getModel() == item:
        self.__tileList[pos[0]][pos[2]].removeTopMostItem()  
        self.removeIsoViewItem(ivplayer)
        removed = True
    if not removed:
      raise Exception("Error: vista de item no eliminada")
        
  def specialTileAdded(self, event):
    pos = event.getParams()['position']
    imageName = event.getParams()['imageName']
    tile = self.__tileList[pos[0]][pos[2]].getImg()
    for img in self.__allBackground:
      if img == tile:
        img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(imageName)).convert_alpha()
        self.__tileList[pos[0]][pos[2]].setImg(imageName)
        return
        
  def addIsoViewItem(self, ivItem):
    """ Inserts a new item view.
    ivItem: item view.
    """
    self.__isoViewItems.append(ivItem)
    self.__allPlayers.add(ivItem.getImg())
    pos = ivItem.getModel().getPosition()
    self.__tileList[pos[0]][pos[2]].addIsoItem(ivItem)
    ivItem.updateScreenPosition()
    
  def addIsoViewChatItem(self, ivChatItem):
    self.__isoViewItems.append(ivChatItem)
    self.__allPlayers.add(ivChatItem.getImg())
    #ivChatItem.updateScreenPosition()
    
  def removeIsoViewItem(self, ivPlayer):
    """ Removes an isometric player viewer from the viewers list.
    ivPlayer: ivPlayer view to be removed.
    """
    self.__isoViewItems.remove(ivPlayer)
    self.__allPlayers.remove(ivPlayer.getImg())
    ivPlayer.unsubscribeAllEvents()
    pos = ivPlayer.getModel().getPosition()
    self.__tileList[pos[0]][pos[2]].removeTopMostItem()
    
  def unsubscribeAllEvents(self):
    """ Unsubscribe this view ands its children from all events.
    """
    for item in self.__isoViewItems:
      item.unsubscribeAllEvents()
    isoview.IsoView.unsubscribeAllEvents(self)

  def itemSelected(self,item):
    """ Sets an item on the room as selected.
    """
    for isoItem in self.__isoViewItems:
      if isoItem.getModel() == item:
        isoItem.selected()

  def itemUnselected(self,item):
    """ Sets an item on the room as unselected.
    """
    pos = item.getPosition()
    if self.__tileList[pos[0]][pos[2]].getIsoItem() != None:
      self.__tileList[pos[0]][pos[2]].getIsoItem().unselected()
    
    """
    for isoItem in self.__isoViewItems:
      if isoItem.getModel() == item:
        isoItem.unselected()
    """      

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
    self.__allPlayers.remove(sprite)
    
  def removeTopSprite(self, sprite):
    self.__allTopPlayers.remove(sprite)    
