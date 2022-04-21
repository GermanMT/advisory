from graph.apis.git.dependencies import get_dependencies
from graph.utils.parse_constraints import parse_constraints

from graph.objects.model.package import Package
from graph.objects.model.relationship import Relationship
from graph.objects.model.constraint import Constraint


class Graph:

    def __init__(
        self,
        owner: str,
        name: str,
        total_level: int
    ) -> None:

        self.total_level = total_level
        self.root = Package(
            0,
            name,
            'None',
            'None',
            True,
            owner + '/' + name,
            []
        )
        self.packages: list['Package'] = list()
        self.relationships: list['Relationship'] = list()
        self.build_graph(self.root)

    def build_graph(
        self,
        parent: 'Package'
    ) -> None:

        if parent.level >= self.total_level:
            return ''

        dependencies = get_dependencies(parent.name_with_owner)

        new_packages = list()

        for pkg_name in dependencies:
            package = self.get_package(pkg_name)

            reqs = dependencies[pkg_name][5].split(',')

            constraints = self.add_constraints(parse_constraints(reqs))

            new_relationship = self.add_relationship(parent, constraints)

            if not package:
                package = self.add_package(pkg_name, parent.level, dependencies, new_relationship)
            else:
                package.level += 1

            new_packages.append(package)

            new_relationship.child = package

            parent.child_relationhips.append(new_relationship)

        for package in new_packages:
            self.build_graph(package)

    def add_package(
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
                dependencies[pkg_name][4],
                parent
            )

        self.packages.append(pkg)
        return pkg

    def add_relationship(
        self,
        parent: 'Package',
        constraints: list['Constraint']
    ) -> 'Relationship':

        rel = Relationship(
                parent,
                constraints = constraints
            )

        self.relationships.append(rel)
        return rel

    def add_constraints(
        self,
        constraints_: list[str]
    ) -> list['Constraint']:

        constraints = list()
        for constraint_ in constraints_:
            new_constraint = Constraint(constraint_)
            constraints.append(new_constraint)
        return constraints

    def get_package(self, pkg_name: str) -> 'Package':
        for package in self.packages:
            if package.pkg_name == pkg_name:
                return package

    def __repr__(self) -> str:
        model_str = f'Root: {self.root.pkg_name} \n'

        model_str += '\n'

        model_str += 'Packages: \n'
        i = 0
        for pkg in self.packages:
            versions = [{parent: str(pkg.versions[parent]) + ' -> ' +str(len(pkg.versions[parent]))} for parent in pkg.versions]
            model_str += f'Package{i}: {pkg.pkg_name}: {versions} \n'
            i += 1

        model_str += '\n'

        model_str += 'Relationships: \n'
        i = 0
        for rel in self.relationships:
            model_str += f'Relationship{i}: {rel.parent.pkg_name} -> {rel.child.pkg_name} \n'
            i += 1

        model_str += '\n'

        model_str += 'Constraints: \n'
        i = 0
        for rel in self.relationships:
            for const in rel.constraints:
                model_str += f'Constraint{i}: {rel.child.pkg_name} {const.signature} \n'
                i += 1

        return model_str
