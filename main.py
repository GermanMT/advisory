from advisory.models import Graph

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

    ''' Atribucion del grafo con vulnerabilidades '''
    builder.attribute()

    print('Grafo de dependencias: ')
    print(graph)

    ''' Transformacion del grafo en un modelo SMT '''
    transform = GraphToSMT(graph)
    modelo_smt = transform.transform()


    ''' Operacion de filtro '''
    filter_configs = FilterConfigs(min_threshold = 0, max_threshold = 0.1, limit = 500)
    filter_configs.execute(modelo_smt)
    result = filter_configs.get_result()

    print(
        'Numero de configuracion con impacto entre 0 y 0.1: ',
        len(result),
        '\n'
    )


    ''' Operacion de minimizacion '''
    minimize = MinimizeImpact(limit = 1)
    minimize.execute(modelo_smt)
    results = minimize.get_result()
    print('Configuracion con el menor impacto: ')
    for result in results:
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
    maximize = MaximizeImpact(limit = 1)
    maximize.execute(modelo_smt)
    results = maximize.get_result()
    print('Configuracion con el mayor impacto: ')
    for result in results:
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
