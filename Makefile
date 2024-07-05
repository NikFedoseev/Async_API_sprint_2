CODE ?= ./apps

.PHONY: up down local lint

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
