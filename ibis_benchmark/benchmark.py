import ibis

from ibis_benchmark.utils import benchmark, param, register_log

# start a new benchmark log
log_path = '/tmp/log_benchmark.json'
register_log(log_path, new_log=True)


# setup
def omniscidb_con(connecion_name='localhost'):
    conn_info = {
        'localhost': {
            'host': 'localhost',
            'port': 6274,
            'user': 'admin',
            'password': 'HyperInteractive',
            'database': 'ibis_testing',
        },
        'metis': {
            'host': 'metis.mapd.com',
            'port': 443,
            'user': 'mapd',
            'password': 'HyperInteractive',
            'database': 'mapd',
            'protocol': 'https',
        },
    }
    return ibis.omniscidb.connect(**conn_info[connecion_name])


def omniscidb_table(name, limit=10000):
    con = omniscidb_con('metis')
    print(con.list_tables())
    return con.table(name).head(limit)


def pandas_table(name, limit=10000):
    con = omniscidb_con('metis')
    return con.table(name).head(limit).execute()


@benchmark(
    "f",
    [
        param(
            lambda: omniscidb_table("functional_alltypes").head().execute(),
            group='omniscidb',
            id="table_head",
        ),
        param(
            lambda: pandas_table("functional_alltypes").head(),
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
            lambda: omniscidb_table("functional_alltypes").head().execute(),
            group='omniscidb',
            id="table_tail",
        ),
        param(
            lambda: pandas_table("functional_alltypes").head(),
            group='pandas',
            id="table_tail",
        ),
    ],
    repeat=10,
)
def benchmark_tail(f):
    f()
