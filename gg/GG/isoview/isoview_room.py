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
    self.__isoViewPlayers = []
    self.__allPlayers = GroupSprite()
    self.__allBackground = GroupSprite()
    self.__tileList = []
    for corx in range(GG.utils.SCENE_SZ[0]):
      listTile = []
      for corz in range(GG.utils.SCENE_SZ[1]):
        varPos = GG.utils.p3dToP2d([corx, 0, corz], GG.utils.FLOOR_SHIFT)
        pos = [int(varPos[0]), int(varPos[1])]
        isotile = isoview_tile.IsoViewTile([pos[0], pos[1]], [pos[0] + GG.utils.TILE_SZ[0], pos[1] + GG.utils.TILE_SZ[1]], \
          self.getModel().spriteFull, [corx, 0, corz])
        self.__allBackground.add(isotile.getImg())
        listTile.append(isotile)
      self.__tileList.append(listTile)
    
    for item in self.getModel().getItems():
      isoviewitem = item.defaultView(self.getScreen(), self, self.__parent)
      self.__isoViewPlayers.append(isoviewitem)
      self.__allPlayers.add(isoviewitem.getImg())
    
    self.getModel().subscribeEvent('addItem', self.itemAdded)
    self.getModel().subscribeEvent('removeItem', self.itemRemoved)
    #self.getModel().subscribeEvent('changeActiveRoom', self.changeActiveRoom)
    
  def getIsoViewPlayers(self):
    """ Returns the isometric view handler.
    """
    return self.__isoViewPlayers
  
  def updateFrame(self):
    """ Paints floor, players and items on the room.
    screen: screen handler.
    """
    for isoitem in self.__isoViewPlayers:
      isoitem.updateFrame()
    
    self.__allPlayers.clear(self.getScreen(), self.__bg.image)
    
    self.__allBackground.clear(self.getScreen(), self.__bg.image)
    self.__allBackground.update()                     
    dirtyRects = self.__allBackground.draw(self.getScreen())
    pygame.display.update(dirtyRects)
    
    self.__allPlayers.update()                     
    dirtyRects = self.__allPlayers.draw(self.getScreen())
    pygame.display.update(dirtyRects)
    
  def getIsoviewPlayers(self):
    """ Returns the isometric view players list.
    """
    return self.__isoViewPlayers
    
  def paintPlayers(self):
    """ Paints all players on screen.
    """
    self.__allPlayers.update()                     
    self.__allPlayers.clear(self.getScreen(), self.__bg.image)
    pygame.display.update(self.__allPlayers.draw(self.getScreen()))
    
  def paintFloorFull(self):
    """ Paints the room's floor using a single sprite.
    screen: screen handler.
    """
    self.getScreen().blit(self.__bg.image, self.__bg.rect)

  def findTile(self, pos):
    """ Gets the 3d tile coords that match a 2d point.
    pos: 2d coords.
    """
    for corx in range(GG.utils.SCENE_SZ[0]):
      for corz in range(GG.utils.SCENE_SZ[1]):
        if self.__tileList[corx][corz].contained(pos):
          if not self.__tileList[corx][corz].onBlank(pos):
            return [corx, corz]
    return [-1, -1]
  
  def itemAdded(self, event):
    """ Updates the room view when an item add event happens.
    event: even info.
    """
    for ivitem in self.__isoViewPlayers:
      if isinstance(ivitem.getModel(), GG.model.player.GGPlayer) and isinstance(event.getParams()['item'], GG.model.player.GGPlayer):
        if ivitem.getModel().username == event.getParams()['item'].username:
          return
          #raise "Ya existe el usuario dentro de la habitacion" 
    self.addIsoViewItem(event.getParams()['item'].defaultView(self.getScreen(), self, self.__parent))
        
  def itemRemoved(self, event):
    """ Updates the room view when an item remove event happens.
    event: even info.
    """
    removed = False
    for ivplayer in self.__isoViewPlayers:
      if ivplayer.getModel() == event.getParams()['item']:
        self.removeIsoViewItem(ivplayer)
        removed = True
    if not removed:
      raise Exception("Error: vista de item no eliminada")
        
  def addIsoViewItem(self, item):
    """ Inserts a new item view.
    item: item view.
    """
    self.__isoViewPlayers.append(item)
    self.__allPlayers.add(item.getImg())
    
  def removeIsoViewItem(self, player):
    """ Removes an isometric player viewer from the viewers list.
    player: player view to be removed.
    """
    self.__isoViewPlayers.remove(player)
    self.__allPlayers.remove(player.getImg())
    player.unsubscribeAllEvents()
  
  def unsubscribeAllEvents(self):
    """ Unsubscribe this view ands its children from all events.
    """
    for item in self.__isoViewPlayers:
      item.unsubscribeAllEvents()
    isoview.IsoView.unsubscribeAllEvents(self)

  def itemSelected(self,item):
    """ Sets an item on the room as selected.
    """
    for isoItem in self.__isoViewPlayers:
      if isoItem.getModel() == item:
        isoItem.selected()

  def itemUnselected(self,item):
    """ Sets an item on the room as unselected.
    """
    for isoItem in self.__isoViewPlayers:
      if isoItem.getModel() == item:
        isoItem.unselected()   

  def addSprite(self, sprite):
    self.__allPlayers.add(sprite)
    
  def removeSprite(self, sprite):
    self.__allPlayers.remove(sprite)