import isoview
import ocempgui.widgets
import GG.utils
import GG.utils
import animation
import pygame

class IsoViewInventoryItem(isoview.IsoView):
  """ IsoViewInventoryItem class.
  Defines an inventory item view.
  """
    
  def __init__(self, model, screen, isohud, destination):
    """ Class constructor.
    model: inventory item model.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__spriteName = model.spriteInventory
    self.__label = model.label
    self.__count = 0
    self.__isohud = isohud
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(model.spriteInventory)  
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = GG.utils.p3dToP2d(model.getPosition(), model.offset)
    #self.__isohud.getIsoviewRoom().addSprite(self.__img)

  def getImg(self):
    return self.__img  

  def setScreenPosition(self, pos):
    """ Sets a new position for the item's image.
    pos: new position.
    """
    self.__img.rect.topleft = pos  
  
  def getScreenPosition(self):
    """ Returns the item's image position.
    """
    return self.__img.rect.topleft  
  
  def getSpriteName(self):
    """ Returns the name of the sprite used to paint the item on the inventory.
    """
    return self.__spriteName

  def getLabel(self):
    """ Returns the itemp's label.
    """
    return self.__label
  
  def getCount(self):
    """ Returns the number of stacked items.
    """
    return self.__count
  
  def increaseCount(self):
    """ Increases by 1 the number of stacked items.
    """
    self.__count += 1
    
  def decreaseCount(self):
    """ Decreases by 1 the number of stacked items.
    """
    self.__count -= 1

  def draw(self, render):
    """ Draws an inventory item.
    render: widget container. 
    """
    imgInventory = ocempgui.widgets.ImageButton(GG.genteguada.GenteGuada.getInstance().getDataPath(self.__spriteName))
    imgInventory.border = 0
    imgInventory.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.selected)
    render.get_managers()[0].add_high_priority_object(imgInventory,ocempgui.widgets.Constants.SIG_MOUSEDOWN)
    return imgInventory

  def selected(self): 
    """ Sets this item as selected.
    """
    self.__isohud.itemInventorySelected(self)
