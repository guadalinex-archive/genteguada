#!/usr/bin/python

import cgi
import dMVC.remoteclient

print "Content-Type: text/plain\r\n\r\n"

#ERROR:02 => El servidor de genteguada no esta levantado
#ERROR:04 => el jugador no se pudo eliminar debiado a un error

form = cgi.FieldStorage()
name = form.getvalue("user")
try:
  client = dMVC.remoteclient.RClient("localhost", 770)
  system = client.getRootModel()
  if system.deletePlayer(name):
    print "el jugador se elimino correctamente"
  else:
    print "ERROR:04"
except:
  print "ERROR:02"


