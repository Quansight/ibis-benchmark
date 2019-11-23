#!/bin/bash

DATA_DIR=${IBIS_BENCHMARK_DATA_PREPARED}

for filename in $DATA_DIR/trips/*.csv; do
      echo "COPY trips
            FROM '/theHoard/trips/$filename'
            WITH (header='false');" | \
          mapdql \
              mapd \
              -u $MAPD_USERNAME \
              -p $MAPD_PASSWORD
  done
