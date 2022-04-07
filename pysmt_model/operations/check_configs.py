from z3 import And, Or, Solver, Optimize, sat

from pysmt_model.pysmt_model import PySMTModel


def check_configs(
    smt_model: PySMTModel, 
    impact_threshold: float = 10., 
    minimize: bool = False,
    maximize: bool = False,
    limit: int = 100000000
    ) -> None:

    results = list()
    CVSSt = smt_model.vars[0]

    threshold_ctc = CVSSt <= impact_threshold
    smt_model.domains.append(threshold_ctc)

    if minimize:
        solver = Optimize()
        solver.minimize(CVSSt)
    elif maximize:
        solver = Optimize()
        solver.maximize(CVSSt)
    else:
        solver = Solver()

    formula = And(smt_model.domains)
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
