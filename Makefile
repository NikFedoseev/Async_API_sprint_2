CODE ?= ./apps
VENV ?= .venv

.PHONY: up down local lint

init:
	python3.12 -m venv $(VENV)
	$(VENV)/bin/pip config --site set global.index-url https://pypi.org/simple/
	$(VENV)/bin/pip config --site set global.extra-index-url https://pypi.org/simple/
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install

up:
	docker compose up --build

down:
	docker compose down -v --remove-orphans

local:
	docker compose -f docker-compose.local.yml up -d --build

plint:
	ruff format $(CODE)
	ruff check $(CODE) --fix --show-fixes
	MYPYPATH=./apps/movies mypy --explicit-package-bases $(CODE)


.DEFAULT_GOAL := up
