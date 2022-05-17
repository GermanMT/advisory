from z3 import And, Or, Solver, sat

from models.pysmt_model.pysmt_model import PySMTModel

import sys


def filter_configs(
    smt_model: PySMTModel, 
    max_threshold: float = 10.,
    min_threshold: float = 0.,
    limit: int = sys.maxsize
    ) -> None:

    results = list()

    _domains = list()
    _domains.extend(smt_model.get_domains())

    if smt_model.get_vars():
        CVSSt = smt_model.get_vars()[0]
        max_ctc = CVSSt <= max_threshold
        min_ctc = CVSSt >= min_threshold
        _domains.extend([max_ctc, min_ctc])

    solver = Solver()
    formula = And(_domains)
    solver.add(formula)
    while solver.check() == sat and len(results) < limit:
        config = solver.model()
        if config:
            results.append(config)

        block = list()
        for var in config: # var is a declaration of a smt variable
            c = var() # create a constant from declaration
            block.append(c != config[var])

        solver.add(Or(block))

    return results
