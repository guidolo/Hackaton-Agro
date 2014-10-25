#!/usr/bin/python

from glob import glob
from utiles import procesarZIP

for archivo in glob("entrada/serie1/*.zip"):
    procesarZIP(archivo)
