#!/bin/bash

mkdir -p ${IBIS_BENCHMARK_DOWNLOAD}/unaltered

mv ${IBIS_BENCHMARK_DOWNLOAD}/yellow_tripdata_2010-02.csv \
   ${IBIS_BENCHMARK_DOWNLOAD}/yellow_tripdata_2010-03.csv \
   ${IBIS_BENCHMARK_DOWNLOAD}/unaltered/

sed -E '/(.*,){18,}/d' ${IBIS_BENCHMARK_DOWNLOAD}/unaltered/yellow_tripdata_2010-02.csv > ${IBIS_BENCHMARK_DOWNLOAD}/yellow_tripdata_2010-02.csv
sed -E '/(.*,){18,}/d' ${IBIS_BENCHMARK_DOWNLOAD}/unaltered/yellow_tripdata_2010-03.csv > ${IBIS_BENCHMARK_DOWNLOAD}/yellow_tripdata_2010-03.csv
