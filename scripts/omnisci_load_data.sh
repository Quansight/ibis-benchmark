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

# CREATE TABLE
CMD=$(cat $PWD/scripts/schema/omniscidb.sql)
echo $(echo "$CMD" | omnisql --db omnisci --user admin --passwd HyperInteractive)

# CREATE TABLE
CMD='\t'
echo $(echo "$CMD" | omnisql --db omnisci --user admin --passwd HyperInteractive)

# LOAD DATA
CMD="COPY nyc_taxi FROM '/opt/ibis_benchmark/data/nyc-taxi.csv' WITH (quoted='false');"
echo $CMD
echo $(echo "$CMD" | omnisql --db omnisci --user admin --passwd HyperInteractive)

CMD="SELECT * FROM nyc_taxi LIMIT 1;"
echo $(echo "$CMD" | omnisql --db omnisci --user admin --passwd HyperInteractive)
