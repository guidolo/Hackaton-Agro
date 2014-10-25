# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 12:45:47 2014

@author: guidolo
"""

import os, ogr, osr
import ogr,csv,sys

directory = "D:\\DataMining\\HackatonAGRO\\rendimiento\\serie-2\\descomprimido\\"
fileEndsWith = '.shp'
driverName = 'ESRI Shapefile'
archivosalida = 'salida.csv'

fileList = os.listdir(directory)

csvfile=open(archivosalida,'wb')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['Nombre','Longitud', 'Latitud'])
i=0
for file in fileList:
    if file.endswith(fileEndsWith):
            csvwriter.writerow(coordenadas(directory, file))
            i = i + 1            
            print(file)
csvfile.close()	


def coordenadas(directorio, inShapefile):
        
    # Get a Layer
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(directorio+inShapefile, 0)
    inLayer = inDataSource.GetLayer()
    
    # Collect all Geometry
    geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
    for feature in inLayer:
        geomcol.AddGeometry(feature.GetGeometryRef())
    
    # Calculate convex hull
    convexhull = geomcol.ConvexHull()
    
    centroide = convexhull.Centroid()
    
    # Close DataSource
    inDataSource.Destroy()
    
    return [inShapefile[:-4], centroide.GetX(), centroide.GetY()]
    