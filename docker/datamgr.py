#!/usr/bin/env python

import logging
import os
import zipfile
from pathlib import Path

import click

SCRIPT_DIR = Path(__file__).parent.absolute()
DATA_DIR_NAME = "ibis-testing-data"
DATA_DIR = Path(
    os.environ.get("IBIS_TEST_DATA_DIRECTORY", SCRIPT_DIR / DATA_DIR_NAME)
)

TEST_TABLES = ['nyc_taxi']


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
@click.option(
    "--repo-url", "-r", default="https://github.com/ibis-project/testing-data"
)
@click.option("-d", "--directory", default=DATA_DIR)
def download(repo_url, directory):
    from plumbum.cmd import curl
    from shutil import rmtree

    directory = Path(directory)
    # download the master branch
    url = repo_url + "/archive/master.zip"
    # download the zip next to the target directory with the same name
    path = directory.with_suffix(".zip")

    if not path.exists():
        logger.info("Downloading {} to {}...".format(url, path))
        path.parent.mkdir(parents=True, exist_ok=True)
        download = curl[url, "-o", path, "-L"]
        download(
            stdout=click.get_binary_stream("stdout"),
            stderr=click.get_binary_stream("stderr"),
        )
    else:
        logger.info("Skipping download: {} already exists".format(path))

    logger.info("Extracting archive to {}".format(directory))

    # extract all files
    extract_to = directory.with_name(directory.name + "_extracted")
    with zipfile.ZipFile(str(path), "r") as f:
        f.extractall(str(extract_to))

    # remove existent folder
    if directory.exists():
        rmtree(str(directory))

    # rename to the target directory
    (extract_to / "testing-data-master").rename(directory)

    # remove temporary extraction folder
    extract_to.rmdir()


@cli.command()
@click.option("-h", "--host", default="localhost")
@click.option("-P", "--port", default=6274, type=int)
@click.option("-u", "--user", default="admin")
@click.option("-p", "--password", default="HyperInteractive")
@click.option("-D", "--database", default="ibis_testing")
@click.option("--protocol", default="binary")
@click.option(
    "-S",
    "--schema",
    type=click.File("rt"),
    default=str(SCRIPT_DIR / "schema" / "omnisci.sql"),
)
@click.option("-t", "--tables", multiple=True, default=TEST_TABLES + ["geo"])
@click.option("-d", "--data-directory", default=DATA_DIR)
def omnisci(schema, tables, data_directory, **params):
    import pymapd

    data_directory = Path(data_directory)
    # reserved_words = ["table", "year", "month"]

    # connection
    logger.info("Initializing OmniSci...")
    default_db = "omnisci"
    if params["database"] != default_db:
        conn = pymapd.connect(
            host=params["host"],
            user=params["user"],
            password=params["password"],
            port=params["port"],
            dbname=default_db,
            protocol=params["protocol"],
        )
        database = params["database"]
        stmt = "DROP DATABASE {}".format(database)
        try:
            conn.execute(stmt)
        except Exception:
            logger.warning("OmniSci DDL statement %r failed", stmt)

        stmt = "CREATE DATABASE {}".format(database)
        try:
            conn.execute(stmt)
        except Exception:
            logger.exception("OmniSci DDL statement %r failed", stmt)
        conn.close()

    conn = pymapd.connect(
        host=params["host"],
        user=params["user"],
        password=params["password"],
        port=params["port"],
        dbname=database,
        protocol=params["protocol"],
    )

    # create tables
    for stmt in filter(None, map(str.strip, schema.read().split(";"))):
        try:
            conn.execute(stmt)
        except Exception:
            logger.exception("OmniSci DDL statement \n%r\n failed", stmt)

    # TODO: import data
    conn.close()


if __name__ == "__main__":
    """
    Environment Variables are automatically parsed:
     - IBIS_TEST_{BACKEND}_PORT
     - IBIS_TEST_{BACKEND}_HOST
     - IBIS_TEST_{BACKEND}_USER
     - IBIS_TEST_{BACKEND}_PASSWORD
     - etc.
    """
    cli(auto_envvar_prefix="IBIS_TEST")
