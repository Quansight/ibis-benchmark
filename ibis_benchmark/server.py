import os
import sys
from pathlib import Path

import ibis
import pandas as pd
import sh

SCRIPT_DIR = Path(__file__).parent.absolute()
DATA_DIR_NAME = "ibis-testing-data"
DATA_DIR = Path(
    os.environ.get("IBIS_TEST_DATA_DIRECTORY", SCRIPT_DIR / DATA_DIR_NAME)
)


def download(url, name, destination=str(DATA_DIR), extension='csv'):
    """Download data and load that into a database"""
    os.makedirs(destination, exist_ok=True)
    file_path = os.path.join(destination, '{}.{}'.format(name, extension))

    print('downloading to {} ...'.format(file_path))

    sh.wget(url, '-c', '-O', file_path, _out=sys.stdout)
    return file_path


def _load_data_omniscidb(file_path, name):
    con = ibis.omniscidb.connect(
        host='localhost',
        port=6274,
        database='omnisci',
        user='admin',
        password='HyperInteractive',
    )
    con.load_data(name, pd.read_csv(file_path))


def load_data(file_path: str, name: str, backend: str):
    """Load data into a database"""
    backends_available = {'omniscidb': _load_data_omniscidb}
    if backend not in backends_available:
        raise Exception('{} is not supported yet'.format(backend))

    _load = backends_available[backend]
    _load(file_path, name)


def start(name):
    """Start a specific docker container server"""
    pwd = sh.pwd(_out=sys.stdout)

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "server")

    sh.cd(path)
    sh.docker_compose("up", "-d", name, _out=sys.stdout)
    sh.docker_compose("up", "waiter", _out=sys.stdout)
    sh.cd(pwd)


def stop(name):
    """Stop a specific docker container server"""
    pwd = sh.pwd(_out=sys.stdout)

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "server")

    sh.cd(path)
    sh.docker_compose("rm", "--force", "--stop", name, _out=sys.stdout)
    sh.cd(pwd)
