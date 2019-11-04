#!/usr/bin/env bash

cd src/humans-of-paris-1900/
source activate humans-of-paris
gunicorn --bind 0.0.0.0:5000 --log-level debug --log-file=- --workers=10 --threads=4 --worker-class=gthread manage:app