import os
import pygame

import GG.utils
import isoview
import isoview_tile

import GG.model.player

class GroupSprite(pygame.sprite.OrderedUpdates):

  def __init__(self, *sprites):
    pygame.sprite.OrderedUpdates.__init__(self, *sprites)
  
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
    bgPath = os.path.join(GG.utils.DATA_PATH, GG.utils.BG_BLACK)
    self.__bg = pygame.sprite.Sprite()
    self.__bg.image = pygame.image.load(bgPath).convert_alpha()
    self.__bg.rect = self.__bg.image.get_rect()
    self.__bg.rect.topleft = GG.utils.BG_FULL_OR
    self.__isoViewPlayers = []
    self.__allPlayers = GroupSprite()
    self.__tileList = []
    for x in range(GG.utils.SCENE_SZ[0]):
      listTile = []
      for z in range(GG.utils.SCENE_SZ[1]):
        varPos = self.p3dToP2d([x, 0, z], GG.utils.FLOOR_SHIFT)
        pos = [int(varPos[0]),int(varPos[1])]
        isotile = isoview_tile.IsoViewTile( [pos[0], pos[1]], [pos[0] + GG.utils.TILE_SZ[0], pos[1] + GG.utils.TILE_SZ[1]], self.getModel().spriteFull, GG.utils.TILE_SZ, 0, [x,0,z])
        self.__allPlayers.add(isotile.getImg())
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
    self.__allPlayers.update()                     
    dirtyRects = self.__allPlayers.draw(self.getScreen())
    #print dirtyRects
    pygame.display.update(dirtyRects)
    
  def getIsoviewPlayers(self):
    return self.__isoViewPlayers
    
  def orderSprites(self):
    """ Order the sprites according to their position.
    """
    #allPlayersTemp = pygame.sprite.OrderedUpdates()
    allPlayersTemp = []
    for image in self.__allPlayers:
    #  print image.rect.topleft[1]
      allPlayersTemp.append([image, image.rect.topleft[1]])
      self.__allPlayers.remove(image)
    allPlayersTemp = sorted(allPlayersTemp, key=operator.itemgetter(1), reverse=True)
    self.__allPlayers = allPlayersTemp
    while len(allPlayersTemp):
      #print allPlayersTemp[0]
      self.__allPlayers.append(allPlayersTemp.pop()[0])
    
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

  def findTile(self,pos):
    """ Gets the 3d tile coords that match a 2d point.
    pos: 2d coords.
    """
    for x in range(GG.utils.SCENE_SZ[0]):
      for z in range(GG.utils.SCENE_SZ[1]):
        if self.__tileList[x][z].contained(pos):
          if not self.__tileList[x][z].onBlank(pos):
            #return [x-1, z+1]
            return [x, z]
    return [-1, -1]
  
  def itemAdded(self, event):
    """ Updates the room view when an item add event happens.
    event: even info.
    """
    # print "anadido", event.getParams()['item']
    for ivitem in self.__isoViewPlayers:
      if isinstance(ivitem.getModel(), GG.model.player.GGPlayer) and isinstance(event.getParams()['item'], GG.model.player.GGPlayer):
        if ivitem.getModel().username == event.getParams()['item'].username:
          # encontrado duplicado
          return
    # no encontrado duplicado
    self.addIsoViewItem(event.getParams()['item'].defaultView(self.getScreen(), self, self.__parent))
        
  def changeActiveRoom(self, event):
    #print "evento en ejecucion"
    pass
  
  def itemRemoved(self, event):
    """ Updates the room view when an item remove event happens.
    event: even info.
    """
    # print "player removed"
    removed = False
    for ivplayer in self.__isoViewPlayers:
      if ivplayer.getModel() == event.getParams()['item']:
        self.removeIsoViewItem(ivplayer)
        removed = True
    if not removed:
      raise "Error: vista de item no eliminada"
        
  def addIsoViewItem(self, item):
    """ Inserts a new item view.
    item: item view.
    """
    self.__isoViewPlayers.append(item)
    self.__allPlayers.add(item.getImg())
    #self.draw()
    
  def removeIsoViewItem(self, player):
    """ Removes an isometric player viewer from the viewers list.
    player: player view to be removed.
    """
    self.__isoViewPlayers.remove(player)
    self.__allPlayers.remove(player.getImg())
    player.unsubscribeAllEvents()
    #self.draw()
  
  def unsubscribeAllEvents(self):
    isoview.IsoView.unsubscribeAllEvents(self)
    for item in self.__isoViewPlayers:
      item.unsubscribeAllEvents()
      
