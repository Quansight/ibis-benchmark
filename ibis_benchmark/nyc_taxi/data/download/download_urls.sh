#!/bin/bash

data_dir=${IBIS_BENCHMARK_DATA}

usage()
{
  echo "usage: download_urls [-d --data-dir] | [-h]\n"
  echo "--data-dir should exist, default \${IBIS_BENCHMARK_DATA}"
}

while [ "$1" != "" ]; do
  case $1 in
    -d | --data-dir )   shift
                    data_dir=$1
                    ;;
    -h | --help )   usage
                    exit
                    ;;
    * )             usage
                    exit 1
  esac
  shift
done

if test -f "$data_dir"; then
  usage
  echo "[EE] Invalid data directory."
  exit 1
fi

# create data directory
mkdir -p $data_dir/theHoard/trips/
# get urls file
url_file=$(pwd)/setup_files/urls.txt
# change directory to the data directory
cd $data_dir/theHoard/trips/
# download files listed inside urls file
cat ${url_file} | xargs -n 1 -P 6 wget -c 
