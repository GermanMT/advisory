from z3 import And, Or, Optimize, sat

from pysmt_model.pysmt_model import PySMTModel

import sys


def minimize_impact(
    smt_model: PySMTModel,
    limit: int = sys.maxsize
    ) -> None:

    results = list()

    _domains = list()
    _domains.extend(smt_model.domains)

    solver = Optimize()
    if smt_model.vars:
        CVSSt = smt_model.vars[0]
        solver.minimize(CVSSt)

    formula = And(_domains)
    solver.add(formula)
    while solver.check() == sat and len(results) < limit:
        config = solver.model()
        results.append(config)

        block = list()
        for var in config: # var is a declaration of a smt variable
            c = var() # create a constant from declaration
            block.append(c != config[var])

        solver.add(Or(block))

    return results