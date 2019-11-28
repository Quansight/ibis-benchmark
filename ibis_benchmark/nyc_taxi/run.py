import argparse

import ibis
import pandas as pd

from ibis_benchmark.nyc_taxi.config import bechmark_config, conn_info
from ibis_benchmark.nyc_taxi.exprs import expr_list
from ibis_benchmark.utils import benchmark, cacheit


def main():
    # using a persistant connection

    parser = argparse.ArgumentParser()

    group_backend = parser.add_mutually_exclusive_group(required=True)

    group_backend.add_argument(
        '--omniscidb',
        dest='is_omniscidb',
        action='store_true',
        help='Set omniscidb as the default backend.',
    )

    group_backend.add_argument(
        '--pandas',
        dest='is_pandas',
        action='store_true',
        help='Set pandas as the default backend.',
    )

    conn_type = parser.add_mutually_exclusive_group(required=True)

    conn_type.add_argument(
        '--ipc',
        dest='is_ipc',
        action='store_true',
        help='Set OmniSciDB IPC as default for the connection.',
    )

    conn_type.add_argument(
        '--cursor',
        dest='is_cursor',
        action='store_true',
        help='Set OmniSciDB Cursor as default for the connection.',
    )

    proc_target = parser.add_mutually_exclusive_group(required=True)

    proc_target.add_argument(
        '--cpu',
        dest='is_cpu',
        action='store_true',
        help='Set OmniSciDB CPU as default for the connection.',
    )

    proc_target.add_argument(
        '--gpu',
        dest='is_gpu',
        action='store_true',
        help='Set OmniSciDB GPU as default for the connection.',
    )

    args = parser.parse_args()

    if args.is_pandas:
        benchmark_name = 'pandas'

        @cacheit
        def table(*args, **kwargs):
            return pd.read_csv('../scripts/data/nyc-taxi.csv')

    else:
        if args.is_cpu:
            conn_name = 'cpu'
        else:
            conn_name = 'gpu'

        if args.is_cursor:
            conn_name += '_cursor'
        else:
            conn_name += '_ipc'

        benchmark_name = 'omniscidb_' + conn_name
        cli = ibis.omniscidb.connect(**conn_info[conn_name])

        @cacheit
        def table(name, cpu=True, ipc=True):
            return cli.table(name)

    # cache data
    table_name = 'trips'
    table(table_name)

    if args.is_omniscidb:
        for op_id, expr_fn in expr_list:

            @benchmark(backend=benchmark_name, id=op_id, **bechmark_config)
            def run_benchmark():
                t = table(table_name)
                expr = expr_fn(t)
                print(op_id)
                print(expr.compile())
                result = expr.execute()
                assert expr is not None
                assert result is not None

    else:
        raise Exception('it is not pandas')
        for op_id, expr_fn in expr_list:

            @benchmark(backend=benchmark_name, id=op_id, **bechmark_config)
            def run_benchmark():
                t = table(table_name)
                result = expr_fn(t)
                assert result is not None


if __name__ == '__main__':
    main()
