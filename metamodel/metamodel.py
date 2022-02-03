from metamodel.raw_data import RawData


class Package():

    def __init__(self, name, versions = None, constraints = None):
        self.name = name
        self.relations = versions if versions else list()
        self.constraints = constraints if constraints else list()

class Relationship():

    def __init__(self, package, versions):
        self.package = package
        self.versions = versions

class Constraint():
    
    def __init__(self, name, package):
        self.name = name
        self.package = package

class Metamodel():

    def __init__(self, files: list[str], nameWithOwner: str) -> None:
        self.files = files
        self.nameWithOwner = nameWithOwner
        self.packages = list()
        self.relationships = list()
        self.constraints = list()

    ''' Una vez obtengamos el dicionario con las dependencias asociadas a las distribuciones
    permitidas por las restricciones comenzaremos a construir el metamodelo '''
    def generate_metamodel(self) -> None:
        for file in self.files:
            data = RawData().get_data(file, self.nameWithOwner)
            for pkg_name in data:
                if pkg_name not in [package.name for package in self.packages]:
                    pkg = self.add_package(pkg_name)
                else:
                    pkg = self.get_package(pkg_name)

                versions = data[pkg_name][0]
                relationship = self.add_relationship(pkg, versions)
                pkg.relations.append(relationship)

                if data[pkg_name][1]:
                    for constraint in data[pkg_name][1]:
                        constraint_ = self.add_constraint(constraint, pkg)
                        pkg.constraints.append(constraint_)

        print(self.__str__())
        return self

    def add_package(self, pkg_name):
        pkg = Package(pkg_name)
        self.packages.append(pkg)
        return pkg
    
    def add_relationship(self, pkg, versions):
        relationship = Relationship(pkg, versions)
        self.relationships.append(relationship)
        return relationship

    def add_constraint(self, name, pkg):
        constraint = Constraint(name, pkg)
        self.constraints.append(constraint)
        return constraint

    def get_package(self, name):
        for pkg in self.packages:
            if pkg.name == name:
                return pkg

    def __str__(self) -> str:
        model_str = 'Packages: \n'
        i = 0
        for pkg in self.packages:
            model_str += f'Package{i}: {pkg.name} \n'
            i += 1

        model_str += '\n'
            
        model_str += 'Relationships: \n'
        i = 0
        for rel in self.relationships:
            model_str += f'Relationship{i}: {rel.package.name} - {rel.versions} \n'
            i += 1

        model_str += '\n'

        model_str += 'Constraints: \n'
        i = 0
        for const in self.constraints:
            model_str += f'Constraint{i}: {const.package.name} {const.name} \n'
            i += 1

        return model_str
