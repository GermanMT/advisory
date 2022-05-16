from z3 import And, Or, Solver, sat

from models.pysmt_model.pysmt_model import PySMTModel


def number_of_products(smt_model: PySMTModel) -> None:
    i = 0
    formula = And(smt_model.domains)
    solver = Solver()
    solver.add(formula)
    while solver.check() == sat:
        config = solver.model()

        block = list()
        for var in config:
            c = var()
            block.append(c != config[var])

        solver.add(Or(block))
        i += 1

    return i