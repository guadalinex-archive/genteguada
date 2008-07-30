#!/usr/bin/python

from distutils.core import setup
import setuptools

setup (  
        name = "genteguada-client",
        version = "0.1",
        description = "Cliente de Juego colaborativo Isomentrico",
        author = "Eduardo Alvarado",
        author_email = "ealvarado@igosoftware.es",
        license='(c) Igo Software.',
        platforms= ["UNIX"],
        packages = ["GG","GG.isoview","GG.model","GG.avatargenerator"],
        scripts = ["genteguada"],
      )

