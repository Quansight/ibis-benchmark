#!/bin/bash

sed s:\{\{DATA_DIR\}\}:${IBIS_BENCHMARK_DOWNLOAD}: export_from_postgresql_to_csv_template.sql | psql
