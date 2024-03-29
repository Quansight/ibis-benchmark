# New York City Taxi and For-Hire Vehicle Data

This benchmark analyzes data for billions of taxi and for-hire vehicle (Uber, Lyft, etc.)
trips originating in New York City since 2009. Most of the
[raw data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
comes from the NYC Taxi & Limousine Commission.

This benchmark was based on a previous works made by `Todd W. Schneider` and `Mark Litwintschik`.
Some explanations, data structure and scripts for downloading and data loading was collected from
[@toddwschneider GitHub repo](https://github.com/toddwschneider/nyc-taxi-data/). Also, this
current document was adapted from
`https://github.com/toddwschneider/nyc-taxi-data/blob/master/README.md`. Additionally,
the scripts in this repo use and adapt some scripts and command line from `Mark Litwintschik`
blog post [A Billion Taxi Rides in Redshift](https://tech.marksblogg.com/billion-nyc-taxi-rides-redshift.html)

The current benchmark compares the time spent for ibis expressions executed on OmniSciDB CPU and GPU
and the respective expression on pure Pandas.

Statistics through June 30, 2019:

- 2.45 billion total trips
  - 1.65 billion taxi
  - 800 million for-hire vehicle
- 279 GB of raw data
- Database takes up 378 GB on disk with minimal indexes

## Instructions

Before run the benchmark, first the data should be downloaded. As the data is
not ready for `OmniSciDB`, it will be loaded first to PostgreSQL/PostGIS\*.
Once the data is completed loaded into PostgreSQL, a script will export data
from PostgreSQL to `csv` files and it should be loaded to OmniSciDB CPU and GPU.

<small>
* As the original script use the `COPY` command with fields as parameters for
header, and OmniSciDB doesn't support that yet.
</small>

### 1. Install and run databases servers

For this benchmark, OmniSciDB CPU and GPU and PostgreSQL/PostGIS will be installed
inside a conda environment.

#### 1.1 Install and run OmniSciDB-CPU and OmniSciDB-GPU using conda

Check the instructions on the main [README.md](../README.md) file,
in section `Install and run OmniSciDB-CPU and OmniSciDB-GPU using conda`.


#### 1.2 Install and run PostgreSQL/PostGIS using conda

To install and run PostgreSQL/PostGIS, in a terminal, run:

```sh
# create PG_DATA_DIR with the desired directory for postgresql data
export PG_DATA_DIR=/work/$(whoami)/postgresql-data
# create a conda environment for postgresql/postgis
# and install postgis with python 3.7
conda create -n postgresql postgis python=3.7
# activate postgresql environment
conda activate postgresql
# initialize the database postgresql and specify the data directory
initdb --username=$(whoami) -D ${PG_DATA_DIR}
# start the postgresql server with the data directory created
postgres -D  ${PG_DATA_DIR}
```

### 2. Download raw data

To download the main data, run the follow code in a terminal:

```sh
# export IBIS_BENCHMARK_DOWNLOAD with the desired folder for download
export IBIS_BENCHMARK_DOWNLOAD=/work/$(whoami)/ibis-benchmark-download
# download taxi data
./download_raw_data.sh
# remove bad rows
./remove_bad_rows.sh
```

The `remove_bad_rows.sh` script fixes two particular files that have a few rows
with too many columns. See the "data issues" section below for more.

Note that the raw data is hundreds of GB, so it will take a while to download.

The [FiveThirtyEight Uber dataset](https://github.com/fivethirtyeight/uber-tlc-foil-response)
contains Uber trip records from Apr–Sep 2014. Uber and other FHV (Lyft, Juno,
Via, etc.) data is available since Jan 2015 in the TLC's data.

To download this extra data, run the follow code in a terminal:

```sh
# export IBIS_BENCHMARK_DOWNLOAD with the desired folder for download
export IBIS_BENCHMARK_DOWNLOAD=/work/$(whoami)/ibis-benchmark-download
# download raw data for uber trips
./download_raw_2014_uber_data.sh
```

### 3. Clean and prepare data

As mentioned before, as the there are some difference among the data, the original
scripts load the data into PostgreSQL first and export that to new `CSV` files,
that would be used to load data into OmniSciDB.

#### 3.1. Initialize database and set up schema

To initialize database and set up the schema, run:

`./initialize_database.sh`

This script creates the database `nyc-taxi-data` and the initial tables with a
initial data.

#### 3.2. Import taxi, FHV and FiveThirtyEight Uber data

```sh
# export IBIS_BENCHMARK_DOWNLOAD with the desired folder for download
export IBIS_BENCHMARK_DOWNLOAD=/work/$(whoami)/ibis-benchmark-download
# import data trip
 ./import_trip_data.sh
# import data trip fhv (for-hire vehicle)
./import_fhv_trip_data.sh
# import uber data
./import_2014_uber_trip_data.sh
```

The full import process takes ~36 hours on a 2013 MacBook Pro with 16 GB of RAM.

### 4. Export normalized data to CSV files

```sh
# export IBIS_BENCHMARK_DOWNLOAD with the desired folder for download
export IBIS_BENCHMARK_DOWNLOAD=/work/$(whoami)/ibis-benchmark-download
export IBIS_BENCHMARK_DATA_CLEANED=/work/$(whoami)/ibis-benchmark-data-cleaned
# run
./export_from_postgresql_to_csv.sh
```

### 5. Load data into OmniSciDB database

Now, the data is ready to be loaded into OmniSciDB database.

To save space in disk, we can reuse the same data directory for both OmniSciDB
CPU and CUDA. So, to load the data into OmniSciDB data directory we can use
just OmniSciDB CPU.

So first, start the OmniSciDB CPU database:

```sh
# export env variables
export OMNISCIDB_DATA_DIR=/work/$(whoami)/omniscidb-data
# start omniscidb-cpu
./scripts/start_omniscidb_cpu.sh
```

Run the `create_table.sh` file to create the initial table and `load_._data.sh`
to load the data from the CSVs files to OmniSciDB database.

```sh
# create table schema
OMNISCI_PORT=6274 ./ibis_benchmark/nyc_taxi/data/omniscidb/create_table.sh
# export ibis benchmark data cleaned
export IBIS_BENCHMARK_DATA_CLEANED=/work/$(whoami)/ibis-benchmark-data-cleaned
# load data
OMNISCI_PORT=6274 ./ibis_benchmark/nyc_taxi/data/omniscidb/load_data.sh
```

### 6. Run the benchmark

First, prepare the conda environment needed by the benchmark:

```sh
# create a conda environment needed by benchmark
conda env create -n ibis-benchmark --file ./environment.yml
# activate the ibis-benchmark conda environment
conda activate ibis-benchmark
# install ibis-benchmark
make develop
```

Start a new benchmark:

```sh
# reset previous results
python ibis_benchmark/main.py --reset-result 
```

In a new terminal, start OmniSciDB CPU:

```sh
# export env variables
export OMNISCIDB_DATA_DIR=/work/$(whoami)/omniscidb-data
# start omniscidb-cpu
./scripts/start_omniscidb_cpu.sh
```

On `ibis-benchmark` conda environment, run the benchmark for OmniSciDB CPU:

```sh
python ibis_benchmark/nyc_taxi/main.py --omniscidb-cpu
```

Now, the first results are ready on `./docs/static/benchmark-nyc-txi.json`.

The next step is run the benchmark for OmniSciDB CUDA. First, ensure that
the OmniSciDB CPU is not running. So, in a new terminal, start OmniSciDB CUDA:

```sh
# export env variables
export OMNISCIDB_DATA_DIR=/work/$(whoami)/omniscidb-data
# start omniscidb-cpu
./scripts/start_omniscidb_cuda.sh
```

On `ibis-benchmark` conda environment, run the benchmark for OmniSciDB CUDA:

```sh
python ibis_benchmark/nyc_taxi/main.py --omniscidb-cuda
```

All expressions used by this benchmark are listed into expr_list at `exprs.py`.

## Schema

- `trips` table contains all yellow and green taxi trips. Each trip has a
    `cab_type_id`, which references the `cab_types` table and refers to one
    of `yellow` or `green`
- `fhv_trips` table contains all for-hire vehicle trip records,
    including ride-hailing apps Uber, Lyft, Via, and Juno
- `fhv_bases` maps `fhv_trips` to base names and "doing business as" labels,
    which include ride-hailing app names
- `nyct2010` table contains NYC census tracts plus the Newark Airport. It also
    maps census tracts to NYC's official neighborhood tabulation areas
- `taxi_zones` table contains the TLC's official taxi zone boundaries.
    Starting in July 2016, the TLC no longer provides pickup and dropoff
    coordinates. Instead, each trip comes with taxi zone pickup and
    dropoff location IDs
- `central_park_weather_observations` has summary weather data by date

## Other data sources

These are bundled with the repository, so no need to download separately, but:

- Shapefile for NYC census tracts and neighborhood tabulation areas comes from
    [Bytes of the Big Apple](https://www1.nyc.gov/site/planning/data-maps/open-data/districts-download-metadata.page)
- Shapefile for taxi zone locations comes from the TLC
- Mapping of FHV base numbers to names comes from
    [the TLC](https://data.cityofnewyork.us/Transportation/FHV-Base-Aggregate-Report/2v9c-2k7f)
- Central Park weather data comes from the [National Climatic Data Center](https://www.ncdc.noaa.gov/)

## Data issues encountered

- Remove carriage returns and empty lines from TLC data before passing to
    Postgres `COPY` command
- Some raw data files have extra columns with empty data, had to create dummy
    columns `junk1` and `junk2` to absorb them
- Two of the `yellow` taxi raw data files had a small number of rows containing
    extra columns. I discarded these rows
- The official NYC neighborhood tabulation areas (NTAs) included in the census
    tracts shapefile are not exactly what I would have expected. Some of them
    are bizarrely large and contain more than one neighborhood, e.g.
    "Hudson Yards-Chelsea-Flat Iron-Union Square", while others are confusingly
    named, e.g. "North Side-South Side" for what I'd call "Williamsburg", and
    "Williamsburg" for what I'd call "South Williamsburg". In a few instances
    I modified NTA names, but I kept the NTA geographic definitions
- The shapefile includes only NYC census tracts. Trips to New Jersey,
    Long Island, Westchester, and Connecticut are not mapped to census
    tracts, with the exception of the Newark Airport

## 2017 update

Code in support of the
[2017 update](https://toddwschneider.com/posts/analyzing-1-1-billion-nyc-taxi-and-uber-trips-with-a-vengeance/#update-2017)
to the original post lives in the `analysis/2017_update/` folder
