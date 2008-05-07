#!/usr/bin/python2.4

from distutils.core import setup
import os
import sys
import setuptools

class doc(setuptools.Command):
  description = "Genera la documentacion del proyecto"
  user_options = []
  doc_src=  "GG"
  doc_dst="doc"
  excepciones=['__init__.py']# Estos no los quiero documentar
  
  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    try:
      import pydoc
    except:
      print "No se encuentra pydoc. No puedo seguir"
      sys.exit(256)
    
    if not os.path.isdir(self.doc_dst):
      os.mkdir(self.doc_dst)
    os.chdir(self.doc_dst)
    print "Generando documentacion de %s..."%self.doc_src,
    pydoc.writedoc(self.doc_src)
    for file in os.listdir('../'+self.doc_src):
      if file.split('.')[-1] == 'py' and file not in self.excepciones:
        print "Generando documentacion de %s..."%file,
        pydoc.writedoc("%s.%s"%(self.doc_src,file.split('.')[0]))
      elif os.path.isdir('../'+self.doc_src+"/"+file):
        pydoc.writedoc("%s.%s"%(self.doc_src,file))
        for subfile in os.listdir('../'+self.doc_src+"/"+file):
          if subfile.split('.')[-1] == 'py' and subfile not in self.excepciones:
            print "Generando documentacion de %s..."%subfile,
            pydoc.writedoc("%s.%s.%s"%(self.doc_src,file,subfile.split('.')[0]))


setup (  
        cmdclass={"doc": doc},
        name = "genteguada",
        version = "0.1",
        description = "Juego colaborativo 3D",
        author = "Eduardo Alvarado",
        author_email = "ealvarado@igosoftware.es",
        license='(c) Igo Software.',
        platforms= ["UNIX"],
        packages = ["GG","GG.isoview","GG.model"],
        scripts = ["genteguada"],
      )

