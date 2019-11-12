#!/usr/bin/env bash
#
# Usage: omnisql [<database>] [{--user|-u} <user>] [{--passwd|-p} <password>] 
#        [--port <port number>] [{-s|--server} <server host>] [--http] 
#        [{--no-header|-n}] [{--quiet|-q}] [{--delimiter|-d}]
# 
# Options:
#   -h [ --help ]                    Print help messages
#   -v [ --version ]                 Print omnisql version number
#   -n [ --no-header ]               Do not print query result header
#   -t [ --timing ]                  Print timing information
#   -d [ --delimiter ] arg (=|)      Field delimiter in row output
#   --db arg                         Database name (server default is omnisci)
#   -u [ --user ] arg (=admin)       User name
#   --ca-cert arg                    Path to trusted server certificate.
#                                    Initiates an encrypted connection
#   -p [ --passwd ] arg              Password
#   --history arg                    History filename
#   -s [ --server ] arg (=localhost) Server hostname
#   --port arg (=6274)               Port number
#   --http                           Use HTTP transport
#   --https                          Use HTTPS transport
#   --skip-verify                    Don't verify SSL certificate validity
#   -q [ --quiet ]                   Do not print result headers or connection
#                                  strings

set -ex

PWD="$(dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" )"

CMD_CREATE_SCHEMA=$(cat $PWD/scripts/schema/omniscidb.sql)
CMD_SHOW_TABLES='\t'
CMD_COPY="COPY nyc_taxi FROM '$PWD/scripts/data/nyc-taxi.csv' WITH (quoted='false');"
CMD_SELECT_TABLE="SELECT * FROM nyc_taxi LIMIT 1;"

# =============
# GPU DATA LOAD
# =============

OMNISCIDB_GPU_PARAMS=" --db omnisci --user admin --passwd HyperInteractive --port 26274"

# CREATE TABLE
echo $(echo "$CMD_CREATE_SCHEMA" | omnisql $OMNISCIDB_GPU_PARAMS)
echo $(echo "$CMD_SHOW_TABLES" | omnisql $OMNISCIDB_GPU_PARAMS)

# LOAD DATA
echo $CMD_COPY
echo $(echo "$CMD_COPY" | omnisql $OMNISCIDB_GPU_PARAMS)
echo $(echo "$CMD_SELECT_TABLE" | omnisql $OMNISCIDB_GPU_PARAMS)
