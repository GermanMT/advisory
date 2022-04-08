from model.model import Model
from model.model import Package
from model.utils.other.add_cves import add_cves
from pysmt_model.operations.check_configs import check_configs

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

root = Package(
            0,
            'dateutil',
            'None',
            'None',
            True,
            'dateutil/dateutil',
            []
        )

begin = time.time()

modelo = Model(root, 2)
modelo.generate_model(root)

print('Grafo de dependencias de MiProyecto: ')
print(modelo)

print('Tiempo de construcción del modelo: ', time.time() - begin)

begin = time.time()

for package in modelo.packages:
    if package.versions:
        add_cves(package)

print('Tiempo de atribución del modelo: ', time.time() - begin)

modelo_smt = PySMTModel(modelo)
modelo_smt.generate_model()

begin = time.time()

# Filtrando menor 0.0
results_1 = check_configs(modelo_smt, impact_threshold = 0., limit = 1000)
print(
    'Número configuraciones con impacto menor que 0.0: ',
    '+' if len(results_1) == 1000 else '',
    len(results_1),
    '\n'
)

print('Tiempo de realización de la operación: ', time.time() - begin, '\n')

begin = time.time()

# Filtrando menor 2.5
results_2 = check_configs(modelo_smt, impact_threshold = 2.5, limit = 1000)
print(
    'Número configuraciones con impacto menor que 2.5: ',
    '+' if len(results_2) == 1000 else '',
    len(results_2),
    '\n'
)

print('Tiempo de realización de la operación: ', time.time() - begin, '\n')

begin = time.time()

# Filtrando menor 5.0
results_3 = check_configs(modelo_smt, impact_threshold = 5., limit = 1000)
print(
    'Número configuraciones con impacto menor que 5.0: ',
    '+' if len(results_3) == 1000 else '',
    len(results_3),
    '\n'
)

print('Tiempo de realización de la operación: ', time.time() - begin, '\n')

begin = time.time()

# Filtrando menor 10.0
results_4 = check_configs(modelo_smt, impact_threshold = 10., limit = 1000)
print(
    'Número configuraciones con impacto menor que 10.0: ',
    '+' if len(results_4) == 1000 else '',
    len(results_4),
    '\n'
)

print('Tiempo de realización de la operación: ', time.time() - begin, '\n')

# Filtrando
# results = check_configs(modelo_smt, impact_threshold = 10., limit = 10)
# print(len(results))

# for result in results:
#     print(result)

# print('Vulnerabilidades extraidas para las dependencias: ')

# for package in modelo.packages:
#     print(package.pkg_name)
#     if package.versions:
#         print(package.versions)
#         add_cves(package)

#     for cve in package.cves:
#         print('*******************')
#         print('CVE: ')
#         print('ID: ', cve.id)
#         print('Descripcion: ', cve.description)
#         print('')
#         print('CVSS: ')
#         print('Vector: ', cve.cvss.vector_string)
#     print('\n')
