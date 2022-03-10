#!/usr/bin/env bash

for dir in ./solar_2022*/
do
    if [ ! -e "${dir}/data.txt" ]; then
        touch "${dir}/data.txt"
        dirclean=${dir%*/}
        dirclean="${dirclean##*/}"
        dirclean=$(echo "${dirclean}" | cut -d"_" -f2,3)
        echo "d ${dirclean}" > "./${dir}/data.txt"
    fi
    mkdir -p "${dir}"/regions
    mkdir -p "${dir}"/regions/sun_discs
    mkdir -p "${dir}"/sunspot_data
done
