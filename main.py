from metamodel.metamodel import Metamodel
from operations import *
from pysmt_model.pysmt_model import PySMTModel

import time


# GermanMT/AMADEUS
# psf/requests

'''
Repositorio con ficheros de dependencias contradictorios: GermanMT/prueba1

Repositorio con ficheros de dependencias no contradictorios: GermanMT/prueba1
'''

begin = time.time()

''' Creamos el metamodelo sobre una serie de ficheros de un repositorio '''

''' TODO: Solucionar error con el simbolo * '''
metamodel = Metamodel(['setup.py'], 'boto/s3transfer')

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
