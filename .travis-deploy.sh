#!/usr/bin/env bash

set -eo pipefail

make docker-build
make docker-push