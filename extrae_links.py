#!/usr/bin/python

from utiles import shp2dataframe

data = shp2dataframe('./datos/files_2.dbf')

for i in data['ID']:
    nombre = i + '.zip'
    url = "http://agrodatos.info/monitores/serie-1/%s" % nombre
    print url
