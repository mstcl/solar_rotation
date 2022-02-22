#!/usr/bin/env bash

for dir in ./solar*/
do
    if [ ! -e "${dir}/data.txt" ]; then
        touch "${dir}/data.txt"
        dirclean=${dir%*/}
        dirclean="${dirclean##*/}"
        dirclean=$(echo "${dirclean}" | cut -d"_" -f2,3)
        echo "${dirclean}" > "./${dir}/data.txt"
    fi
done
