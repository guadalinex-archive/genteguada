# -*- coding: utf-8 -*-

import dMVC.model
import commands
import os

MAX_PROCESS = 10

class AvatarGenerator(dMVC.model.Model):

  def __init__(self):
    dMVC.model.Model.__init__(self)
    self.__numProcess = 0

  def isFullProcess(self):
    if self.__numProcess < MAX_PROCESS: 
      return False
    return True

  def incNumProcess(self):
    self.__numProcess += 1

  def decNumProcess(self):
    self.__numProcess -= 1
  
  def copyImageMask(self, nameMask, data):
    fileMask = open("/tmp/"+nameMask,"wb")
    fileMask.write(data)
    fileMask.close()

  def executeCommand(self, configuration, player, nameMask):
    comando = self.__generateRenderCommand(player.username, configuration, nameMask)
    print comando
    #return False
    output = commands.getstatusoutput(comando)
    if not output[0] == 0:
      return False
    else:
      return True

  def __generateRenderCommand(self, name, configuration, nameMask):
    command = "avatargenerator "+name
    #gender 
    command += " " + self.__adaptGender(configuration["gender"])
    #headSize
    command += " " + configuration["headSize"]
    #mask
    command += " " + self.__adaptMask(nameMask)
    #hairStyle
    command += " 0" + configuration["hairStyle"]
    #hairColour
    command += " 0" + configuration["hairColor"] + ".tga"
    #skin
    command += " " + self.__adaptIntConfiguration(configuration["skin"])
    #bodySize
    command += " " + configuration["bodySize"]
    #typeShirt
    command += " " + self.__adaptSleeve(configuration)
    #shirt
    command += " " + self.__adaptIntConfiguration(configuration["shirt"])
    #typeTrousers
    command += " " + self.__adaptWinterSummer(configuration["typeTrousers"])
    #trousers
    command += " " + self.__adaptIntConfiguration(configuration["trousers"])
    #skirt
    command += " " + self.__adaptIntConfiguration(configuration["skirt"])
    #shoes
    command += " " + self.__adaptIntConfiguration(configuration["shoes"])
    return command

  def __adaptGender(self, gender):
    if gender == "boy":
      return "male"
    else:
      return "female"

  def __adaptMask(self, nameMask):
    if nameMask is None:
      return "\"\""
    else: 
      return os.path.join("/tmp", nameMask)

  def __adaptIntConfiguration(self, value):
    if value in ["10", "11", "12"]:
      return value + ".tga"
    else:
      return "0" + value +".tga"

  def __adaptSleeve(self, configuration):
    if configuration["gender"] == "boy":
      return self.__adaptWinterSummer(configuration["typeShirt"])
    else:
      return self.__adaptWinterSummer(configuration["typeSkirt"])
  
  def __adaptWinterSummer(self, value):
    if value == "short":
      return "0"
    else:
      return "1"

  def getImages(self, player):
    dirPlayerImages = "/usr/share/avatargenerator/imagesGenerated/"+player.username
    files = {}
    for playerImage in os.listdir(dirPlayerImages):
      filePlayerImage = open(os.path.join(dirPlayerImages, playerImage), "rb")
      files[playerImage] = filePlayerImage.read()
      filePlayerImage.close()
    return files

  def deleteImages(self, player):
    dirPlayerImages = "/usr/share/avatargenerator/imagesGenerated/"+player.username
    for playerImage in os.listdir(dirPlayerImages):
      os.remove(os.path.join(dirPlayerImages, playerImage))
    os.rmdir(dirPlayerImages)

