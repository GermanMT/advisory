from metamodel.dependencies import dependencies
from metamodel.versions import get_versions

import operator


class metamodel():

    def __init__(self, files: list[str]) -> None:
        self.files = files
        self.dependencies = dependencies('')
        self.ops = {
            '=': operator.eq,
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            '!=': operator.ne,
            '~>': self.approx_gt
            }

    ''' Una vez obtengamos el dicionario con las dependencias asociadas a las distribuciones
    permitidas por el formato de la versión comenzaremos a construir el metamodelo'''
    def generate_metamodel(self) -> None:
        for file in self.files:
            print(self.get_raw(file))

    ''' Usar metodo para recoger y comparar versiones obtenidas en pypi con el formato
    obtenido, y así construir el diccionario de dependencias asocidas a las distribuciones 
    aceptadas '''
    def get_raw(self, file: str) -> dict[str, list[str]]:
        self.dependencies.file_type = file

        # GermanMT/AMADEUS
        # psf/requests
        dependencies = self.dependencies.get_dependencies('psf/requests')

        relationships = {}

        for pkg_name in dependencies:
            if dependencies[pkg_name] == 'Any':
                distributions = get_versions(pkg_name)
                relationships[pkg_name] = distributions
            else:
                parts = dependencies[pkg_name].split(',')
                constraints = self.get_constraints(parts)
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
