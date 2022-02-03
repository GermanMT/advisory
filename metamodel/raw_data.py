from ctypes import sizeof
from metamodel.dependencies import Dependencies
from metamodel.versions import get_versions

from operator import eq, gt, lt, ge, le, ne


class RawData():

    def __init__(self) -> None:
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
    def get_data(self, file: str, nameWithOwner:str) -> dict[str, list]:
        dependencies = Dependencies(file).get_dependencies(nameWithOwner)

        data = {}

        for pkg_name in dependencies:
            if dependencies[pkg_name] == 'Any':
                distributions = get_versions(pkg_name)
                data[pkg_name] = [distributions, None]
            else:
                parts = dependencies[pkg_name].split(',')
                constraints = self.get_constraints(parts)
                distributions = self.get_distributions(pkg_name, constraints)
                data[pkg_name] = [distributions, constraints]

        return data

    @staticmethod
    def approx_gt(version: str, version_: str) -> bool:
        dots = version.count('.')
        if dots == 2:
            version += '.0'
        elif dots == 1:
            version += '.0.0'
        elif dots == 0:
            version += '.0.0.0'
        
        parts = version.split('.')
        parts_ = version_.split('.')
        tam_ = len(parts_) - 1

        return version >= version_ and parts[tam_] >= parts_[tam_]

    @staticmethod
    def get_constraints(parts: list[str]) -> list[str]:
        constraints = []

        for part in parts:
            attr = part.split(' ')
            if part.__contains__('||'):
                attr = part.split(' ')
                constraint = '!= ' + attr[1]
            else:
                constraint = part
            constraints.append(constraint)

        return constraints

    def get_distributions(self, pkg_name: str, constraints: list[str]) -> list[str]:
        distributions = []

        for version in get_versions(pkg_name):
            checkers = []
            for constraint in constraints:
                parts = constraint.split(' ')
                checkers.append(self.ops[parts[0]](version, parts[1]))

            if all(checkers):
                distributions.append(version)

        return distributions
