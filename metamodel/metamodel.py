from metamodel.raw_data import RawData


class Feature():

    def __init__(self, name, parent = None, relations = None):
        self.name = name
        self.parent = parent
        self.relations = relations if relations else list()

class Relationship():

    def __init__(self, parent, childrens):
        self.parent = parent
        self.childrens = childrens

class Constraint():
    
    def __init__(self, name, feature):
        self.name = name
        self.feature = feature

class Metamodel():

    def __init__(self, files: list[str], nameWithOwner: str) -> None:
        self.files = files
        self.nameWithOwner = nameWithOwner
        self.features = list()
        self.relationships = list()
        self.constraints = list()

    ''' Una vez obtengamos el dicionario con las dependencias asociadas a las distribuciones
    permitidas por el formato de la versión comenzaremos a construir el metamodelo'''
    def generate_metamodel(self) -> None:
        data = RawData().get_data(self.files[0], self.nameWithOwner)
        for pkg_name in data:
            parent = self.add_feature(pkg_name)
            childrens = list()
            for children in data[pkg_name][0]:
                childrens.append(self.add_feature(children))

            self.add_relationship(parent, childrens)

            if data[pkg_name][1]:
                for constraints in data[pkg_name][1]:
                    self.add_constraint(constraints + ' ' + data[pkg_name][1][constraints], parent)


        print(self.__str__())

    def add_feature(self, pkg_name):
        feature = Feature(pkg_name)
        self.features.append(feature)
        return feature
    
    def add_relationship(self, parent, childrens):
        relationship = Relationship(parent, childrens)
        self.relationships.append(relationship)
        return relationship

    def add_constraint(self, name, feature):
        constraint = Constraint(name, feature)
        self.constraints.append(constraint)
        return constraint

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
