from z3 import And, Solver, sat

from pysmt_model.pysmt_model import PySMTModel


def valid_model(smt_model: PySMTModel) -> None:
    formula = And(smt_model.domains)
    solver = Solver()
    solver.add(formula)
    return solver.check() == sat