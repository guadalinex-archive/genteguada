# -*- coding: iso-8859-15 -*-

import dMVC.model
import ggmodel
import GG.model.teleport
import GG.model.box_heavy
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
    
  def getRoomLabels(self):
    return self.__system.getRoomLabels()  

  def getRoom(self, roomLabel):
    return self.__system.existsRoom(roomLabel)  
    
  def getObjectsData(self):
    if not self.__player.getAccessMode():
      return None  
    
    self.imagesDict = {}
    
    self.imagesDict["BoxHeavy"] = {"heavy_box.png": [[26, -10], [0, -10]]}
    
    self.imagesDict["Door"] = {}
    self.imagesDict["Door"]["wooden_door.png"] = [[28, 23], [0, 0]]
    self.imagesDict["Door"]["wooden_door_a.png"] = [[24, 37], [0, 0]]
    self.imagesDict["Door"]["wooden_door_b.png"] = [[24, 55], [0, 0]]
    self.imagesDict["Door"]["armored_door_left.png"] = [[17, 15], [0, 0]]
    
    self.imagesDict["DoorWithKey"] = self.imagesDict["Door"]
    
    self.imagesDict["RoomItem"] = {}
    self.imagesDict["RoomItem"]["hedge.png"] = [[55, 13], [0, -26]]
    self.imagesDict["RoomItem"]["fence_up.png"] = [[55, 15], [0, 0]]
    self.imagesDict["RoomItem"]["fence_left.png"] = [[55, 15], [0, 0]]
    self.imagesDict["RoomItem"]["tree.png"] = [[100, 150], [0, -26]]
    self.imagesDict["RoomItem"]["stone_column.png"] = [[13, 15], [0, 0]]
    self.imagesDict["RoomItem"]["wooden_beam.png"] = [[57, 142], [0, 0]]
    self.imagesDict["RoomItem"]["wall_left.png"] = [[55, 0], [0, 0]]
    self.imagesDict["RoomItem"]["wall_up.png"] = [[35, 10], [0, 0]]
    self.imagesDict["RoomItem"]["yard_up.png"] = [[25, 50], [0, 0]]
    self.imagesDict["RoomItem"]["yard_left.png"] = [[45, 50], [0, 0]]
    self.imagesDict["RoomItem"]["yard_lamp_up.png"] = [[25, 50], [0, 0]]
    self.imagesDict["RoomItem"]["yard_lamp_left.png"] = [[45, 50], [0, 0]]
    self.imagesDict["RoomItem"]["yard_corner.png"] = [[55, 45], [0, 0]]
    self.imagesDict["RoomItem"]["warehouseWallUp01.png"] = [[35, 33], [0, 0]]
    self.imagesDict["RoomItem"]["warehouseWallUp02.png"] = [[35, 33], [0, 0]]
    self.imagesDict["RoomItem"]["warehouseWallLeft01.png"] = [[35, 33], [0, 0]]
    self.imagesDict["RoomItem"]["warehouseWallLeft02.png"] = [[35, 33], [0, 0]]
    self.imagesDict["RoomItem"]["warehouseWallCorner.png"] = [[35, 33], [0, 0]]
    self.imagesDict["RoomItem"]["skylineWallUp01.png"] = [[35, 40], [0, 0]]
    self.imagesDict["RoomItem"]["skylineWallUp02.png"] = [[35, 40], [0, 0]]
    self.imagesDict["RoomItem"]["skylineWallUp03.png"] = [[35, 40], [0, 0]]
    self.imagesDict["RoomItem"]["skylineWallUp04.png"] = [[35, 40], [0, 0]]
    self.imagesDict["RoomItem"]["skylineWallLeft01.png"] = [[35, 40], [0, 0]]
    self.imagesDict["RoomItem"]["skylineWallLeft02.png"] = [[35, 40], [0, 0]]
    self.imagesDict["RoomItem"]["skylineCorner.png"] = [[35, 40], [0, 0]]
    
    self.imagesDict["PenguinTalker"] = {}
    self.imagesDict["PenguinTalker"]["andatuz_right.png"] = [[30, 0], [0, 0]]
    self.imagesDict["PenguinTalker"]["andatuz_down.png"] = [[30, 0], [0, 0]]
    self.imagesDict["PenguinTalker"]["andatuz_bottomright.png"] = [[30, 0], [0, 0]]

    self.imagesDict["PenguinTrade"] = self.imagesDict["PenguinTalker"]
    
    self.imagesDict["PenguinQuiz"] = self.imagesDict["PenguinTalker"]
    
    pos = self.__player.getRoom().getNearestEmptyCell(self.__player.getPosition())
    
    self.objectsDict = {
                   "BoxHeavy": {
                            "position": [pos[0], pos[2]],
                            "label": [""],
                            "images": self.imagesDict["BoxHeavy"].keys() 
                            },
                   "Door": {
                            "position": [pos[0], pos[2]],
                            "destinationRoom": [self.__player.getRoom().label],
                            "exitPosition": [0, 0],
                            "label": [""], 
                            "images": self.imagesDict["Door"].keys()                     
                            },
                   "DoorWithKey": {
                            "position": [pos[0], pos[2]],
                            "destinationRoom": [self.__player.getRoom().label],
                            "exitPosition": [0, 0],
                            "label": [""],
                            "key": [""],        
                            "images": self.imagesDict["DoorWithKey"].keys()                     
                            },
                   "PenguinQuiz": {
                            "position": [pos[0], pos[2]],
                            "label": [""],
                            "filePath": [GG.utils.QUESTIONS_PATH],        
                            "images": self.imagesDict["PenguinTalker"].keys()                     
                            },
                   "PenguinTalker": {
                            "position": [pos[0], pos[2]],
                            "label": [""],
                            "message": [""],        
                            "images": self.imagesDict["PenguinTalker"].keys()                     
                            },
                   "PenguinTrade": {
                            "position": [pos[0], pos[2]],
                            "label": [""],
                            "gift": [""],        
                            "images": self.imagesDict["PenguinTrade"].keys()                     
                            },
                   "RoomItem": {
                            "position": [pos[0], pos[2]],
                            "images": self.imagesDict["RoomItem"].keys()                     
                            }
                  }
    
    return self.objectsDict
    
  def createObject(self, name, data):
    print "*** Nuevo objeto: ", name
    print "*** ", data
    
    try: 
      posX = int(data["position"][0])    
      posZ = int(data["position"][1])
    except ValueError: 
      self.__player.newChatMessage("Valor \"Position\" incorrecto", 1) 
      return
    
    if name == "Door":
      #room = self.__system.existsRoom(data["room"][0])  
      room = self.__player.getRoom()
      destinationRoom = self.__system.existsRoom(data["destinationRoom"][0])
      if not room or not destinationRoom:
        self.__player.newChatMessage("No existe esa habitación.", 1)
        return
      if data["label"][0] == "":
        self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
        return
      try: 
        exPosX = int(data["exitPosition"][0])    
        exPosZ = int(data["exitPosition"][1])
      except ValueError: 
        self.__player.newChatMessage("Valor \"exitPosition\" incorrecto", 1) 
        return
      img = data["images"]
      door = GG.model.teleport.GGDoor("furniture/" + img, self.imagesDict[name][img][0], 
                                      self.imagesDict[name][img][1], [exPosX, 0, exPosZ], destinationRoom, 
                                      data["label"][0])
      room.addItemFromVoid(door, [posX, 0, posZ])

    #-----------------------------------------------

    if name == "DoorWithKey":
      #room = self.__system.existsRoom(data["room"][0])
      room = self.__player.getRoom()
      destinationRoom = self.__system.existsRoom(data["destinationRoom"][0])
      if not room or not destinationRoom:
        self.__player.newChatMessage("No existe esa habitación.", 1)
        return
      if data["label"][0] == "":
        self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
        return
      if data["key"][0] == "":
        self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
        return
      try: 
        exPosX = int(data["exitPosition"][0])    
        exPosY = int(data["exitPosition"][1])
        exPosZ = int(data["exitPosition"][2])
      except ValueError: 
        self.__player.newChatMessage("Valor \"exitPosition\" incorrecto", 1) 
        return
      img = data["images"]
      door = GG.model.teleport.GGDoorWithKey("furniture/" + img, self.imagesDict[name][img][0], \
                                             self.imagesDict[name][img][1], [exPosX, 0, exPosZ], destinationRoom, 
                                             data["label"][0], data["key"][0])
      room.addItemFromVoid(door, [posX, 0, posZ])

    #-----------------------------------------------
    
    if name == "BoxHeavy":
      room = self.__player.getRoom()
      if data["label"][0] == "":
        self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
        return
      img = data["images"]
      box = GG.model.box_heavy.GGBoxHeavy("furniture/" + img, self.imagesDict[name][img][0], self.imagesDict[name][img][1], data["label"][0])
      room.addItemFromVoid(box, [posX, 0, posZ])
    
    #-----------------------------------------------
    
    if name == "RoomItem":
      room = self.__player.getRoom()
      img = data["images"]
      box = GG.model.room_item.GGRoomItem("furniture/" + img, self.imagesDict[name][img][0], self.imagesDict[name][img][1])
      room.addItemFromVoid(box, [posX, 0, posZ])
    
    #-----------------------------------------------
    
    if name == "PenguinTalker":
      room = self.__player.getRoom()
      if data["label"][0] == "":
        self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
        return
      if data["message"][0] == "":
        self.__player.newChatMessage("Debe introducir un mensaje.", 1)
        return
      img = data["images"]
      box = GG.model.penguin.GGPenguinTalker("furniture/" + img, self.imagesDict[name][img][0], self.imagesDict[name][img][1], data["label"][0], data["message"][0])
      room.addItemFromVoid(box, [posX, 0, posZ])
    
    #-----------------------------------------------
    
    if name == "PenguinTrade":
      room = self.__player.getRoom()
      if data["label"][0] == "":
        self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
        return
      if data["gift"][0] == "":
        self.__player.newChatMessage("Debe introducir el nombre del objeto regalo recibido.", 1)
        return
      img = data["images"]
      box = GG.model.penguin.GGPenguinTrade("furniture/" + img, self.imagesDict[name][img][0], self.imagesDict[name][img][1], data["label"][0], data["gift"][0])
      room.addItemFromVoid(box, [posX, 0, posZ])

    #-----------------------------------------------
    
    if name == "PenguinQuiz":
      room = self.__player.getRoom()
      if data["label"][0] == "":
        self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
        return
      if data["filePath"][0] == "":
        self.__player.newChatMessage("Debe introducir el nombre del fichero de preguntas.", 1)
        return
      img = data["images"]
      box = GG.model.penguin.GGPenguinQuiz("furniture/" + img, self.imagesDict[name][img][0], self.imagesDict[name][img][1], data["label"][0], data["filePath"][0])
      room.addItemFromVoid(box, [posX, 0, posZ])

    
    