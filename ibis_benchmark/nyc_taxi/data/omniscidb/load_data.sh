#!/bin/bash

DATA_DIR=${IBIS_BENCHMARK_DATA_CLEANED}

for filename in ${DATA_DIR}/trips/*.csv; do
      echo "COPY trips
            FROM '$filename'
            WITH (header='false');" | \
          omnisql -u admin -p HyperInteractive --port $OMNISCI_PORT
  done
