#!/usr/bin/env bash
source activate omniscidb-cuda

# define env variables
export OMNISCI_STORAGE=${OMNISCIDB_DATA_DIR}/data
export MAPD_DATA=${OMNISCI_STORAGE}
# create folder
mkdir -p $OMNISCI_STORAGE

cd $CONDA_PREFIX/opt/omnisci
./startomnisci --base-port 26275 --data $OMNISCI_STORAGE
