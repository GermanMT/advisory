from graph.graph import Graph
from graph.utils.add_cves import add_cves

from pysmt_model.pysmt_model import PySMTModel
from pysmt_model.operations import maximize_impact

from experimentation.packages.packages import all_packages

import time


def experiment_maximize():

    file = open('./experimentation/results/maximize_results.txt', 'w+')

    packages = all_packages()

    for package in packages:
        time.sleep(30)

        file.write(package[1] + '\n')

        modelo = Graph(package[0], package[1], 1)

        for _package in modelo.packages:
            if _package.versions:
                add_cves(_package)

        begin = time.time()

        modelo_smt = PySMTModel(modelo)
        modelo_smt.generate_model()

        file.write('Tiempo de transformacion a SMT: ' + str(time.time() - begin) + '\n')

        begin = time.time()

        # Obtener la configuracion con mayor impacto
        results = maximize_impact(modelo_smt, limit = 1)
        file.write('La configuracion con mayor impacto:\n')
        file.write(str(results[0]) + '\n')

        file.write('Tiempo de realizacion de la operacion: ' + str(time.time() - begin) + '\n')

        file.write('-' * 25 + '\n')

    file.close()