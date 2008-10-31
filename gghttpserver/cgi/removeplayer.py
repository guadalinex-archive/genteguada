#!/usr/bin/python

import cgi
import os
import GG.model.ggsystem
import shutil

print "Content-Type: text/plain\r\n\r\n"

form = cgi.FieldStorage()
name = form.getvalue("user")
try:
  system = GG.model.ggsystem.GGSystem.getInstance()
except:
  system = None
if system:
  if system.deletePlayer(name):
    print "el jugador se elimino correctamente"
  else:
    print "ocurrio un error al eliminar el jugador"
else:
  dir = "/home/jmariscal/proyectos/genteguada/gg/GG/data/savedata/players"
  file = os.path.join(dir,name+".serialized")
  if not os.path.isfile(file):
    print "ERROR!!! no se tienen datos del usuario"
  else:
    os.remove(file)
    if isdir("/home/jmariscal/proyectos/genteguada/gg/GG/data/avatars/"+name):
      shutil.rmtree("/home/jmariscal/proyectos/genteguada/gg/GG/data/avatars/"+name)
    if isfile("/home/jmariscal/proyectos/genteguada/gg/GG/data/avatars/masks/"+name+".png")
      os.remove("/home/jmariscal/proyectos/genteguada/gg/GG/data/avatars/masks/"+name+".png")


