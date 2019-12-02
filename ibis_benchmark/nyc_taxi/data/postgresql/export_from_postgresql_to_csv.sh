#!/bin/bash

sed s:\{\{DATA_DIR\}\}:${IBIS_BENCHMARK_DATA_CLEANED}: export_from_postgresql_to_csv_template.sql | psql nyc-taxi-data
