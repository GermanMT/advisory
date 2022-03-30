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
    [],
    'GermanMT/prueba1'
)

begin = time.time()

modelo = Model(root, 2)
modelo.generate_model('GermanMT/prueba1', root)

print('Tiempo de construcción del modelo: ', time.time() - begin)

print('Grafo de dependencias de MiProyecto: ')
print(modelo)

begin = time.time()

for package in modelo.packages:
    if package.versions:
        add_cves(package)

print('Tiempo de atribución del modelo: ', time.time() - begin)

modelo_smt = PySMTModel(modelo)
modelo_smt.generate_model()

# Todas
# results = check_configs(modelo_smt)

# Filtrando
# results = check_configs(modelo_smt, impact_threshold = 3)

# Priorizando
results = check_configs(modelo_smt, sorted = True)

# Filtrando y Priorizando
# results = check_configs(modelo_smt, impact_threshold = 3, sorted = True)

for result in results:
    print(result)

# print('Vulnerabilidades extraidas para las dependencias: ')

# begin = time.time()
# for package in modelo.packages:
#     time.sleep(10)
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

# print('Tiempo de de extración cves: ', time.time() - begin)
