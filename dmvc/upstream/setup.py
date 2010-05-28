#!/usr/bin/python

from distutils.core import setup
import setuptools

setup (  
        name = "dMVC",
        version = "0.1",
        description = "distributed model view controller",
        author = "Diego Gomez Deck,Joseba Mariscal",
        author_email = "DiegoGomezDeck@consultar.com,jmariscal@igosoftware.es",
        license='(c) Igo Software.',
        platforms= ["UNIX"],
        packages = ["dMVC"]
      )

