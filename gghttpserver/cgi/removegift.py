#!/usr/bin/python

import cgi
import GG.model.ggsystem

print "Content-Type: text/plain\r\n\r\n"

form = cgi.FieldStorage()
name = form.getvalue("user")
idgift = form.getvalue("id")
try:
  system = GG.model.ggsystem.GGSystem.getInstance()
  if system.deleteGift(idgift, name):
    print "el regalo se elimino correctamente"
  else:
    print "ocurrio un error al eliminar el regalo"
except:
  print "El servidor del juego no esta levantado"
