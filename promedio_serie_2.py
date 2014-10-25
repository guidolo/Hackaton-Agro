#!/usr/bin/python

from glob import glob
from zipfile import ZipFile
from pandas import DataFrame
from shapefile import Reader as shapefileReader

import numpy

from IPython import embed

from os.path import join
from os import walk, remove, rmdir

import ogr,csv,sys

def borrarArbol(top):
    # http://docs.python.org/2/library/os.html  ->  os.walk example
    for root, dirs, files in walk(top, topdown=False):
        for archivo in files:
            remove(join(root, archivo))
        for directorio in dirs:
            rmdir(join(root, directorio))
    rmdir(top)


def extraer(archivo):
    ds = ogr.Open(archivo)
    lyr = ds.GetLayer()
    dfn = lyr.GetLayerDefn()
    nfields = dfn.GetFieldCount()

    for i in range(nfields):
        if dfn.GetFieldDefn(i).GetName() == 'RENDIMI_01':
            break

    datos = []
    for feat in lyr:
        datos.append(feat.GetField(i))

    return datos


def procesarZIP(archivo):
    try:
        z = ZipFile(archivo)
    except:
        return

    nombre = z.filename.split('.')[0]
    ruta_temporal = '/tmp/%s/' % nombre
    z.extractall(ruta_temporal)

    for a in z.filelist:
        if a.filename[-3:] == "shp":
            archivo_dbf = "%s%s" % (ruta_temporal, a.filename)

            datos = extraer(archivo_dbf)

            # ya quito los nulos
            no_nulos = filter(None, datos)

            if no_nulos:
                promedio = promedioRendimiento(no_nulos)
                print "%s,%s" % (nombre.split('/')[-1], promedio)

    borrarArbol(ruta_temporal)


def brusco(valor):
    if valor > 1 or valor < 20:
        return True


def fino(lista):
    #valores = filter(brusco, lista)
    valores = lista
    media = numpy.mean(valores)
    desvio = numpy.std(valores)
    minimo = media - desvio
    maximo = media + desvio
    # print media, desvio, minimo, maximo

    return [x for x in valores if x > minimo and x < maximo]


def promedioRendimiento(lista):
    filtrados = fino(lista)
    return numpy.mean(filtrados)


for archivo in glob("serie2/*.zip"):
    try:
        procesarZIP(archivo)
    except:
        print archivo
