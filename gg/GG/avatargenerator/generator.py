
import dMVC.model
import commands
import os

class AvatarGenerator(dMVC.model.Model):

  def __init__(self):
    dMVC.model.Model.__init__(self)
  
  def copyImageMask(self, nameMask ,data):
    f = open("/tmp/"+nameMask,"wb")
    f.write(data)
    f.close()

  def executeCommand(self, configuration, player, nameMask):
    comando = self.__generateRenderCommand(player.username, configuration, nameMask)
    output = commands.getstatusoutput(comando)
    if not output[0] == 0:
      return False
    else:
      return True

  def __generateRenderCommand(self, name, configuration, nameMask):
    #gender 
    if configuration["gender"] == "boy":
      configuration["gender"] = "male"
    else:
      configuration["gender"] = "female"
    #mask
    if nameMask is None:
      configuration["mask"] = "\"\""
    else: 
      configuration["mask"] = os.path.join("/tmp",nameMask)
    #hairStyle
    configuration["hairStyle"] = "0"+configuration["hairStyle"]
    #hairColour
    configuration["hairColor"] = "0"+configuration["hairColor"]+".tga"
    #skin
    if configuration["skin"] in ["10","11"]:
      configuration["skin"] = configuration["skin"]+".tga"
    else:
      configuration["skin"] = "0"+configuration["skin"]+".tga"
    #sleeve
    if configuration["gender"] == "male":
      if configuration["typeShirt"] == "short":
        configuration["typeShirt"] = "0"
      else:
        configuration["typeShirt"] = "1"
    else:
      if configuration["typeSkirt"] == "short": 
        configuration["typeShirt"] = "0"
      else:
        configuration["typeShirt"] = "1"
    #shirt
    if configuration["shirt"] in ["10","11","12"]:
      configuration["shirt"] = configuration["shirt"]+".tga"
    else:
      configuration["shirt"] = "0"+configuration["shirt"]+".tga" 
    #typeTrousers
    if configuration["typeTrousers"] == "short":
      configuration["typeTrousers"] = "0"
    else:
      configuration["typeTrousers"] = "1"
    #trousers
    if configuration["trousers"] in ["10","11","12"]:
      configuration["trousers"] = configuration["trousers"]+".tga"
    else:
      configuration["trousers"] = "0"+configuration["trousers"]+".tga"
    #skirt
    if configuration["skirt"] in ["10","11","12"]:
      configuration["skirt"] = configuration["skirt"]+".tga"
    else:
      configuration["skirt"] = "0"+configuration["skirt"]+".tga"
    #shoes
    if configuration["shoes"] in ["10","11"]:
      configuration["shoes"] = configuration["shoes"]+".tga"
    else:
      configuration["shoes"] = "0"+configuration["shoes"]+".tga"

    command = "avatargenerator "+name+" "+configuration["gender"]+" "+configuration["headSize"]+" "+configuration["mask"]+" "+configuration["hairStyle"]+" "+configuration["hairColor"]+" "+configuration["skin"]+" "+configuration["bodySize"]+" "+configuration["typeShirt"]+" "+configuration["shirt"]+" "+configuration["typeTrousers"]+" "+configuration["trousers"]+" "+configuration["skirt"]+" "+configuration["shoes"]
    print command
    return command

  def getImages(self, player):
    dir = "/usr/share/avatargenerator/imagesGenerated/"+player.username
    files = {}
    for file in os.listdir(dir):
      f = open(os.path.join(dir,file),"rb")
      files[file] = f.read()
      f.close()
    return files

  def deleteImages(self, player):
    dir = "/usr/share/avatargenerator/imagesGenerated/"+player.username
    for file in os.listdir(dir):
      os.remove(os.path.join(dir,file))
    os.rmdir(dir)

