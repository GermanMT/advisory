from pysmt.shortcuts import  Symbol, And, EqualsOrIff, Solver, Not
from pysmt.oracles import get_logic


def number_of_products(formula, keys: list[Symbol]) -> None:
    i = 0
    target_logic = get_logic(formula)
    with Solver(logic = target_logic, name = 'z3') as solver:
        solver.add_assertion(formula)
        while solver.solve():
            partial_model = [EqualsOrIff(k, solver.get_value(k)) for k in keys]
            i += 1
            # print(i)
            # print(partial_model)
            solver.add_assertion(Not(And(partial_model)))

    print(i)