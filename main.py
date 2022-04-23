from graph.graph import Graph
from graph.utils.add_cves import add_cves
from pysmt_model.operations import *

from pysmt_model.pysmt_model import PySMTModel
from pysmt_model.operations import *



'''
    Modifica estos parametros para analizar el repositorio que desea
    param1: Propietario del repositorio
    param2: Nombre del repositorio
    param3: Profundidad del grafo
    param4: Gestor de paquetes
'''
param1 = 'GermanMT'
param2 = 'urllib3'
param3 = 1
param4 = 'PIP'
# param1 = 'request'
# param2 = 'request'
# param3 = 1
# param4 = 'NPM'

''' Construccion del grafo de dependencias '''
graph = Graph(param1, param2, param3, param4)

print(f'Grafo de dependencias de {param2}: ')
print(graph)


''' Atribucion del grafo con vulnerabilidades '''
for package in graph.packages:
    if package.versions:
        add_cves(package)


''' Transformacion del grafo en un modelo SMT '''
modelo_smt = PySMTModel(graph)
modelo_smt.generate_model()


''' Operacion de filtro '''
results = filter_configs(modelo_smt, min_threshold = 0, max_threshold = 0.1, limit = 500)
print(
    'Numero de configuracion con impacto entre 0 y 0.1: ',
    len(results),
    '\n'
)


''' Operacion de minimizacion '''
minimize = minimize_impact(modelo_smt, limit = 1)
print('Configuracion con el menor impacto: ')
for result in minimize:
    _results = dict()

    for part in result:
        name = str(part)
        package = graph.get_package(name)
        if package:
            _results[name] = modelo_smt.versions[name][result[part].as_long()]
        if str(part) == 'CVSSt':
            _results['CVSSt'] = result[part]

    for _result in _results:
        print('-' * 25)
        print(_result, ' --> ', _results[_result])
print('-' * 25 + '\n')


''' Operacion de maximizacion '''
maximize = maximize_impact(modelo_smt, limit = 1)
print('Configuracion con el mayor impacto: ')
for result in maximize:
    _results = dict()

    for part in result:
        name = str(part)
        package = graph.get_package(name)
        if package:
            _results[name] = modelo_smt.versions[name][result[part].as_long()]
        if str(part) == 'CVSSt':
            _results['CVSSt'] = result[part]

    for _result in _results:
        print('-' * 25)
        print(_result, ' --> ', _results[_result])
print('-' * 25 + '\n')