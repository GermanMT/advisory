import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from model.model import Model
from model.utils.other.add_cves import add_cves
from pysmt_model.operations.check_configs import check_configs

from pysmt_model.pysmt_model import PySMTModel
from pysmt_model.operations import *

from experimentation.packages import all_packages

import time


packages = all_packages()

for package in packages:
    time.sleep(40)

    begin = time.time()

    modelo = Model(package, 2)
    modelo.generate_model(package)

    print('Grafo de dependencias de ' + package.pkg_name + ': ')
    print(modelo)

    print('Tiempo de construcción del grafo: ', time.time() - begin)

    begin = time.time()

    num_cves = 0

    for package in modelo.packages:
        if package.versions:
            add_cves(package)
        num_cves += len(package.cves)

    print('Número de CVEs asociados al grafo: ', num_cves)
        

    print('Tiempo de atribución del grafo: ', time.time() - begin)

    begin = time.time()

    modelo_smt = PySMTModel(modelo)
    modelo_smt.generate_model()

    print('Tiempo de transformación a SMT: ', time.time() - begin)

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

    print('-' * 25 + '\n')
