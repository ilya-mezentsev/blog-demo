ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

TARGET_PYTHON_VERSION = python3

SOURCE_FOLDER := $(ROOT_DIR)/src
BACKEND_DIR := $(SOURCE_FOLDER)/blog-demo-backend
CONFIG_DIR := $(SOURCE_FOLDER)/config

VENV_DIR ?= $(BACKEND_DIR)/venv
VENV_PIP := $(VENV_DIR)/bin/pip
VENV_PYTHON = $(VENV_DIR)/bin/python
VENV_MYPY := $(VENV_DIR)/bin/mypy
VENV_FMT := $(VENV_DIR)/bin/autopep8
VENV_LOCUST := $(VENV_DIR)/bin/locust

ENTRYPOINT_FILE := $(BACKEND_DIR)/main.py
INIT_TEST_DATA_FILE := $(BACKEND_DIR)/test_data.py
REQUIREMENTS_FILE := $(BACKEND_DIR)/requirements.txt

BACKEND_SOURCE_FOLDER := $(BACKEND_DIR)/blog_demo_backend

MAIN_CONFIG_PATH ?= $(CONFIG_DIR)/main.json

DOCKER_COMPOSE_FILE := $(ROOT_DIR)/docker-compose.yaml
DOCKER_COMPOSE_HL_FILE := $(ROOT_DIR)/docker-compose.hl.yaml

LOCUST_FILE := $(SOURCE_FOLDER)/high-load/tests/locustfile.py

PG_SCHEMA_FILE := $(SOURCE_FOLDER)/schema/pg.sql

PROJECT_NAME := blog_demo

run:
	$(VENV_PYTHON) $(ENTRYPOINT_FILE) --config-path $(MAIN_CONFIG_PATH) --logging-level warning

run-inside-container: clean install
	$(VENV_PYTHON) $(ENTRYPOINT_FILE) --config-path $(MAIN_CONFIG_PATH) --logging-level warning

debug:
	$(VENV_PYTHON) $(ENTRYPOINT_FILE) --config-path $(MAIN_CONFIG_PATH) --logging-level debug

install: venv-dir requirements

requirements:
	$(VENV_PIP) install -r $(REQUIREMENTS_FILE)

clean:
	rm -rf $(VENV_DIR)

check:
	$(VENV_MYPY) $(BACKEND_SOURCE_FOLDER)

fmt:
	$(VENV_FMT) --in-place --recursive $(BACKEND_SOURCE_FOLDER)

venv-dir:
	virtualenv --python=$(TARGET_PYTHON_VERSION) $(VENV_DIR)

calc-lines:
	( find $(BACKEND_SOURCE_FOLDER) -name '*.py' -print0 | xargs -0 cat ) | wc -l

init-test-data: db-reset
	$(VENV_PYTHON) $(INIT_TEST_DATA_FILE) --config-path $(MAIN_CONFIG_PATH)

start-load-test-master:
	$(VENV_LOCUST) -f $(LOCUST_FILE) -H http://127.0.0.1:4000 --master

start-load-test-worker:
	$(VENV_LOCUST) -f $(LOCUST_FILE) --worker

db-reset:
	cat $(PG_SCHEMA_FILE) | docker-compose -f $(DOCKER_COMPOSE_FILE) -p $(PROJECT_NAME) exec -T db psql -U blog_demo -d blog_demo

containers-build:
	docker-compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_HL_FILE) -p $(PROJECT_NAME) build

containers-run:
	docker-compose -f $(DOCKER_COMPOSE_FILE) -p $(PROJECT_NAME) up

containers-hl-run:
	docker-compose \
		-f $(DOCKER_COMPOSE_FILE) \
		-f $(DOCKER_COMPOSE_HL_FILE) \
		-p $(PROJECT_NAME) \
		up backend nginx alertmanager prometheus

containers-hl-run-scaled:
	docker-compose \
		-f $(DOCKER_COMPOSE_FILE) \
		-f $(DOCKER_COMPOSE_HL_FILE) \
		-p $(PROJECT_NAME) \
		up --scale backend=3 backend nginx

containers-clean:
	docker-compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_HL_FILE) -p $(PROJECT_NAME) down
