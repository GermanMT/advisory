from model.model import Model, Version

from z3 import And, Or, Int, Real, Implies

from operator import eq, gt, lt, ge, le, ne

from re import sub

from typing import Union


class PySMTModel():

    def __init__(self, model: Model) -> None:
        self.model = model
        self.domains = list()
        self.vars = list()
        self.impacts = list()
        self.__ops = {
            '=': eq,
            '>': gt,
            '<': lt,
            '>=': ge,
            '<=': le,
            '!=': ne,
            '~>': ge,
            '^': ge,
            '~': ge
            }

    def generate_model(self) -> 'PySMTModel':
        if self.model.packages:
            CVSSt = Real('CVSSt')
            self.vars.append(CVSSt)
            CVSSs = dict()

            for package in self.model.packages:
                name = 'CVSS' + package.pkg_name
                CVSSs[name] = Real(name)
                self.vars.append(CVSSs[name])

                var = Int(package.pkg_name)
                self.vars.append(var)

                versions = list()
                [versions.extend(package.versions[parent_name]) for parent_name in package.versions]

                all_p_cves, p_vars, p_cvss = self.add_versions(versions, var, CVSSs[name])

                p_domain = self.add_problems(var, package.parent_relationship.constraints)

                sub_domain = [Or(p_vars), And(p_cvss)]
                sub_domain.extend(all_p_cves)
                sub_domain.extend(p_domain)

                self.domains.append(And(sub_domain))

            p_impact = self.division(CVSSs.values())
            self.domains.append(eq(CVSSt, p_impact))

        return self

    def add_versions(self, versions: list[Version], var: Int, part_cvss: Real) -> tuple[list, list, list]:
        all_p_cves = list()
        p_vars = list()
        p_cvss = list()

        for version in versions:
            trans_ver = self.transform(version.ver_name)
            p_vars.append(var == trans_ver)

            p_cves = self.add_cves(version)
            
            exprs = [p_cve == p_cves[p_cve] for p_cve in p_cves]

            for expr in exprs:
                if expr not in all_p_cves:
                    all_p_cves.append(expr)

            v_impact = self.division(p_cves.keys()) if version.cves else 0.
            ctc = Implies(var == trans_ver, part_cvss == v_impact)
            p_cvss.append(Or(ctc))

        return (all_p_cves, p_vars, p_cvss)

    def add_cves(self, version: Version) -> dict[Real, float]:
        p_cves = dict()

        for cve in version.cves:

            old_p_cve = self.get_var(cve.id)

            if not old_p_cve:
                p_cve = Real(cve.id)
            else:
                p_cve = old_p_cve

            if cve.cvss.impact_score:
                p_cves[p_cve] = float(cve.cvss.impact_score)

        return p_cves

    @staticmethod
    def division(problem) -> float:
        return sum(problem) / len(problem) if problem else 0.

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
    def add_problems(self, var: Int, constrains: list) -> list:
        problems_ = list()

        for constraint in constrains:
            signature = constraint.signature
            if signature.__contains__('Any'):
                continue

            parts = constraint.signature.split(' ')
            problem_ = self.__ops[parts[0]](var, self.transform(parts[1]))
            problems_.append(problem_)

        return problems_

    def get_var(self, name: str) -> Union[Real, Int]:
        for var in self.vars:
            if str(var) == name:
                return var
