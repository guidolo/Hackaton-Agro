#!/usr/bin/python

from glob import glob
from zipfile import ZipFile
from pandas import DataFrame
from shapefile import Reader as shapefileReader
from os.path import join
from os import walk, remove, rmdir

import numpy




def borrarArbol(top):
    # http://docs.python.org/2/library/os.html  ->  os.walk example
    for root, dirs, files in walk(top, topdown=False):
        for archivo in files:
            remove(join(root, archivo))
        for directorio in dirs:
            rmdir(join(root, directorio))
    rmdir(top)


def shp2dataframe(fname):
    shp = shapefileReader(fname)
    r = shp.records()
    fld = numpy.array(shp.fields[1:], dtype=str)
    data = DataFrame(r, columns=fld[:, 0])
    return data


def procesarZIP(archivo):
    try:
        z = ZipFile(archivo)
    except:
        return

    nombre = z.filename.split('.')[0]
    ruta_temporal = '/tmp/%s/' % nombre
    z.extractall(ruta_temporal)

    for a in z.filelist:
        if a.filename[-3:] == "dbf":
            archivo_dbf = "%s%s" % (ruta_temporal, a.filename)

            print archivo_dbf
            puntos = shp2dataframe(archivo_dbf)
            # print "%s %s" % (nombre, puntos['REND'].mean())

            # ya quito los nulos
            no_nulos = filter(None, puntos.REND.values)
            promedio = promedioRendimiento(no_nulos)

            print "%s,%s" % (nombre.split('/')[-1], promedio)

    borrarArbol(ruta_temporal)


def brusco(valor):
    if valor > 1 or valor < 20:
        return True


def fino(lista):
    valores = filter(brusco, lista)
    media = numpy.mean(valores)
    desvio = numpy.std(valores)
    minimo = media - desvio
    maximo = media + desvio
    # print media, desvio, minimo, maximo

    return [x for x in valores if x > minimo and x < maximo]


def promedioRendimiento(lista):
    filtrados = fino(lista)
    return numpy.mean(filtrados)


for archivo in glob("serie1/*.zip"):
    procesarZIP(archivo)
