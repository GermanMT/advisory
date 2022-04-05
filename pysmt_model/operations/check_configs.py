from pysmt.shortcuts import Solver, And, EqualsOrIff, Not, LE, Real
from pysmt.oracles import get_logic

from pysmt_model.pysmt_model import PySMTModel


def check_configs(smt_model: PySMTModel, impact_threshold: float = 10., sorted: bool = False) -> None:
    results = list()
    CVSSt = smt_model.vars[0]

    threshold_ctc = LE(CVSSt, Real(impact_threshold))
    smt_model.domains.append(threshold_ctc)

    formula = And(smt_model.domains)
    target_logic = get_logic(formula)
    with Solver(logic = target_logic, name = 'z3') as solver:
        solver.add_assertion(formula)
        while solver.solve():
            config = [EqualsOrIff(key, solver.get_value(key)) for key in smt_model.vars]

            solver.add_assertion(Not(And(config)))

            results.append(config)
            print(config)

    return results
