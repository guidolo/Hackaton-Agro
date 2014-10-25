# Proyecto Hackaton Agrodatos 

Recomendación de variedades de semillas a sembrar en base a los resultados de su utilización en campos similares.

[hackdash](http://agrodatos.hackdash.org/projects/54469f6a7fd3d5704c0002c0)


## Datasets Utilizados 

Utilizamos dos sets de datos de monitores de rendimiento provistos por AACREA para el hackaton.

[serie-1](http://agrodatos.info/dataset/monitores-de-rendimiento-serie-1)
[serie-2](http://agrodatos.info/dataset/monitores-de-rendimiento-serie-2)

En la carpeta 'entrada' hay un script para descargar los archivos de cada lote/campaña.


Además, utilizamos la base de datos de [worldclim](http://www.worldclim.org).


## Procesamiento 

Abstraimos el manejo de los datos para poder mejorar los algoritmos de depuración de datos y estimaciones.
Caracterizamos cada lote en un centroide y un valor promedio de rendimiento.


## Salida
