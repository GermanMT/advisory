from metamodel.raw_data import raw_data

from pysmt.shortcuts import  Equals, GT, LT, GE, LE, NotEquals, Symbol, And, Or, EqualsOrIff, Int, get_model, Solver, Not
from pysmt.typing import INT
from pysmt.oracles import get_logic


class metamodel():

    def __init__(self, files: list[str], nameWithOwner: str) -> None:
        self.files = files
        self.nameWithOwner = nameWithOwner
        self.raw_data = raw_data()
        self.ops = {
            '=': Equals,
            '>': GT,
            '<': LT,
            '>=': GE,
            '<=': LE,
            '!=': NotEquals,
            '~>': GE
            }

    ''' Una vez obtengamos el dicionario con las dependencias asociadas a las distribuciones
    permitidas por el formato de la versión comenzaremos a construir el metamodelo'''
    def generate_metamodel(self) -> None:
        for file in self.files:
            raw_data = self.raw_data.get_data(file, self.nameWithOwner)
            ''' Añadir variables y restricciones al smt '''
            domains = []
            vars_ = []
            for variable in raw_data:
                var = Symbol(variable, INT)
                vars_.append(var)

                if variable in self.raw_data.problems:
                    p_domain = self.add_problems(var, self.raw_data.problems[variable])
                v_domain = Or([Equals(var, Int(self.transform(version))) for version in raw_data[variable]])
                
                aux = [v_domain]
                aux.extend(p_domain)
                domains.append(And(aux))

            ''' Muestra la cantidad de soluciones posibles '''
            self.all_smt(And(domains), vars_)


    @staticmethod
    def all_smt(formula, keys: list[Symbol]) -> None:
        i = 0
        target_logic = get_logic(formula)
        with Solver(logic = target_logic, name = 'z3') as solver:
            solver.add_assertion(formula)
            while solver.solve():
                partial_model = [EqualsOrIff(k, solver.get_value(k)) for k in keys]
                i += 1
                print(i)
                # print(partial_model)
                solver.add_assertion(Not(And(partial_model)))

        print(i)

    ''' Mejorar método para asignar a las versiones una combinación única'''
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