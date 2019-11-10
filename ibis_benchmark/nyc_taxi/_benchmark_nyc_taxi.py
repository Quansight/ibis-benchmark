"""
This module will run a benchmark for expressions related to NYC TAXI dataset.

The available fields are:

    * VendorID
    * tpep_pickup_datetime
    * tpep_dropoff_datetime
    * passenger_count
    * trip_distance
    * RatecodeID
    * store_and_fwd_flag
    * PULocationID
    * DOLocationID
    * payment_type
    * fare_amount
    * extra
    * mta_tax
    * tip_amount
    * tolls_amount
    * improvement_surcharge
    * total_amount

"""
import os

import ibis
import pandas as pd

from ibis_benchmark.chart import gen_chart
from ibis_benchmark.nyc_taxi import config
from ibis_benchmark.utils import benchmark, cacheit, register_log

ExecutionType = ibis.omniscidb.ExecutionType

# start a new benchmark log
results_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'docs',
    'static',
)
os.makedirs(results_path, exist_ok=True)

log_path = os.path.join(results_path, 'benchmark-nyc-taxi.json')
register_log(log_path, new_log=True)

conn_info_cpu_cursor = {
    'host': 'localhost',
    'port': 6274,
    'user': 'admin',
    'password': 'HyperInteractive',
    'database': 'omnisci',
    'execution_type': ExecutionType.CURSOR,
}

conn_info_cpu_ipc = dict(conn_info_cpu_cursor)
conn_info_cpu_ipc.update({'execution_type': ExecutionType.IPC_CPU})

conn_info_gpu_ipc = dict(conn_info_cpu_cursor)
conn_info_gpu_ipc.update(
    {'port': 26274, 'execution_type': ExecutionType.IPC_GPU}
)

# using a persistant connection
omniscidb_cli_cpu_cursor = ibis.omniscidb.connect(**conn_info_cpu_cursor)
omniscidb_cli_cpu_ipc = ibis.omniscidb.connect(**conn_info_cpu_ipc)
omniscidb_cli_gpu_ipc = ibis.omniscidb.connect(**conn_info_gpu_ipc)


@cacheit
def omniscidb_table(name, cpu=True, ipc=True):
    if cpu:
        if ipc:
            return omniscidb_cli_cpu_ipc.table(name)
        return omniscidb_cli_cpu_cursor.table(name)
    # GPU is always ICP
    return omniscidb_cli_gpu_ipc.table(name)


@cacheit
def pandas_table(name):
    return pd.read_csv('../scripts/data/nyc-taxi.csv')


# cache data
table_name = 'nyc_taxi'
omniscidb_table(table_name, cpu=True, ipc=True)
omniscidb_table(table_name, cpu=True, ipc=False)
omniscidb_table(table_name, cpu=False)
# pandas_table(table_name)

bechmark_config = {'repeat': 3, 'log_path': log_path}

# ==========
# Benchmarks
# ==========

# added `is_pandas` because ibis cannot apply filter on a column


for op_id, expr_fn in config.expr_list:
    # OMNISCIDB
    @benchmark(backend='ibis_omniscidb_cpu_ipc', id=op_id, **bechmark_config)
    def benchmark_omniscidb_cpu_ipc():
        t = omniscidb_table("nyc_taxi", cpu=True, ipc=True)
        raise Exception(t.head(1).execute().columns)
        expr = expr_fn(t, is_pandas=False)
        result = expr.execute()
        assert expr is not None
        assert result is not None

    @benchmark(
        backend='ibis_omniscidb_cpu_cursor', id=op_id, **bechmark_config
    )
    def benchmark_omniscidb_cpu_cursor():
        t = omniscidb_table("nyc_taxi", cpu=True, ipc=False)
        expr = expr_fn(t, is_pandas=False)
        result = expr.execute()
        assert expr is not None
        assert result is not None

    # OMNISCIDB
    @benchmark(backend='ibis_omniscidb_gpu_ipc', id=op_id, **bechmark_config)
    def benchmark_omniscidb_gpu():
        t = omniscidb_table("nyc_taxi", cpu=False)
        expr = expr_fn(t, is_pandas=False)
        result = expr.execute()
        assert expr is not None
        assert result is not None

    # PANDAS
    @benchmark(backend='pandas', id=op_id, **bechmark_config)
    def benchmark_pandas():
        t = pandas_table("nyc_taxi")
        result = expr_fn(t, is_pandas=True)
        assert result is not None


# generate a comparison chart
gen_chart('nyc-taxi')
