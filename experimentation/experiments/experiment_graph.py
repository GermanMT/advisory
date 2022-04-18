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

        for package_ in modelo.packages:
            if package_.versions:
                add_cves(package_)
            
        file.write('Tiempo de atribucion del grafo: ' + str(time.time() - begin) + '\n')
        file.write('\n')

        file.write('Asociacion de CVE:\n')
        file.write('\n')

        cves = set()
        for package in modelo.packages:
            for parent in package.versions:
                for version in package.versions[parent]:
                    for cve in version.cves:
                        cves.add(cve.id)

        file.write('Numero de CVE asociados al grafo: ' + str(len(cves)) + '\n')
        file.write('\n')

        file.write('-' * 25 + '\n')
    
    file.close()
