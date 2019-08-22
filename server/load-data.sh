#!/usr/bin/env bash

CWD="$(dirname "${0}")"

declare -A argcommands=([omnisci]=omniscidb)

if [[ "$#" == 0 ]]; then
    ARGS=(${!argcommands[@]})  # keys of argcommands
else
    ARGS=($*)
fi

python $CWD/datamgr.py download

for arg in ${ARGS[@]}; do
    python "${CWD}"/datamgr.py ${argcommands[${arg}]} &
done

FAIL=0

for job in `jobs -p`
do
    wait "${job}" || let FAIL+=1
done

if [[ "${FAIL}" == 0 ]]; then
    exit 0
else
    exit 1
fi
