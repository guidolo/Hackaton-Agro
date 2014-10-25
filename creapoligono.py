# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 09:42:40 2014

@author: guidolo
"""




from osgeo import ogr
import os
import sys 

#inShapefile = sys.argv[1]

inShapefile = '0aURHfMU49-1.shp'
outShapefile  = 'out-' + inShapefile

# Get a Layer
#inShapefile = "*.shp"
inDriver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = inDriver.Open(inShapefile, 0)
#inDataSource  = ogr.Open(inShapefile)
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
outLayer = outDataSource.CreateLayer("poligono", geom_type=ogr.wkbPoint)


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

