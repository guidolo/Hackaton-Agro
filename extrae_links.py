#!/usr/bin/python

from util import shp2dataframe

data = shp2dataframe('files_serie_1.dbf')

for i in data['ID']:
    nombre = i + '.zip'
    url = "http://agrodatos.info/monitores/serie-1/%s" % nombre
    print url
