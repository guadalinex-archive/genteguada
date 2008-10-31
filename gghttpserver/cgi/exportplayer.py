#!/usr/bin/python

import cgi
import os
import pickle

print "Content-Type: text/plain\r\n\r\n"

form = cgi.FieldStorage()
name = form.getvalue("user")
dir = "/home/jmariscal/proyectos/genteguada/gg/GG/data/savedata/players"
file = os.path.join(dir,name+".serialized")
if not os.path.isfile(file):
  print "ERROR!!! no se tienen datos del usuario"
else:
  f = open(file, "r")
  dict = pickle.load(f)
  f.close()
  print str(dict["points"])+"#"+str(dict["playedTime"])+"#"+str(dict["exp"])+"\n"
  for itemInventory in dict["inventory"]:
    if str(itemInventory["class"]) == "GGGeneratedGift":
      print str(itemInventory["idGift"])+"#"+str(itemInventory["label"])+"\n"

