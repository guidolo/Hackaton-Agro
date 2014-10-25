#!/bin/bash 

cd serie1
for link in `cat ../links_serie1.txt`; do 
    archivo=$(echo $link | sed 's/\//\n/g' | grep zip)

    if [ ! -e $archivo ]; then 
        wget $link
    fi 
done
