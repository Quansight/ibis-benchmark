import argparse
import os

from ibis_benchmark.chart import gen_chart
from ibis_benchmark.nyc_taxi import config
from ibis_benchmark.utils import register_log


def main():
    parser = argparse.ArgumentParser()

    group_backend = parser.add_mutually_exclusive_group(required=True)

    group_backend.add_argument(
        '--omniscidb-cpu',
        dest='is_omniscidb_cpu',
        action='store_true',
        help='Set OmniSciDB CPU as the default backend.',
    )

    group_backend.add_argument(
        '--omniscidb-cuda',
        dest='is_omniscidb_cuda',
        action='store_true',
        help='Set OmniSciDB CUDA as the default backend.',
    )

    group_backend.add_argument(
        '--pandas',
        dest='is_pandas',
        action='store_true',
        help='Set pandas as the default backend.',
    )

    group_backend.add_argument(
        '--reset-results',
        dest='reset_results',
        action='store_true',
        help='Reset previous result.',
    )

    ns = parser.parse_args()

    if ns.reset_results:
        # start a new benchmark log
        register_log(config.log_path, new_log=True)
        return
    elif ns.is_omniscidb_cpu:
        os.system('python run.py --omniscidb --cpu --cursor')
        os.system('python run.py --omniscidb --cpu --ipc')
    elif ns.is_omniscidb_cuda:
        os.system('python run.py --omniscidb --gpu --ipc')
    elif ns.is_pandas:
        os.system('python run.py --pandas')

    # generate a comparison chart
    gen_chart('nyc-taxi')


if __name__ == '__main__':
    main()
