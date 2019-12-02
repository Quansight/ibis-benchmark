#!/usr/bin/env bash
# conda create -n postgresql postgis python=3.7
# TODO: use a env variable for postgresql data directory
# initdb --username=$(whoami) -D /work/$(whoami)/postgresql-data
# postgres -D /work/$(whoami)/postgresql-data
# pg_ctl -D /work/$(whoami)/postgresql-data -l logfile start
source activate postgresql
cd $CONDA_PREFIX
# TODO: use a env variable for postgresql data directory
postgres -D /work/$(whoami)/postgresql-data
