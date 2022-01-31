from metamodel.dependencies import dependencies
from metamodel.versions import get_versions

from operator import eq, gt, lt, ge, le, ne


class raw_data():

    def __init__(self) -> None:
        self.problems = {}
        self.dependencies = dependencies('')
        self.ops = {
            '=': eq,
            '>': gt,
            '<': lt,
            '>=': ge,
            '<=': le,
            '!=': ne,
            '~>': self.approx_gt
            }

    ''' Usar metodo para recoger y comparar versiones obtenidas en pypi con el formato
    obtenido, y así construir el diccionario de dependencias asocidas a las distribuciones 
    aceptadas '''
    def get_data(self, file: str, nameWithOwner:str) -> dict[str, list[str]]:
        self.dependencies.file_type = file

        # GermanMT/AMADEUS
        # psf/requests
        dependencies = self.dependencies.get_dependencies(nameWithOwner)

        relationships = {}

        for pkg_name in dependencies:
            if dependencies[pkg_name] == 'Any':
                distributions = get_versions(pkg_name)
                relationships[pkg_name] = distributions
            else:
                parts = dependencies[pkg_name].split(',')
                constraints = self.get_constraints(parts)
                self.problems[pkg_name] = constraints
                distributions = self.get_distributions(pkg_name, constraints)
                relationships[pkg_name] = distributions

        return relationships

    @staticmethod
    def approx_gt(version: str, version_: str) -> bool:
        tam = len(version_) - 1
        return version >= version_ and version[tam] >= version_[tam]

    @staticmethod
    def get_constraints(parts: list[str]) -> dict[str, str]:
        constraints = {}

        for part in parts:
            attr = part.split(' ')
            if part.__contains__('||'):
                op = '!='
                version_ = attr[1]
            else:
                op = attr[0]
                version_ = attr[1]
            constraints[op] = version_

        return constraints

    def get_distributions(self, pkg_name: str, constraints: dict[str, str]) -> list[str]:
        distributions = []

        for version in get_versions(pkg_name):
            checkers = [self.ops[op](version, constraints[op]) for op in constraints]
            if all(checkers):
                distributions.append(version)

        return distributions
