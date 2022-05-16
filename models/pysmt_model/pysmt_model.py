from models.graph.graph import Graph
from models.graph.objects.model.version import Version

from z3 import And, Or, Int, Real, Implies

from operator import eq

from typing import Union


class PySMTModel():

    def __init__(self, model: Graph) -> None:
        self.model = model
        self.domains = list()
        self.vars = list()
        self.impacts = list()
        self.versions = dict()
        self.num_version = 0

    def generate_model(self) -> 'PySMTModel':
        if self.model.packages:
            CVSSt = Real('CVSSt')
            self.vars.append(CVSSt)
            CVSSs = dict()

            for package in self.model.packages:
                self.num_version = 0
                name = 'CVSS' + package.pkg_name
                CVSSs[name] = Real(name)
                self.vars.append(CVSSs[name])

                var = Int(package.pkg_name)
                self.vars.append(var)

                versions = list()
                [versions.extend(package.versions[parent_name]) for parent_name in package.versions]

                all_p_cves, p_cvss = self.add_versions(versions, var, CVSSs[name])

                p_domain = self.add_problems(var)

                sub_domain = [And(p_cvss)]
                sub_domain.extend(all_p_cves)
                sub_domain.extend(p_domain)

                self.domains.append(And(sub_domain))

            p_impact = self.division(CVSSs.values())
            self.domains.append(eq(CVSSt, p_impact))

        return self

    def add_versions(self, versions: list[Version], var: Int, part_cvss: Real) -> tuple[list, list, list]:
        all_p_cves = list()
        p_cvss = list()
        self.versions[str(var)] = dict()

        for version in versions:
            self.versions[str(var)].update({self.num_version: version})

            p_cves = self.add_cves(version)
            
            exprs = [p_cve == p_cves[p_cve] for p_cve in p_cves]

            for expr in exprs:
                if expr not in all_p_cves:
                    all_p_cves.append(expr)

            v_impact = self.division(p_cves.keys()) if version.cves else 0.
            ctc = Implies(var == self.num_version, part_cvss == v_impact)
            p_cvss.append(Or(ctc))
            self.num_version += 1

        return (all_p_cves, p_cvss)

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

    ''' Crea las restricciones para el modelo smt '''
    def add_problems(self, var: Int) -> list:
        problems_ = [
            var >= 0,
            var <= self.num_version - 1
        ]

        return problems_

    def get_var(self, name: str) -> Union[Real, Int]:
        for var in self.vars:
            if str(var) == name:
                return var
