#!/usr/bin/python

import cgi
import dMVC.remoteclient

print "Content-Type: text/plain\r\n\r\n"

#ERROR:02 => El servidor de genteguada no esta levantado
#ERROR:03 => el regalo no se pudo eliminar debiado a un error

form = cgi.FieldStorage()
name = form.getvalue("user")
idgift = form.getvalue("id")
try:
  client = dMVC.remoteclient.RClient("localhost", 770)
  system = client.getRootModel()
  if system.deleteGift(idgift, name):
    print "el regalo se elimino correctamente"
  else:
    print "ERROR:03"
except:
  print "ERROR:02"
