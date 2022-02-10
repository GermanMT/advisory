from pysmt.shortcuts import Solver, And
from pysmt.oracles import get_logic


def valid_model(domains) -> None:
    formula = And(domains)
    target_logic = get_logic(formula)
    with Solver(logic = target_logic, name = 'z3') as solver:
        solver.add_assertion(formula)
        return solver.solve()