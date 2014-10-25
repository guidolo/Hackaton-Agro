import urllib
import pandas as pd
import shapefile
import numpy as np

data = shp2dataframe('files_serie_1.dbf')

for i in data['ID']:
    nombre = i + '.zip'
    print(nombre)
    urllib.urlretrieve ("http://agrodatos.info/monitores/serie-1/" + nombre, nombre)
