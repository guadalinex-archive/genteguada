#!/usr/bin/python

import cgi
import os
import pickle
import GG.model.ggsystem

print "Content-Type: text/plain\r\n\r\n"

form = cgi.FieldStorage()
name = form.getvalue("user")
idgift = form.getvalue("id")
try:
  system = GG.model.ggsystem.GGSystem.getInstance()
except:
  system = None
if system:
  if system.deleteGift(idgift, name):
    print "el regalo se elimino correctamente"
  else:
    print "ocurrio un error al eliminar el regalo"
else:
  dir = "/home/jmariscal/proyectos/genteguada/gg/GG/data/savedata/players"
  file = os.path.join(dir,name+".serialized")
  if not os.path.isfile(file):
    print "ERROR!!! no se tienen datos del usuario"
  else:
    f = open(file, "r")
    dict = pickle.load(f)
    f.close()
    list = []
    for itemInventory in dict["inventory"]:
      if str(itemInventory["class"]) == "GGGeneratedGift":
        if not itemInventory["idGift"] == idgift: 
          list.append(itemInventory)
        else:
          print "el regalo se elimino correctamente"
      else:
        list.append(itemInventory)
  dict["inventory"] = list
  f = open(file, "w")
  pickle.dump(dict, f)
  f.close()


