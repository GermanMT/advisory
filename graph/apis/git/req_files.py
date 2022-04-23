from requests import request


headers = {
    'Accept': 'application/vnd.github.hawkgirl-preview+json',
    'Authorization': 'Bearer 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',
}

url = 'https://api.github.com/graphql'

def get_req_files(name_with_owner: str) -> dict[str, str]:
    atts = name_with_owner.split('/')
    query = '{\"query\":\"query {\\n repository(owner:\\\"' \
        + atts[0] + '\\\", name:\\\"' + atts[1] + '\\\")' \
        '{\\n dependencyGraphManifests {  \\n nodes' \
        '{ \\n filename \\n } \\n } \\n } \\n } \" }'

    response = request('POST', url, data = query, headers = headers)
    return json_reader(response.json())

def json_reader(data) -> dict[str, str]: 
    req_files = list()

    for node in data['data']['repository']['dependencyGraphManifests']['nodes']:
        req_files.append(node['filename'])

    return req_files