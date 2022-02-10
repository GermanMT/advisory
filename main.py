from metamodel.metamodel import Metamodel
from pysmt_model.pysmt_model import PySMTModel
from pysmt_model.operations import *

import time


# GermanMT/AMADEUS
# psf/requests

'''
Repositorio con ficheros de dependencias contradictorios: GermanMT/prueba1

Repositorio con ficheros de dependencias no contradictorios: GermanMT/prueba1
'''

begin = time.time()

''' Creamos el metamodelo sobre una serie de ficheros de un repositorio '''

metamodel = Metamodel(['requirements-check.txt', 'requirements-dev-lock.txt', 'requirements-dev.txt', 'requirements-docs.txt', 'setup.py'], 'aws/aws-cli')

metamodelo = metamodel.generate_metamodel()

''' Transformamos el metamodelo en un modelo PySMT '''
psymt_model = PySMTModel(metamodelo)

modelo_smt = psymt_model.generate_model()

print('Tiempo: ', time.time() - begin)

''' Añadir operaciones '''

print('\n')
print('¿Es el modelo válido? \n')
print(valid_model(modelo_smt.domains))

# print('¿Cuál es el número de productos del modelo? \n')
# print(number_of_products(modelo_smt.domains, modelo_smt.vars))
