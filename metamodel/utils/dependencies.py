import json, requests


headers = {
    'Accept': 'application/vnd.github.hawkgirl-preview+json',
    'Authorization': 'Bearer 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',
    }
url = 'https://api.github.com/graphql'

def get_dependencies(name_with_owner: str, file: str) -> dict[str, str]:
    atts = name_with_owner.split(' ')[0].split('/')
    query = '{\"query\":\"query {\\n repository(owner:\\\"' + atts[0] + '\\\", name:\\\"' + atts[1] + '\\\") {\\n dependencyGraphManifests { \\n totalCount \\n nodes { \\n filename \\n } \\n edges { \\n node { \\n blobPath \\n dependencies { \\n totalCount \\n nodes { \\n repository { \\n nameWithOwner \\n } \\n packageName \\n requirements \\n hasDependencies \\n packageManager \\n } \\n } \\n } \\n } \\n } \\n }\\n}\"}'

    response = requests.request('POST', url, data = query, headers = headers)
    return json_reader(response.json(), file)

def json_reader(data: json, file: str) -> dict[str, str]: 
    result = {}

    for edge in data['data']['repository']['dependencyGraphManifests']['edges']:
        for node in edge['node']['dependencies']['nodes']:
            if edge['node']['blobPath'].__contains__(file):
                if node['repository'] != None:
                    req = node['requirements'] if node['requirements'] else 'Any'
                    result[node['packageName']] = req

    return result
