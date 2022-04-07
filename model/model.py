from model.utils.pypi.versions import get_versions
from model.utils.git.dependencies import get_dependencies
from model.utils.other.parse_constraints import parse_constraints

from cve.CVE import CVE


class Version:

    def __init__(
        self,
        ver_name: str,
        release_date: str
    ) -> None:

        self.ver_name = ver_name
        self.release_date = release_date
        self.cves: 'CVE' = list()

    def __repr__(self) -> str:
        return self.ver_name

class Package:

    def __init__(
        self,
        level: int,
        pkg_name: str,
        pkg_manager: str,
        file: str,
        has_dependencies: bool,
        name_with_owner: str,
        req_files: list[str],
        parent_relationship: 'Relationship' = None,
        child_relationhips: list['Relationship'] = list()
    ) -> None:

        self.level = level
        self.pkg_name = pkg_name
        self.pkg_manager = pkg_manager
        self.file = file
        self.has_dependencies = has_dependencies
        self.name_with_owner = name_with_owner
        self.req_files = req_files
        self.parent_relationship = parent_relationship
        self.child_relationhips = child_relationhips
        self.versions = dict()
        self.cves: list['CVE'] = list()
        if parent_relationship: self.generate_versions()

    def generate_versions(self) -> list['Version']:
        versions_ = get_versions(self.pkg_name, self.parent_relationship)
        parent_name = self.parent_relationship.parent.pkg_name
        versions = {parent_name: []}

        for ver_name in versions_:
            versions[parent_name].append(Version(ver_name, versions_[ver_name]))

        return self.versions.update(versions)

    def get_cve(
        self,
        id: str
    ) -> 'CVE':
        for cve in self.cves:
            if cve.id == id:
                return cve

class Constraint:
    
    def __init__(
        self,
        signature: str
        ) -> None:

        self.signature = signature

class Relationship:

    def __init__(
        self,
        parent: 'Package',
        child: 'Package' = None ,
        constraints: 'Constraint' = list()
    ) -> None:

        self.parent = parent
        self.child = child
        self.constraints = constraints

class Model:

    def __init__(
        self,
        root: 'Package',
        total_level: int
    ) -> None:

        self.root = root
        self.total_level = total_level
        self.packages: list['Package'] = list()
        self.relationships: list['Relationship'] = list()

    def generate_model(
        self,
        parent: 'Package'
    ) -> None:

        if parent.level >= self.total_level - 1:
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
            self.generate_model(package)

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
            model_str += f'Package{i}: {pkg.pkg_name}: {pkg.versions} \n'
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
