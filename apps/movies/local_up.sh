#!/usr/bin/env bash

exec gunicorn main:app --workers 4 --access-logfile - --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
