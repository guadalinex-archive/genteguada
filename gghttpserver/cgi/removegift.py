#!/usr/bin/python

import cgi
import GG.model.ggsystem

print "Content-Type: text/plain\r\n\r\n"

#ERROR:02 => El servidor de genteguada no esta levantado
#ERROR:03 => el regalo no se pudo eliminar debiado a un error

form = cgi.FieldStorage()
name = form.getvalue("user")
idgift = form.getvalue("id")
try:
  system = GG.model.ggsystem.GGSystem.getInstance()
  if system.deleteGift(idgift, name):
    print "el regalo se elimino correctamente"
  else:
    print "ERROR:03"
except:
  print "ERROR:02"
