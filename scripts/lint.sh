#!/usr/bin/env bash

set -e
set -x

mypy coriander
flake8 coriander tests
black coriander tests --check
isort coriander tests --check-only
