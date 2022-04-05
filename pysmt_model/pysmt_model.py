from model.model import Model

from pysmt.shortcuts import  Equals, GT, LT, GE, LE, NotEquals, Symbol, And, Or, Int, Real, Div, Plus, Implies
from pysmt.typing import INT, REAL

from re import sub


class PySMTModel():

    def __init__(self, model: Model) -> None:
        self.model = model
        self.domains = list()
        self.vars = list()
        self.impacts = list()
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

    ''' 
    Con el metamodelo construido lo transformamos en un modelo PySMT
    Reglas de las leyes de Morgan:
        A <=> B      = (A => B) AND (B => A)
        A  => B      = NOT(A) OR  B
        NOT(A AND B) = NOT(A) OR  NOT(B)
        NOT(A OR  B) = NOT(A) AND NOT(B)
    '''
    def generate_model(self) -> 'PySMTModel':
        CVSSt = Symbol('CVSSt', REAL)
        self.vars.append(CVSSt)
        CVSSs = dict()

        for package in self.model.packages:
            name = 'CVSS' + package.pkg_name
            CVSSs[name] = Symbol(name, REAL)
            self.vars.append(CVSSs[name])

            var = Symbol(package.pkg_name, INT)
            self.vars.append(var)

            versions = list()
            [versions.extend(package.versions[parent_name]) for parent_name in package.versions]

            all_p_cves, p_vars, p_cvss = self.add_versions(versions, var, CVSSs[name])

            p_domain = self.add_problems(var, package.parent_relationship.constraints)

            sub_domain = [Or(p_vars), And(p_cvss)]
            sub_domain.extend(all_p_cves)
            sub_domain.extend(p_domain)

            # print('************')
            # print(Or(p_vars))
            # print('------------')
            # print(And(p_cvss))
            # print('------------')
            # print(all_p_cves)
            # print('------------')
            # print(p_domain)
            # print('------------')
            # print(And(sub_domain))

            self.domains.append(And(sub_domain))

        div = self.division(CVSSs.values())
        self.domains.append(Equals(CVSSt, div))

        print(self.domains)

        return self

    def add_versions(self, versions, var, part_cvss) -> None:
        all_p_cves = list()
        p_vars = list()
        p_cvss = list()

        for version in versions:
            trans_ver = self.transform(version.ver_name)

            p_vars.append(Equals(var, Int(trans_ver)))

            p_cves = self.add_cves(version)
            all_p_cves.extend(p_cves.values())

            v_impact = self.division(p_cves.keys()) if version.cves else Real(0.)
            ctc = Implies(Equals(var, Int(trans_ver)), Equals(part_cvss, v_impact))
            p_cvss.append(Or(ctc))

        return (all_p_cves, p_vars, p_cvss)

    def add_cves(self, version) -> dict:
        p_cves = dict()

        for cve in version.cves:
            cve_var = Symbol(cve.id, REAL)
            self.vars.append(cve_var)
            cve_val = Equals(cve_var, Real(cve.cvss.impact_score))
            p_cves[cve_var] = cve_val

        return p_cves

    @staticmethod
    def division(problem) -> Div:
        return Div(Plus(problem), Real(len(problem)))

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

        l = [int(sub('[^0-9]', '0', x), 10) for x in version.split('.')]
        l.reverse()
        version = sum(x * (100 ** i) for i, x in enumerate(l))
        return version

    ''' Crea las restricciones para el modelo smt '''
    def add_problems(self, var: Symbol, constrains: list) -> list:
        problems_ = list()

        for constraint in constrains:
            parts = constraint.signature.split(' ')
            problem_ = self.__ops[parts[0]](var, Int(self.transform(parts[1])))
            problems_.append(problem_)

        return problems_
