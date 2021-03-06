import json
import os
from requests import request

from graph.apis.git.req_files import get_req_files

from dotenv import load_dotenv


load_dotenv()

GIT_GRAPHQL_API_KEY = os.getenv('GIT_GRAPHQL_API_KEY')

headers = {
    'Accept': 'application/vnd.github.hawkgirl-preview+json',
    'Authorization': f'Bearer {GIT_GRAPHQL_API_KEY}',
}

url = 'https://api.github.com/graphql'

def get_dependencies(name_with_owner: str) -> dict[str, str]:
    atts = name_with_owner.split('/')
    query = '{\"query\":\"query {\\n repository(owner:\\\"' \
        + atts[0] + '\\\", name:\\\"' \
        + atts[1] + '\\\") {\\n dependencyGraphManifests { \\n edges ' \
        '{ \\n node { \\n blobPath \\n dependencies { \\n nodes ' \
        '{ \\n repository { \\n nameWithOwner \\n } \\n packageName ' \
        '\\n requirements \\n hasDependencies \\n packageManager \\n ' \
        '} \\n } \\n } \\n } \\n } \\n } \\n } \" }'

    response = request('POST', url, data = query, headers = headers)
    return json_reader(response.json())

def json_reader(data: json) -> dict[str, str]: 
    dependencies = dict()

    for edge in data['data']['repository']['dependencyGraphManifests']['edges']:
        file = edge['node']['blobPath'].split('/')[-1]
        for node in edge['node']['dependencies']['nodes']:
            ''' De momento solo paquetes desplegados en PIP '''
            if node['repository'] != None and node['packageManager'] == 'PIP':
                package_manager = node['packageManager']
                has_dependencies = node['hasDependencies']
                name_with_owner = node['repository']['nameWithOwner']
                req_files = get_req_files(name_with_owner)
                req = node['requirements'] if node['requirements'] else 'Any'
                dependencies[node['packageName']] = [package_manager, file, has_dependencies, name_with_owner, req_files, req]

    return dependencies
