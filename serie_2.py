#!/usr/bin/python


from utiles import borrarArbol, obtenerCentroide
from glob import glob
from zipfile import ZipFile
import numpy
import ogr


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

        if a.filename[-3:] == "shp":
            archivo_shp = "%s%s" % (ruta_temporal, a.filename)
            centro_x, centro_y = obtenerCentroide(archivo_shp)

    print "%s,%s,%s,%s" % (nombre.split('/')[-1], promedio, centro_x, centro_y)

    borrarArbol(ruta_temporal)


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


for archivo in glob("entrada/serie2/*.zip"):
    try:
        procesarZIP(archivo)
    except:
        pass
