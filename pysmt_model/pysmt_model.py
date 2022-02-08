from metamodel.metamodel import Metamodel

from pysmt.shortcuts import  Equals, GT, LT, GE, LE, NotEquals, Symbol, And, Or, Int
from pysmt.typing import INT

import re


class PySMTModel():

    def __init__(self, metamodel: Metamodel) -> None:
        self.metamodel = metamodel
        self.domains = list()
        self.vars = list()
        self.ops = {
            '=': Equals,
            '>': GT,
            '<': LT,
            '>=': GE,
            '<=': LE,
            '!=': NotEquals,
            '~>': GE
            }

    ''' Con el metamodelo construido lo transformamos en un modelo PySMT '''
    def generate_model(self) -> None:
        for pkg in self.metamodel.packages:
            var = Symbol(pkg.name, INT)
            self.vars.append(var)

            for rel in pkg.relations:
                v_domain = Or([Equals(var, Int(self.transform(version))) for version in rel.versions])
                aux = [v_domain]
                # if v_domain is false there aren't any version that satisfies the constraints
                # print(v_domain)

                if pkg.constraints:
                    p_domain = self.add_problems(var, pkg.constraints)
                    aux.extend(p_domain)

                self.domains.append(And(aux))

        print(self.vars)
        print(self.domains)
        return self

    ''' Transforma las versiones en un entero '''
    @staticmethod
    def transform(version: str) -> int:
        ''' Si no está completa se añade un '0.0.0' / '.0.0' / '.0' al final de la version '''
        dots = version.count('.')
        if dots == 2:
            version += '.0'
        elif dots == 1:
            version += '.0.0'
        elif dots == 0:
            version += '.0.0.0'

        l = [int(re.sub('[^0-9]','', x), 10) for x in version.split('.')]
        l.reverse()
        version = sum(x * (100 ** i) for i, x in enumerate(l))
        return version

    ''' Crea las restricciones para el modelo smt '''
    def add_problems(self, var: Symbol, problems: list) -> list:
        problems_ = []

        for problem in problems:
            parts = problem.name.split(' ')
            problem_ = self.ops[parts[0]](var, Int(self.transform(parts[1])))
            problems_.append(problem_)

        return problems_