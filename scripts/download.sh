#!/bin/bash

PWD="$(dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" )"

cd $PWD

mkdir -p ./data

wget -c https://data.cityofnewyork.us/api/views/biws-g3hs/rows.csv?accessType=DOWNLOAD \
  -O ./data/nyc-taxi.csv
