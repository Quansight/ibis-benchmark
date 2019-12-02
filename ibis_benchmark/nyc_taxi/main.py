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
    runpy_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'run.py'
    )

    if ns.reset_results:
        # start a new benchmark log
        register_log(config.log_path, new_log=True)
        return
    elif ns.is_omniscidb_cpu:
        os.system('python {} --omniscidb --cpu --cursor'.format(runpy_file))
        os.system('python {} --omniscidb --cpu --ipc'.format(runpy_file))
    elif ns.is_omniscidb_cuda:
        os.system('python {} --omniscidb --cuda --ipc'.format(runpy_file))
    elif ns.is_pandas:
        os.system('python {} --pandas'.format(runpy_file))

    # generate a comparison chart
    gen_chart('nyc-taxi')


if __name__ == '__main__':
    main()
