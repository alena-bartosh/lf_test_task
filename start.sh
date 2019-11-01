#!/usr/bin/env bash

# stop script if any command fails
set -e

# build docker image with tag name
docker build -t queries_calc_api .
# run all unittests before service start-up
docker run queries_calc_api python -m unittest discover tests
# run service
docker run -p 5000:5000 queries_calc_api
