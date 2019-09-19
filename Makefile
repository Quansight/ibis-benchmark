.PHONY: all clean stop build start load restart init benchmark

SHELL := /bin/bash
MAKEFILE_DIR = $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
PYTHON_VERSION := 3.6
PYTHONHASHSEED := "random"
COMPOSE_FILE := "$(MAKEFILE_DIR)/docker-compose.yml"
DOCKER := docker-compose -f $(COMPOSE_FILE)
DOCKER_RUN := PYTHON_VERSION=${PYTHON_VERSION} $(DOCKER) run --rm
PYTEST_OPTIONS :=
SERVICES := omniscidb postgres waiter-postgres mysql clickhouse impala kudu-master kudu-tserver

clean:
	python setup.py clean
	find $(MAKEFILE_DIR) -name '*.pyc' -type f -delete
	rm -rf $(MAKEFILE_DIR)/build $(MAKEFILE_DIR)/dist $(find $(MAKEFILE_DIR) -name __pycache__ -type d)

develop: clean
	pip install -e .
	pre-commit install

stop:
# stop all running docker compose services
	$(DOCKER) rm --force --stop ${SERVICES}

build:
# build the ibis image
	$(DOCKER) build --pull ibis

start:
# start all docker compose services
	$(DOCKER) up --remove-orphans -d --no-build ${SERVICES}
# wait for services to start
	$(DOCKER_RUN) waiter

load:
	$(DOCKER_RUN) -e LOGLEVEL ibis load-data.sh

restart: stop
	$(MAKE) start

init: restart
	$(MAKE) build
	$(MAKE) load

benchmark:
	PYTHONHASHSEED=${PYTHONHASHSEED} $(MAKEFILE_DIR)/benchmark.sh ${PYTEST_OPTIONS} -k 'not test_import_time' \
