from pysmt.shortcuts import Solver, And, EqualsOrIff, Not
from pysmt.oracles import get_logic

from pysmt_model.pysmt_model import PySMTModel

import re


def check_configs(smt_model: PySMTModel, impact_threshold: int = 10, sorted: bool = False) -> None:
    results = list()

    formula = And(smt_model.domains)
    target_logic = get_logic(formula)
    with Solver(logic = target_logic, name = 'z3') as solver:
        solver.add_assertion(formula)
        while solver.solve():
            config = [EqualsOrIff(key, solver.get_value(key)) for key in smt_model.vars]

            solver.add_assertion(Not(And(config)))

            impact_score = sum(smt_model.impacts[re.sub(r'=|\(|\)| ', '', str(key))] for key in config) / len(config)
            if impact_score <= impact_threshold:
                results.append({'config': config, 'impact_score': impact_score})

    if sorted:
        results.sort(key = lambda d: d['impact_score'], reverse = True) 

    return results
