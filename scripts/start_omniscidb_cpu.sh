#!/usr/bin/env bash
source activate omniscidb-cpu

# define env variables
export OMNISCI_STORAGE=${OMNISCIDB_DATA_DIR}/data
export MAPD_DATA=${OMNISCI_STORAGE}
# create folder
mkdir -p $OMNISCI_STORAGE
# start server
cd $CONDA_PREFIX
./startomnisci --data $OMNISCI_STORAGE
