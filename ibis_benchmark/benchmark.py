import ibis

from ibis_benchmark.utils import benchmark, param, register_log

# start a new benchmark log
log_path = '/tmp/log_benchmark.json'
register_log(log_path, new_log=True)


# setup
def omniscidb_con():
    return ibis.omniscidb.connect(
        host="localhost",
        port="6274",
        user="admin",
        password="HyperInteractive",
        database="ibis_testing",
    )


def omniscidb_table(name):
    con = omniscidb_con()
    return con.table(name)


def pandas_table(name):
    con = omniscidb_con()
    return con.table(name).execute()


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
