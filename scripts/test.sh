#!/usr/bin/env bash

set -e
set -x

pytest --cov=coriander tests --cov-report term-missing
