#!/usr/bin/env bash

ROOT_DIR=$(dirname "$0")/..
docker build -t pythomata-dev:latest -f $ROOT_DIR/Dockerfile $ROOT_DIR

