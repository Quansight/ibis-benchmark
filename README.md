# Ibis Benchmark

The goal of this project is the measuring of some expressions using 
`Ibis` with `OmniSciDB` `CPU` and `GPU` and pure `Pandas`.

The current benchmark was tested in a Ubuntu machine with kernel 4.15.0-62-generic.

## Environment

First, it is necessary to prepare the environments and install and start 
the servers.

### Install and run OmniSciDB-CPU and OmniSciDB-GPU using conda

For installing and running OmniSciDB-CPU, in a terminal, run:

```sh
# create a conda environment and install omniscidb-cpu
conda create -n omniscidb-cpu -c conda-forge omniscidb-cpu
# activate omniscidb-cpu conda environemtn
source activate omniscidb-cpu
# rename initdb to pg_initdb
cp $CONDA_PREFIX/bin/initdb pg_initdb
# rename initdb to pg_initdb
cp $CONDA_PREFIX/bin/omnisci_initdb initdb
# deactivate the environment
source deactivate
# export env variables
export OMNISCIDB_CPU_DATA_DIR=/work/$(whoami)/omniscidb-cpu-data
# start omniscidb-cpu
cd scripts && ./start_omniscidb_cpu.sh
```

For installing and running OmniSciDB-GPU, in another terminal, run:

```sh
# create a conda environment and install omniscidb-gpu
conda create -n omniscidb-gpu -c quansight omniscidb-gpu
# activate omniscidb-gpu conda environemtn
source activate omniscidb-gpu
# rename initdb to pg_initdb
cp $CONDA_PREFIX/bin/initdb pg_initdb
# rename initdb to pg_initdb
cp $CONDA_PREFIX/bin/omnisci_initdb initdb
# deactivate the environment
source deactivate
# start omniscidb-gpu
cd scripts && ./start_omniscidb_gpu.sh
```


### Ibis-benchmark

To prepare the conda environment, run:

```sh
conda env create -n ibis-benchmark --file environment.yml
conda activate ibis-benchmark
```

Install ibis-benchmark in development mode and some libraries that help the 
develpment:

```
make develop
```

## NYC Taxi Benchmark

To load the data used by this benchark, run the follow commands:

```sh
cd scripts
./download.sh
./load_data_cpu.sh
./load_data_gpu.sh
```

To run the benchmark, follow the commands bellow:

```sh
cd ./ibis_benchmark/nyc_taxi
python main.py
```

The results is stored at `ibis_benchmark/results/`. 
It stores a `JSON` file with the time used by each set of expressions and a
`PNG` with the chart representation of this `JSON` file. 
