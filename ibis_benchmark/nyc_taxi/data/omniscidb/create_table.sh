#!/bin/bash
omnisql -u admin -p HyperInteractive --port $OMNISCI_PORT < schema/create_trips_table.sql
