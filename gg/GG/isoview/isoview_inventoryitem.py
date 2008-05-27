import isoview
import ocempgui.widgets
import GG.utils

class IsoViewInventoryItem(isoview.IsoView):
  """ IsoViewInventoryItem class.
  Defines an inventory item view.
  """
    
  def __init__(self, model, screen, isohud):
    """ Class constructor.
    model: inventory item model.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__spriteName = model.spriteInventory
    self.__label = model.label
    self.__count = 0
    self.__isohud = isohud

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
    imgInventory = ocempgui.widgets.ImageButton(os.path.join(GG.utils.DATA_PATH, self.__spriteName))
    imgInventory.border = 0
    imgInventory.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.selected)
    render.get_managers()[0].add_high_priority_object(imgInventory,ocempgui.widgets.Constants.SIG_MOUSEDOWN)
    return imgInventory

  def selected(self):
    self.__isohud.itemInventorySelected(self)
