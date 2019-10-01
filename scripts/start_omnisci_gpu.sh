#!/usr/bin/env bash
source activate omniscidb-cuda
cd $CONDA_PREFIX
./startomnisci --base-port 26275
