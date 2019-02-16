#!/usr/bin/env bash

docker run -i -t -w /build --rm -v $(pwd):/build pythomata-dev:latest /bin/bash

