from metamodel.metamodel import Metamodel

from pysmt.shortcuts import  Equals, GT, LT, GE, LE, NotEquals, Symbol, And, Or, Int
from pysmt.typing import INT


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
        dist_feats = filter(lambda feat: feat.parent is None, self.metamodel.features)
        for feat in dist_feats:
            var = Symbol(feat.name, INT)
            self.vars.append(var)
            ctc_names = {}
            for ctc in feat.constraints:
                ctc_names.update(ctc.name)

            for rel in feat.relations:
                if feat.constraints:
                    p_domain = self.add_problems(var, ctc_names)
                v_domain = Or([Equals(var, Int(self.transform(version.name))) for version in rel.childrens])
                
                aux = [v_domain]
                aux.extend(p_domain)
                self.domains.append(And(aux))

        print(self.vars)
        print(self.domains)
        return self

    ''' Transforma las versiones en un entero '''
    @staticmethod
    def transform(version: str) -> int:
        ''' Si no está completa se añade un '.0.0' / '.0' al final de la version '''
        dots = version.count('.')
        if dots == 1:
            version = version + '.0'
        elif dots == 0:
            version = version + '.0.0'

        l = [int(x, 10) for x in version.split('.') if x.isnumeric()]
        l.reverse()
        version = sum(x * (100 ** i) for i, x in enumerate(l))
        return version

    ''' Crea las restricciones para el modelo smt '''
    def add_problems(self, var: Symbol, problems: dict[str, str]) -> list:
        problems_ = []

        for problem in problems:
            if problem.__contains__('||'):
                op = '!='
                version_ = problems[problem]
            else:
                op = problem
                version_ = problems[problem]
            problem_ = self.ops[op](var, Int(self.transform(version_)))
            problems_.append(problem_)

        return problems_