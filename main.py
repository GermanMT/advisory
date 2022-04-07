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
    'MiProyecto',
    'None',
    'None',
    True,
    'pyca/cryptography',
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

# Todas
# results = check_configs(modelo_smt, limit = 10)

# Filtrando
results = check_configs(modelo_smt, impact_threshold = 0., limit = 1000)

# Minimizando
# results = check_configs(modelo_smt, minimize = True)

# Maximizando
# results = check_configs(modelo_smt, maximize = True)

# Filtrando y maximizando
# results = check_configs(modelo_smt, impact_threshold = 2., maximize = True)

# Filtrando y minimizando
# results = check_configs(modelo_smt, impact_threshold = 2., minimize = True)

# for result in results:
#     print(result)

# print('Tiempo de realización de la operación: ', time.time() - begin)

print(len(results))

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
