from graph.graph import Graph
from graph.utils.add_cves import add_cves

from pysmt_model.pysmt_model import PySMTModel
from pysmt_model.operations import filter_configs

from experimentation.packages.packages import all_packages

import time


def experiment_filter():

    file = open('./experimentation/results/filter_results.txt', 'w+')

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
        file.write('\n')

        # Filtrando con impacto 0.0
        results = filter_configs(modelo_smt, max_threshold = 0.0, limit = 1000)
        sum = '+' if len(results) == 1000 else ''
        file.write('Numero configuraciones con impacto 0.0: ' + sum + str(len(results)) + '\n')

        file.write('Tiempo de realizacion de la operacion: ' + str(time.time() - begin) + '\n')

        begin = time.time()
        file.write('\n')

        # Filtrando entre 0.0 y 2.5 sin incluir el 0
        results = filter_configs(modelo_smt, max_threshold = 2.5, min_threshold = 0.001, limit = 1000)
        sum = '+' if len(results) == 1000 else ''
        file.write('Numero configuraciones con impacto entre 0.0 y 2.5: ' + sum + str(len(results)) + '\n')

        file.write('Tiempo de realizacion de la operacion: ' + str(time.time() - begin) + '\n')

        begin = time.time()
        file.write('\n')

        # Filtrando entre 2.5 y 5.0
        results = filter_configs(modelo_smt, max_threshold = 5.0, min_threshold = 2.5, limit = 1000)
        sum = '+' if len(results) == 1000 else ''
        file.write('Numero configuraciones con impacto entre 2.5 y 5.0: ' + sum + str(len(results)) + '\n')

        file.write('Tiempo de realizacion de la operacion: ' + str(time.time() - begin) + '\n')

        begin = time.time()
        file.write('\n')

        # Filtrando entre 5.0 y 7.5
        results = filter_configs(modelo_smt, max_threshold = 7.5, min_threshold = 5.0, limit = 1000)
        sum = '+' if len(results) == 1000 else ''
        file.write('Numero configuraciones con impacto entre 5.0 y 7.5: ' + sum + str(len(results)) + '\n')

        file.write('Tiempo de realizacion de la operacion: ' + str(time.time() - begin) + '\n')

        begin = time.time()
        file.write('\n')

        # Filtrando entre 7.5 y 10.0
        results = filter_configs(modelo_smt, min_threshold = 7.5, limit = 1000)
        sum = '+' if len(results) == 1000 else ''
        file.write('Numero configuraciones con impacto entre 7.5 y 10.0: ' + sum + str(len(results)) + '\n')

        file.write('Tiempo de realizacion de la operacion: ' + str(time.time() - begin) + '\n')

        file.write('-' * 25 + '\n')

    file.close()
