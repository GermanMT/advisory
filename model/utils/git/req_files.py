import json, requests


headers = {
    'Accept': 'application/vnd.github.hawkgirl-preview+json',
    'Authorization': 'Bearer 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',
}

url = 'https://api.github.com/graphql'

def get_req_files(name_with_owner: str) -> dict[str, str]:
    atts = name_with_owner.split('/')
    query = '{\"query\":\"query {\\n repository(owner:\\\"' + atts[0] + '\\\", name:\\\"' + atts[1] + '\\\") {\\n dependencyGraphManifests {  \\n nodes { \\n filename \\n } \\n } \\n } \\n } \" }'

    response = requests.request('POST', url, data = query, headers = headers)
    return json_reader(response.json())

def json_reader(data: json) -> dict[str, str]: 
    req_files = []

    for node in data['data']['repository']['dependencyGraphManifests']['nodes']:
        req_files.append(node['filename'])

    return req_files