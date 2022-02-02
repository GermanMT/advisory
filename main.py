from metamodel.metamodel import Metamodel
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
