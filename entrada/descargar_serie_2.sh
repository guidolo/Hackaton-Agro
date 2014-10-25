#!/bin/bash 

cd serie2
for link in `cat ../links_serie2.txt`; do 
    archivo=$(echo $link | sed 's/\//\n/g' | grep zip)

    if [ ! -e $archivo ]; then 
        wget $link
    fi 
done
