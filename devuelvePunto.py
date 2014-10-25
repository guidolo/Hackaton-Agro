# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 12:54:15 2014

@author: guidolo
"""

from osgeo import ogr
import os
import sys 


def coordenadas(inShapefile):
        
    # Get a Layer
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(inShapefile, 0)
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
    
    
coordenadas('0aURHfMU49-1.shp')