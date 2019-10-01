#!/bin/bash

PWD="$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd

mkdir -p $PWD/data

wget -c https://data.cityofnewyork.us/api/views/biws-g3hs/rows.csv?accessType=DOWNLOAD \
 -O $PWD/data/nyc-taxi.csv
