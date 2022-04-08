from model.model import Model
from model.utils.other.add_cves import add_cves
from pysmt_model.operations.check_configs import check_configs

from pysmt_model.pysmt_model import PySMTModel
from pysmt_model.operations import *

from packages import all_packages

import time


packages = all_packages()

for package in packages:
    begin = time.time()

    modelo = Model(package, 2)
    modelo.generate_model(package)

    print('Grafo de dependencias de ' + package.pkg_name + ': ')
    print(modelo)

    print('Tiempo de construcción del modelo: ', time.time() - begin)

    begin = time.time()

    for package in modelo.packages:
        if package.versions:
            add_cves(package)

    print('Tiempo de atribución del modelo: ', time.time() - begin)

    begin = time.time()

    modelo_smt = PySMTModel(modelo)
    modelo_smt.generate_model()

    print('Tiempo de transformación a SMT: ', time.time() - begin)

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

    print('Tiempo de realización de la operación: ', time.time() - begin)

    print(len(results))
