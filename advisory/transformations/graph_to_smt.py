from advisory.models import Graph, PySMTModel
from advisory.objects import Version, Package

from z3 import And, Or, Int, Real, Implies

from operator import eq

from famapy.core.transformations import ModelToModel

class GraphToSMT(ModelToModel):

    @staticmethod
    def get_source_extension() -> str:
        return 'graph'

    @staticmethod
    def get_destination_extension() -> str:
        return 'smt'

    def __init__(self, source_model: Graph) -> None:
        self.source_model: Graph = source_model
        self.destination_model: PySMTModel = PySMTModel()
        self.counter: int = 0
        self.CVSSs: dict = dict()

    def transform(self) -> PySMTModel:
        if self.source_model.get_packages():
            CVSSt = Real('CVSSt')
            self.destination_model.add_var(CVSSt)

            for package in self.source_model.get_packages():
                self.add_package(package)

            p_impact = self.division(self.CVSSs.values())
            self.destination_model.add_domain(eq(CVSSt, p_impact))

        return self.destination_model

    def add_package(self, package: Package):
        name = 'CVSS' + package.pkg_name
        self.CVSSs[name] = Real(name)
        self.destination_model.add_var(self.CVSSs[name])

        var = Int(package.pkg_name)
        self.destination_model.add_var(var)

        versions = list()
        [versions.extend(package.versions[parent_name]) for parent_name in package.versions]

        self.counter = 0
        all_p_cves, p_cvss = self.add_versions(versions, var, self.CVSSs[name])

        p_domain = self.add_problems(var)

        sub_domain = [And(p_cvss)]
        sub_domain.extend(all_p_cves)
        sub_domain.extend(p_domain)

        self.destination_model.add_domain(And(sub_domain))

    def add_versions(self, versions: list[Version], var: Int, part_cvss: Real) -> tuple[list, list, list]:
        all_p_cves = list()
        p_cvss = list()

        for version in versions:
            self.destination_model.add_version(str(var), {self.counter: version})

            p_cves = self.add_cves(version)
            
            exprs = [p_cve == p_cves[p_cve] for p_cve in p_cves]

            for expr in exprs:
                if expr not in all_p_cves:
                    all_p_cves.append(expr)

            v_impact = self.division(p_cves.keys()) if version.cves else 0.
            ctc = Implies(var == self.counter, part_cvss == v_impact)
            p_cvss.append(Or(ctc))
            self.counter += 1

        return (all_p_cves, p_cvss)

    def add_cves(self, version: Version) -> dict[Real, float]:
        p_cves = dict()

        for cve in version.cves:

            old_p_cve = self.destination_model.get_var(cve.id)

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
            var <= self.counter - 1
        ]

        return problems_