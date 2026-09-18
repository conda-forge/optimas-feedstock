"""Smoke test for the optimas conda package.

Importing ``optimas`` alone only executes ``optimas/__init__.py``, which
contains nothing but ``__version__``. That succeeds even when every runtime
dependency is missing, so it cannot detect a broken dependency list. This
script exercises the parts of the package that actually pull in the runtime
dependencies.
"""

import inspect

from gest_api.vocs import VOCS

from optimas.diagnostics import ExplorationDiagnostics
from optimas.evaluators import FunctionEvaluator, TemplateEvaluator
from optimas.explorations import Exploration
from optimas.generators import (
    AxClientGenerator,
    AxMultiFidelityGenerator,
    AxMultitaskGenerator,
    AxSingleFidelityGenerator,
    GridSamplingGenerator,
    LineSamplingGenerator,
    RandomSamplingGenerator,
)

# The public API must be made of real classes. This pulls in jinja2, libensemble,
# mpi4py, pandas, matplotlib and pydantic through the respective modules.
for obj in (
    Exploration,
    ExplorationDiagnostics,
    FunctionEvaluator,
    TemplateEvaluator,
    GridSamplingGenerator,
    LineSamplingGenerator,
    RandomSamplingGenerator,
):
    assert inspect.isclass(obj), obj

# The Ax generators are silently replaced by a dummy that raises on
# instantiation when ax-platform cannot be imported, so importing them is not
# enough: check that the real implementations were loaded.
for generator in (
    AxClientGenerator,
    AxMultiFidelityGenerator,
    AxMultitaskGenerator,
    AxSingleFidelityGenerator,
):
    assert generator.__name__ != "AxImportErrorDummyGenerator", (
        f"{generator.__name__} fell back to the import-error dummy; "
        "ax-platform is missing or unusable."
    )

# Exercise a generator end to end, which requires numpy, pydantic and gest-api.
vocs = VOCS(
    variables={"x0": [-5.0, 5.0], "x1": [-5.0, 5.0]},
    objectives={"f": "MINIMIZE"},
)
gen = RandomSamplingGenerator(vocs=vocs, seed=0)
trials = gen.suggest(3)
assert len(trials) == 3, trials
assert set(trials[0]) == {"x0", "x1"}, trials[0]

print("optimas smoke test passed")
