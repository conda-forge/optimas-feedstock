#!/usr/bin/env bash

set -eu -x -o pipefail

# Python
# $PYTHON examples/dummy/run_example.py

# Python: pytest
#   test_xopt_generators.py imports xopt at module level, which is not a
#   dependency of optimas, so skip that file.
$PYTHON -m pytest -s -vvvv tests/ --ignore=tests/test_xopt_generators.py
