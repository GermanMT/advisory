from model.model import Model
from model.utils.other.add_cves import add_cves

from experimentation.packages.packages import all_packages

import time


def experiment_graph():

    file = open('./experimentation/results/graph_results.txt', 'w+')

    packages = all_packages()

    for package in packages:
        time.sleep(20)

        begin = time.time()

        modelo = Model(package, 1)
        modelo.generate_model(package)

        file.write('Grafo de dependencias de ' + package.pkg_name + ': \n')
        file.write(str(modelo) + '\n')

        file.write('Tiempo de construccion del grafo: ' + str(time.time() - begin) + '\n')
        file.write('\n')

        begin = time.time()

        num_cves = 0

        for package in modelo.packages:
            if package.versions:
                add_cves(package)
            num_cves += len(package.cves)

        file.write('Numero de CVEs asociados al grafo: ' +  str(num_cves) + '\n')
        file.write('\n')
            
        file.write('Tiempo de atribucion del grafo: ' + str(time.time() - begin) + '\n')
        file.write('\n')

        file.write('Asociacion de CVE:\n')
        file.write('\n')

        for package in modelo.packages:
            file.write('\n')
            file.write('Numero de CVE asociados a la dependencia' + package.pkg_name + ': ' + str(len(package.cves)) + '\n')

            file.write('{\n')
            for parent in package.versions:
                for version in package.versions[parent]:
                    file.write('Numero de CVE asociados a la version' + version.ver_name +': ' + str(len(version.cves)) + '\n')
            file.write('}\n')

        file.write('-' * 25 + '\n')
    
    file.close()
