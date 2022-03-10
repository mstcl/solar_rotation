#!/usr/bin/env bash

for dir in ./solar_2022*
do
    mkdir -p "${dir}"/fits
    for file in "${dir}/"bitmaps/*
    do
        name=$(echo "${file}" | cut -d'/' -f4 | cut -d'.' -f1)
        magick "${file}" "${dir}"/fits/"${name}".fits
    done
done
