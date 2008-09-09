# -*- coding: utf-8 -*-

import os
import dMVC.model
import ggmodel
import GG.model.teleport
import GG.model.box_heavy
import GG.utils

    
# ======================= CONSTANTS ===========================    
    
IMAGES_DICT = {}
IMAGES_DICT["BoxHeavy"] = {"heavy_box.png": [[26, -10], [0, -12]]}
IMAGES_DICT["Door"] = {}
IMAGES_DICT["Door"]["wooden_door.png"] = [[28, 23], [0, 0]]
IMAGES_DICT["Door"]["wooden_door_a.png"] = [[24, 37], [0, 0]]
IMAGES_DICT["Door"]["wooden_door_b.png"] = [[24, 55], [0, 0]]
IMAGES_DICT["Door"]["armored_door_left.png"] = [[17, 15], [0, 0]]
IMAGES_DICT["DoorWithKey"] = IMAGES_DICT["Door"]
IMAGES_DICT["RoomItem"] = {}
IMAGES_DICT["RoomItem"]["hedge.png"] = [[55, 13], [0, -26]]
IMAGES_DICT["RoomItem"]["fence_up.png"] = [[55, 15], [0, 0]]
IMAGES_DICT["RoomItem"]["fence_left.png"] = [[55, 15], [0, 0]]
IMAGES_DICT["RoomItem"]["tree.png"] = [[100, 150], [0, -26]]
IMAGES_DICT["RoomItem"]["stone_column.png"] = [[13, 15], [0, 0]]
IMAGES_DICT["RoomItem"]["wooden_beam.png"] = [[57, 142], [0, 0]]
IMAGES_DICT["RoomItem"]["wall_left.png"] = [[55, 0], [0, 0]]
IMAGES_DICT["RoomItem"]["wall_up.png"] = [[35, 10], [0, 0]]
IMAGES_DICT["RoomItem"]["yard_up.png"] = [[25, 50], [0, 0]]
IMAGES_DICT["RoomItem"]["yard_left.png"] = [[45, 50], [0, 0]]
IMAGES_DICT["RoomItem"]["yard_lamp_up.png"] = [[25, 50], [0, 0]]
IMAGES_DICT["RoomItem"]["yard_lamp_left.png"] = [[45, 50], [0, 0]]
IMAGES_DICT["RoomItem"]["yard_corner.png"] = [[55, 45], [0, 0]]
IMAGES_DICT["RoomItem"]["warehouseWallUp01.png"] = [[35, 33], [0, 0]]
IMAGES_DICT["RoomItem"]["warehouseWallUp02.png"] = [[35, 33], [0, 0]]
IMAGES_DICT["RoomItem"]["warehouseWallLeft01.png"] = [[35, 33], [0, 0]]
IMAGES_DICT["RoomItem"]["warehouseWallLeft02.png"] = [[35, 33], [0, 0]]
IMAGES_DICT["RoomItem"]["warehouseWallCorner.png"] = [[35, 33], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallUp01.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallUp02.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallUp03.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallUp04.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallLeft01.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallLeft02.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineCorner.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["PenguinTalker"] = {}
IMAGES_DICT["PenguinTalker"]["andatuz_right.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["PenguinTalker"]["andatuz_down.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["PenguinTalker"]["andatuz_bottomright.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["PenguinTrade"] = IMAGES_DICT["PenguinTalker"]
IMAGES_DICT["PenguinQuiz"] = IMAGES_DICT["PenguinTalker"]
IMAGES_DICT["GiverNpc"] = {}
IMAGES_DICT["GiverNpc"]["gift.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["GiverNpc"]["golden_key.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["PickableItem"] = {}
IMAGES_DICT["PickableItem"]["gift.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["PickableItem"]["golden_key.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["PaperMoney"] = {}
IMAGES_DICT["PaperMoney"]["5Guadapuntos.png"] = [[14, -25], [0, -10]]
IMAGES_DICT["PaperMoney"]["10Guadapuntos.png"] = [[14, -25], [0, -10]]
IMAGES_DICT["PaperMoney"]["50Guadapuntos.png"] = [[14, -25], [0, -10]]

# ====================================================================
class GGSession(ggmodel.GGModel):
  """ GGSession class.
  Includes room and player objects, and some procedures to manage data.
  """
    
  def __init__(self, player, system):
    """ Initializes session attributes.
    player: session user.
    system: system object
    """
    ggmodel.GGModel.__init__(self)
    self.__player = player
    self.__system = system
    player.subscribeEvent('chatAdded', self.chatAdded)
    player.getRoom().subscribeEvent('chatAdded', self.chatAdded)
    player.subscribeEvent('roomChanged', self.roomChanged)
      
  def setStartRoom(self, room, startRoom):
    self.__system.setStartRoom(room, startRoom)
      
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
      
  @dMVC.model.localMethod
  def defaultView(self, screen, fullscreen):
    """ Esto deberia ser IsoViewSession.
    screen: screen handler.
    """
    import GG.isoview.isoview_hud
    return GG.isoview.isoview_hud.IsoViewHud(self, screen, fullscreen)
    
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
    """ Unsubscribes itself from all events.
    """
    self.__player.getRoom().unsubscribeEventObserver(self)
    self.__player.unsubscribeEventObserver(self)

  def logout(self):
    """ Logs out and ends session.
    """  
    self.__system.logout(self)
    self.__player = None
    self.__system = None
    
  def getRoomLabels(self):
    """ Returns rooms labels.
    """  
    return self.__system.getRoomLabels()  

  def getRooms(self):
    """ Returns the room list.
    """  
    return self.__system.getRooms()  

  def getRoom(self, roomLabel):
    """ Returns one specific room.
    roomLabel: room label.
    """  
    return self.__system.existsRoom(roomLabel)

  def getPlayersList(self):
    """ Returns the player's list.
    """  
    return self.__system.getPlayersList()    

  def getSpecificPlayer(self, name):
    """ Returns a specific player.
    name: player name.
    """  
    return self.__system.getSpecificPlayer(name)  
    
  def newBroadcastMessage(self, line):
    self.__system.newBroadcastMessage(line, self.__player)  
    
  def labelChange(self, oldLabel, newLabel):
    self.__system.labelChange(oldLabel, newLabel)
    
  def getObjectsData(self):
    """ Returns the objects data.
    """  
    if not self.__player.getAccessMode():
      return None  
    pos = self.__player.getRoom().getNearestEmptyCell(self.__player.getPosition())
    self.objectsDict = {
                   "BoxHeavy": {
                            "position": pos,
                            "label": [""],
                            "images": IMAGES_DICT["BoxHeavy"].keys() 
                            },
                   "Door": {
                            "position": pos,
                            "destinationRoom": [self.__player.getRoom().label],
                            "exitPosition": [0, 0],
                            "label": [""], 
                            "images": IMAGES_DICT["Door"].keys()                     
                            },
                   "DoorWithKey": {
                            "position": pos,
                            "destinationRoom": [self.__player.getRoom().label],
                            "exitPosition": [0, 0],
                            "label": [""],
                            "key": [""],        
                            "images": IMAGES_DICT["DoorWithKey"].keys()                     
                            },
                   "GiverNpc": {
                            "position": pos,
                            "label": [""],
                            "images": IMAGES_DICT["GiverNpc"].keys()     
                            },
                   "PenguinQuiz": {
                            "position": pos,
                            "label": [""],
                            "filePath": [GG.utils.QUESTIONS_PATH],        
                            "images": IMAGES_DICT["PenguinTalker"].keys()                     
                            },
                   "PenguinTalker": {
                            "position": pos,
                            "label": [""],
                            "message": [""],        
                            "images": IMAGES_DICT["PenguinTalker"].keys()                     
                            },
                   "PenguinTrade": {
                            "position": pos,
                            "label": [""],
                            "gift": [""],        
                            "message": [""],        
                            "images": IMAGES_DICT["PenguinTrade"].keys()                     
                            },
                   "RoomItem": {
                            "position": pos,
                            "images": IMAGES_DICT["RoomItem"].keys()                     
                            },
                   "PickableItem": {
                            "position": pos,
                            "label": [""],
                            "images": IMAGES_DICT["PickableItem"].keys()                     
                            },
                   "PaperMoney": {
                            "position": pos,
                            "label": [""],
                            "value": [5],
                            "images": IMAGES_DICT["PaperMoney"].keys()           
                            }
                  }
    return self.objectsDict
    
  def createObject(self, name, data):
    """ Creates a new object.
    name: object type.
    data: object data.
    """  
    room = self.__player.getRoom()
    roomSz = self.__player.getRoom().size
    try: 
      posX = int(data["position"][0])    
      posY = int(data["position"][1])
    except ValueError: 
      self.__player.newChatMessage('Valor "Position" incorrecto', 1) 
      return
    if not room.getTile([posX, posY]).stepOn():
      self.__player.newChatMessage('No se puede colocar un objeto en esa posicion', 1) 
      return
    if name != "RoomItem":
      label = data["label"][0]  
      if label == "":
        self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
        return
    img = data["images"]
    if not img:
      self.__player.newChatMessage("Debe seleccionar una imagen para el objeto.", 1)
      return
    if not (0 <= posX <= roomSz[0] and 0 <= posY <= roomSz[1]):
      self.__player.newChatMessage("Las coordenadas del objeto no son correctas.", 1)
      return
    #===============================================
    if name == "BoxHeavy":
      box = GG.model.box_heavy.GGBoxHeavy(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], label)
    #===============================================
    elif name == "Door":
      destinationRoom = self.__system.existsRoom(data["destinationRoom"][0])
      if not room or not destinationRoom:
        self.__player.newChatMessage("No existe esa habitaci�n.", 1)
        return
      try: 
        exPosX = int(data["exitPosition"][0])    
        exPosY = int(data["exitPosition"][1])
      except ValueError: 
        self.__player.newChatMessage('Valor "exitPosition" incorrecto', 1) 
        return
      roomSz = destinationRoom.size
      if not (0 <= exPosX <= roomSz[0] and 0 <= exPosY <= roomSz[1]):
        self.__player.newChatMessage("Las coordenadas de destino no son correctas.", 1)
        return
      box = GG.model.teleport.GGDoor(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], [exPosX, exPosY], destinationRoom, label)
    #===============================================
    elif name == "DoorWithKey":
      destinationRoom = self.__system.existsRoom(data["destinationRoom"][0])
      if not room or not destinationRoom:
        self.__player.newChatMessage("No existe esa habitaci�n.", 1)
        return
      if data["key"][0] == "":
        self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
        return
      try: 
        exPosX = int(data["exitPosition"][0])    
        exPosY = int(data["exitPosition"][1])
      except ValueError: 
        self.__player.newChatMessage('Valor "exitPosition" incorrecto', 1) 
        return
      roomSz = destinationRoom.size
      if not (0 <= exPosX <= roomSz[0] and 0 <= exPosY <= roomSz[1]):
        self.__player.newChatMessage("Las coordenadas de destino no son correctas.", 1)
        return
      box = GG.model.teleport.GGDoorWithKey(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], [exPosX, exPosY], destinationRoom, label, data["key"][0])
    #===============================================
    elif name == "GiverNpc":
      box = GG.model.giver_npc.GGGiverNpc(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], os.path.join("furniture", img), label)
    #===============================================
    elif name == "RoomItem":
      box = GG.model.room_item.GGRoomItem(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1])
    #===============================================
    elif name == "PenguinTalker":
      if data["message"][0] == "":
        self.__player.newChatMessage("Debe introducir un mensaje.", 1)
        return
      box = GG.model.penguin.GGPenguinTalker(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], label, data["message"][0])
    #===============================================
    elif name == "PenguinTrade":
      room = self.__player.getRoom()
      if data["gift"][0] == "":
        self.__player.newChatMessage("Debe introducir el nombre del objeto regalo recibido.", 1)
        return
      box = GG.model.penguin.GGPenguinTrade(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], label, data["message"][0], data["gift"][0])
    #===============================================
    elif name == "PenguinQuiz":
      if data["filePath"][0] == "":
        self.__player.newChatMessage("Debe introducir el nombre del fichero de preguntas.", 1)
        return
      box = GG.model.penguin.GGPenguinQuiz(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], label, data["filePath"][0])
    #===============================================
    elif name == "PickableItem":
      box = GG.model.pickable_item.GGPickableItem(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], os.path.join("furniture", img), label)
    #===============================================
    elif name == "PaperMoney":
      try: 
        moneyValue = int(data["value"][0])    
      except ValueError: 
        self.__player.newChatMessage('Valor "value" incorrecto', 1) 
        return
      if not (moneyValue > 0):
        self.__player.newChatMessage("El valor del billete debe ser un numero positivo.", 1)
        return
      spriteImg = os.path.join("furniture", img)
      box = GG.model.pickable_item.PaperMoney(spriteImg, IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], label, moneyValue)
    #===============================================
    room.addItemFromVoid(box, [posX, posY])
    
    
