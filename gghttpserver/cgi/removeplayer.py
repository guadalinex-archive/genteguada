#!/usr/bin/python

import cgi
import GG.model.ggsystem

print "Content-Type: text/plain\r\n\r\n"

form = cgi.FieldStorage()
name = form.getvalue("user")
try:
  system = GG.model.ggsystem.GGSystem.getInstance()
  if system.deletePlayer(name):
    print "el jugador se elimino correctamente"
  else:
    print "ocurrio un error al eliminar el jugador"
except:
  print "El servidor del juego no esta levantado"


