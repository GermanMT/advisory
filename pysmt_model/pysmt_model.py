from model.model import Model

from pysmt.shortcuts import  Equals, GT, LT, GE, LE, NotEquals, Symbol, And, Or, Int
from pysmt.typing import INT

import re


class PySMTModel():

    def __init__(self, model: Model) -> None:
        self.model = model
        self.domains = list()
        self.vars = list()
        self.__ops = {
            '=': Equals,
            '>': GT,
            '<': LT,
            '>=': GE,
            '<=': LE,
            '!=': NotEquals,
            '~>': GE,
            '^': GE,
            '~': GE
            }

    ''' Con el metamodelo construido lo transformamos en un modelo PySMT '''
    def generate_model(self) -> None:
        for package in self.model.packages:
            var = Symbol(package.pkg_name, INT)
            self.vars.append(var)

            versions_ = list()
            for parent_name in package.versions:
                versions_.extend(package.versions[parent_name])

            aux = [Or([Equals(var, Int(self.transform(version.ver_name))) for version in versions_])]
            # if v_domain is false there aren't any version that satisfies the constraints
            # print(v_domain)

            # for relelationship in package.parent_relationship:
            p_domain = self.add_problems(var, package.parent_relationship.constraints)
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

        l = [int(re.sub('[^0-9]', '0', x), 10) for x in version.split('.')]
        l.reverse()
        version = sum(x * (100 ** i) for i, x in enumerate(l))
        return version

    ''' Crea las restricciones para el modelo smt '''
    def add_problems(self, var: Symbol, constrains: list) -> list:
        problems_ = []

        for constraint in constrains:
            parts = constraint.signature.split(' ')
            problem_ = self.__ops[parts[0]](var, Int(self.transform(parts[1])))
            problems_.append(problem_)

        return problems_