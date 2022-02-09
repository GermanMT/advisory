from metamodel.dependencies import Dependencies
from metamodel.versions import get_versions

from pkg_resources import parse_version

from operator import eq, gt, lt, ge, le, ne


class RawData():

    def __init__(self) -> None:
        self.ops = {
            '=': eq,
            '>': gt,
            '<': lt,
            '>=': ge,
            '<=': le,
            '!=': ne
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

        return parse_version(version) >= parse_version(version_) and parts[tam_] >= parts_[tam_]

    @staticmethod
    def get_constraints(parts: list[str]) -> list[str]:
        constraints = []

        for part in parts:
            if part.__contains__('||'):
                attr = part.split(' ')
                constraint = '!= ' + attr[1]
            elif part.__contains__('*'):
                part = part.replace('*', '0').replace('=', '').strip()
                constraint = '~> ' + part
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
                if parts[0] == '~>':
                    checkers.append(self.approx_gt(version, parts[1]))
                else:
                    checkers.append(self.ops[parts[0]](parse_version(version), parse_version(parts[1])))

            if all(checkers):
                distributions.append(version)

        return distributions
