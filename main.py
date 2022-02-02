from metamodel.metamodel import Metamodel
from operations import *
from pysmt_model.pysmt_model import PySMTModel

import time


# GermanMT/AMADEUS
# psf/requests

begin = time.time()

''' Creamos el metamodelo sobre una serie de fciheros de un repositorio '''
metamodel = Metamodel(['setup.py'], 'psf/requests')

metamodelo = metamodel.generate_metamodel()

''' Transformamos el metamodelo en un modelo PySMT '''
psymt_model = PySMTModel(metamodelo)

modelo_smt = psymt_model.generate_model()

print('Tiempo: ', time.time() - begin)

''' Añadir operaciones '''

print('\n')
print('¿Es el modelo válido? \n')
print(valid_model(modelo_smt.domains))
