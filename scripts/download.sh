#!/bin/bash

mkdir -p ../ibis_benchmark/data

wget -c https://data.cityofnewyork.us/api/views/biws-g3hs/rows.csv?accessType=DOWNLOAD \
  -O ../ibis_benchmark/data/nyc-taxi.csv
