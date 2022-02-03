from metamodel.raw_data import RawData


class Feature():

    def __init__(self, name, parent = None, relations = None, constraints = None):
        self.name = name
        self.parent = parent
        self.relations = relations if relations else list()
        self.constraints = constraints if constraints else list()

class Relationship():

    def __init__(self, parent, childrens):
        self.parent = parent
        self.childrens = childrens

class Constraint():
    
    def __init__(self, op, version, feature):
        self.name = {op: version}
        self.feature = feature

class Metamodel():

    def __init__(self, files: list[str], nameWithOwner: str) -> None:
        self.files = files
        self.nameWithOwner = nameWithOwner
        self.features = list()
        self.relationships = list()
        self.constraints = list()

    ''' Una vez obtengamos el dicionario con las dependencias asociadas a las distribuciones
    permitidas por las restricciones comenzaremos a construir el metamodelo '''
    def generate_metamodel(self) -> None:
        for file in self.files:
            data = RawData().get_data(file, self.nameWithOwner)
            for pkg_name in data:
                if pkg_name not in [feat.name for feat in self.features]:
                    parent = self.add_feature(pkg_name)
                else:
                    parent = self.get_feature(pkg_name)

                childrens = list()
                for children in data[pkg_name][0]:
                    childrens.append(self.add_feature(children, parent))

                relationship = self.add_relationship(parent, childrens)
                parent.relations.append(relationship)

                if data[pkg_name][1]:
                    for constraints in data[pkg_name][1]:
                        constraint = self.add_constraint(constraints, data[pkg_name][1][constraints], parent)
                        parent.constraints.append(constraint)

        print(self.__str__())
        return self

    def add_feature(self, pkg_name, parent = None):
        feature = Feature(pkg_name, parent)
        self.features.append(feature)
        return feature
    
    def add_relationship(self, parent, childrens):
        relationship = Relationship(parent, childrens)
        self.relationships.append(relationship)
        return relationship

    def add_constraint(self, op, version, feature):
        constraint = Constraint(op, version, feature)
        self.constraints.append(constraint)
        return constraint

    def get_feature(self, name):
        for feat in self.features:
            if feat.name == name:
                return feat

    def __str__(self) -> str:
        model_str = 'Features: \n'
        i = 0
        for feat in self.features:
            model_str += f'Feature{i}: {feat.name} \n'
            i += 1

        model_str += '\n'
            
        model_str += 'Relationships: \n'
        i = 0
        for rel in self.relationships:
            names = [child.name for child in rel.childrens]
            model_str += f'Relationship{i}: {rel.parent.name} - {names} \n'
            i += 1

        model_str += '\n'

        model_str += 'Constraints: \n'
        i = 0
        for const in self.constraints:
            model_str += f'Constraint{i}: {const.feature.name} {const.name} \n'
            i += 1

        return model_str
