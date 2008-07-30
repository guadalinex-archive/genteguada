# -*- coding: iso-8859-15 -*-

import dMVC.model
import ggmodel
import GG.model.teleport
import GG.utils

class GGSession(ggmodel.GGModel):
  """ GGSession class.
  Includes room and player objects, and some procedures to manage data.
  """
    
  def __init__(self, player, system):
    """ Initializes session attributes.
    player: session user.
    """
    ggmodel.GGModel.__init__(self)
    self.__player = player
    self.__system = system
    player.subscribeEvent('chatAdded', self.chatAdded)
    player.getRoom().subscribeEvent('chatAdded', self.chatAdded)
    #player.getRoom().subscribeEvent('quizAdded', self.quizAdded)
    player.subscribeEvent('roomChanged', self.roomChanged)
      
  # self.__player
  
  def getPlayer(self):
    """ Returns the active player.
    """
    return self.__player
   
  def roomChanged(self, event):
    """ Triggers after receiving a change room event.
    event: event info.
    """
    oldRoom = event.getParams()['oldRoom']
    if oldRoom:
      oldRoom.unsubscribeEventMethod(self.chatAdded)
    newRoom = self.__player.getRoom()
    if newRoom: 
      newRoom.subscribeEvent('chatAdded', self.chatAdded)
      #self.__player.subscribeEvent('chatAdded', self.chatAdded)
      
      #newRoom.subscribeEvent('quizAdded', self.quizAdded)
    
  @dMVC.model.localMethod
  def defaultView(self, screen, parent, fullscreen):
    """ Esto deberia ser IsoViewSession.
    screen: screen handler.
    """
    import GG.isoview.isoview_hud
    return GG.isoview.isoview_hud.IsoViewHud(self, screen, parent, fullscreen)
    
  def chatAdded(self, event):
    """ Triggers after receiving a chat added event.
    event: event info.
    """
    self.triggerEvent('chatAdded', message=event.getParams()['message'])
  
  def quizAdded(self, event):
    """ Triggers after receiving a chat added event.
    event: event info.
    """
    self.triggerEvent('quizAdded', message=event.getParams()['message'])

  def unsubscribeEvents(self):
    self.__player.getRoom().unsubscribeEventObserver(self)
    self.__player.unsubscribeEventObserver(self)

  def logout(self):
    self.__system.logout(self)
    self.__player = None
    self.__system = None
    
  def getObjectsData(self):
    if not self.__player.getAccessMode():
      return None  
    
    objectsDict = {
                   "BoxHeavy": {"room": [self.__player.getRoom().label], 
                            "position": self.__player.getRoom().getNearestEmptyCell(self.__player.getPosition()),
                            "label": [""]                            
                            },
                   "Door": {"room": [self.__player.getRoom().label], 
                            "position": self.__player.getRoom().getNearestEmptyCell(self.__player.getPosition()),
                            "destinationRoom": [self.__player.getRoom().label],
                            "exitPosition": [0, 0, 0],
                            "label": [""]                            
                            },
                   "DoorWithKey": {"room": [self.__player.getRoom().label], 
                            "position": self.__player.getRoom().getNearestEmptyCell(self.__player.getPosition()),
                            "destinationRoom": [self.__player.getRoom().label],
                            "exitPosition": [0, 0, 0],
                            "label": [""],
                            "key": [""]        
                            }
                  }
    
    return objectsDict
    
  def createObject(self, name, data):
    print "*** Nuevo objeto: ", name
    print "*** ", data
    
    try: 
      posX = int(data["position"][0])    
      posY = int(data["position"][1])
      posZ = int(data["position"][2])
    except ValueError: 
      self.__player.newChatMessage("Valor \"Position\" incorrecto", 1) 
      return
    
    if name == "Door":
      room = self.__system.existsRoom(data["room"][0])
      destinationRoom = self.__system.existsRoom(data["destinationRoom"][0])
      if not room or not destinationRoom:
        self.__player.newChatMessage("No existe esa habitación.", 1)
        return
      if data["label"][0] == "":
        self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
        return
       
      try: 
        exPosX = int(data["exitPosition"][0])    
        exPosY = int(data["exitPosition"][1])
        exPosZ = int(data["exitPosition"][2])
      except ValueError: 
        self.__player.newChatMessage("Valor \"exitPosition\" incorrecto", 1) 
        return
        
      door = GG.model.teleport.GGDoor("furniture/wooden_door.png", [28, 23], [0, 0], [exPosX, exPosY, exPosZ], destinationRoom, data["label"][0])
      room.addItemFromVoid(door, [posX, posY, posZ])
      
    
    
    
    
    
    
    
    
    
    
    
    