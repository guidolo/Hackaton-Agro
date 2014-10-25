# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 15:39:11 2014

@author: guidolo
"""

import ogr,csv,sys

#clean up
del lyr

shpfile = '0aURHfMU49-1.shp'

#Open files
ds=ogr.Open(shpfile)
lyr=ds.GetLayer()

#Get field names
dfn=lyr.GetLayerDefn()
nfields=dfn.GetFieldCount()

for i in range(nfields):
    if dfn.GetFieldDefn(i).GetName() == 'RENDIMI_01':
        break
        
fields=[]    
# Write attributes and kml out to csv
for feat in lyr:
    fields.append(feat.GetField(18))
    
#clean up
del lyr
