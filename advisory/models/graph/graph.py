from advisory.objects import Package, Relationship, Constraint

from famapy.core.models import VariabilityModel


class Graph(VariabilityModel):

    @staticmethod
    def get_extension() -> str:
        return 'graph'

    def __init__(
        self,
        owner: str,
        name: str,
        pkg_manager: str
    ) -> None:

        self._root: 'Package' = Package(
            0,
            name,
            pkg_manager,
            None,
            True,
            owner + '/' + name,
            []
        )
        self._packages: list['Package'] = list()
        self._relationships: list['Relationship'] = list()

    def get_root(self) -> 'Package':
        return self._root

    def get_packages(self) -> list['Package']:
        return self._packages

    def get_relationships(self) -> list['Relationship']:
        return self._relationships

    def add_package(
        self,
        package: 'Package'
    ) -> 'Package':

        self._packages.append(package)

    def add_relationship(
        self,
        relationship: 'Relationship'
    ) -> 'Relationship':

        self._relationships.append(relationship)

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
        for package in self._packages:
            if package.pkg_name == pkg_name:
                return package

    def __repr__(self) -> str:
        model_str = f'Root: {self._root.pkg_name} \n'

        model_str += '\n'

        model_str += 'Packages: \n'
        i = 0
        for pkg in self._packages:
            versions = [{parent: str(pkg.versions[parent]) + ' -> ' +str(len(pkg.versions[parent]))} for parent in pkg.versions]
            model_str += f'Package{i}: {pkg.pkg_name}: {versions} \n'
            i += 1

        model_str += '\n'

        model_str += 'Relationships: \n'
        i = 0
        for rel in self._relationships:
            model_str += f'Relationship{i}: {rel.parent.pkg_name} -> {rel.child.pkg_name} \n'
            i += 1

        model_str += '\n'

        model_str += 'Constraints: \n'
        i = 0
        for rel in self._relationships:
            for const in rel.constraints:
                model_str += f'Constraint{i}: {rel.child.pkg_name} {const.signature} \n'
                i += 1

        return model_str