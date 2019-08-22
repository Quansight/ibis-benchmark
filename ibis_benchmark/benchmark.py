import ibis

from ibis_benchmark.utils import benchmark, param


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
    "fn1,fn2",
    [
        param(
            lambda: omniscidb_table("functional_alltypes"),
            id="omniscidb_table",
        ),
        param(lambda: pandas_table("functional_alltypes"), id="pandas_table"),
    ],
)
def benchmark_head(f):
    f()
