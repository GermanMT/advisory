from z3 import And, Solver, sat

from advisory.models import PySMTModel


def valid_model(smt_model: PySMTModel) -> None:
    formula = And(smt_model.domains)
    solver = Solver()
    solver.add(formula)
    return solver.check() == sat