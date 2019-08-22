import logging
import os
from pathlib import Path

import click

from ibis_benchmark import server

BENCHMARK_TABLES = []

SCRIPT_DIR = Path(__file__).parent.absolute()
DATA_DIR_NAME = "ibis-testing-data"
DATA_DIR = Path(
    os.environ.get("IBIS_TEST_DATA_DIRECTORY", SCRIPT_DIR / DATA_DIR_NAME)
)

if os.path.exists(".env"):
    # load .env as local variables
    with open(".env", "r") as f:
        for l in f.readlines():
            _var, _val = l.split("=")
            locals()[_var] = _val.replace("\n", "")
else:
    IBIS_BENCHMARK_OMNISCIDB_HOST = "localhost"
    IBIS_BENCHMARK_OMNISCIDB_PORT = 6274
    IBIS_BENCHMARK_OMNISCIDB_USER = "admin"
    IBIS_BENCHMARK_OMNISCIDB_PASSWORD = "HyperInteractive"
    IBIS_BENCHMARK_OMNISCIDB_DATABASE = "omnisci"


def get_logger(name, level=None, format=None, propagate=False):
    logging.basicConfig()
    handler = logging.StreamHandler()

    if format is None:
        format = (
            "%(relativeCreated)6d "
            "%(name)-20s "
            "%(levelname)-8s "
            "%(threadName)-25s "
            "%(message)s"
        )
    handler.setFormatter(logging.Formatter(fmt=format))
    logger = logging.getLogger(name)
    logger.propagate = propagate
    logger.setLevel(
        level
        or getattr(logging, os.environ.get("LOGLEVEL", "WARNING").upper())
    )
    logger.addHandler(handler)
    return logger


logger = get_logger(Path(__file__).with_suffix("").name)


@click.group()
@click.option("--quiet/--verbose", "-q", default=False, is_flag=True)
def cli(quiet):
    if quiet:
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.INFO)


@cli.command()
@click.option("--name", default="omniscidb")
def start_server(name):
    server.start(name)


@cli.command()
@click.option("-h", "--host", default=IBIS_BENCHMARK_OMNISCIDB_HOST)
@click.option("-P", "--port", default=IBIS_BENCHMARK_OMNISCIDB_PORT, type=int)
@click.option("-u", "--user", default=IBIS_BENCHMARK_OMNISCIDB_USER)
@click.option("-p", "--password", default=IBIS_BENCHMARK_OMNISCIDB_PASSWORD)
@click.option("-D", "--database", default=IBIS_BENCHMARK_OMNISCIDB_DATABASE)
@click.option("--protocol", default="binary")
@click.option(
    "-S",
    "--schema",
    type=click.File("rt"),
    default=str(SCRIPT_DIR / "schema" / "omniscidb.sql"),
)
@click.option("-t", "--tables", multiple=True, default=BENCHMARK_TABLES)
@click.option("-d", "--data-directory", default=DATA_DIR)
def omniscidb(schema, tables, data_directory, **params):
    print("OK")


if __name__ == "__main__":
    """
    Environment Variables are automatically parsed:
     - IBIS_BENCHMARK_{BACKEND}_PORT
     - IBIS_BENCHMARK_{BACKEND}_HOST
     - IBIS_BENCHMARK_{BACKEND}_USER
     - IBIS_BENCHMARK_{BACKEND}_PASSWORD
     - etc.
    """
    cli(auto_envvar_prefix="IBIS_BENCHMARK")
