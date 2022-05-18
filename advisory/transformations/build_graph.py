from advisory.models.graph.apis.git.dependencies import get_dependencies
from advisory.models.graph.utils.parse_constraints import parse_constraints

from advisory.models import Graph

from advisory.objects import Package, Relationship, Constraint

from famapy.core.transformations import Transformation


class BuildGraph(Transformation):

    def __init__(self, source_model: Graph, total_level: int) -> None:
        self.source_model = source_model
        self.total_level = total_level

    def transform(
        self,
        parent: 'Package'
    ) -> None:

        if parent.level >= self.total_level:
            return ''

        dependencies = get_dependencies(parent)

        new_packages = list()

        for pkg_name in dependencies:
            package = self.source_model.get_package(pkg_name)

            reqs = dependencies[pkg_name][4].split(',')

            constraints = self.source_model.add_constraints(parse_constraints(reqs))

            new_relationship = self.build_relationship(parent, constraints)

            if not package:
                package = self.build_package(pkg_name, parent.level, dependencies, new_relationship)
                
                are_void = False
                for version in package.versions:
                    if not package.versions[version]:
                        are_void = True
                        break

                if are_void:
                    continue

                self.source_model.add_package(package)
                self.source_model.add_relationship(new_relationship)
            else:
                package.level += 1

            new_packages.append(package)

            new_relationship.child = package

            parent.child_relationhips.append(new_relationship)

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