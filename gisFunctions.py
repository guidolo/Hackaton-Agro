# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 09:42:40 2014

@author: guidolo
"""

import os
import struct
from osgeo import gdal,ogr

def createPoligono(inShapefile, outShapefile):
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
    
    # Save extent to a new Shapefile
    #outShapefile = ".shp"
    outDriver = ogr.GetDriverByName("ESRI Shapefile")

    # Remove output shapefile if it already exists
    if os.path.exists(outShapefile):
        outDriver.DeleteDataSource(outShapefile)
    
    # Create the output shapefile
    outDataSource = outDriver.CreateDataSource(outShapefile)
    #outLayer = outDataSource.CreateLayer("poligono", geom_type=ogr.wkbPolygon)
    outLayer = outDataSource.CreateLayer(inShapefile, geom_type=ogr.wkbPoint)
    
    # Add an ID field
    idField = ogr.FieldDefn("id", ogr.OFTInteger)
    outLayer.CreateField(idField)
    
    # Create the feature and set values
    featureDefn = outLayer.GetLayerDefn()
    feature = ogr.Feature(featureDefn)
    #feature.SetGeometry(convexhull)
    feature.SetGeometry(centroide)
    feature.SetField("id", 1)
    outLayer.CreateFeature(feature)
    
    # Close DataSource
    inDataSource.Destroy()
    outDataSource.Destroy()




def obtenerCentroide(archivo_shape):
    # Get a Layer
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(archivo_shape, 0)
    inLayer = inDataSource.GetLayer()

    # Collect all Geometry
    geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
    for feature in inLayer:
        try:
            geomcol.AddGeometry(feature.GetGeometryRef())
        except:
            return 0,0
        
    # Calculate convex hull
    convexhull = geomcol.ConvexHull()
    centroide = convexhull.Centroid()

    # Close DataSource
    inDataSource.Destroy()
    return centroide.GetX(), centroide.GetY()
    
    
    
def getRasterVal(path_raster, file_raster, path_shp, file_shp):
    
    full_path_img = path_raster + file_raster
    
    full_path_shp =  path_shp + file_shp
    
    src_ds= gdal.Open(full_path_img, gdal.GA_ReadOnly) 
    
    #toma el punto de referencia del raster
    gt    = src_ds.GetGeoTransform()
    
    #toma la banda 1
    rb    = src_ds.GetRasterBand(1)
    
    ds=ogr.Open(full_path_shp)
    lyr=ds.GetLayer()
    fields=[]    
    
    for feat in lyr:
        geom = feat.GetGeometryRef()
        mx,my=geom.GetX(), geom.GetY()  #coord in map units
    
        #Convert from map to pixel coordinates.
        #Only works for geotransforms with no rotation.
        #If raster is rotated, see http://code.google.com/p/metageta/source/browse/trunk/metageta/geometry.py#493
        px = int((mx - gt[0]) / gt[1]) #x pixel
        py = int((my - gt[3]) / gt[5]) #y pixel
    
        structval=rb.ReadRaster(px,py,1,1,buf_type=gdal.GDT_UInt16) #Assumes 16 bit int aka 'short'
        intval = struct.unpack('h' , structval) #use the 'short' format code (2 bytes) not int (4 bytes)
        
        fields.append([mx, my, intval[0]])
    
    return fields
    
    
def getShpColumnValue(inShapefile, columnName):
    
    #Open files
    ds=ogr.Open(inShapefile)
    lyr=ds.GetLayer()
    
    #Get field names
    dfn=lyr.GetLayerDefn()
    nfields=dfn.GetFieldCount()
    fields=[]
    for i in range(nfields):
        #print dfn.GetFieldDefn(i).GetName()
        if dfn.GetFieldDefn(i).GetName() == columnName:
            fields.append(dfn.GetFieldDefn(i).GetName())

    valores=[]    
    #control de que exista la columna    
    if len(fields) == 0:
        return valores

    # Write attributes and kml out to csv
    for feat in lyr:
        attributes=feat.items()
        valores.append(attributes[columnName])
        
    #clean up
    del lyr
    
    return valores


def printColumnNames(inShapefile):    
    #Open files
    ds=ogr.Open(inShapefile)
    lyr=ds.GetLayer()
    #Get field names
    dfn=lyr.GetLayerDefn()
    nfields=dfn.GetFieldCount()
    for i in range(nfields):
        print dfn.GetFieldDefn(i).GetName()        
    #clean up
    del lyr
    