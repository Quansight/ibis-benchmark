# ibis-benchmark

The goal of this project is the measuring of some expressions using 
`Ibis` with `OmniSciDB` `CPU` and `GPU` and pure `Pandas`.

## Environment

First, it is necessary to prepare the environments and install and start 
the servers.

### OmniSciDB CPU

To prepare and install `OmniSciDB` for `CPU`, open a new terminal and run the
following commands:

```sh
conda create -n omniscidb-cpu
conda activate omniscidb-cpu
conda install -c conda-forge omniscidb-cpu
cd $CONDA_PREFIX
mv bin/omnisci_initdb bin/initdb
./startomnisci
```

It will ask if you want to download and insert sample data, you can answer `n`.


### OmniSciDB GPU (CUDA)

To prepare and install `OmniSciDB` for `GPU` (CUDA), open a new terminal and run the
following commands:

```sh
conda create -n omniscidb-cuda
conda activate omniscidb-cuda
conda install -c quansight omniscidb-cuda
cd $CONDA_PREFIX
mv bin/omnisci_initdb bin/initdb
./omnisci_server --port 26274 --calcite-port 26279 --http-port 26278
```

It will ask if you want to download and insert sample data, you can answer `n`.


### Ibis-benchmark

To prepare the conda environment, run:

```sh
conda env create -n ibis-benchmark --file environment.yml
conda activate ibis-benchmark
```

To load the data used by this benchark, run the follow commands:

```sh
cd scripts
./download.sh
./load_data_cpu.sh
./load_data_gpu.sh
```

## Benchmark

To run the benchmark, follow the commands bellow:

```sh
cd ~/ibis_benchmark
python benchmark_nyc_taxi.py
```

The results is stored at `ibis_benchmark/results/`. 
It stores a `JSON` file with the time used by each set of expressions and a
`PNG` with the chart representation of this `JSON` file. 
