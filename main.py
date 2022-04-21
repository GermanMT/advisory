from graph.graph import Graph
from graph.graph import Package
from graph.utils.add_cves import add_cves
from pysmt_model.operations import *

from pysmt_model.pysmt_model import PySMTModel
from pysmt_model.operations import *

import time

'''
TODO:
- Asociar las versiones al fichero de requisitos del que provienen
- Implementar la transformación al grafo
- Averiguar extracción 'https://nvd.nist.gov/vuln/detail/CVE-2021-45958#range-7645712'
- Plantear coger versiones de proyectos de github
- Crear fichero para las transformaciones entre entero y version
- Optimizar extracción de CVE's
'''

begin = time.time()

modelo = Graph('GermanMT', 'urllib3', 1)

# print('Grafo de dependencias de MiProyecto: ')
# print(modelo)

print('Tiempo de construcción del modelo: ', time.time() - begin)

begin = time.time()

for package in modelo.packages:
    if package.versions:
        add_cves(package)

print('Tiempo de atribución del modelo: ', time.time() - begin)

modelo_smt = PySMTModel(modelo)
modelo_smt.generate_model()

begin = time.time()

results = filter_configs(modelo_smt, limit = 500)

print(time.time() - begin)

# results = minimize_impact(modelo_smt, limit = 10)

# for result in results:
#     _results = dict()

#     for part in result:
#         name = str(part)
#         package = modelo.get_package(name)
#         if package:
#             _results[name] = modelo_smt.versions[name][result[part].as_long()]
#         if str(part) == 'CVSSt':
#             _results['CVSSt'] = result[part]

#     print('*' * 25)
#     for _result in _results:
#         print('-' * 25)
#         print(_result, ' --> ', _results[_result])


# results = maximize_impact(modelo_smt, limit = 1)
# print(results)

# results_1 = check_configs(modelo_smt, max_threshold = 2.5, limit = 1000)
# print(
#     'Número configuraciones con impacto entre 0.0 y 2.5: ',
#     '+' if len(results_1) == 1000 else '',
#     len(results_1),
#     '\n'
# )

# # Filtrando entre 2.5 y 5.0
# results_2 = check_configs(modelo_smt, max_threshold = 5.0, min_threshold = 2.5, limit = 1000)
# print(
#     'Número configuraciones con impacto entre 2.5 y 5.0: ',
#     '+' if len(results_2) == 1000 else '',
#     len(results_2),
#     '\n'
# )

# # Filtrando entre 5.0 y 7.5
# results_3 = check_configs(modelo_smt, max_threshold = 7.5, min_threshold = 5.0, limit = 1000)
# print(
#     'Número configuraciones con impacto entre 5.0 y 7.5: ',
#     '+' if len(results_3) == 1000 else '',
#     len(results_3),
#     '\n'
# )

# # Filtrando entre 7.5 y 10.0
# results_4 = check_configs(modelo_smt, min_threshold = 7.5, limit = 1000)
# print(
#     'Número configuraciones con impacto entre 7.5 y 10.0: ',
#     '+' if len(results_4) == 1000 else '',
#     len(results_4),
#     '\n'
# )

# results_1 = check_configs(modelo_smt, maximize = True, limit = 1000)

# groups = dict()

# for result in results_1:
#     for var in result:
#         if str(var) == 'CVSSt':
#             impact = result[var]
#             if impact not in groups:
#                 groups[impact] = 1
#             else:
#                 groups[impact] += 1

# print(groups)

# print('Vulnerabilidades extraidas para las dependencias: ')

# cves = list()
# for package in modelo.packages:
#     # if package.versions:
#     #     print(package.versions)
#     #     add_cves(package)

#     for parent in package.versions:
#         for version in package.versions[parent]:
#             # print(version.ver_name)
#             # print(len(version.cves))
#             for cve in version.cves:
#             # #     print('*******************')
#                 # print('CVE: ')
#                 # print(cve.id)
#                 cves.append(cve.id)
#             #     print('Descripcion: ', cve.description)
#             #     print('')
#             #     print('CVSS: ')
#             #     print('Vector: ', cve.cvss.vector_string)
#             # print('\n')

# print(set(cves))
# print('Número de CVEs detectados: ', len(set(cves)))
