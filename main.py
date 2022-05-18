from advisory.models import Graph
from advisory.models.graph.utils.add_cves import add_cves

from advisory.transformations import *

from advisory.operations import *

import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        '--owner',
        help = 'Name of the owner',
        required = True,
        type = str
    )
    parser.add_argument(
        '-r',
        '--repository',
        help = 'Name of the repository',
        required = True,
        type = str
    )
    parser.add_argument(
        '-m',
        '--manager',
        help = 'Package manager of the repository',
        required = True,
        type = str
    )
    parser.add_argument(
        '-d',
        '--depth',
        help = 'The depht of dependency graph',
        default = 1,
        type = int
    )
    args = parser.parse_args()

    ''' Construccion del grafo de dependencias '''
    graph = Graph(args.owner, args.repository, args.manager)
    builder = BuildGraph(graph, args.depth)
    builder.transform(graph.get_root())

    print('Grafo de dependencias: ')
    print(graph)


    ''' Atribucion del grafo con vulnerabilidades '''
    for package in graph.get_packages():
        if package.versions:
            add_cves(package)


    ''' Transformacion del grafo en un modelo SMT '''
    transform = GraphToSMT(graph)
    modelo_smt = transform.transform()


    ''' Operacion de filtro '''
    results = filter_configs(modelo_smt, min_threshold = 0, max_threshold = 0.1, limit = 500)
    print(
        'Numero de configuracion con impacto entre 0 y 0.1: ',
        len(results),
        '\n'
    )


    ''' Operacion de minimizacion '''
    minimize = minimize_impact(modelo_smt, limit = 1)
    print('Configuracion con el menor impacto: ')
    for result in minimize:
        _results = dict()

        for part in result:
            name = str(part)
            package = graph.get_package(name)
            if package:
                _results[name] = modelo_smt.get_versions()[name][result[part].as_long()]
            if str(part) == 'CVSSt':
                _results['CVSSt'] = result[part]

        for _result in _results:
            print('-' * 25)
            print(_result, ' --> ', _results[_result])
    print('-' * 25 + '\n')


    ''' Operacion de maximizacion '''
    maximize = maximize_impact(modelo_smt, limit = 1)
    print('Configuracion con el mayor impacto: ')
    for result in maximize:
        _results = dict()

        for part in result:
            name = str(part)
            package = graph.get_package(name)
            if package:
                _results[name] = modelo_smt.get_versions()[name][result[part].as_long()]
            if str(part) == 'CVSSt':
                _results['CVSSt'] = result[part]

        for _result in _results:
            print('-' * 25)
            print(_result, ' --> ', _results[_result])
    print('-' * 25 + '\n')
