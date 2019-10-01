#!/usr/bin/env bash
conda activate omniscidb-gpu
cd $CONDA_PREFIX
./startomnisci --base-port 26275
