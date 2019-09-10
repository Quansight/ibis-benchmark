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
from ibis_benchmark.utils import benchmark, cacheit, register_log

# start a new benchmark log
results_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'results'
)
os.makedirs(results_path, exist_ok=True)
log_path = os.path.join(results_path, 'benchmark-nyc-taxi.json')
register_log(log_path, new_log=True)

conn_info = {
    'host': 'localhost',
    'port': 6274,
    'user': 'admin',
    'password': 'HyperInteractive',
    'database': 'omnisci',
}

# using a persistant connection
omniscidb_cli = ibis.omniscidb.connect(**conn_info)


@cacheit
def omniscidb_table(name):
    return omniscidb_cli.table(name)


@cacheit
def pandas_table(name):
    return pd.read_csv('../scripts/data/nyc-taxi.csv')


# caching tables
omniscidb_table('nyc_taxi')
pandas_table('nyc_taxi')

bechmark_config = {'repeat': 3, 'log_path': log_path}

# ==========
# Benchmarks
# ==========

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
    @benchmark(backend='omniscidb', id=op_id, **bechmark_config)
    def benchmark_sum_fare_less_100_omniscidb():
        t = omniscidb_table("nyc_taxi")
        expr = expr_fn(t)
        result = expr.execute()
        assert expr is not None
        assert result is not None

    # PANDAS
    @benchmark(backend='pandas', id=op_id, **bechmark_config)
    def benchmark_sum_fare_less_100_pandas():
        t = pandas_table("nyc_taxi")
        result = expr_fn(t)
        assert result is not None


# generate a comparison chart
gen_chart('nyc-taxi')
