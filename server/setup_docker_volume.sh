#!/bin/bash

if [ -z "${IBIS_TEST_DATA_DIRECTORY}" ]; then
    echo "IBIS_TEST_DATA_DIRECTORY environment variable is empty"
    exit 1
fi

if [ ! -e "${IBIS_TEST_DATA_DIRECTORY}" ]; then
    echo "IBIS_TEST_DATA_DIRECTORY=${IBIS_TEST_DATA_DIRECTORY} does not exist"
    exit 1
fi

if [ ! -d "${IBIS_TEST_DATA_DIRECTORY}" ]; then
    echo "IBIS_TEST_DATA_DIRECTORY=${IBIS_TEST_DATA_DIRECTORY} is not a directory"
    exit 1
fi

mkdir -p /tmp/ibis
