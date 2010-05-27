# -*- coding: utf-8 -*-

import GG.utils
import os
import pickle

MAILBOX_FILE = os.path.join(GG.utils.SAVE_DATA, "mailbox.serialized")

class MailBox:

  def __init__(self):
    self.__boxes = {}
    self.__loadBox()

  def __loadBox(self):
    if os.path.isfile(MAILBOX_FILE):
      f = open(MAILBOX_FILE, "r")
      self.__boxes = pickle.load(f)
      f.close()

  def __save(self):
    f = open(MAILBOX_FILE, "w")
    pickle.dump(self.__boxes, f)

  def newPlayerActive(self, player):
    username = player.username
    if username in self.__boxes.keys():
      for event in self.__boxes[username]:
        if event["type"] == "deletePlayer":
          player.removePlayerContactFromAgenda(event["username"])
        elif event["type"] == "deleteGift":
          if player.deleteGift(event["gift"]):
            self.deleteEventDeleteGift(event["gift"])
    self.__boxes[username] = []
    self.__save()

  def newEventDeletePlayer(self, connectedPlayers, username):
    connectedUsername = connectedPlayers.keys()
    for key in self.__boxes.keys():
      if not key == username:
        if key in connectedUsername:
          connectedPlayers[key].removePlayerContactFromAgenda(username)
        else:
          eventData = {"type":"deletePlayer","username":username}
          self.__boxes[key].append(eventData)
    del self.__boxes[username]
    self.__save()

  def newEventDeleteGift(self, connectedPlayers, idGift, username=None):
    eventData = {"type":"deleteGift","gift":idGift}
    if username:
      if username in self.__boxes.keys():
        self.__boxes[username].append(eventData)
        self.__save()
        return True
      else:
        return False
    else:
      connectedUsername = connectedPlayers.keys()
      eventKeys = []
      for key in self.__boxes.keys():
        if key in connectedUsername:
          if connectedPlayers[key].deleteGift(idGift):
            return True
        else:
          eventKeys.append(key)
      for key in eventKeys:
        self.__boxes[key].append(eventData)
      self.___save()
      return True
 
  def deleteEventDeleteGift(self, idGift):
    for key in self.__boxes.keys():
      for event in self.__boxes[key]:
        if event["type"] == "deleteGift":
          if event["gift"] == idGift:
            self.__boxes[key].remove(event)
        


