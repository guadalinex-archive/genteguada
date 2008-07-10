
import dMVC.model

class AvatarGenerator(dMVC.model.Model):

  def __init__(self):
    dMVC.model.Model.__init__(self)

  def executeCommand(self, configuration, player):
    comando = self.__generateRenderCommand(player.username, configuration)
    """
    output = commands.getstatusoutput(comando)
    if not output[0] == 0:
      print "Ocurrio un error al ejecutar el comando"
    else:
      print "finalizo"
    """

  def __generateRenderCommand(self, name, configuration):
    #gender 
    if configuration["gender"] == "boy":
      configuration["gender"] = "male"
    else:
      configuration["gender"] = "female"
    #mask
    if configuration["mask"] is None:
      configuration["mask"] = "\"\""
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
    return command

