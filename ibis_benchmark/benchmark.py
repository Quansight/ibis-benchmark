import ibis

from ibis_benchmark.utils import benchmark, param, register_log

# start a new benchmark log
log_path = '/tmp/log_benchmark.json'
register_log(log_path, new_log=True)

conn_info = {
    'host': 'localhost',
    'port': 6274,
    'user': 'admin',
    'password': 'HyperInteractive',
    'database': 'omnisci',
}

omniscidb_con = ibis.omniscidb.connect(**conn_info)


def omniscidb_table(name, limit=10000):
    con = omniscidb_con
    return con.table(name).head(limit)


def pandas_table(name, limit=10000):
    con = omniscidb_con
    return con.table(name).head(limit).execute()


@benchmark(
    "f",
    [
        param(
            lambda: omniscidb_table("nyc_taxi").head().execute(),
            group='omniscidb',
            id="table_head",
        ),
        param(
            lambda: pandas_table("nyc_taxi").head(),
            group='pandas',
            id="table_head",
        ),
    ],
    repeat=10,
)
def benchmark_head(f):
    f()


@benchmark(
    "f",
    [
        param(
            lambda: omniscidb_table("nyc_taxi").head().execute(),
            group='omniscidb',
            id="table_tail",
        ),
        param(
            lambda: pandas_table("nyc_taxi").head(),
            group='pandas',
            id="table_tail",
        ),
    ],
    repeat=10,
)
def benchmark_tail(f):
    f()
