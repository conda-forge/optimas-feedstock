#!/usr/bin/env bash

set -eu -x -o pipefail

# Python
# $PYTHON examples/dummy/run_example.py

# Python: pytest
$PYTHON -m pytest -s -vvvv tests/
