from advisory.models.graph.apis.git.dependencies import get_dependencies
from advisory.models.graph.utils.parse_constraints import parse_constraints
from advisory.models.graph.utils.add_cves import add_cves

from advisory.models import Graph

from advisory.objects import Package, Relationship, Constraint

from famapy.core.transformations import Transformation


class BuildGraph(Transformation):

    def __init__(self, source_model: Graph, total_level: int) -> None:
        self.__source_model = source_model
        self.__total_level = total_level

    def transform(
        self,
        parent: 'Package'
    ) -> None:

        if parent.get_level() >= self.__total_level:
            return ''

        dependencies = get_dependencies(parent)

        new_packages = list()

        for pkg_name in dependencies:
            package = self.__source_model.get_package(pkg_name)

            reqs = dependencies[pkg_name][4].split(',')

            constraints = self.__source_model.add_constraints(parse_constraints(reqs))

            new_relationship = self.build_relationship(parent, constraints)

            if not package:
                package = self.build_package(pkg_name, parent.get_level(), dependencies, new_relationship)
                
                are_void = False
                for version in package.get_versions():
                    if not package.get_versions()[version]:
                        are_void = True
                        break

                if are_void:
                    continue

                self.__source_model.add_package(package)
                self.__source_model.add_relationship(new_relationship)
            else:
                package.level += 1

            new_packages.append(package)

            new_relationship.add_child(package)

            parent.add_child_relationship(new_relationship)

        for package in new_packages:
            self.transform(package)

    def build_package(
        self,
        pkg_name: str,
        current_level: int,
        dependencies: dict[str, str],
        parent: 'Relationship'
    ) -> 'Package':

        pkg = Package(
                current_level + 1,
                pkg_name,
                dependencies[pkg_name][0],
                dependencies[pkg_name][1],
                dependencies[pkg_name][2],
                dependencies[pkg_name][3],
                parent
            )

        return pkg

    def build_relationship(
        self,
        parent: 'Package',
        constraints: list['Constraint']
    ) -> 'Relationship':

        rel = Relationship(
                parent,
                constraints = constraints
            )

        return rel

    def attribute(self):
        for package in self.__source_model.get_packages():
            if package.get_versions():
                add_cves(package)
