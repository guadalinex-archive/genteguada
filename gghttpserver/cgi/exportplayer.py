#!/usr/bin/python

import cgi
import os
import pickle
import GG.utils

print "Content-Type: text/plain\r\n\r\n"

form = cgi.FieldStorage()
name = form.getvalue("user")
SAVE_DATA_PLAYER = os.path.join(GG.utils.SAVE_DATA, "players")
file = os.path.join(SAVE_DATA_PLAYER,name+".serialized")
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

