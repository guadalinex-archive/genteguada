#!/usr/bin/python

from distutils.core import setup
import setuptools

setup (  
        name = "genteguada",
        version = "0.1",
        description = "Juego colaborativo isometrico",
        author = "Eduardo Alvarado",
        author_email = "ealvarado@igosoftware.es",
        license='(c) Igo Software.',
        platforms= ["UNIX"],
        packages = ["GG","GG.isoview","GG.model"],
        scripts = ["genteguada","ggserver"],
      )

