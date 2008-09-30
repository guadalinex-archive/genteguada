# -*- coding: utf-8 -*-

import os
import dMVC.model
import ggmodel
import GG.model.teleport
import GG.model.box_heavy
import GG.model.giver_npc
import GG.model.penguin
import GG.model.pickable_item
import GG.model.web_item
import GG.utils

    
# ======================= CONSTANTS ===========================    
    
IMAGES_DICT = {}
IMAGES_DICT["BoxHeavy"] = {"heavy_box.png": [[26, -10], [0, -12]]}
IMAGES_DICT["Door"] = {}
IMAGES_DICT["Door"]["wooden_door.png"] = [[28, 23], [0, 0]]
IMAGES_DICT["Door"]["wooden_door_a.png"] = [[24, 37], [0, 0]]
IMAGES_DICT["Door"]["wooden_door_b.png"] = [[24, 55], [0, 0]]
IMAGES_DICT["Door"]["armored_door_left.png"] = [[17, 15], [0, 0]]
IMAGES_DICT["Door"]["downArrow.png"] = [GG.utils.FLOOR_SHIFT, [0, 0]]
IMAGES_DICT["Door"]["leftArrow.png"] = [GG.utils.FLOOR_SHIFT, [0, 0]]
IMAGES_DICT["Door"]["rightArrow.png"] = [GG.utils.FLOOR_SHIFT, [0, 0]]
IMAGES_DICT["Door"]["upArrow.png"] = [GG.utils.FLOOR_SHIFT, [0, 0]]
IMAGES_DICT["DoorWithKey"] = IMAGES_DICT["Door"]
IMAGES_DICT["DoorOpenedByPoints"] = IMAGES_DICT["Door"]
IMAGES_DICT["DoorPressedTiles"] = IMAGES_DICT["Door"]
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
IMAGES_DICT["WebGift"] = {}
IMAGES_DICT["WebGift"]["gift.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["WebItem"] = IMAGES_DICT["RoomItem"]
IMAGES_DICT["WebItem"]["heavy_box.png"] = [[26, -10], [0, -12]]
IMAGES_DICT["WebItem"]["andatuz_right.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["WebItem"]["andatuz_down.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["WebItem"]["andatuz_bottomright.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["WebItem"]["gift.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["WebItem"]["golden_key.png"] = [[15, -30], [0, 0]]

IMAGES_GIFT_PATH = os.path.join(GG.utils.DATA_PATH, GG.utils.IMAGES_GIFT)

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
    """ Adds a new startRoom.
    startRoom: new start room.
    """  
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
  def defaultView(self, screen, fullscreen, user, accesMode):
    """ Creates the isoview hud.
    screen: screen handler.
    fullscreen: sets view as fullscreen or windowed mode.
    """
    import GG.isoview.isoview_hud
    return GG.isoview.isoview_hud.IsoViewHud(self, screen, fullscreen, user, accesMode)
    
  def chatAdded(self, event):
    """ Triggers after receiving a chat added event.
    event: event info.
    """
    self.triggerEvent('chatAdded', message=event.getParams()['message'], text=event.getParams()['text'], 
                      header=event.getParams()['header'])
  
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
    if self.__system:
      self.__system.logout(self)
      self.__system = None
    self.__player = None
    
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

  def getSystem(self):
    """ Returns the system object.
    """  
    return self.__system  
    
  def newBroadcastMessage(self, line):
    """ Sends a new broadcast message.
    line: new message.
    """  
    self.__system.newBroadcastMessage(line, self.__player)  
    
  def labelChange(self, oldLabel, newLabel):
    """ Changes an item label and all its references on all items.
    oldLabel: old label.
    newLabel: new label.
    """  
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
                   "DoorOpenedByPoints": {
                            "position": pos,
                            "destinationRoom": [self.__player.getRoom().label],
                            "exitPosition": [0, 0],
                            "label": [""],
                            "pointsGiver": [""], 
                            "images": IMAGES_DICT["DoorOpenedByPoints"].keys()                     
                            },
                   "DoorPressedTiles": {
                            "position": pos,
                            "destinationRoom": [self.__player.getRoom().label],
                            "exitPosition": [0, 0],
                            "label": [""],
                            "pressedTile1": [0, 0], 
                            "pressedTile2": [0, 0], 
                            "images": IMAGES_DICT["DoorPressedTiles"].keys()                     
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
                   "WebItem": {
                            "position": pos,
                            "label": [""],
                            "url": [""],
                            "images": IMAGES_DICT["WebItem"].keys()                     
                            },
                   "PickableItem": {
                            "position": pos,
                            "label": [""],
                            "images": IMAGES_DICT["PickableItem"].keys()                     
                            },
                   "PaperMoney": {
                            "position": pos,
                            "label": [""],
                            "images": IMAGES_DICT["PaperMoney"].keys()           
                            },
                   "WebGift": {
                            "position": pos,
                            "label": [""],
                            "images": IMAGES_DICT["WebGift"].keys(),           
                            "imagesGift": self.getImagesGift()          
                            }
                  }
    return self.objectsDict
    
  def createObject(self, name, data):
    """ Creates a new object.
    name: object type.
    data: object data.
    """  
    room = self.__player.getRoom()
    roomSz = room.size
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
    if not (0 <= posX < roomSz[0] and 0 <= posY < roomSz[1]):
      self.__player.newChatMessage("Las coordenadas del objeto no son correctas.", 1)
      return
    #===============================================
    if name == "BoxHeavy":
      box = GG.model.box_heavy.GGBoxHeavy(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], label)
    #===============================================
    elif name == "Door":
      destinationRoom = self.__system.existsRoom(data["destinationRoom"][0])
      if not room or not destinationRoom:
        self.__player.newChatMessage("No existe esa habitación.", 1)
        return
      try: 
        exPosX = int(data["exitPosition"][0])    
        exPosY = int(data["exitPosition"][1])
      except ValueError: 
        self.__player.newChatMessage('Valor "exitPosition" incorrecto', 1) 
        return
      roomSz = destinationRoom.size
      if not (0 <= exPosX < roomSz[0] and 0 <= exPosY < roomSz[1]):
        self.__player.newChatMessage("Las coordenadas de destino no son correctas.", 1)
        return
      box = GG.model.teleport.GGTeleport(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], [exPosX, exPosY], destinationRoom.getName(), label)
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
      if not (0 <= exPosX < roomSz[0] and 0 <= exPosY < roomSz[1]):
        self.__player.newChatMessage("Las coordenadas de destino no son correctas.", 1)
        return
      box = GG.model.teleport.GGDoorWithKey(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], [exPosX, exPosY], destinationRoom.getName(), label, data["key"][0])
    #===============================================
    elif name == "DoorOpenedByPoints":
      destinationRoom = self.__system.existsRoom(data["destinationRoom"][0])
      if not room or not destinationRoom:
        self.__player.newChatMessage("No existe esa habitación.", 1)
        return
      try: 
        exPosX = int(data["exitPosition"][0])    
        exPosY = int(data["exitPosition"][1])
      except ValueError: 
        self.__player.newChatMessage('Valor "exitPosition" incorrecto', 1) 
        return
      pointsGiver = data["pointsGiver"][0]
      roomSz = destinationRoom.size
      if not (0 <= exPosX < roomSz[0] and 0 <= exPosY < roomSz[1]):
        self.__player.newChatMessage("Las coordenadas de destino no son correctas.", 1)
        return
      box = GG.model.teleport.GGDoorOpenedByPoints(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], [exPosX, exPosY], destinationRoom.getName(), label, pointsGiver)
    #===============================================
    elif name == "DoorPressedTiles":
      destinationRoom = self.__system.existsRoom(data["destinationRoom"][0])
      if not room or not destinationRoom:
        self.__player.newChatMessage("No existe esa habitación.", 1)
        return
      try: 
        exPosX = int(data["exitPosition"][0])    
        exPosY = int(data["exitPosition"][1])
      except ValueError: 
        self.__player.newChatMessage('Valor "exitPosition" incorrecto', 1) 
        return
      try: 
        pt1PosX = int(data["pressedTile1"][0])    
        pt1PosY = int(data["pressedTile1"][1])
        pt2PosX = int(data["pressedTile2"][0])    
        pt2PosY = int(data["pressedTile2"][1])
      except ValueError: 
        self.__player.newChatMessage('Valores "pressedTiles" incorrectos', 1) 
        return
      roomSz = destinationRoom.size
      if not (0 <= exPosX < roomSz[0] and 0 <= exPosY < roomSz[1]):
        self.__player.newChatMessage("Las coordenadas de destino no son correctas.", 1)
        return
      if not (0 <= pt1PosX < roomSz[0] and 0 <= pt1PosY < roomSz[1]):
        self.__player.newChatMessage("Las coordenadas de celda no son correctas.", 1)
        return
      pt1 = [pt1PosX, pt1PosY]
      if pt2PosX == "" and pt2PosY == "":
        pt2 = None
      else:
        if not (0 <= pt2PosX < roomSz[0] and 0 <= pt2PosY < roomSz[1]):
          self.__player.newChatMessage("Las coordenadas de celda no son correctas.", 1)
          return
        pt2 = [pt2PosX, pt2PosY]
      box = GG.model.teleport.GGDoorPressedTiles(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], [exPosX, exPosY], destinationRoom.getName(), label, [pt1, pt2])
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
      spriteImg = os.path.join("furniture", img)
      moneyValue = int(img[0:img.find("G")])
      box = GG.model.pickable_item.PaperMoney(spriteImg, IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], label, moneyValue)
    #===============================================
    elif name == "WebGift":
      imgGift = data["imagesGift"]
      if not imgGift:
        self.__player.newChatMessage("Debe seleccionar una imagen de premio para el objeto.", 1)
        return
      spriteImgGift = os.path.join(GG.utils.IMAGES_GIFT, imgGift) 
      spriteImg = os.path.join("furniture", img)
      box = GG.model.giver_npc.WebGift(spriteImg, IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], spriteImgGift, label, self.__player.username)
    #===============================================
    elif name == "WebItem":
      url = data["url"][0]    
      box = GG.model.web_item.GGWebItem(os.path.join("furniture", img), IMAGES_DICT[name][img][0], IMAGES_DICT[name][img][1], url, label)
    #===============================================
    room.addItemFromVoid(box, [posX, posY])
    
  def getImagesGift(self):
    """ Returns all available images for an admin created gift.
    """  
    result = []
    for giftFile in os.listdir(IMAGES_GIFT_PATH):
      if os.path.isfile(os.path.join(IMAGES_GIFT_PATH, giftFile)):
        filepath, fileName = os.path.split(giftFile)
        name, ext = os.path.splitext(fileName)
        if ext in [".jpg", ".png", ".JPG", ".PNG"]:
          result.append(fileName)
    return result

  def getAdminInitData(self):
    package = {}
    package["objectsData"] = self.getObjectsData()
    package["roomList"] = self.getRooms()
    package["roomListLabel"] = self.getRoomLabels()
    package["playerList"] = self.getPlayersList()
    return package
