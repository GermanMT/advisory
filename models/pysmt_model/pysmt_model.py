from models.graph.objects.model.version import Version

from z3 import And, Or, Int, Real, Implies

from operator import eq

from typing import Union

from famapy.core.models import VariabilityModel


class PySMTModel(VariabilityModel):

    @staticmethod
    def get_extension() -> str:
        return 'pysmt'

    def __init__(self) -> None:
        self._domains = list()
        self._vars = list()
        self._versions = dict()

    def add_domain(self, domain: Union[And, Or, Implies]) -> None:
        self._domains.append(domain)

    def add_var(self, var: Union[Real, Int]) -> None:
        self._vars.append(var)

    def add_version(self, name: str, version: dict[int, Version]) -> None:
        # print(name)
        # print(version)
        # print(self._versions)
        if name not in self._versions:
            self._versions[name] = version
        else:
            self._versions[name].update(version)

    def get_domains(self) -> list[Union[And, Or, Implies]]:
        return self._domains

    def get_vars(self) -> list[Union[Real, Int]]:
        return self._vars

    def get_versions(self) -> dict[str, dict[int, Version]]:
        return self._versions

    def get_var(self, name: str) -> Union[Real, Int]:
        for var in self._vars:
            if str(var) == name:
                return var