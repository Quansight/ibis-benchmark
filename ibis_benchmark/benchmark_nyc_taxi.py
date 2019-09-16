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
from ibis_benchmark.utils import benchmark, register_log

# start a new benchmark log
results_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'results'
)
os.makedirs(results_path, exist_ok=True)
log_path = os.path.join(results_path, 'benchmark-nyc-taxi.json')
register_log(log_path, new_log=True)

conn_info_cpu = {
    'host': 'localhost',
    'port': 6274,
    'user': 'admin',
    'password': 'HyperInteractive',
    'database': 'omnisci',
}

conn_info_gpu = dict(conn_info_cpu)
conn_info_gpu.update({'port': 26274})

# using a persistant connection
omniscidb_cli_cpu = ibis.omniscidb.connect(**conn_info_cpu)
omniscidb_cli_gpu = ibis.omniscidb.connect(**conn_info_gpu)


def omniscidb_table(name, cpu=True):
    if cpu:
        return omniscidb_cli_cpu.table(name)
    return omniscidb_cli_gpu.table(name)


def pandas_table(name):
    return pd.read_csv('../scripts/data/nyc-taxi.csv')


bechmark_config = {'repeat': 3, 'log_path': log_path}

# ==========
# Benchmarks
# ==========
"""
# load data. it will create a cache for each connection
op_id = 'backend_load_data'
@benchmark(backend='omniscidb_cpu', id=op_id, **bechmark_config)
def benchmark_load_omniscidb_cpu():
    omniscidb_table('nyc_taxi', cpu=True)


@benchmark(backend='omniscidb_gpu', id=op_id, **bechmark_config)
def benchmark_load_omniscidb_gpu():
    omniscidb_table('nyc_taxi', cpu=False)

@benchmark(backend='pandas', id=op_id, **bechmark_config)
def benchmark_load_pandas():
    pandas_table('nyc_taxi')
"""

for op_id, expr_fn in [
    ('table_head', lambda t: t.head()),
    ('trip_distance_max', lambda t: t.trip_distance.max()),
    ('trip_distance_min', lambda t: t.trip_distance.min()),
    ('trip_distance_mean', lambda t: t.trip_distance.mean()),
    ('trip_distance_std', lambda t: t.trip_distance.std()),
    ('trip_distance_sum', lambda t: t.trip_distance.sum()),
    (
        'fare_amount_less_100_sum',
        lambda t: t[t.fare_amount < 100].fare_amount.sum(),
    ),
    (
        'fare_amount_less_100_mean',
        lambda t: t[t.fare_amount < 100].fare_amount.mean(),
    ),
    (
        'fare_amount_less_100_std',
        lambda t: t[t.fare_amount < 100].fare_amount.std(),
    ),
]:
    # OMNISCIDB
    @benchmark(backend='omniscidb_cpu', id=op_id, **bechmark_config)
    def benchmark_omniscidb_cpu():
        t = omniscidb_table("nyc_taxi")
        expr = expr_fn(t)
        result = expr.execute()
        assert expr is not None
        assert result is not None

    # OMNISCIDB
    @benchmark(backend='omniscidb_gpu', id=op_id, **bechmark_config)
    def benchmark_omniscidb_gpu():
        t = omniscidb_table("nyc_taxi", cpu=False)
        expr = expr_fn(t)
        result = expr.execute()
        assert expr is not None
        assert result is not None

    # PANDAS
    @benchmark(backend='pandas', id=op_id, **bechmark_config)
    def benchmark_pandas():
        t = pandas_table("nyc_taxi")
        result = expr_fn(t)
        assert result is not None


# generate a comparison chart
gen_chart('nyc-taxi')
