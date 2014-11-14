# -*- coding: utf-8 -*-
"""
Created on Sun Nov 02 19:30:22 2014

@author: guidolo
"""

import zipfile
import os
import gisFunctions as gf
import utiles
from imp import reload
reload(gf)
import csv

path = "D:\\DataMining\\HackatonAGRO\\rendimiento\\serie-2\\"
os.chdir(path)
fileEndsWith = '.zip'
fileList = os.listdir(path)
i=0
datos=[]

#para todos los zip del directorio
for file in fileList:
    if file.endswith(fileEndsWith):
            i = i + 1
            print('archivo ' + str(i) + ' de ' + str(len(fileList)) + ' Nombre Archivo: ' + file)
            try:
                zf = zipfile.ZipFile(file)
            except:
                print('archivo ' + file + ' con problemas')
                continue
            
            zf.extractall('temp')
            #break        

            #recorro la lista de archivos del zip
            for filezip in zf.filelist:
                if filezip.filename[-3:] == "shp":
                    
                    match = [x for x in datos if filezip.filename == x[0]] 
                    if len(match) > 0: 
                        print "%s%s" % (file, ' ya procesado')
                        break
            
                    archivo_shp = "%s%s%s" % (path, 'temp\\', filezip.filename)
                    
                    centro_x, centro_y = gf.obtenerCentroide(archivo_shp)
                    
                    columnName = 'RENDIMI_01'
                    #columnName = 'REND'
                    puntos = gf.getShpColumnValue(archivo_shp, columnName )   
                    no_nulos = filter(None, puntos)
                    promedio = utiles.promedioRendimiento(no_nulos)
                    
                    #print "%s,%s,%s,%s" % (archivo_shp.split('\\')[-1], promedio, centro_x, centro_y)
                    #break
                    datos.append([archivo_shp.split('\\')[-1], promedio, centro_x, centro_y])
                    
            utiles.borrarArbol(path + 'temp\\')

with open('salida2.csv','wb',) as f:           
    csvwriter = csv.writer(f, delimiter=';')
    csvwriter.writerows(datos)
f.close()	

