from z3 import And, Or, Optimize, sat

from advisory.models import PySMTModel

import sys


def maximize_impact(
    smt_model: PySMTModel,
    limit: int = sys.maxsize
    ) -> None:

    results = list()

    _domains = list()
    _domains.extend(smt_model.get_domains())

    solver = Optimize()
    if smt_model.get_vars():
        CVSSt = smt_model.get_vars()[0]
        solver.maximize(CVSSt)

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