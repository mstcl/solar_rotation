#!/usr/bin/env bash

files=$1
spots=$2
sequence=$3

for ((file=1;file<=files;file++))
do
    for ((spot=1;spot<=spots;spot++))
    do
        cp ./"${sequence}"/sunspot_data/x_constant_"${file}".txt ./"${sequence}"/sunspot_data/x_constant_"${file}"_"${spot}".txt
        cp ./"${sequence}"/sunspot_data/y_constant_"${file}".txt ./"${sequence}"/sunspot_data/y_constant_"${file}"_"${spot}".txt
    done
done
