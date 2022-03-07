from pysmt.shortcuts import Solver, And, EqualsOrIff, Not
from pysmt.oracles import get_logic

import re


def new_operation(modelo, impact_score) -> None:
    result = list()

    formula = And(modelo.domains)
    target_logic = get_logic(formula)
    with Solver(logic = target_logic, name = 'z3') as solver:
        solver.add_assertion(formula)
        while solver.solve():
            partial_model = [EqualsOrIff(k, solver.get_value(k)) for k in modelo.vars]

            aux = list()
            for semi_model in partial_model:
                aux.append(re.sub(r'=|\(|\)| ', '', str(semi_model)))
            solver.add_assertion(Not(And(partial_model)))

            threshold = sum(modelo.impacts[key] for key in aux) / len(aux)
            if threshold <= impact_score:
                result.append(partial_model)

    return result
